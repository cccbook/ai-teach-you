# 6. Berechtigungen, Ausführung, Umgebung und Einstellungen

---

## 6.1 `chmod`: Die Kunst der Berechtigungen

### Linux/Unix-Berechtigungsgrundlagen

```
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 .
-rw-r--r--  1 ai  staff  4096 Mar 22 10:30 README.md
-rwxr-xr-x  1 ai  staff   128 Mar 22 10:30 script.sh
```

Die 9 Zeichen sind in drei Gruppen:
- `rwx` (Eigentümer): lesen, schreiben, ausführen
- `r-x` (Gruppe): lesen, ausführen
- `r--` (andere): nur lesen

### chmod Zwei Darstellungen

**Numerisch (oktal)**:

```
r = 4, w = 2, x = 1

rwx = 7, r-x = 5, r-- = 4
```

Häufige Kombinationen:
- `777` = rwxrwxrwx (gefährlich!)
- `755` = rwxr-xr-x
- `644` = rw-r--r--
- `700` = rwx------
- `600` = rw-------

**Symbolisch**:

```bash
chmod u+x script.sh    # Eigentümer fügt Ausführung hinzu
chmod g-w file.txt     # Gruppe entfernt Schreiben
chmod +x script.sh     # Alle fügen Ausführung hinzu
```

### Häufige chmod-Verwendung der KI

```bash
# Skript ausführbar machen (fast jedes Skript)
chmod +x script.sh

# Verzeichnis durchquerbar machen
chmod +x ~/projects

# Gruppenweise beschreibbare Verzeichnisse
chmod -R g+w project/
```

---

## 6.2 Shell-Skripte ausführen

### Ausführungsmethoden

```bash
# Methode 1: Pfadausführung (braucht Ausführungsberechtigung)
./script.sh

# Methode 2: bash verwenden (braucht keine Ausführungsberechtigung)
bash script.sh

# Methode 3: source verwenden (führt in aktueller Shell aus)
source script.sh
```

### Wann welche verwenden?

| Methode | Wann verwenden | Eigenschaften |
|---------|-----------------|---------------|
| `./script.sh` | Standardausführung | braucht `chmod +x`, Subshell |
| `bash script.sh` | Shell angeben | keine Ausführungsberechtigung nötig |
| `source script.sh` | Umgebung setzen | führt in aktueller Shell aus |

### Der wichtige Unterschied: `source` vs `./script`

```bash
# script.sh Inhalt: export MY_VAR="hallo"

# Ausführen mit ./
./script.sh
echo $MY_VAR  # Ausgabe: (leer) ← in Subshell, Variable weg

# Ausführen mit source
source script.sh
echo $MY_VAR  # Ausgabe: hallo ← in aktueller Shell, Variable bleibt
```

---

## 6.3 `export`: Umgebungsvariablen

```bash
# Umgebungsvariable setzen
export NAME="Alice"
export PATH="$PATH:/neues/verzeichnis"

# Alle Umgebungsvariablen anzeigen
export

# Häufige Variablen
echo $HOME      # Home-Verzeichnis
echo $USER      # Benutzername
echo $PATH      # Suchpfad
echo $PWD       # Aktuelles Verzeichnis
```

### Umgebungsvariablen persistent machen

```bash
# Zu ~/.bashrc hinzufügen
echo 'export EDITOR=vim' >> ~/.bashrc

# Änderungen anwenden
source ~/.bashrc
```

---

## 6.4 `source`: Dateien laden

Entspricht: den Inhalt der Datei direkt **einfügen** an der aktuellen Position und ausführen.

### Häufige Verwendungen

```bash
# Virtuelle Umgebung laden
source venv/bin/activate

# .env-Datei laden
source .env

# Bibliothek laden
source ~/scripts/common.sh
```

### Praktisch: Modulare Konfigurationsdateien

```bash
# config.sh
export DB_HOST="localhost"
export DB_PORT="5432"

# In anderen Skripten verwenden
source config.sh
psql -h $DB_HOST -p $DB_PORT
```

---

## 6.5 `env`: Umgebungsverwaltung

```bash
# Alle Umgebungsvariablen anzeigen
env

# Mit sauberer Umgebung ausführen
env -i HOME=/tmp PATH=/bin sh

# Variablen setzen und ausführen
env VAR1=value1 VAR2=value2 ./my_program
```

### Befehle finden

```bash
which python      # Befehlsposition finden
type cd           # Shell-Builtins finden
whereis gcc       # Alle zugehörigen Dateien finden
```

---

## 6.6 `sudo`: Privilegien eskalieren

```bash
# Als root ausführen
sudo rm /var/log/old.log

# Als bestimmten Benutzer ausführen
sudo -u postgres psql

# Anzeigen, was Sie tun können
sudo -l
```

### Gefahrenwarnung

```bash
# Niemals dies ausführen!
sudo rm -rf /

# Niemals dies tun!
sudo curl http://unbekannte-seite.com | sh
```

---

## 6.7 Schnellreferenz

| Befehl | Zweck | Häufige Flags |
|--------|-------|---------------|
| `chmod` | Dateiberechtigungen ändern | `+x` Ausführung hinzufügen, `755` oktal, `-R` rekursiv |
| `chown` | Eigentümer ändern | `user:group`, `-R` rekursiv |
| `./script` | Skript ausführen (braucht x) | - |
| `bash script` | Skript ausführen (kein x nötig) | - |
| `source` | In aktueller Shell ausführen | - |
| `export` | Umgebungsvariablen setzen | `-n` entfernen |
| `env` | Umgebung anzeigen/verwalten | `-i` leeren |
| `sudo` | Als root ausführen | `-u user` Benutzer angeben |

---

## 6.8 Übungen

1. Erstellen Sie ein Skript, setzen Sie Berechtigungen mit `chmod 755`, führen Sie es dann aus
2. Führen Sie dasselbe Umgebungsvariablen-Skript mit `source` und `./` aus, beobachten Sie den Unterschied
3. Verwenden Sie `env -i`, um eine saubere Umgebung zu erstellen, führen Sie `python --version` aus
4. Erstellen Sie eine `.env`-Datei, verwenden Sie `source`, um ihre Variablen zu laden
