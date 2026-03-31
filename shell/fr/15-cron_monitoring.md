# 15. Tâches Planifiées et Surveillance

---

## 15.1 Bases de crontab

### Format de Base

```
min heure jour mois jour_semaine  commande
┬    ┬      ┬    ┬     ┬           ┬
│    │      │    │     │           │
│    │      │    │     │           └─ commande
│    │      │    │     └─ jour de la semaine (0-7, 0 et 7 = dimanche)
│    │      │    └─ mois (1-12)
│    │      └─ jour du mois (1-31)
│    └─ heure (0-23)
└─ minute (0-59)
```

### Exemples Courants

```bash
# Chaque minute
* * * * * /chemin/vers/script.sh

# Chaque heure à la minute 30
30 * * * * /chemin/vers/script.sh

# Quotidien à 3h du matin
0 3 * * * /chemin/vers/script.sh

# Hebdomadaire le lundi à 9h
0 9 * * 1 /chemin/vers/script.sh

# Toutes les 5 minutes
*/5 * * * * /chemin/vers/script.sh
```

---

## 15.2 Gérer crontab

```bash
# Afficher le crontab actuel
crontab -l

# Éditer le crontab
crontab -e

# Supprimer le crontab
crontab -r

# Créer un fichier crontab
cat > mycron << 'EOF'
# Sauvegarde quotidienne
0 3 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1

# Nettoyage hebdomadaire
0 4 * * 0 /scripts/clean-logs.sh

# Vérification santé toutes les 5 minutes
*/5 * * * * /scripts/health-check.sh
EOF

crontab mycron
crontab -l
```

---

## 15.3 Script de Vérification Santé

```bash
cat > scripts/health-check.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ALERT_EMAIL="admin@example.com"
WEB_URL="https://myapp.com/health"
LOG_FILE="/var/log/health-check.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $@" >> "$LOG_FILE"
}

check_web() {
    if curl -sf "$WEB_URL" &>/dev/null; then
        log "WEB: OK"
        return 0
    else
        log "WEB: ÉCHEC"
        return 1
    fi
}

check_disk() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $usage -gt 90 ]]; then
        log "DISK: ATTENTION (${usage}%)"
        return 1
    fi
    log "DISK: OK (${usage}%)"
    return 0
}

FAILED=0

check_web || ((FAILED++))
check_disk || ((FAILED++))

if [[ $FAILED -gt 0 ]]; then
    echo "Vérification santé échouée, $FAILED éléments anormaux" | mail -s "Alerte" "$ALERT_EMAIL"
fi

exit $FAILED
EOF

chmod +x scripts/health-check.sh
```

---

## 15.4 Script de Nettoyage Automatique

```bash
cat > scripts/clean-logs.sh << 'EOF'
#!/bin/bash
set -euo pipefail

LOG_DIR="/var/log"
MAX_AGE_DAYS=30

# Supprimer les anciens logs
find "$LOG_DIR" -name "*.log" -mtime +$MAX_AGE_DAYS -delete

# Compresser les anciens logs
find "$LOG_DIR" -name "*.log" -mtime +7 -exec gzip {} \;

echo "Nettoyage terminé : $(date)"
EOF

chmod +x scripts/clean-logs.sh
```

---

## 15.5 Exercices

1. Configurez un crontab qui affiche "bonjour" chaque heure et enregistre dans un fichier
2. Écrivez un script de surveillance d'espace disque qui alerte à plus de 80%
3. Créez un script qui sauvegarde automatiquement une base de données MySQL
4. Utilisez systemd timer au lieu de cron pour exécuter la vérification santé chaque minute
