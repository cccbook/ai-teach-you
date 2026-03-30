# 4. Textgenerierung und Schreiben

---

## 4.1 Warum die KI keinen Editor braucht

Der Workflow der meisten menschlichen Ingenieure beim Schreiben von Code:
1. Editor öffnen (VS Code, Vim, Emacs...)
2. Code eingeben
3. Datei speichern
4. Editor schließen

Für die KI:
```
"Eines Python-Programm schreiben" = Text generieren
"Dieses Programm in einer Datei speichern" = Text auf Disk schreiben
```

Der Codegenerierungsprozess der KI ist ein **Textgenerierungsprozess**. Also verwendet die KI die Textwerkzeuge von Shell:

- `echo`: Eine Textzeile ausgeben
- `printf`: Formatierte Ausgabe
- `heredoc`: Mehrzeiligen Text ausgeben (am wichtigsten!)

---

## 4.2 `echo`: Einfachste Ausgabe

### Grundlegende Verwendung

```bash
# String ausgeben
echo "Hallo, Welt!"

# Variable ausgeben
name="Alice"
echo "Hallo, $name!"

# Mehrere Werte ausgeben
echo "Heute ist $(date +%Y-%m-%d)"
```

### `echo`-Fallen

```bash
# echo fügt standardmäßig einen Zeilenumbruch hinzu
echo -n "Laden: "  # Kein Zeilenumbruch
```

### Dateien mit `echo` schreiben

```bash
# Überschreiben
echo "Hallo, Welt!" > file.txt

# Anhängen
echo "Zweite Zeile" >> file.txt
```

**Hinweis**: `echo` für mehrzeilige Dateien zu verwenden ist schmerzhaft, also verwendet die KI es fast nie für Code. `heredoc` ist der Star.

---

## 4.3 `printf`: Leistungsfähigere formatierte Ausgabe

### Vergleich mit `echo`

```bash
# printf unterstützt C-Stil-Formatierung
printf "Wert: %.2f\n" 3.14159
# Ausgabe: Wert: 3.14

printf "%s\t%s\n" "Name" "Alter"
```

### Tabellen erstellen

```bash
printf "%-15s %10s\n" "Name" "Preis"
printf "%-15s %10.2f\n" "iPhone" 999.99
printf "%-15s %10.2f\n" "MacBook" 1999.99
```

---

## 4.4 heredoc: Die Kernwaffe der KI zum Schreiben von Code

### Was ist heredoc?

heredoc ist eine spezielle Shell-Syntax zum **wörtlichen Ausgeben von mehrzeiligem Text**.

```bash
cat << 'EOF'
All dieser Inhalt
wird wörtlich ausgegeben
einschließlich Zeilenumbrüchen, Leerzeichen
EOF
```

### Dateien schreiben (die häufigste Verwendung der KI)

```bash
cat > program.py << 'EOF'
#!/usr/bin/env python3

def hello(name):
    print(f"Hallo, {name}!")

if __name__ == "__main__":
    hello("Welt")
EOF
```

### Warum `'EOF'` (einfaches Anführungszeichen) verwenden?

```bash
# Einfaches Anführungszeichen EOF: Nichts expandieren
cat << 'EOF'
HOME ist: $HOME
Heute ist: $(date)
EOF
# Ausgabe: HOME ist: $HOME (nicht expandiert)

# Doppeltes Anführungszeichen EOF oder keine Anführungszeichen: wird expandieren
cat << EOF
HOME ist: $HOME
EOF
# Ausgabe: HOME ist: /home/ai (expandiert)
```

**Die Wahl der KI**: Fast immer `'EOF'` (einfaches Anführungszeichen) verwenden. Weil Code normalerweise keine Shell-Variablenexpansion braucht.

---

## 4.5 Die KI schreibt verschiedene Dateien mit heredoc

### Python-Programm schreiben

