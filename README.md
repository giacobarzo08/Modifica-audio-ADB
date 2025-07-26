# Modifica-audio-ADB
## **PREGETTO IN FARE DI COSTRUZIONE**
Questo progetto ha lo scopo facilitare delle semplici modifiche a file audio (estensione .mp3) registati da telefono sfruttando la potenza di calcolo di Hardware di grandi dimensioni e le prestanti librerie Python disponibili su PC (Windows o Linux).

Collegando il telefono cellulare al computer tramite cavo USB (il **debug USB** deve essere abilitato, per quasto è possibile seguire la guida allegata ed il cavo deve **essere in grado di trasferire dati**) il programma è in grado di clonare in automatico tutti i file .mp3 dalla directory Music del telefono fino alla cartella ` %userprifile%\AppData\local\a4a\Music\Music ` (su Windows) o ` ~/.a4a ` (su Linux). I file potranno poi essere selezionati direttamente nell'**interfaccia grafica**.

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

*SCRITTO A SCOPO DIDATTICO*
