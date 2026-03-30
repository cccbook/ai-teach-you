# 16. Debugging-Techniken

---

## 16.1 KI-Debugging-Mindset

Wenn Menschen auf Fehler stoßen: Panik, online suchen, kopieren-einfügen
Wenn KI auf Fehler stößt: Nachricht analysieren, Ursache ableiten, Fix ausführen

KIs Debugging-Ablauf:
```
Fehlerausgabe beobachten → Fehlertyp verstehen → Problem lokalisieren → Beheben → Verifizieren
```

---

## 16.2 `bash -x`: Ausführung verfolgen

Einfachstes Debugging: `-x` Flag hinzufügen

```bash
bash -x skript.sh
```

Gibt jede ausgeführte Zeile mit `+` Präfix aus:

```bash
+ mkdir -p test
+ cd test
+ echo 'Hallo'
Hallo
```

### Nur einen Abschnitt debuggen

```bash
#!/bin/bash

echo "Das wird nicht angezeigt"
set -x
# Debugging beginnt hier
name="Alice"
echo "Hallo, $name"
set +x
# Debugging endet hier
echo "Das wird nicht angezeigt"
```

---

## 16.3 Häufige Fehler und Lösungen

### Fehler 1: Zugriff verweigert

```bash
# Fehler
./skript.sh
# Ausgabe: Permission denied

# Lösung
chmod +x skript.sh
./skript.sh
```

### Fehler 2: Befehl nicht gefunden

```bash
# Fehler
python skript.py
# Ausgabe: command not found: python

# Lösung: vollen Pfad verwenden
/usr/bin/python3 skript.py
```

### Fehler 3: Undefinierte Variable

```bash
#!/bin/bash
set -u

echo $undefined_var
# Ausgabe: bash: undefined_var: unbound variable

# Lösung: Standardwert angeben
echo ${undefined_var:-Standardwert}
```

---

## 16.4 `echo`-Debugging

Wenn `-x` nicht ausreicht, manuell `echo` hinzufügen:

```bash
#!/bin/bash

echo "DEBUG: Funktion betreten"
echo "DEBUG: Parameter = $@"

process() {
    echo "DEBUG: In process"
    local result=$(expensive_command)
    echo "DEBUG: result = $result"
}
```

---

## 16.5 Kurzreferenz

| Befehl | Beschreibung |
|--------|-------------|
| `bash -n skript.sh` | Nur Syntax prüfen |
| `bash -x skript.sh` | Ausführung verfolgen |
| `set -x` | Debug-Modus aktivieren |
| `set +x` | Debug-Modus deaktivieren |
| `trap 'echo cmd' DEBUG` | Jeden Befehl verfolgen |

---

## 16.6 Übungen

1. Führe ein Skript mit `bash -x` aus und beobachte das Ausgabeformat
2. Verwende `set -x` in einem Skript, um nur eine bestimmte Funktion zu debuggen
3. Finde einen fehlschlagenden Befehl, analysiere die Fehlermeldung und behebe sie
4. Erstelle eine elegante Fehlerbehandlung mit `trap`
