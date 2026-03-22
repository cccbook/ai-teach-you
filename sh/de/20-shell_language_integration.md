# 20. Shell mit anderen Sprachen verbinden

---

## 20.1 Welche Aufgaben sollte Shell übernehmen?

Aufgaben, bei denen Shell glänzt:
- Dateioperationen
- Systemverwaltung
- Automatisierungsworkflows
- Pipeline-Zusammenstellung
- Schnelle Prototypen

Aufgaben, die besser für andere Sprachen geeignet sind:
- Komplexe Datenverarbeitung (Python, AWK)
- Webprogrammierung (JavaScript, Go)
- Numerische Berechnung (Python, R, Julia)
- Systemb программирование (C, Rust)

---

## 20.2 Shell ruft Python auf

### Einfacher Aufruf

```bash
#!/bin/bash

# Python-Skript aufrufen
python3 process_data.py input.csv

# Argumente übergeben
python3 skript.py arg1 arg2

# Ausgabe erhalten
result=$(python3 -c "print('hallo von python')")
echo "$result"
```

### Python in Shell einbetten

```bash
#!/bin/bash

python3 << 'PYEOF'
import csv

with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    total = sum(int(row['amount']) for row in reader)
    print(f"Gesamt: {total}")
PYEOF
```

---

## 20.3 Python ruft Shell auf

### `subprocess` verwenden

```python
import subprocess

# Einfachen Befehl ausführen
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Komplexen Befehl ausführen
result = subprocess.run(
    'find . -name "*.py" | wc -l',
    shell=True,
    capture_output=True,
    text=True
)
```

---

## 20.4 Shell ruft JavaScript/Node.js auf

```bash
#!/bin/bash

# Node.js-Befehl ausführen
node -e "console.log('hallo von node')"

# Node.js-Skript ausführen
node process-json.js data.json
```

---

## 20.5 Bridging-Tools

### `jq`: JSON-Verarbeitung

```bash
# JSON parsen
echo '{"name": "Alice", "age": 25}' | jq '.name'

# Aus Datei lesen
jq '.users[] | select(.age > 18)' data.json
```

### `yq`: YAML-Verarbeitung

```bash
# YAML parsen
yq '.database.host' config.yaml

# YAML zu JSON konvertieren
yq -o=json config.yaml
```

---

## 20.6 Kurzreferenz

| Bridge | Syntax |
|--------|--------|
| Shell→Python | `python3 skript.py` oder `python3 << PYEOF` |
| Python→Shell | `subprocess.run(['ls'])` |
| Shell→Node | `node skript.js` oder `node << JSEOF` |
| JSON parsen | `jq '.key' datei.json` |
| YAML parsen | `yq '.key' datei.yaml` |
| Orchestrieren | `make` |

---

## 20.7 Übungen

1. Verwende Shell, um Python zur CSV-Dateiverarbeitung aufzurufen
2. Verwende Pythons `subprocess`, um Shell-Befehle auszuführen
3. Verwende `jq`, um eine JSON-API-Antwort zu parsen
4. Verwende Makefile, um Shell-, Python- und Node.js-Aufgaben zu orchestrieren
