# 19. KI + Shell Kollaboration

---

## 19.1 Neue Form der Mensch-Maschine-Zusammenarbeit

Traditionelle Programmierung:
- Menschen tippen mit Tastatur
- Menschen bedienen IDE mit Maus
- Menschen führen aus und testen

Programmierung im KI-Zeitalter:
- Menschen beschreiben Anforderungen
- KI generiert Shell-Befehle und Skripte
- Menschen prüfen und führen aus
- Menschen und KI debuggen gemeinsam

---

## 19.2 Anforderungen an die KI beschreiben

### Gute Beschreibungen

```bash
# Klare Aufgabe
"Finde alle .log-Dateien größer als 100MB in /var/log"

# Erwartetes Ausgabeformat angeben
"Liste alle .py-Dateien, zeige: Zeilenanzahl Dateiname pro Zeile"

# Einschränkungen angeben
"Komprimiere alle .txt-Dateien, aber überspringe solche mit 'test'"
```

### Schlechte Beschreibungen

```bash
# Zu vage
"Hilf mir, Logs zu verarbeiten"

# Unrealistisch
"Schreib mir ein Betriebssystem"
```

---

## 19.3 KI-generierte Shell-Befehlsmuster

### Muster 1: Einzelner Befehl

```bash
# Mensch fragt: Finde die 10 Python-Dateien mit den meisten Zeilen
find . -name "*.py" -exec wc -l {} + | sort -rn | head -10
```

### Muster 2: Shell-Skript

```bash
# Mensch fragt: Bilder stapelverarbeiten
cat > process_images.sh << 'EOF'
#!/bin/bash
for img in *.jpg; do
    convert "$img" -resize 800x600 "thumb_$img"
done
EOF
```

---

## 19.4 Iterative Entwicklung

### Runde 1: Initiale Version generieren

```bash
# Mensch: schreibe ein Backup-Skript
# KI generiert initiale Version, dann testet Mensch und meldet Probleme:

# Mensch: gut, aber brauche --dry-run Modus
```

### Runde 2: Features hinzufügen

```bash
# Mensch: füge auch Fehlerbehandlung und Logging hinzu
```

### Runde 3: Debuggen

```bash
# Mensch: bekomme 'Permission denied' Fehler nach dem Ausführen
# KI: behebt das Problem...
```

---

## 19.5 KI beim Debuggen helfen lassen

```bash
# Mensch: bekomme Fehler nach dem Ausführen dieses Befehls
$ ./deploy.sh
# Ausgabe: /bin/bash^M: bad interpreter: No such file or directory

# KI: Das ist ein Windows-Zeilenende-Problem. Führe aus:
sed -i 's/\r$//' deploy.sh
```

---

## 19.6 Empfohlene Kollaborationstools

### Terminal Multiplexer

```bash
# tmux: Fenster teilen
tmux new -s mysession
# Strg+b %  # Vertikal teilen
# Strg+b "  # Horizontal teilen
```

---

## 19.7 Übungen

1. Beschreibe eine komplexe Aufgabe und lass KI Shell-Befehle generieren
2. Lass KI ein bestehendes Skript auf Sicherheitsprobleme prüfen
3. Verwende Iteration, um mit KI ein praktisches Tool zu schreiben
4. Lass KI Shell-Code erklären, den du nicht verstehst
