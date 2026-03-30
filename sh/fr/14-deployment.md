# 14. Scripts de Deploiement

---

## 14.1 Elements Essentiels d'un Bon Script de Deploiement

Un bon script de deploiement doit :
1. Supporter le mode test (dry-run)
2. Avoir une sortie de journal claire
3. Effectuer un retour arriere en cas d'echec
4. Gerer les interruptions
5. avoir un suivi de version

---

## 14.2 Script de Deploiement Simple

```bash
cat > deploiement.sh << 'EOF'
#!/bin/bash
set -euo pipefail

SERVEUR_DEPLOIEMENT="serveur.exemple.com"
CHEMIN_DEPLOIEMENT="/var/www/monapp"
UTILISATEUR_DEPLOIEMENT="deploy"

ROUGE='\033[0;31m'
VERT='\033[0;32m'
JAUNE='\033[1;33m'
NC='\033[0m'

journal() { echo -e "${VERT}[INFO]${NC} $@"; }
warn() { echo -e "${JAUNE}[WARN]${NC} $@"; }
erreur() { echo -e "${ROUGE}[ERROR]${NC} $@" >&2; }

verifier() {
    command -v rsync &>/dev/null || { erreur "rsync requis"; exit 1; }
    if ! ssh -o ConnectTimeout=5 "$UTILISATEUR_DEPLOIEMENT@$SERVEUR_DEPLOIEMENT" "exit 0" 2>/dev/null; then
        erreur "Connexion a $SERVEUR_DEPLOIEMENT impossible"
        exit 1
    fi
    journal "Pre-verifications reussies"
}

sauvegarder() {
    journal "Creation de la sauvegarde..."
    HORODATAGE=$(date +%Y%m%d_%H%M%S)
    ssh "$UTILISATEUR_DEPLOIEMENT@$SERVEUR_DEPLOIEMENT" "cp -r $CHEMIN_DEPLOIEMENT $CHEMIN_DEPLOIEMENT.sauvegarde.$HORODATAGE"
    journal "Sauvegarde terminee : $CHEMIN_DEPLOIEMENT.sauvegarde.$HORODATAGE"
}

deployer() {
    journal "Demarrage du deploiement..."
    rsync -avz --delete \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='.env' \
        ./ "$UTILISATEUR_DEPLOIEMENT@$SERVEUR_DEPLOIEMENT:$CHEMIN_DEPLOIEMENT/"
    journal "Fichiers synchronises"
}

redemarrer() {
    journal "Redemarrage du service..."
    ssh "$UTILISATEUR_DEPLOIEMENT@$SERVEUR_DEPLOIEMENT" "systemctl restart monapp"
    sleep 2
    
    if ssh "$UTILISATEUR_DEPLOIEMENT@$SERVEUR_DEPLOIEMENT" "systemctl is-active monapp" | grep -q "active"; then
        journal "Service demarre avec succes"
    else
        erreur "Le service n'a pas pu demarrer"
        exit 1
    fi
}

principal() {
    journal "Demarrage du deploiement"
    journal "Cible : $UTILISATEUR_DEPLOIEMENT@$SERVEUR_DEPLOIEMENT:$CHEMIN_DEPLOIEMENT"
    
    verifier
    sauvegarder
    deployer
    redemarrer
    
    journal "Deploiement termine !"
}

principal
EOF

chmod +x deploiement.sh
```

---

## 14.3 Supporter le Mode Test (Dry-run)

```bash
cat > deploiement.sh << 'EOF'
#!/bin/bash
set -euo pipefail

DRY_RUN=false
SERVEUR_DEPLOIEMENT="serveur.exemple.com"

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

journal() { echo "[INFO] $@"; }

deployer() {
    if $DRY_RUN; then
        journal "[TEST] Synchroniserait les fichiers vers $SERVEUR_DEPLOIEMENT"
        rsync -avz --dry-run ./ "$SERVEUR_DEPLOIEMENT:/tmp/test/"
    else
        journal "Demarrage du deploiement..."
        rsync -avz ./ "$SERVEUR_DEPLOIEMENT:/var/www/app/"
    fi
}

deployer
EOF
```

---

## 14.4 Deploiement Multi-Environnement

```bash
cat > deploiement.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ENVIRONNEMENT="${1:-staging}"

case "$ENVIRONNEMENT" in
    staging)
        SERVEUR="staging.exemple.com"
        CHEMIN="/var/www/staging"
        ;;
    production)
        SERVEUR="prod.exemple.com"
        CHEMIN="/var/www/production"
        CONFIRMER=true
        ;;
    *)
        echo "Environnement inconnu : $ENVIRONNEMENT"
        exit 1
        ;;
esac

journal() { echo "Cible : [$ENVIRONNEMENT] $@"; }

if [[ "$CONFIRMER" == "true" ]]; then
    echo "Proceeding du deploiement en production : $SERVEUR"
    read -p "Continuer ? (o/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Oo]$ ]] || exit 0
fi

journal "Demarrage du deploiement vers $SERVEUR"

rsync -avz --delete \
    --exclude='.env' \
    ./ "$SERVEUR:$CHEMIN/"

ssh "$SERVEUR" "cd $CHEMIN && npm install --production"

journal "Deploiement termine"
EOF
```

---

## 14.5 Exercices

1. Ecrire un script de deploiement supportant l'option `--dry-run`
2. Ajouter la fonctionnalite de sauvegarde au script de deploiement
3. Ecrire un script de deploiement multi-environnement (dev/staging/production)
4. Creer un script de retour arriere qui liste et permet de choisir quelle version restaurer