```bash
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""Haupteinstiegspunkt"""

import sys
import os

def main():
    print("Python + C Hybridprojekt")
    print(f"Arbeitsverzeichnis: {os.getcwd()}")

if __name__ == "__main__":
    main()
EOF
```

### Shell-Skript schreiben

```bash
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash
set -e

DEPLOY_HOST="server.example.com"

echo "🚀 Bereitstellung auf $DEPLOY_HOST"
rsync -avz --delete ./dist/ "$DEPLOY_HOST:/var/www/app/"
ssh "$DEPLOY_HOST" "systemctl restart myapp"
echo "✅ Bereitstellung abgeschlossen!"
EOF

chmod +x scripts/deploy.sh
```

### Konfigurationsdatei schreiben

```bash
cat > config.json << 'EOF'
{
    "site_name": "Mein Blog",
    "author": "Anonym",
    "theme": "minimal"
}
EOF
```

### Dockerfile schreiben

```bash
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "http.server", "8000"]
EOF
```

---

## 4.6 heredoc-Fallen und Lösungen

### Falle 1: Enthält einfache Anführungszeichen

```bash
# Problem: einfaches Anführungszeichen EOF erlaubt keine einfachen Anführungszeichen
cat << 'EOF'
He's going.
EOF
# Ausgabe: syntax error

# Lösung: doppeltes Anführungszeichen EOF verwenden
cat << "EOF"
He's going.
EOF
```

### Falle 2: Enthält `$` (Aber keine Expansion gewünscht)

```bash
# Problem: doppeltes Anführungszeichen EOF expandiert $
cat << "EOF"
Preis ist $100
EOF
# Ausgabe: Preis ist (leer)

# Lösung: einzeln escapen
cat << "EOF"
Preis ist $$100
EOF
# Ausgabe: Preis ist $100
```

---

## 4.7 Übung: Ein vollständiges Projekt von Grund auf aufbauen

```bash
# 1. Verzeichnisstruktur erstellen
mkdir -p myblog/{src,themes,content}

# 2. Konfigurationsdatei erstellen
cat > myblog/config.json << 'EOF'
{
    "site_name": "Mein Blog",
    "author": "Anonym",
    "theme": "minimal"
}
EOF

# 3. Python-Hauptprogramm erstellen
cat > myblog/src/blog.py << 'EOF'
#!/usr/bin/env python3
"""Einfacher Blog-Generator"""
import json
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path) as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config()
    print(f"Generiere: {config['site_name']}")
EOF

# 4. Build-Skript erstellen
cat > myblog/build.sh << 'EOF'
#!/bin/bash
set -e
echo "🔨 Blog wird gebaut..."
cd "$(dirname "$0")"
python3 src/blog.py
echo "✅ Build abgeschlossen!"
EOF

chmod +x myblog/build.sh

# 5. Struktur überprüfen
find myblog -type f | sort
```

---

## 4.8 Schnellreferenz

| Werkzeug | Zweck | Beispiel |
|----------|-------|---------|
| `echo` | Einzelne Zeile ausgeben | `echo "Hallo"` |
| `echo -n` | Kein Zeilenumbruch | `echo -n "Laden..."` |
| `printf` | Formatierte Ausgabe | `printf "%s: %d\n" "alter" 25` |
| `>` | Datei überschreiben | `echo "hi" > file.txt` |
| `>>` | An Datei anhängen | `echo "hi" >> file.txt` |
| `<< 'EOF'` | heredoc (keine Expansion) | bevorzugt für Code |
| `<< "EOF"` | heredoc (expandieren) | selten verwendet |

---

## 4.9 Übungen

1. Erstellen Sie eine Ladeanimation mit `echo -n` und einer `for`-Schleife
2. Erstellen Sie eine formatierte Tabelle (Name, Alter, Beruf) mit `printf`
3. Schreiben Sie ein 20-zeiliges Python-Programm mit heredoc
4. Schreiben Sie eine docker-compose.yml mit heredoc
