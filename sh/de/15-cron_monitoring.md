# 15. Geplante Aufgaben und Überwachung

---

## 15.1 crontab Grundlagen

### Grundlegendes Format

```
Min  Std  Tag  Mon  Wochentag  Befehl
┬    ┬    ┬    ┬    ┬          ┬
│    │    │    │    │          │
│    │    │    │    │          └─ Befehl
│    │    │    │    └─ Wochentag (0-7, 0 und 7 = Sonntag)
│    │    │    └─ Monat (1-12)
│    │    └─ Tag des Monats (1-31)
│    └─ Stunde (0-23)
└─ Minute (0-59)
```

### Häufige Beispiele

```bash
# Jede Minute
* * * * * /pfad/zu/skript.sh

# Jede Stunde zur Minute 30
30 * * * * /pfad/zu/skript.sh

# Täglich um 3 Uhr morgens
0 3 * * * /pfad/zu/skript.sh

# Wöchentlich montags um 9 Uhr
0 9 * * 1 /pfad/zu/skript.sh

# Alle 5 Minuten
*/5 * * * * /pfad/zu/skript.sh
```

---

## 15.2 crontab verwalten

```bash
# Aktuellen crontab anzeigen
crontab -l

# crontab bearbeiten
crontab -e

# crontab entfernen
crontab -r

# crontab-Datei erstellen
cat > mycron << 'EOF'
# Tägliches Backup
0 3 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1

# Wöchentliche Bereinigung
0 4 * * 0 /scripts/clean-logs.sh

# Gesundheitscheck alle 5 Minuten
*/5 * * * * /scripts/health-check.sh
EOF

crontab mycron
crontab -l
```

---

## 15.3 Gesundheitscheck-Skript

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
        log "WEB: FEHLGESCHLAGEN"
        return 1
    fi
}

check_disk() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $usage -gt 90 ]]; then
        log "DISK: WARNUNG (${usage}%)"
        return 1
    fi
    log "DISK: OK (${usage}%)"
    return 0
}

FAILED=0

check_web || ((FAILED++))
check_disk || ((FAILED++))

if [[ $FAILED -gt 0 ]]; then
    echo "Gesundheitscheck fehlgeschlagen, $FAILED Elemente abnormal" | mail -s "Alarm" "$ALERT_EMAIL"
fi

exit $FAILED
EOF

chmod +x scripts/health-check.sh
```

---

## 15.4 Automatisches Bereinigungsskript

```bash
cat > scripts/clean-logs.sh << 'EOF'
#!/bin/bash
set -euo pipefail

LOG_DIR="/var/log"
MAX_AGE_DAYS=30

# Alte Logs löschen
find "$LOG_DIR" -name "*.log" -mtime +$MAX_AGE_DAYS -delete

# Alte Logs komprimieren
find "$LOG_DIR" -name "*.log" -mtime +7 -exec gzip {} \;

echo "Bereinigung abgeschlossen: $(date)"
EOF

chmod +x scripts/clean-logs.sh
```

---

## 15.5 Übungen

1. Richte einen crontab ein, der jede Stunde "hallo" ausgibt und in eine Datei protokolliert
2. Schreibe ein Skript zur Überwachung des Festplattenplatzes, das bei über 80% warnt
3. Erstelle ein Skript, das automatisch eine MySQL-Datenbank sichert
4. Verwende systemd timer statt cron, um den Gesundheitscheck jede Minute auszuführen
