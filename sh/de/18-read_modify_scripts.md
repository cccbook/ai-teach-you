# 18. Skripte anderer lesen und ändern

---

## 18.1 Warum die Skripte anderer lesen

- Projektwartung übernehmen
- Open-Source-Tools verwenden
- Probleme debuggen
- Neue Techniken lernen

KI begegnet täglich unbekannten Skripten, daher ist es wichtig, schnell zu lernen, von anderen geschriebene Shell-Skripte zu verstehen.

---

## 18.2 Erste Beobachtung

### Schritt 1: Shebang prüfen

```bash
head -1 skript.sh
```

```bash
#!/bin/bash      # Bash verwenden
#!/bin/sh        # POSIX sh verwenden (kompatibler)
```

### Schritt 2: Berechtigungen und Größe prüfen

```bash
ls -la skript.sh
wc -l skript.sh
```

### Schritt 3: Schnelle Syntaxprüfung

```bash
bash -n skript.sh  # Nur Syntax prüfen, nicht ausführen
```

---

## 18.3 Struktur verstehen

### Typische Struktur

```bash
#!/bin/bash
# Kommentar: Skriptbeschreibung

# Setup
set -euo pipefail
VAR="wert"

# Funktionsdefinitionen
function help() { ... }

# Hauptfluss
main() { ... }

# Ausführen
main "$@"
```

### Hauptfluss finden

```bash
# Letzte Zeilen prüfen
tail -20 skript.sh

# Funktionsdefinitionen finden
grep -n "^function\|^[[:space:]]*[a-z_]*\(" skript.sh
```

---

## 18.4 Häufige Analysebefehle

```bash
# Alle Funktionsdefinitionen finden
grep -n "^[[:space:]]*function" skript.sh

# Alle Bedingungen finden
grep -n "if\|\[\[" skript.sh

# Alle Schleifen finden
grep -n "for\|while\|do\|done" skript.sh

# Kommando-Substitutionen finden
grep -n '\$(' skript.sh

# Alle Exits finden
grep -n "exit" skript.sh
```

---

## 18.5 Sicherheitsprüfungen

```bash
# Gefährliche Befehle finden
grep -n "rm -rf" skript.sh
grep -n "sudo" skript.sh
grep -n "eval" skript.sh

# Variablen-Injection-Risiken prüfen
grep -n '\$[A-Za-z_][A-Za-z0-9_]*[^"}]' skript.sh
```

---

## 18.6 Übungen

1. Analysiere ein bestehendes Shell-Skript mit `grep` und `awk`
2. Finde alle Variablen in einem Skript und verstehe ihre Zwecke
3. Verwende `bash -n`, um die Syntax eines Skripts zu prüfen
4. Füge Kommentare zu einem unkommentierten Skript hinzu, die jeden Abschnitt erklären
