# 5. Textverarbeitung

---

## 5.1 Die Textverarbeitungsphilosophie der KI

In der Welt der KI ist **alles Text**.

- Code ist Text
- Konfigurationsdateien sind Text
- Logs sind Text
- JSON, HTML, Markdown sind alles Text

Also sind Textverarbeitungsbefehle der Kern des Werkzeugkastens der KI.

Wenn menschliche Ingenieure auf Probleme stoßen: "Ich brauche ein Werkzeug, um dies zu behandeln..."
Wenn die KI auf Probleme stößt: "Dies kann mit `grep | sed | awk` in einer Zeile gelöst werden."

---

## 5.2 `cat`: Die Kunst des Dateilesens

### Grundlegende Verwendung

```bash
# Dateiinhalt anzeigen
cat file.txt

# Dateien kombinieren
cat part1.txt part2.txt > whole.txt

# Zeilennummern anzeigen
cat -n script.sh
```

### Eigentlicher Zweck: Kombinieren und Erstellen

```bash
cat << 'EOF' > newfile.txt
Dateinhalt
Kann viele Zeilen schreiben
EOF
```

---

## 5.3 `head` und `tail`: Nur sehen, was Sie brauchen

### `head`: Anfang betrachten

```bash
# Erste 10 Zeilen (Standard)
head file.txt

# Erste 5 Zeilen
head -n 5 file.txt

# Erste 100 Bytes
head -c 100 file.txt
```

### `tail`: Ende betrachten

```bash
# Letzte 10 Zeilen (Standard)
tail file.txt

# Letzte 5 Zeilen
tail -n 5 file.txt

# Datei in Echtzeit verfolgen (am häufigsten!)
tail -f /var/log/syslog

# Verfolgen und filtern
tail -f app.log | grep --line-buffered ERROR
```

### Bestimmten Zeilenbereich betrachten

```bash
# Zeilen 100-150 betrachten
tail -n +100 file.txt | head -n 50
```

---

## 5.4 `wc`: Zählwerkzeug

```bash
# Zeilen zählen
wc -l file.txt

# Zeilen für mehrere Dateien zählen
wc -l *.py

# Dateien im Verzeichnis zählen
ls | wc -l
```

---

## 5.5 `grep`: König der Textsuche

### Grundlegende Verwendung

```bash
# Nach "error"-Zeilen suchen
grep "error" log.txt

# Groß-/Kleinschreibung ignorieren
grep -i "error" log.txt

# Zeilennummern anzeigen
grep -n "error" log.txt

# Nur Dateinamen anzeigen
grep -l "TODO" *.md

# Umkehren (nicht übereinstimmende Zeilen)
grep -v "debug" log.txt

# Ganzes Wort
grep -w "error" log.txt
```

### Reguläre Ausdrücke

```bash
# Anfang übereinstimmen
grep "^Error" log.txt

# Ende übereinstimmen
grep "done.$" log.txt

# Beliebiges Zeichen
grep "e.or" log.txt

# Bereich
grep -E "[0-9]{3}-" log.txt
```

### Fortgeschrittene Techniken

```bash
# Rekursive Suche
grep -r "TODO" src/

# Nur bestimmte Erweiterung
grep -r "TODO" --include="*.py" src/

# Kontextzeilen anzeigen
grep -B 2 -A 2 "ERROR" log.txt

# Mehrere Bedingungen (ODER)
grep -E "error|warning|fatal" log.txt
```

---

## 5.6 `sed`: Textersetzungswerkzeug

### Grundlegende Ersetzung

```bash
# Erste Übereinstimmung ersetzen
sed 's/alt/neu/' file.txt

# Alle Übereinstimmungen ersetzen
sed 's/alt/neu/g' file.txt

# Direkte Ersetzung in Datei
sed -i 's/alt/neu/g' file.txt

# Backup dann ersetzen
sed -i.bak 's/alt/neu/g' file.txt
```

