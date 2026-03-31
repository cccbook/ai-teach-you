# 9. Fehlerbehandlung

---

## 9.1 Warum Fehlerbehandlung wichtig ist

Ohne Fehlerbehandlung:
- Nach einem fehlgeschlagenen Befehl wird mit falschen Operationen fortgefahren
- Mögliche Löschung falscher Dateien
- Mögliche Überschreibung wichtiger Daten
- System kann in inkonsistentem Zustand hinterlassen werden

Mit Fehlerbehandlung:
- Sofort bei Fehler stoppen
- Aussagekräftige Fehlermeldungen bereitstellen
- Vor dem Beenden aufräumen

---

## 9.2 Exit-Codes

Jeder Befehl gibt nach der Ausführung einen Exit-Code zurück:

- `0`: Erfolg
- `non-zero`: Fehler

```bash
# Exit-Code des letzten Befehls pruefen
ls /tmp
echo $?  # Ausgabe: 0 (bei Erfolg)

ls /nichtvorhanden
echo $?  # Ausgabe: 2 (bei Fehler)
```

---

## 9.3 `set -e`: Bei Fehler stoppen

```bash
#!/bin/bash
set -e

mkdir -p sicherung
cp wichtige.txt sicherung/  # Wenn dies fehlschlaegt, stoppt das Skript hier
rm wichtige.txt            # Wird hier nicht erreicht
```

### Wann verwenden

Fast alle Skripte sollten `set -e` verwenden:
- Initialisierungsskripte
- Deployment-Skripte
- Automatisierte Testskripte

---

## 9.4 `set -u`: Fehler bei undefinierten Variablen

```bash
#!/bin/bash
set -u

echo $undefinierte_var
# Ausgabe: bash: undefinierte_var: unbound variable
```

### Kombinierte Verwendung

```bash
#!/bin/bash
set -euo pipefail

# -e: Bei Fehler stoppen
# -u: Fehler bei undefinierter Variable
# -o pipefail: Pipe schlaegt fehl, wenn ein Befehl fehlschlaegt
```

**Dies ist der Standard-Skript-Header der KI!**

---

## 9.5 `trap`: Elegante Fehlerbehandlung

### Grundlegende Verwendung

```bash
#!/bin/bash
set -euo pipefail

bereinige() {
    echo "Bereinige..."
    rm -f /tmp/tempdatei
}

trap bereinige EXIT

# Hauptprogramm
echo "Starte Prozess..."
```

### Fehler abfangen

```bash
#!/bin/bash
set -euo pipefail

fehlerbehandlung() {
    local exit_code=$?
    echo "❌ Skript fehlgeschlagen in Zeile $1, Exit-Code: $exit_code"
    exit $exit_code
}

trap 'fehlerbehandlung $LINENO' ERR
```

---

## 9.6 Eigene Fehlerfunktionen

```bash
#!/bin/bash
set -euo pipefail

die() {
    echo "❌ $@" >&2
    exit 1
}

warne() {
    echo "⚠️ $@"
}

brauche_befehl() {
    command -v "$1" &>/dev/null || die "Erforderlicher Befehl: $1"
}

brauche_datei() {
    [[ -f "$1" ]] || die "Erforderliche Datei: $1"
}
```

---

## 9.7 Kurzreferenz

| Befehl | Beschreibung |
|--------|--------------|
| `$?` | Exit-Code des letzten Befehls |
| `set -e` | Bei Fehler stoppen |
| `set -u` | Fehler bei undefinierter Variable |
| `set -o pipefail` | Pipe schlaegt fehl, wenn ein Befehl fehlschlaegt |
| `set -euo pipefail` | Kombiniert (empfohlen) |
| `trap 'func' EXIT` | Bei Beendigung ausführen |
| `trap 'func' ERR` | Bei Fehler ausführen |
| `trap 'func' INT` | Bei Strg+C ausführen |
| `exit 1` | Mit Exit-Code 1 beenden |

---

## 9.8 Übungen

1. Schreibe ein Skript mit `set -euo pipefail`, das bei Fehler "Fehler aufgetreten" ausgibt
2. Erstelle eine `die()`-Funktion, die eine Meldung ausgibt und beendet
3. Verwende `trap`, um "Auf Wiedersehen" anzuzeigen, wenn das Skript beendet wird
4. Schreibe ein Deployment-Skript mit automatischem Rollback bei Fehler
