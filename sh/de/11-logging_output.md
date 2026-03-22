# 11. Protokollierung und Ausgabe

---

## 11.1 Warum Protokollierung wichtig ist

Ohne Protokollierung:
- Man weiß nicht, wo das Skript steht
- Man weiß nicht, warum es fehlgeschlagen ist
- Man weiß nicht, was es bei Erfolg getan hat

Mit Protokollierung:
- Fortschritt verfolgen
- Genügend Info zum Debuggen von Fehlern
- Ausführungsverlauf prüfen können

---

## 11.2 Grundlegende Protokollebenen

```bash
#!/bin/bash

DEBUG=0
INFO=1
WARN=2
ERROR=3

LOG_LEVEL=${LOG_LEVEL:-$INFO}

log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [[ $level -ge $LOG_LEVEL ]]; then
        echo "[$timestamp] $message"
    fi
}

log $DEBUG "Dies ist Debug"
log $INFO "Dies ist Info"
log $WARN "Dies ist Warnung"
log $ERROR "Dies ist Fehler"
```

---

## 11.3 Farbausgabe

```bash
#!/bin/bash

ROT='\033[0;31m'
GRUEN='\033[0;32m'
GELB='\033[1;33m'
BLAU='\033[0;34m'
NC='\033[0m'  # No Color

log_info() { echo -e "${GRUEN}[INFO]${NC} $@"; }
log_warn() { echo -e "${GELB}[WARN]${NC} $@"; }
log_error() { echo -e "${ROT}[ERROR]${NC} $@" >&2; }

log_info "Installation abgeschlossen"
log_warn "Verwende Standardwerte"
log_error "Verbindung fehlgeschlagen"
```

---

## 11.4 Ausgabe in Datei

```bash
#!/bin/bash

LOG_FILE="/var/log/myapp.log"

log() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $@"
    echo "$message"
    echo "$message" >> "$LOG_FILE"
}

log "Anwendung gestartet"
```

---

## 11.5 `tee`: Ausgabe auf Bildschirm und Datei

```bash
# Anzeigen und gleichzeitig speichern
echo "Hallo" | tee ausgabe.txt

# Anhang-Modus
echo "Welt" | tee -a ausgabe.txt

# Auch stderr erfassen
./skript.sh 2>&1 | tee ausgabe.log
```

---

## 11.6 Fortschrittsanzeigen

### Einfache Punkte

```bash
echo -n "Verarbeite"
for i in {1..10}; do
    echo -n "."
    sleep 0.2
done
echo " Fertig"
```

### Fortschrittsbalken

```bash
zeichne_fortschritt() {
    local current=$1
    local total=$2
    local width=40
    local percent=$((current * 100 / total))
    local chars=$((width * current / total))
    
    printf "\r[%s%s] %3d%%" \
        "$(printf '%*s' $chars | tr ' ' '=')" \
        "$(printf '%*s' $((width - chars)) | tr ' ' '-')" \
        "$percent"
    
    [[ $current -eq $total ]] && echo
}
```

---

## 11.7 `2>&1` erklärt

```bash
# 1 = stdout, 2 = stderr

# stderr zu stdout umleiten
befehl 2>&1

# stdout zu Datei, stderr auf Bildschirm
befehl > ausgabe.txt

# Beides zu Datei umleiten
befehl > ausgabe.txt 2>&1

# Beides nach /dev/null umleiten (verstecken)
befehl > /dev/null 2>&1
```

---

## 11.8 Kurzreferenz

| Syntax | Beschreibung |
|--------|--------------|
| `echo "text"` | Grundlegende Ausgabe |
| `echo -e "\033[31m"` | Farbausgabe |
| `2>&1` | stderr zu stdout umleiten |
| `> datei` | Datei überschreiben |
| `>> datei` | An Datei anhängen |
| `tee datei` | Ausgeben und speichern |
| `tee -a datei` | Anhang-Modus |
| `/dev/null` | Ausgabe verwerfen |

---

## 11.9 Übungen

1. Schreibe ein Skript, das INFO-, WARN-, ERROR-Meldungen in verschiedenen Farben anzeigt
2. Verwende `tee`, um Ausgabe gleichzeitig anzuzeigen und in einer Protokolldatei zu speichern
3. Erstelle ein Dateiverarbeitungsskript mit einem Fortschrittsbalken
4. Baue eine Protokollierungs-Bibliothek, die Dateiausgabe und Protokollebenen unterstützt