### Zeilen löschen

```bash
# Leere Zeilen löschen
sed '/^$/d' file.txt

# Kommentarzeilen löschen
sed '/^#/d' file.txt

# Nachgestellte Leerzeichen löschen
sed 's/[[:space:]]*$//' file.txt
```

### Praktische Beispiele

```bash
# Stapelweise Erweiterung ändern (.txt → .md)
for f in *.txt; do
    mv "$f" "$(sed 's/.txt$/.md/' <<< "$f")"
done

# Windows-Zeilenenden entfernen
sed -i 's/\r$//' file.txt
```

---

## 5.7 `awk`: Schweizer Taschenmesser der Textverarbeitung

### Grundkonzept

`awk` verarbeitet Text zeilenweise, teilt automatisch in Felder ($1, $2, $3...), führt angegebene Aktionen für jede Zeile aus.

### Grundlegende Verwendung

```bash
# Standardmäßige Whitespace-Aufteilung
awk '{print $1}' file.txt

# Trennzeichen angeben
awk -F: '{print $1}' /etc/passwd

# Mehrere Felder ausgeben
awk -F: '{print $1, $3, $7}' /etc/passwd
```

### Bedingte Verarbeitung

```bash
# Nur übereinstimmende Zeilen verarbeiten
awk -F: '$3 > 1000 {print $1}' /etc/passwd

# BEGIN und END
awk 'BEGIN {print "Start"} {print} END {print "Fertig"}' file.txt
```

### Praktische Beispiele

```bash
# Eine CSV-Spalte summieren
awk -F, '{sum += $3} END {print sum}' data.csv

# Maximum finden
awk 'NR==1 {max=$3} $3>max {max=$3} END {print max}' data.csv

# Formatierte Ausgabe
awk '{printf "%-20s %10.2f\n", $1, $2}' data.txt
```

---

## 5.8 Übung: Alle Werkzeuge kombinieren

### Szenario: Server-Logs analysieren

```bash
# 1. Fehlermeldungen finden
grep -i "error" access.log

# 2. Fehler zählen
grep -ci "error" access.log

# 3. Häufigste Fehler finden
grep "error" access.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head

# 4. Anfragen pro Stunde zählen
awk '{print $4}' access.log | cut -d: -f2 | sort | uniq -c
```

### Szenario: Code stapelweise ändern

```bash
# "print" zu "logger.info" in allen .py-Dateien ändern
find . -name "*.py" -exec sed -i 's/print(/logger.info(/g' {} +

# var zu const ändern
find . -name "*.js" -exec sed -i 's/\bvar\b/const/g' {} +
```

---

## 5.9 Schnellreferenz

| Befehl | Zweck | Häufige Flags |
|--------|-------|---------------|
| `cat` | Dateien anzeigen/kombinieren | `-n` Zeilennummern |
| `head` | Dateianfang betrachten | `-n` Zeilen, `-c` Bytes |
| `tail` | Dateiende betrachten | `-n` Zeilen, `-f` folgen |
| `wc` | Zählen | `-l` Zeilen, `-w` Wörter, `-c` Bytes |
| `grep` | Textsuche | `-i` ignorieren, `-n` Zeilennummer, `-r` rekursiv, `-c` zählen |
| `sed` | Textersetzung | `s/alt/neu/g`, `-i` direkt |
| `awk` | Feldverarbeitung | `-F` Trennzeichen, `{print}` Aktion |

---

## 5.10 Übungen

1. Verwenden Sie `head` und `tail`, um Zeilen 100-120 zu betrachten
2. Verwenden Sie `grep`, um alle Benutzer mit `/bin/bash` in /etc/passwd zu finden
3. Verwenden Sie `sed`, um alle `\r\n` durch `\n` zu ersetzen
4. Verwenden Sie `awk`, um Maximum, Minimum und Durchschnitt einer numerischen Datei zu berechnen
