# 10. Argumentanalyse und CLI-Tools

---

## 10.1 Grundlagen zu Kommandozeilenargumenten

```bash
#!/bin/bash

echo "Skript: $0"
echo "Erstes Argument: $1"
echo "Zweites Argument: $2"
echo "Drittes Argument: ${3:-standard}"  # Standardwert
echo "Argumentanzahl: $#"
echo "Alle Argumente: $@"
```

### Ausführung

```bash
./skript.sh foo bar
# Ausgabe:
# Skript: ./skript.sh
# Erstes Argument: foo
# Zweites Argument: bar
# Drittes Argument: standard
# Argumentanzahl: 2
# Alle Argumente: foo bar
```

---

## 10.2 Einfache Argumentanalyse

### Positionsparameter

```bash
#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Verwendung: $0 <datei>"
    exit 1
fi

DATEI="$1"

if [[ ! -f "$DATEI" ]]; then
    echo "Fehler: Datei existiert nicht"
    exit 1
fi

echo "Verarbeite $DATEI..."
```

### Optionale Argumente behandeln

```bash
#!/bin/bash

VERBOSE=false
AUSGABE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -o|--output)
            AUSGABE="$2"
            shift 2
            ;;
        -*)
            echo "Unbekannte Option: $1"
            exit 1
            ;;
        *)
            DATEI="$1"
            shift
            ;;
    esac
done

$VERBOSE && echo "verbose Modus an"
[[ -n "$AUSGABE" ]] && echo "Ausgabe nach: $AUSGABE"
```

---

## 10.3 `getopts`: Standard-Optionsanalyse

```bash
#!/bin/bash

while getopts "hv:o:" opt; do
    case $opt in
        h)
            echo "Hilfe-Information"
            exit 0
            ;;
        v)
            echo "verbose Modus: $OPTARG"
            ;;
        o)
            echo "Ausgabedatei: $OPTARG"
            ;;
        \?)
            echo "Ungueltige Option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))

echo "Verbleibende Argumente: $@"
```

### Optionsformat-Referenz

| Format | Bedeutung |
|--------|-----------|
| `getopts "hv:"` | `-h` ohne Argument, `-v` braucht Argument |
| `OPTARG` | Aktueller Optionsargumentwert |
| `OPTIND` | Naechster Argumentindex |

---

## 10.4 Interaktive Eingabe

### `read`: Benutzereingabe lesen

```bash
#!/bin/bash

# Einfaches Lesen
read -p "Namen eingeben: " name
echo "Hallo, $name"

# Passwort (versteckt)
read -sp "Passwort eingeben: " passwort
echo

# Mehrere Werte lesen
read -p "Namen und Alter eingeben: " name alter
echo "$name ist $alter Jahre alt"

# Zeitlimit
read -t 5 -p "Innerhalb von 5 Sekunden eingeben: " wert
```

### Bestaetigungsabfrage

```bash
bestaetige() {
    read -p "$1 (j/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Jj]$ ]]
}

if bestaetige "Diese Datei loeschen?"; then
    echo "Loesche..."
fi
```

---

## 10.5 Menüoberfläche

```bash
#!/bin/bash

PS3="Vorgang auswaehlen: "

select auswahl in "Projekt erstellen" "Projekt loeschen" "Beenden"; do
    case $auswahl in
        "Projekt erstellen")
            echo "Erstelle..."
            ;;
        "Projekt loeschen")
            echo "Loesche..."
            ;;
        "Beenden")
            echo "Auf Wiedersehen!"
            exit 0
            ;;
        *)
            echo "Ungueltige Auswahl"
            ;;
    esac
done
```

---

## 10.6 Kurzreferenz

| Syntax | Beschreibung |
|--------|--------------|
| `$0` | Skriptname |
| `$1`, `$2`... | Positionsparameter |
| `$#` | Argumentanzahl |
| `${var:-standard}` | Standardwert |
| `getopts "hv:" opt` | Optionen analysieren |
| `$OPTARG` | Aktuelles Optionsargument |
| `read -p "prompt:" var` | Eingabe lesen |
| `read -s var` | Verborgene Eingabe (Passwort) |
| `read -t 5 var` | 5 Sekunden Zeitlimit |
| `select` | Menüoberfläche |

---

## 10.7 Übungen

1. Schreibe ein CLI-Tool, das `-n` für Anzahl und `-v` für verbose akzeptiert
2. Verwende `getopts` zum Analysieren von `-h` (Hilfe), `-o` (Ausgabedatei) Optionen
3. Schreibe eine Bestaetigungsfunktion, die nur bei j-Antwort fortfährt
4. Erstelle ein einfaches Rechner-Menü mit `select`
