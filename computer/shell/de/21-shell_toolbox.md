# 21. Deine KI Shell Werkzeugkiste bauen

---

## 21.1 Warum du eine Werkzeugkiste brauchst

Wenn du dich dabei erwischst, wiederholt das Gleiche zu tun, ist es Zeit zu automatisieren und es in einer Werkzeugkiste zu sammeln.

KI ist besonders gut darin:
- Schnell Tools zu erstellen
- Komplexe Workflows in einfache Befehle zu verpacken
- Häufig verwendete Skripte kontinuierlich zu verbessern

---

## 21.2 Werkzeugkisten-Verzeichnisstruktur

```
~/bin/
├── lib/              # Gemeinsame Bibliotheken
│   ├── logging.sh
│   ├── utils.sh
│   └── colors.sh
├── project/          # Projektvorlagen
│   ├── python/
│   ├── nodejs/
│   └── static-site/
├── scripts/          # Tool-Skripte
│   ├── git-clean
│   ├── docker-clean
│   ├── backup
│   └── log-parse
└── bin/
    ├── greet         # Ausführbares Tool
    └── monitor       # Ausführbares Tool
```

---

## 21.3 Deine Bibliothek erstellen

### logging.sh

```bash
cat > ~/bin/lib/logging.sh << 'EOF'
#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $@"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $@"; }
log_error() { echo -e "${RED}[ERROR]${NC} $@" >&2; }
EOF

source ~/bin/lib/logging.sh
```

### utils.sh

```bash
cat > ~/bin/lib/utils.sh << 'EOF'
#!/bin/bash

need_command() {
    command -v "$1" &>/dev/null || {
        echo "Benötigter Befehl: $1"
        exit 1
    }
}

need_file() {
    [[ -f "$1" ]] || {
        echo "Benötigte Datei: $1"
        exit 1
    }
}

need_dir() {
    [[ -d "$1" ]] || {
        echo "Benötigtes Verzeichnis: $1"
        exit 1
    }
}
EOF
```

---

## 21.4 Praktisches Tool: git-clean

```bash
cat > ~/bin/git-clean << 'EOF'
#!/bin/bash
set -euo pipefail

DRY_RUN=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--dry-run) DRY_RUN=true; shift ;;
        *) shift ;;
    esac
done

if $DRY_RUN; then
    echo "[TROCKENLAUF] Würde löschen:"
fi

git branch --merged main | grep -v "main\|master\|develop" | while read branch; do
    if $DRY_RUN; then
        echo "  Branch löschen: $branch"
    else
        git branch -d "$branch"
        echo "Gelöscht: $branch"
    fi
done

git clean -n -d
EOF

chmod +x ~/bin/git-clean
```

---

## 21.5 Praktisches Tool: docker-clean

```bash
cat > ~/bin/docker-clean << 'EOF'
#!/bin/bash
set -euo pipefail

echo "Alle Container stoppen..."
docker stop $(docker ps -aq) 2>/dev/null || true

echo "Gestoppte Container entfernen..."
docker container prune -f

echo "Unbenutzte Images entfernen..."
docker image prune -af

echo "Unbenutzte Netzwerke entfernen..."
docker network prune -f

echo "Build-Cache entfernen..."
docker builder prune -af

echo "Docker-Bereinigung abgeschlossen"
docker system df
EOF

chmod +x ~/bin/docker-clean
```

---

## 21.6 Tools im PATH verfügbar machen

```bash
# Prüfen ob ~/bin im PATH ist
echo $PATH | grep -q "$HOME/bin" && echo "Gesetzt" || echo "Nicht gesetzt"

# Zum PATH hinzufügen (zu ~/.bashrc oder ~/.zshrc hinzufügen)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 21.7 KI helfen lassen, die Werkzeugkiste zu erweitern

```bash
# Mensch: Hilf mir, ein Tool zur Analyse von Nginx Access Logs zu erstellen

# KI:
cat > ~/bin/nginx-analyze << 'EOF'
#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Verwendung: $0 <access_log_datei>"
    exit 1
fi

FILE=$1

echo "=== Nginx Analyse: $FILE ==="
echo ""

echo "Dateigröße: $(du -h "$FILE" | cut -f1)"
echo "Gesamte Zeilen: $(wc -l < "$FILE")"
echo ""

echo "=== Top 10 IPs ==="
awk '{print $1}' "$FILE" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Top 10 URLs ==="
awk '{print $7}' "$FILE" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Statuscode-Verteilung ==="
awk '{print $9}' "$FILE" | sort | uniq -c | sort -rn
EOF

chmod +x ~/bin/nginx-analyze
```

---

## 21.8 Kontinuierliche Verbesserung

```bash
# Werkzeugkiste jährlich überprüfen
# - Welche Tools werden selten verwendet? Löschen
# - Welche Tools können verbessert werden?
# - Welche sich wiederholenden Aufgaben können automatisiert werden?

# Werkzeugkiste unter Versionskontrolle stellen
cd ~/bin
git init
git add .
git commit -m "Initiale Version"
```

---

## 21.9 Übungen

1. Erstelle deine ~/bin Verzeichnisstruktur
2. Schreibe häufig verwendete Funktionen in wiederverwendbare Bibliotheken
3. Schreibe ein Tool für Aufgaben, die du täglich wiederholst
4. Lass KI helfen, ein Nginx Log-Analyse-Tool zu erstellen
5. Nimm deine Werkzeugkiste unter Git-Versionskontrolle
