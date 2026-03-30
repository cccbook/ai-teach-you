# 7. Flusskontrolle und bedingte Schleifen

---

## 7.1 Befehle kombinieren: Das Wesen von Shell

Einzelne Befehle haben begrenzte Fähigkeiten. Nur durch **Kombinieren** können Sie komplexe Aufgaben erledigen.

Die KI ist leistungsstark, largely weil sie diese Kombinationen beherrscht:

```bash
cat access.log | grep "ERROR" | sort | uniq -c | sort -rn | head -10
```

Das bedeutet: "Von access.log, Fehler finden, Vorkommen zählen, Top 10 anzeigen"

---

## 7.2 `|` (Pipe): Die Kunst des Datenflusses

Die Pipe verwandelt die **Ausgabe** des vorherigen Befehls in die **Eingabe** des nächsten.

```bash
# Dateiinhalt sortieren
cat unsorted.txt | sort

# Häufigste Befehle finden
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# IPs aus Log extrahieren und zählen
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```

### stderr leiten

```bash
# stderr zur Pipe senden
command1 2>&1 | command2

# Oder Bash 4+
command1 |& command2
```

---

## 7.3 `&&`: Nächsten nur ausführen, wenn erfolgreich

**Nur wenn `command1` erfolgreich ist (Exit-Code = 0) wird `command2` ausgeführt.**

```bash
# Verzeichnis erstellen dann hineinwechseln
mkdir -p project && cd project

# Kompilieren dann ausführen
gcc -o program source.c && ./program

# Herunterladen dann entpacken
curl -L -o archive.tar.gz http://example.com/file && tar -xzf archive.tar.gz
```

---

## 7.4 `||`: Nächsten nur ausführen, wenn fehlgeschlagen

**Nur wenn `command1` fehlschlägt (Exit-Code ≠ 0) wird `command2` ausgeführt.**

```bash
# Datei erstellen wenn sie nicht existiert
[ -f config.txt ] || echo "Config fehlt" > config.txt

# Versuche einen Weg, fallback zu einem anderen
cd /opt/project || cd /home/user/project

# Erfolg sicherstellen auch bei Fehler (häufig in Makefiles)
cp file.txt file.txt.bak || true
```

### `&&` und `||` kombinieren

```bash
# Bedingter Ausdruck
[ -f config ] && echo "Gefunden" || echo "Nicht gefunden"

# Äquivalent zu:
if [ -f config ]; then
    echo "Gefunden"
else
    echo "Nicht gefunden"
fi
```

---

## 7.5 `;`: Unabhängig ausführen

```bash
# Alle drei werden ausgeführt
mkdir /tmp/test ; cd /tmp/test ; pwd
```

---

## 7.6 `$()`: Befehlssubstitution

**Befehl ausführen, `$()` durch seine Ausgabe ersetzen.**

```bash
# Grundlegende Verwendung
echo "Heute ist $(date +%Y-%m-%d)"
# Ausgabe: Heute ist 2026-03-22

# In Variablen
FILES=$(ls *.txt)

# Verzeichnisnamen holen
DIR=$(dirname /path/to/file.txt)
BASE=$(basename /path/to/file.txt)

# Berechnen
echo "Ergebnis ist $((10 + 5))"
# Ausgabe: Ergebnis ist 15
```

### vs Backticks

```bash
# Beide sind äquivalent
echo "Heute ist $(date +%Y)"
echo "Heute ist `date +%Y`"

# Aber $() ist besser, weil es verschachteln kann
echo $(echo $(echo verschachtelt))
```

---

## 7.7 `[[ ]]` und `[ ]`: Bedingte Tests

### Datei-Tests

```bash
[[ -f file.txt ]]      # Reguläre Datei existiert
[[ -d directory ]]     # Verzeichnis existiert
[[ -e path ]]           # Irgendetwas existiert
[[ -L link ]]           # Symbolischer Link existiert
[[ -r file ]]           # Lesbar
[[ -w file ]]           # Schreibbar
[[ -x file ]]           # Ausführbar
[[ file1 -nt file2 ]]  # file1 ist neuer als file2
```

