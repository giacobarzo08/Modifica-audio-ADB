# Modifica-audio-ADB

Questo progetto ha lo scopo facilitare delle semplici modifiche a file audio (estensione .mp3) registati da telefono sfruttando la potenza di calcolo di Hardware di grandi dimensioni e le prestanti librerie Python disponibili su PC (Windows o Linux).

Collegando il telefono cellulare al computer tramite cavo USB (il **debug USB** deve essere abilitato, per quasto è possibile seguire la guida allegata ed il cavo deve **essere in grado di trasferire dati**) il programma è in grado di clonare in automatico tutti i file .mp3 dalla directory Music del telefono fino alla cartella ` %userprifile%\.a4a ` (su Windows) o ` ~/.a4a ` (su Linux). I file potranno poi essere selezionati direttamente nell'**interfaccia grafica**.

Le modifiche ai file permesse sono le seguenti:
- aumentare il volume
- diminuire il rumore di sottofondo

E' possibile verificare se:
- l'audio distorce
- l'audio è bilanciato
- è presente un fischio crescente in volume
- la frequenza prevalente nell'audio è fastidiosa (compresa tra 2kHz e 5kHz)

E' inoltre possibile vedere il plot della traccia audio mostrando:
- Le linee orizzontali che indicano i valori massimo positivo e massimo negativo (con i valori soglia +1 e -1 di riferimento)
- Le linee orizzontali che mostrano i valori medi dei canali destro e sinistro
- Le linee verticali che mostrano i periodi di lungo (più del 10% dell'intera durata dell'audio) di silenzio (ampiezza minore del 20% della media maggiore)

La parte grafica del software è stata scritta dal software AI Gemini 2.5 Pro (anche se Grok dopo la revisione ha deciso di prendersi il merito, [daltrocanto ...](https://help.x.com/it/using-x/about-grok)). Sono stati sfruttati altri software AI per la revisione: ChatGPT 4.1 mini, Grok 3, Copilot, Gemini 2.5 Flash

## Requisiti di sistema
E' necessario avere Python 3.6+. (o usare il file exe per Windows)
E' necessario avere installato `pydub` (E' possibile installarlo con `sudo apt install ffmpeg` su Debian-like o `winget install ffmpeg` su Windows)

Le librerie usate sono:
- `os`: di sistema
- `threading`: di sistema
- `tkinter`: solitamente installata automaticamente con l'installazione di Python sul computer
- `subprocess`: di sistema
- `typing`: di sistema
- `numpy`: solitamente installata automaticamente con l'installazione di Python sul computer
- `sounddevice`: da installare
- `pydub`: da installare
- `ffmpeg-python`: da installare
- `noisereduce`: da installare
- `shutil`: di sistema
- `matplotlib`: da installare
- `datetime`: di sistema
- `sys`: di sistema
- `tracenack`: di sistema
Ne consegue che il comando da usare per installare i pacchetti mancanti è il seguente:
```bash
python.exe -m pip install --upgrade pip
pip install sounddevice pydub noisereduce matplotlib ffmpeg-python
# solo se necessario
pip install tkinter numpy
```
E' possibile che in Linux l'installazione sia diversa (ed esempio pip viene aggiornato in automatico con l'aggiornamento del sistema: `sudo apt update` seguito da `sudo apt upgrade -y`); può essere necessario sostituire `pip` con `pip3`; Può essere impossibile installare sounndevice tramite pip o apt (è necessario usare conda). In vrsioni recenti di Ubuntu, pip non è autorizzato ad installare pacchetti globalmente: bisogna usare `sudo pip install` (sconsigliato), `pip install --user` o un ambiente virtuale creato con `venv`. Per installare pip è sufficiente il seguente comando:
```bash
sudo apt update
sudo apt install python-pip
sudo apt install python3-venv
```
L'uso di WSL (Windows Subsistem for Linux) è **altamente sconsigliato**: il sistema Linux non è in grado di usare gli altoparlante e le porte USB del hardware.

## Guida all'uso
Come prima cosa assicurarsi che la variabile `REMOTE_MUSIC_PATH` contenga il percorso giusto per la dirctory della musica del telefono.

Eseguendo il file `main.py` (o il file `main.exe`) si aprirà un un display, suddiviso in più parti:
- A sinistra si vedono tutti i file audio della directory in cui viene salvata la musica del telefono (carica solo file `.mp3` e salva i file in estensione `.wav`).
- E' possibile ricaricare la directroy, qualora i file fossero stati modoficati manualmente.
- Nella sezione "Audio Analysis" è possibile verificare se l'audio distorce (Check Distorsion), l'audio è bilanciato (canali destro e sinistro) (Check Balance), è presente un fischio crescente in volume (Detect Whistle) o verficare la presenza di frequenze fastidiose (Check Annoying Frequencies). Per queste informazioni, apparirà una maschera che mostra i risultati.
- Nella sezione "Audio Modification" è possibile aumentare il volume moltiplicando tutti i valori del vettore contenente l'audio per un fattore comune (da inserire a destra del bottone) e rimuovere il rumore di sottofondo, specificando l'istante di inizio e di fine (in secondi) di una pausa (in cui c'è solo rumore).
- I bottoni della funzione "Visualizzation" consentono di mostrare il plot dell'audio, evidenziando: i limiti di ampiezza, i valori medi positivi e negativi ed i periodi di lungo silenzio.

## Licenza
*SCRITTO A SCOPO DIDATTICO*
Non esiste una licenza per questo progetto: potete fare qualsiasi cosa, anche venderlo (sebbene non ricavereste molto ;-) ).

Il progetto è stato creato a scopo didattico (compito) e pupplicato a tale scopo.
