# 15. Tarefas Agendadas e Monitoramento

---

## 15.1 Fundamentos do crontab

### Formato Básico

```
min hour day month weekday  command
┬   ┬    ┬   ┬     ┬        ┬
│   │    │   │     │        │
│   │    │   │     │        └─ comando
│   │    │   │     └─ dia da semana (0-7, 0 e 7 são domingo)
│   │    │   └─ mês (1-31)
│   │    └─ dia do mês (1-31)
│   └─ hora (0-23)
└─ minuto (0-59)
```

### Exemplos Comuns

```bash
# A cada minuto
* * * * * /path/to/script.sh

# A cada hora no minuto 30
30 * * * * /path/to/script.sh

# Diariamente às 3 horas
0 3 * * * /path/to/script.sh

# Semanalmente às segundas-feira às 9 horas
0 9 * * 1 /path/to/script.sh

# A cada 5 minutos
*/5 * * * * /path/to/script.sh
```

---

## 15.2 Gerenciando crontab

```bash
# Mostrar crontab atual
crontab -l

# Editar crontab
crontab -e

# Remover crontab
crontab -r

# Criar arquivo crontab
cat > mycron << 'EOF'
# Backup diário
0 3 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1

# Limpeza semanal
0 4 * * 0 /scripts/clean-logs.sh

# Verificação de saúde a cada 5 minutos
*/5 * * * * /scripts/health-check.sh
EOF

crontab mycron
crontab -l
```

---

## 15.3 Script de Verificação de Saúde

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
        log "WEB: FALHOU"
        return 1
    fi
}

check_disk() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $usage -gt 90 ]]; then
        log "DISK: AVISO (${usage}%)"
        return 1
    fi
    log "DISK: OK (${usage}%)"
    return 0
}

FAILED=0

check_web || ((FAILED++))
check_disk || ((FAILED++))

if [[ $FAILED -gt 0 ]]; then
    echo "Verificação de saúde falhou, $FAILED itens anormais" | mail -s "Alerta" "$ALERT_EMAIL"
fi

exit $FAILED
EOF

chmod +x scripts/health-check.sh
```

---

## 15.4 Script de Limpeza Automática

```bash
cat > scripts/clean-logs.sh << 'EOF'
#!/bin/bash
set -euo pipefail

LOG_DIR="/var/log"
MAX_AGE_DAYS=30

# Excluir logs antigos
find "$LOG_DIR" -name "*.log" -mtime +$MAX_AGE_DAYS -delete

# Compactar logs antigos
find "$LOG_DIR" -name "*.log" -mtime +7 -exec gzip {} \;

echo "Limpeza concluída: $(date)"
EOF

chmod +x scripts/clean-logs.sh
```

---

## 15.5 Exercícios

1. Configure um crontab que ecolha "olá" a cada hora e registre em um arquivo
2. Escreva um script de monitoramento de espaço em disco que alerte quando passar de 80%
3. Crie um script que faça backup automático de um banco de dados MySQL
4. Use o systemd timer em vez do cron para executar verificação de saúde a cada minuto