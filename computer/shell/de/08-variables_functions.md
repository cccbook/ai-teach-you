# 8. Variablen und Funktionen

---

## 8.1 Grundlagen zu Variablen

### Grundlegende Zuweisung

```bash
# Zeichenkette
name="Alice"
gruss="Hallo, Welt!"

# Zahl
alter=25
anzahl=0

# Leer
leer=
leer2=""
```

### Variablen lesen

```bash
echo $name
echo ${name}    # Empfohlene Form, expliziter

# In Anführungszeichen
echo "Mein Name ist ${name}"
```

### Häufige Fehler

```bash
# Falsch: Leerzeichen um =
name = "Alice"   # Wird als Befehl interpretiert

# Falsch: Keine Anführungszeichen
gruss=Hallo Welt  # Gibt nur "Hallo" aus

# Richtig:
name="Alice"
gruss="Hallo Welt"
```

---

## 8.2 Die Kunst der Anführungszeichen

### Doppelte Anführungszeichen `"`
Erweitern Variablen und Befehlssubstitution

```bash
name="Alice"
echo "Hallo, $name"           # Hallo, Alice
echo "Heute ist $(date +%Y)"   # Heute ist 2026
```

### Einfache Anführungszeichen `'`
Gibt wörtlich aus, erweitert nichts

```bash
name="Alice"
echo 'Hallo, $name'           # Hallo, $name
echo 'Heute ist $(date +%Y)'   # Heute ist $(date +%Y)
```

### Ohne Anführungszeichen
Vermeiden, es sei denn, man ist sicher, dass die Variable keine Leerzeichen enthält

---

## 8.3 Spezielle Variablen

```bash
$0          # Skriptname
$1, $2...   # Positionsparameter
$#          # Argumentanzahl
$@          # Alle Argumente (einzeln)
$*          # Alle Argumente (als eine Zeichenkette)
$?          # Exit-Code des letzten Befehls
$$          # PID des aktuellen Prozesses
$!          # PID des letzten Hintergrundprozesses
$-          # Aktuelle Shell-Optionen
```

---

## 8.4 Arrays

### Grundlegende Verwendung

```bash
# Array definieren
farben=("rot" "gruen" "blau")

# Elemente lesen
echo ${farben[0]}    # rot
echo ${farben[1]}    # gruen

# Alle lesen
echo ${farben[@]}    # rot gruen blau

# Array-Laenge
echo ${#farben[@]}   # 3
```

### Assoziative Arrays (Bash 4+)

```bash
declare -A benutzer
benutzer["name"]="Alice"
benutzer["email"]="alice@example.com"

echo ${benutzer["name"]}    # Alice
```

---

## 8.5 Grundlagen zu Funktionen

### Funktionen definieren

```bash
# Methode 1: function-Schluesselwort
function gruss {
    echo "Hallo!"
}

# Methode 2: Direkte Definition (empfohlen)
gruss() {
    echo "Hallo!"
}
```

### Funktionsparameter

```bash
gruss() {
    echo "Hallo, $1!"
}

gruss "Alice"    # Hallo, Alice!
```

### Rückgabewerte

```bash
# return: fuer Exit-Code (0-255)
pruefe() {
    if [[ $1 -gt 10 ]]; then
        return 0  # Erfolg
    else
        return 1  # Fehler
    fi
}

if pruefe 15; then
    echo "Groesser als 10"
fi
```

---

## 8.6 Lokale Variablen

```bash
zaehler() {
    local anzahl=0
    ((anzahl++))
    echo $anzahl
}
```

---

## 8.7 Funktionsbibliotheken

### Bibliothek erstellen

```bash
cat > lib.sh << 'EOF'
#!/bin/bash

log() {
    echo "[$(date +%H:%M:%S)] $@"
}

error() {
    echo "[$(date +%H:%M:%S)] FEHLER: $@" >&2
}

bestaetige() {
    read -p "$1 (j/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Jj]$ ]]
}
EOF
```

### Bibliothek verwenden

```bash
#!/bin/bash

source lib.sh

log "Starte Prozess"
error "Etwas ist schief gelaufen"
bestaetige "Fortfahren?" && echo "Fortfahren"
```

---

## 8.8 Kurzreferenz

| Thema | Syntax | Beschreibung |
|-------|--------|--------------|
| Zuweisung | `var=value` | Keine Leerzeichen um = |
| Lesen | `$var` oder `${var}` | `${var}` verwenden |
| Doppelte Anfuehrungszeichen | `"..."` | Variablen erweitern |
| Einfache Anfuehrungszeichen | `'...'` | Keine Erweiterung |
| Argumente | `$1`, `$2`, `$@` | Parameter abrufen |
| Funktion | `name() { }` | empfohlene Definition |
| Lokale Variable | `local var=value` | nur in Funktion |
| Array | `arr=(a b c)` | indiziert und assoziativ |
| source | `source datei.sh` | Bibliothek laden |

---

## 8.9 Übungen

1. Schreibe ein Skript, das Name- und Altersparameter akzeptiert, und gibt "Hallo, Y, du bist X Jahre alt!" aus
2. Erstelle eine Bibliothek mit `log`- und `error`-Funktionen und verwende sie in einem anderen Skript
3. Schreibe eine rekursive Funktion zur Berechnung von Fibonacci-Zahlen
4. Verwende `mapfile`, um eine Datei zeilenweise in ein Array einzulesen, und gib sie dann in umgekehrter Reihenfolge aus
