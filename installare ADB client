### **Cos'è ADB?**
ADB è uno strumento a riga di comando incluso nell'Android SDK (Software Development Kit) che permette di comunicare con un dispositivo Android per eseguire operazioni come il debug, l'installazione di app, il trasferimento di file e molto altro.

---

### **1. Installazione di ADB su Windows**

#### **Passo 1: Scaricare gli strumenti della piattaforma Android SDK**
1. Visita il sito ufficiale di Android per scaricare gli strumenti della piattaforma SDK:
   - **URL**: [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)
2. Scorri fino alla sezione **"Command line tools only"** e scarica il file .zip per Windows (es. `platform-tools_rXX.X.X-windows.zip`, dove `XX.X.X` è la versione più recente).

#### **Passo 2: Estrazione del file**
1. Una volta scaricato, estrai il contenuto del file .zip in una cartella a tua scelta (es. `%userprofile%\platform-tools`).
   - Usa un programma come WinRAR, 7-Zip o l'estrattore integrato di Windows per decomprimere il file.
2. All'interno della cartella estratta troverai file come `adb.exe`, `fastboot.exe`, ecc.

#### **Passo 3: Configurare le variabili d'ambiente (opzionale, ma consigliato)**
Per eseguire il comando `adb` da qualsiasi posizione nel Prompt dei comandi o PowerShell, aggiungi la cartella di ADB alle variabili d'ambiente:
1. Cerca nella barra diricerca di Windows "Modifica le variabili d'ambiente per l'account" e apri il programma.
2. Seleziona Path e fai click su modifica.
3. Seleziona `aggiungi nuovo` ed incolla il precorso della cartella (es. `%userprofile%\platform-tools`). Fai click su `salva` o `applica`.
4. Conferma con **OK**.
5. Rievvia il sistema
Altrimenti dovrai intrare nella cartella di installazione di adb per eseguire i comandi, tuttavia il software in questo repertory richiede l'installazione in path.

#### **Passo 4: Verifica dell'installazione**
1. Apri il **Prompt dei comandi** (digita Win + R sulla tastiera e cerca `cmd.exe`).
2. Digita:
   ```bash
   adb version
   ```
3. Se l'installazione è corretta, vedrai la versione di ADB installata (es. `Android Debug Bridge version X.X.X`).

#### **Passo 5: Abilitare il debug USB sul dispositivo Android**
Segui la guida dettagliata allegata

---

### **2. Installazione di ADB su sistemi Debian-like (es. Ubuntu)**

#### **Passo 1: Installazione tramite il gestore dei pacchetti**
Su sistemi Debian-like, puoi installare ADB direttamente dai repository ufficiali senza scaricare manualmente il file .zip:
1. Apri il **Terminale**.
2. Aggiorna la lista dei pacchetti:
   ```bash
   sudo apt update
   ```
3. Installa ADB con il comando:
   ```bash
   sudo apt install adb
   ```
   Questo installerà ADB e le sue dipendenze.

#### **Passo 2: Scaricare manualmente gli strumenti della piattaforma Android SDK (opzionale)**
Se preferisci scaricare l'ultima versione di ADB direttamente dal sito di Android:
1. Visita lo stesso sito: [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools).
2. Scarica il file .zip per Linux (es. `platform-tools_rXX.X.X-linux.zip`).
3. Estrai il file in una cartella, ad esempio:
   ```bash
   unzip platform-tools_rXX.X.X-linux.zip -d ~/platform-tools
   ```
   - Se `unzip` non risulta installato, si può installare con:
    ```bash
    sudo apt update
    suo apt install -y unzip
    ```

#### **Passo 3: Configurare il percorso (opzionale, per l'installazione manuale)**
Per rendere il comando `adb` accessibile da qualsiasi posizione:
1. Apri il file di configurazione del terminale (es. `~/.bashrc` o `~/.zshrc`):
   ```bash
   nano ~/.bashrc
   ```
2. Aggiungi questa riga alla fine del file:
   ```bash
   export PATH=$PATH:~/platform-tools
   ```
3. Salva il file (Ctrl+O, poi Ctrl+X in nano) e aggiorna la configurazione:
   ```bash
   source ~/.bashrc
   ```

#### **Passo 4: Verifica dell'installazione**
1. Nel terminale, digita:
   ```bash
   adb version
   ```
2. Dovresti vedere l'output con la versione di ADB installata.

#### **Passo 5: Configurare le regole udev per il dispositivo Android**
Per garantire che il dispositivo Android sia riconosciuto correttamente:
1. Crea o modifica le regole udev:
   ```bash
   sudo nano /etc/udev/rules.d/51-android.rules
   ```
2. Aggiungi una riga come questa (sostituisci `VENDOR_ID` con l'ID del produttore del dispositivo Android, reperibile online):
   ```bash
   SUBSYSTEM=="usb", ATTR{idVendor}=="VENDOR_ID", MODE="0666", GROUP="plugdev"
   ```
3. Salva il file e ricarica le regole:
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```
4. Aggiungi il tuo utente al gruppo `plugdev`:
   ```bash
   sudo usermod -aG plugdev $USER
   ```

#### **Passo 6: Abilitare il debug USB**
Come per Windows, abilita il **Debug USB** sul dispositivo Android.

---

### **Note aggiuntive**
- **Sito ufficiale per il download**: Il file .zip di Android SDK Platform Tools è sempre disponibile su [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools). Questo garantisce che stai scaricando una versione ufficiale e sicura.
- **Driver USB per Windows**: Su Windows, potrebbe essere necessario installare i driver USB specifici per il tuo dispositivo Android. Puoi scaricarli dal sito del produttore (es. Samsung, Xiaomi, ecc.).
- **Comandi utili di ADB**:
  - `adb devices`: Elenca i dispositivi connessi.
  - `adb shell`: Apre una shell interattiva sul dispositivo.
  - `adb push <file> <percorso>`: Trasferisce un file sul dispositivo.
  - `adb install <apk>`: Installa un'app APK sul dispositivo.

Se hai bisogno di ulteriori dettagli o di aiuto con comandi specifici, fammi sapere!
