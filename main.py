# --> AI GENERATED: Grok 3 <--
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import traceback
import sys
# Import user-provided modules
import functions
import utility
from logger import Message

# Constant for Android music path
REMOTE_MUSIC_PATH = '/storage/emulated/0/Android/data/org.test.audiorecorder/files/Music'

def get_local_audio_dir():
    """Returns the local audio directory path."""
    if sys.platform == 'win32':
        return os.path.join(os.path.expandvars('%userprofile%'), '.a4a')
    elif sys.platform == 'linux':
        return os.path.join(os.path.expandvars('~'), '.a4a')
    
class AudioEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Main Window Settings ---
        self.title("Audio For Android - Editor")
        self.geometry("800x600")

        # --- State Variables ---
        self.log = utility.log
        self.local_audio_dir = get_local_audio_dir()  # Accesses directory managed by logger
        self.current_file_path = None
        self.audio_data_obj = None

        # --- Create Widgets ---
        self.create_widgets()

        # --- Start phone synchronization ---
        self.sync_phone_music()

    def create_widgets(self):
        """Creates and organizes all GUI widgets."""
        
        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Pane (File Selection) ---
        left_pane = ttk.Frame(main_frame, padding="10")
        left_pane.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(left_pane, text="Local Audio Files", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

        self.file_listbox = tk.Listbox(left_pane, width=30)
        self.file_listbox.pack(fill=tk.Y, expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        
        refresh_button = ttk.Button(left_pane, text="Refresh List", command=self.refresh_file_list)
        refresh_button.pack(pady=10)

        # --- Right Pane (Controls) ---
        right_pane = ttk.Frame(main_frame, padding="10")
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- Controls divided into sections ---
        self.create_analysis_controls(right_pane)
        self.create_modification_controls(right_pane)
        self.create_visualization_controls(right_pane)

        # --- Save Button ---
        save_button = ttk.Button(right_pane, text="Save Changes", command=self.save_audio_file, style="Accent.TButton")
        save_button.pack(pady=20, fill=tk.X)

        # --- Play Button ---
        play_button = ttk.Button(right_pane, text="Play", command=self.play_audio, style="Accent.TButton")
        play_button.pack(pady=30, fill=tk.X)
        
        # --- Status Bar ---
        self.status_bar = ttk.Label(self, text="Ready.", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Style for Save and Play buttons
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="black", background="green")

        # Disable controls on startup
        self.toggle_controls(tk.DISABLED)

    def create_analysis_controls(self, parent):
        """Creates widgets for analysis functions."""
        analysis_frame = ttk.LabelFrame(parent, text="Audio Analysis", padding="10")
        analysis_frame.pack(fill=tk.X, pady=5)
        
        self.btn_distortion = ttk.Button(analysis_frame, text="Check Distortion", command=self.run_distortion_check)
        self.btn_distortion.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_balance = ttk.Button(analysis_frame, text="Check Balance", command=self.run_balance_check)
        self.btn_balance.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_whistle = ttk.Button(analysis_frame, text="Detect Whistle", command=self.run_whistle_check)
        self.btn_whistle.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.btn_annoying_freq = ttk.Button(analysis_frame, text="Check Annoying Frequencies", command=self.run_annoying_freq_check)
        self.btn_annoying_freq.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        analysis_frame.columnconfigure((0, 1), weight=1)

    def create_modification_controls(self, parent):
        """Creates widgets for modification functions."""
        mod_frame = ttk.LabelFrame(parent, text="Audio Modification", padding="10")
        mod_frame.pack(fill=tk.X, pady=5)
        
        # Volume Adjustment
        ttk.Label(mod_frame, text="Volume Factor:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.volume_factor = tk.StringVar(value="1.5")
        ttk.Entry(mod_frame, textvariable=self.volume_factor, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.btn_increase_volume = ttk.Button(mod_frame, text="Apply Volume", command=self.apply_volume_change)
        self.btn_increase_volume.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Noise Reduction
        ttk.Label(mod_frame, text="Noise Start (s):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.noise_start = tk.StringVar(value="0")
        ttk.Entry(mod_frame, textvariable=self.noise_start, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(mod_frame, text="Noise End (s):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.noise_end = tk.StringVar(value="3")
        ttk.Entry(mod_frame, textvariable=self.noise_end, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.btn_reduce_noise = ttk.Button(mod_frame, text="Reduce Noise", command=self.apply_noise_reduction)
        self.btn_reduce_noise.grid(row=1, column=2, rowspan=2, padx=5, pady=5, sticky="nsew")
        
        mod_frame.columnconfigure(2, weight=1)

    def create_visualization_controls(self, parent):
        """Creates widgets for visualization functions."""
        vis_frame = ttk.LabelFrame(parent, text="Visualization", padding="10")
        vis_frame.pack(fill=tk.X, pady=5)

        self.btn_show_limits = ttk.Button(vis_frame, text="Show Amplitude Limits", command=self.show_max_limits)
        self.btn_show_limits.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        self.btn_show_averages = ttk.Button(vis_frame, text="Show Average Values", command=self.show_average_values)
        self.btn_show_averages.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.btn_show_pauses = ttk.Button(vis_frame, text="Show Long Pauses", command=self.show_long_pauses)
        self.btn_show_pauses.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
    def toggle_controls(self, state):
        """Enables or disables all control widgets."""
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.LabelFrame):
                        for sub_widget in widget.winfo_children():
                            if isinstance(sub_widget, (ttk.Button, ttk.Entry)):
                                sub_widget.config(state=state)

    def sync_phone_music(self):
        """Starts synchronization of music files from phone in a separate thread."""
        self.status_bar.config(text=f"Synchronizing from {REMOTE_MUSIC_PATH}...")
        Message("Starting ADB synchronization.", 'i').on_file(self.log)
        
        thread = threading.Thread(target=self._run_adb_pull, daemon=True)
        thread.start()

    def _run_adb_pull(self):
        """Executes adb pull and updates the interface upon completion."""
        try:
            # The adb_pull function already handles logging
            functions.adb_pull(REMOTE_MUSIC_PATH, self.local_audio_dir)
            self.status_bar.config(text="Synchronization completed.")
            Message("ADB synchronization completed successfully.", 'i').on_file(self.log)
        except Exception as e:
            error_msg = f"Error during ADB synchronization: {e}"
            self.status_bar.config(text=error_msg)
            Message(error_msg, 'e').on_file(self.log)
            messagebox.showerror("ADB Error", "Unable to sync with device. Ensure ADB is installed, device is connected, and USB debugging is enabled.")
            traceback.print_exc()
        
        # Update file list in the main interface
        self.after(0, self.refresh_file_list)

    def refresh_file_list(self):
        """Updates the Listbox with audio files in the local directory."""
        self.file_listbox.delete(0, tk.END)
        try:
            audio_files = [f for f in os.listdir(self.local_audio_dir) if f.lower().endswith(('.wav', '.mp3', '.flac'))]
            for file in audio_files:
                self.file_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Read Error", f"Unable to read local directory: {e}")
            Message(f"Unable to read directory {self.local_audio_dir}: {e}", 'e').on_file(self.log)

    def on_file_select(self, event=None):
        """Handles file selection from the list."""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return

        filename = self.file_listbox.get(selected_indices[0])
        self.current_file_path = os.path.join(self.local_audio_dir, filename)

        try:
            audio_file = utility.AudioFile(self.current_file_path)
            self.audio_data_obj = utility.AudioData(audio_file)
            
            self.status_bar.config(text=f"File loaded: {filename}")
            Message(f"File loaded successfully: {self.current_file_path}", 'i').on_file(self.log)
            self.toggle_controls(tk.NORMAL)  # Enable controls
            
        except Exception as e:
            self.status_bar.config(text=f"Error loading {filename}")
            Message(f"Error loading {self.current_file_path}: {e}", 'e').on_file(self.log)
            messagebox.showerror("File Error", f"Unable to load or read audio file:\n{e}")
            self.audio_data_obj = None
            self.toggle_controls(tk.DISABLED)  # Disable controls again
            traceback.print_exc()

    # --- Callback Methods for Buttons ---
    def _check_audio_loaded(self):
        if not self.audio_data_obj:
            messagebox.showwarning("No File", "Select and load an audio file before performing an operation.")
            return False
        return True

    def run_distortion_check(self):
        if not self._check_audio_loaded(): return
        Message(f"Running distortion check on {self.current_file_path}", 'd').on_file(self.log)
        result = self.audio_data_obj.is_distorted()
        messagebox.showinfo("Analysis Result", f"Is the file distorted? {'Yes' if result else 'No'}")
        Message(f"Distortion check result: {result}", 'i').on_file(self.log)

    def run_balance_check(self):
        if not self._check_audio_loaded(): return
        Message(f"Running balance check on {self.current_file_path}", 'd').on_file(self.log)
        result = self.audio_data_obj.is_balanced()
        messagebox.showinfo("Analysis Result", f"Is the file balanced? {'Yes' if result else 'No'}")
        Message(f"Balance check result: {result}", 'i').on_file(self.log)

    def run_whistle_check(self):
        if not self._check_audio_loaded(): return
        Message(f"Running whistle detection on {self.current_file_path}", 'd').on_file(self.log)
        result = self.audio_data_obj.is_rising_trend()
        messagebox.showinfo("Analysis Result", f"Whistle detected? {'Yes' if result else 'No'}")
        Message(f"Whistle detection result: {result}", 'i').on_file(self.log)

    def run_annoying_freq_check(self):
        if not self._check_audio_loaded(): return
        Message(f"Running annoying frequencies check on {self.current_file_path}", 'd').on_file(self.log)
        result = self.audio_data_obj.has_annoying_frequency()
        messagebox.showinfo("Analysis Result", f"Contains annoying frequencies (2-5 kHz)? {'Yes' if result else 'No'}")
        Message(f"Annoying frequencies check result: {result}", 'i').on_file(self.log)

    def apply_volume_change(self):
        if not self._check_audio_loaded(): return
        try:
            factor = float(self.volume_factor.get())
            Message(f"Applying volume increase (factor: {factor}) to {self.current_file_path}", 'd').on_file(self.log)
            self.audio_data_obj.increase_volume(factor)
            messagebox.showinfo("Operation Completed", f"Volume modified with factor {factor}.")
            Message("Volume modified successfully.", 'i').on_file(self.log)
        except ValueError:
            messagebox.showerror("Input Error", "Volume factor must be a number.")
        except Exception as e:
            messagebox.showerror("Operation Error", f"Error modifying volume: {e}")
            Message(f"Error modifying volume: {e}", 'e').on_file(self.log)

    def apply_noise_reduction(self):
        if not self._check_audio_loaded(): return
        try:
            start_time = float(self.noise_start.get())
            end_time = float(self.noise_end.get())
            Message(f"Applying noise reduction (from {start_time}s to {end_time}s) to {self.current_file_path}", 'd').on_file(self.log)
            self.audio_data_obj.reduce_noise_section(start_time, end_time)
            messagebox.showinfo("Operation Completed", "Noise reduction applied.")
            Message("Noise reduction applied successfully.", 'i').on_file(self.log)
        except ValueError:
            messagebox.showerror("Input Error", "Start and end times must be numbers.")
            traceback.print_exc()
        except Exception as e:
            messagebox.showerror("Operation Error", f"Error during noise reduction: {e}")
            Message(f"Error during noise reduction: {e}", 'e').on_file(self.log)
            
    def show_max_limits(self):
        if not self._check_audio_loaded(): return
        Message(f"Visualizing amplitude limits for {self.current_file_path}", 'd').on_file(self.log)
        self.audio_data_obj.plot_max_amplitude_limits()

    def show_average_values(self):
        if not self._check_audio_loaded(): return
        Message(f"Visualizing average values for {self.current_file_path}", 'd').on_file(self.log)
        self.audio_data_obj.plot_average_values()

    def show_long_pauses(self):
        if not self._check_audio_loaded(): return
        Message(f"Visualizing long pauses for {self.current_file_path}", 'd').on_file(self.log)
        self.audio_data_obj.plot_long_silences()
        
    def save_audio_file(self):
        """Saves modified audio data to a new file."""
        if not self._check_audio_loaded(): return

        # Ask user where to save the new file
        initial_filename = os.path.splitext(os.path.basename(self.current_file_path))[0] + "_modified.wav"
        save_path = filedialog.asksaveasfilename(
            initialdir=self.local_audio_dir,
            initialfile=initial_filename,
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )

        if not save_path:
            return  # User canceled

        try:
            import soundfile as sf
            Message(f"Saving modified file to: {save_path}", 'i').on_file(self.log)
            sf.write(save_path, self.audio_data_obj.data, self.audio_data_obj.rate)
            messagebox.showinfo("Save Completed", f"File saved successfully to:\n{save_path}")
            Message("File saved successfully.", 'i').on_file(self.log)
        except Exception as e:
            messagebox.showerror("Save Error", f"Unable to save file: {e}")
            Message(f"Error saving file to {save_path}: {e}", 'e').on_file(self.log)
    
    def play_audio(self):
        if not self._check_audio_loaded(): return

        try:
            self.audio_data_obj.play_audio()
            Message("File played successfully.", 'i').on_file(self.log)
        except Exception as e:
            Message(f"Error playing file: {e}", 'e').on_file(self.log)

if __name__ == "__main__":
    app = AudioEditorApp()
    app.mainloop()