### String-Tests

```bash
[[ -z "$str" ]]        # String ist leer
[[ -n "$str" ]]        # String ist nicht leer
[[ "$str" == "wert" ]] # Gleich
[[ "$str" =~ muster ]]  # Regex übereinstimmen
```

### Numerische Tests

```bash
[[ $num -eq 10 ]]      # Gleich
[[ $num -ne 10 ]]      # Nicht gleich
[[ $num -gt 10 ]]      # Größer als
[[ $num -lt 10 ]]      # Kleiner als
```

---

## 7.8 `if`: Bedingte Anweisungen

```bash
if [[ bedingung ]]; then
    # etwas tun
elif [[ bedingung2 ]]; then
    # etwas anderes tun
else
    # fallback
fi
```

### Vollständiges Beispiel

```bash
#!/bin/bash

FILE="config.yaml"

if [[ ! -f "$FILE" ]]; then
    echo "Fehler: $FILE existiert nicht"
    exit 1
fi

if [[ -r "$FILE" ]]; then
    echo "Datei ist lesbar"
else
    echo "Datei ist nicht lesbar"
fi
```

---

## 7.9 `for`: Schleifen

### Grundlegende Syntax

```bash
for variable in liste; do
    # $variable verwenden
done
```

### Häufige Muster der KI

```bash
# Alle .txt-Dateien verarbeiten
for file in *.txt; do
    echo "Verarbeite $file"
done

# Zahlenbereich
for i in {1..10}; do
    echo "Iteration $i"
done

# Array
for color in rot grün blau; do
    echo $color
done

# C-Stil-Schleife (Bash 3+)
for ((i=0; i<10; i++)); do
    echo $i
done
```

---

## 7.10 `while`: Bedingte Schleifen

```bash
# Zeilen lesen
while IFS= read -r line; do
    echo "Gelesen: $line"
done < file.txt

# Zählschleife
count=0
while [[ $count -lt 10 ]]; do
    echo $count
    ((count++))
done
```

---

## 7.11 `case`: Musterabgleich

```bash
case $AKTION in
    start)
        echo "Service wird gestartet..."
        ;;
    stop)
        echo "Service wird gestoppt..."
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Verwendung: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### Wildcard-Muster

```bash
case "$filename" in
    *.txt)
        echo "Textdatei"
        ;;
    *.jpg|*.png|*.gif)
        echo "Bilddatei"
        ;;
    *)
        echo "Unbekannter Typ"
        ;;
esac
```

---

## 7.12 Schnellreferenz

| Symbol | Name | Beschreibung |
|--------|------|-------------|
| `\|` | Pipe | Ausgabe an nächste Eingabe weiterleiten |
| `&&` | UND | Nächsten nur ausführen, wenn vorheriger erfolgreich |
| `\|\|` | ODER | Nächsten nur ausführen, wenn vorheriger fehlschlägt |
| `;` | Semikolon | Unabhängig ausführen |
| `$()` | Befehlssubstitution | Ausführen, durch Ausgabe ersetzen |
| `[[ ]]` | Bedingter Test | empfohlene Test-Syntax |
| `if` | Bedingung | Verzweigung basierend auf Bedingung |
| `for` | Zählschleife | durch Liste iterieren |
| `while` | Bedingte Schleife | wiederholen solange Bedingung wahr |
| `case` | Musterabgleich | Mehrweg-Verzweigung |

---

## 7.13 Übungen

1. Verwenden Sie `|`, um `ls`, `grep`, `wc` zu kombinieren und `.log`-Dateien zu zählen
2. Verwenden Sie `&&`, um sicherzustellen, dass `cd` erfolgreich ist, bevor Sie fortfahren
3. Verwenden Sie eine `for`-Schleife, um 10 Verzeichnisse (dir1 bis dir10) zu erstellen
4. Verwenden Sie `while read`, um /etc/hosts zu lesen und anzuzeigen
5. Schreiben Sie einen einfachen Rechner mit `case` (addieren, subtrahieren, multiplizieren, dividieren)
