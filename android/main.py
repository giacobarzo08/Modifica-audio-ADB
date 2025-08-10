import os
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import mainthread

# Import specifici per Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass

    # Importiamo le classi native di Android direttamente
    MediaRecorder = autoclass('android.media.MediaRecorder')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
    AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
    MediaPlayer = autoclass('android.media.MediaPlayer')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Environment = autoclass('android.os.Environment')


KV = '''
MainLayout:
    orientation: 'vertical'
    padding: '20dp'
    spacing: '10dp'

    Label:
        id: status_label
        text: 'Pronto.'
        size_hint_y: None
        height: '80dp'
        text_size: self.width, None

    Button:
        id: record_button
        text: 'Registra'
        on_press: app.toggle_recording()

    Button:
        id: play_button
        text: 'Riproduci ultimo audio'
        on_press: app.play_last_audio()
        disabled: True
'''

class MainLayout(BoxLayout):
    pass

class AudioApp(App):

    def build(self):
        self.is_recording = False
        self.last_audio_path = None
        self.recorder = None
        self.player = None
        self.storage_path = self.get_storage_path()
        return Builder.load_string(KV)

    def get_storage_path(self):
        """ Ottiene un percorso di archiviazione scrivibile e permanente. """
        if platform == 'android':
            context = PythonActivity.mActivity
            # Usiamo la directory esterna privata (permanente)
            path = context.getExternalFilesDir(Environment.DIRECTORY_MUSIC).getAbsolutePath()
            return path
        else:
            path = os.path.join(os.path.expanduser('~'), 'AudioAppRecordings')
            return path

    def on_start(self):
        # La gestione dei permessi viene fatta al click, non all'avvio
        pass

    def toggle_recording(self):
        if not self.is_recording:
            self.check_and_request_permissions()
        else:
            self.stop_recording()

    def check_and_request_permissions(self):
        if platform == 'android':
            permissions = [Permission.RECORD_AUDIO]
            request_permissions(permissions, self.on_permissions_result)
        else:
            self.start_recording()

    def on_permissions_result(self, permissions, grants):
        if grants and grants[0]:
            self.start_recording()
        else:
            self.update_status('Permesso RECORD_AUDIO negato.')

    def start_recording(self):
        """ Avvia la registrazione usando MediaRecorder nativo di Android. """
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # Il file verrà salvato come .3gp, un formato contenitore standard
        self.last_audio_path = os.path.join(self.storage_path, f'registrazione_{timestamp}.3gp')

        self.recorder = MediaRecorder()
        self.recorder.setAudioSource(AudioSource.MIC)
        self.recorder.setOutputFormat(OutputFormat.THREE_GPP)
        self.recorder.setOutputFile(self.last_audio_path)
        self.recorder.setAudioEncoder(AudioEncoder.AMR_NB)

        try:
            self.recorder.prepare()
            self.recorder.start()
            self.is_recording = True
            self.root.ids.record_button.text = 'Ferma registrazione'
            self.root.ids.play_button.disabled = True
            self.update_status(f'Registrazione in corso...\nSalvataggio in: {os.path.basename(self.last_audio_path)}')
        except Exception as e:
            self.update_status(f'Errore in MediaRecorder: {e}')
            self.recorder = None

    def stop_recording(self):
        """ Ferma la registrazione. """
        if self.recorder and self.is_recording:
            self.recorder.stop()
            self.recorder.release()
            self.recorder = None
            self.is_recording = False
            self.root.ids.record_button.text = 'Registra'
            self.root.ids.play_button.disabled = False
            self.update_status(f'Registrazione salvata:\n{os.path.basename(self.last_audio_path)}')

    def play_last_audio(self):
        """ Riproduce l'ultimo file usando MediaPlayer nativo di Android. """
        if self.player:
             self.player.release()
             self.player = None
        
        if self.last_audio_path and os.path.exists(self.last_audio_path):
            self.player = MediaPlayer()
            try:
                self.player.setDataSource(self.last_audio_path)
                self.player.prepare()
                self.player.start()
                self.update_status(f'In riproduzione...')
            except Exception as e:
                self.update_status(f'Errore MediaPlayer: {e}')
                self.player = None
        else:
            self.update_status('Nessun file da riprodurre.')

    @mainthread
    def update_status(self, text):
        self.root.ids.status_label.text = text

if __name__ == '__main__':
    AudioApp().run()
