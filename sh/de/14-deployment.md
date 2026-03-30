# 14. Deployment-Skripte

---

## 14.1 Wesentliche Elemente eines guten Deployment-Skripts

Ein gutes Deployment-Skript sollte:
1. Dry-run Modus unterstützen
2. Klare Protokollausgabe haben
3. Bei Fehler Rollback durchführen
4. Unterbrechungen behandeln
5. Versionsverfolgung haben

---

## 14.2 Einfaches Deployment-Skript

```bash
cat > deploy.sh << 'EOF'
#!/bin/bash
set -euo pipefail

DEPLOY_HOST="server.example.com"
DEPLOY_PATH="/var/www/myapp"
DEPLOY_USER="deploy"

ROT='\033[0;31m'
GRUEN='\033[0;32m'
GELB='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GRUEN}[INFO]${NC} $@"; }
warn() { echo -e "${GELB}[WARN]${NC} $@"; }
error() { echo -e "${ROT}[ERROR]${NC} $@" >&2; }

check() {
    command -v rsync &>/dev/null || { error "rsync erforderlich"; exit 1; }
    if ! ssh -o ConnectTimeout=5 "$DEPLOY_USER@$DEPLOY_HOST" "exit 0" 2>/dev/null; then
        error "Keine Verbindung zu $DEPLOY_HOST möglich"
        exit 1
    fi
    log "Vorabprüfungen bestanden"
}

backup() {
    log "Erstelle Sicherungskopie..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    ssh "$DEPLOY_USER@$DEPLOY_HOST" "cp -r $DEPLOY_PATH $DEPLOY_PATH.backup.$TIMESTAMP"
    log "Sicherung erstellt: $DEPLOY_PATH.backup.$TIMESTAMP"
}

deploy() {
    log "Starte Deployment..."
    rsync -avz --delete \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='.env' \
        ./ "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/"
    log "Dateien synchronisiert"
}

restart() {
    log "Starte Dienst neu..."
    ssh "$DEPLOY_USER@$DEPLOY_HOST" "systemctl restart myapp"
    sleep 2
    
    if ssh "$DEPLOY_USER@$DEPLOY_HOST" "systemctl is-active myapp" | grep -q "active"; then
        log "Dienst erfolgreich gestartet"
    else
        error "Dienst konnte nicht gestartet werden"
        exit 1
    fi
}

main() {
    log "🚀 Deployment wird gestartet"
    log "Ziel: $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH"
    
    check
    backup
    deploy
    restart
    
    log "✅ Deployment abgeschlossen!"
}

main
EOF

chmod +x deploy.sh
```

---

## 14.3 Dry-run unterstützen

```bash
cat > deploy.sh << 'EOF'
#!/bin/bash
set -euo pipefail

DRY_RUN=false
DEPLOY_HOST="server.example.com"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

log() { echo "[INFO] $@"; }

deploy() {
    if $DRY_RUN; then
        log "[DRY-RUN] Wuerde Dateien zu $DEPLOY_HOST synchronisieren"
        rsync -avz --dry-run ./ "$DEPLOY_HOST:/tmp/test/"
    else
        log "Starte Deployment..."
        rsync -avz ./ "$DEPLOY_HOST:/var/www/app/"
    fi
}

deploy
EOF
```

---

## 14.4 Multi-Umgebungs-Dployment

```bash
cat > deploy.sh << 'EOF'
#!/bin/bash
set -euo pipefail

UMGEBUNG="${1:-staging}"

case "$UMGEBUNG" in
    staging)
        HOST="staging.example.com"
        PATH="/var/www/staging"
        ;;
    production)
        HOST="prod.example.com"
        PATH="/var/www/production"
        BESTAETIGEN=true
        ;;
    *)
        echo "Unbekannte Umgebung: $UMGEBUNG"
        exit 1
        ;;
esac

log() { echo "🚀 [$UMGEBUNG] $@"; }

if [[ "$BESTAETIGEN" == "true" ]]; then
    echo "Ueber Deployment auf Production: $HOST"
    read -p "Fortfahren? (j/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Jj]$ ]] || exit 0
fi

log "Starte Deployment zu $HOST"

rsync -avz --delete \
    --exclude='.env' \
    ./ "$HOST:$PATH/"

ssh "$HOST" "cd $PATH && npm install --production"

log "Deployment abgeschlossen"
EOF
```

---

## 14.5 Übungen

1. Schreibe ein Deployment-Skript, das die `--dry-run` Option unterstützt
2. Füge dem Deployment-Skript Sicherungfunktionalität hinzu
3. Schreibe ein Multi-Umgebungs-Deployment-Skript (dev/staging/production)
4. Erstelle ein Rollback-Skript, das Versionen auflistet und die Auswahl ermöglicht, auf welche Version zurückgesetzt werden soll
