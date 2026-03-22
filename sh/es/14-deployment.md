# 14. Scripts de Despliegue

---

## 14.1 Elementos Esenciales de un Buen Script de Despliegue

Un buen script de despliegue deberia:
1. Soportar modo de prueba (dry-run)
2. Tener salida de log clara
3. Revertir en caso de fallo
4. Manejar interrupciones
5. Tener seguimiento de versiones

---

## 14.2 Script de Despliegue Simple

```bash
cat > desplegar.sh << 'EOF'
#!/bin/bash
set -euo pipefail

SERVIDOR_DESTINO="servidor.ejemplo.com"
RUTA_DESTINO="/var/www/miapp"
USUARIO_DESTINO="despliegue"

ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
NC='\033[0m'

registrar() { echo -e "${VERDE}[INFO]${NC} $@"; }
advertir() { echo -e "${AMARILLO}[AVISO]${NC} $@"; }
error() { echo -e "${ROJO}[ERROR]${NC} $@" >&2; }

verificar() {
    command -v rsync &>/dev/null || { error "rsync es requerido"; exit 1; }
    if ! ssh -o ConnectTimeout=5 "$USUARIO_DESTINO@$SERVIDOR_DESTINO" "exit 0" 2>/dev/null; then
        error "No se puede conectar a $SERVIDOR_DESTINO"
        exit 1
    fi
    registrar "Verificaciones previas aprobadas"
}

respaldar() {
    registrar "Creando respaldo..."
    MARCA=$(date +%Y%m%d_%H%M%S)
    ssh "$USUARIO_DESTINO@$SERVIDOR_DESTINO" "cp -r $RUTA_DESTINO $RUTA_DESTINO.respaldo.$MARCA"
    registrar "Respaldo creado: $RUTA_DESTINO.respaldo.$MARCA"
}

desplegar() {
    registrar "Iniciando despliegue..."
    rsync -avz --delete \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='.env' \
        ./ "$USUARIO_DESTINO@$SERVIDOR_DESTINO:$RUTA_DESTINO/"
    registrar "Archivos sincronizados"
}

reiniciar() {
    registrar "Reiniciando servicio..."
    ssh "$USUARIO_DESTINO@$SERVIDOR_DESTINO" "systemctl restart miapp"
    sleep 2
    
    if ssh "$USUARIO_DESTINO@$SERVIDOR_DESTINO" "systemctl is-active miapp" | grep -q "active"; then
        registrar "Servicio iniciado exitosamente"
    else
        error "El servicio no pudo iniciar"
        exit 1
    fi
}

principal() {
    registrar "Despliegue iniciando"
    registrar "Destino: $USUARIO_DESTINO@$SERVIDOR_DESTINO:$RUTA_DESTINO"
    
    verificar
    respaldar
    desplegar
    reiniciar
    
    registrar "Despliegue completado!"
}

principal
EOF

chmod +x desplegar.sh
```

---

## 14.3 Soporte para Dry-run

```bash
cat > desplegar.sh << 'EOF'
#!/bin/bash
set -euo pipefail

PRUEBA_SECA=false
SERVIDOR_DESTINO="servidor.ejemplo.com"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--dry-run)
            PRUEBA_SECA=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

registrar() { echo "[INFO] $@"; }

desplegar() {
    if $PRUEBA_SECA; then
        registrar "[PRUEBA-SECA] Sincronizaria archivos a $SERVIDOR_DESTINO"
        rsync -avz --dry-run ./ "$SERVIDOR_DESTINO:/tmp/prueba/"
    else
        registrar "Iniciando despliegue..."
        rsync -avz ./ "$SERVIDOR_DESTINO:/var/www/app/"
    fi
}

desplegar
EOF
```

---

## 14.4 Despliegue Multi-Entorno

```bash
cat > desplegar.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ENTORNO="${1:-pruebas}"

case "$ENTORNO" in
    pruebas)
        SERVIDOR="pruebas.ejemplo.com"
        RUTA="/var/www/pruebas"
        ;;
    produccion)
        SERVIDOR="prod.ejemplo.com"
        RUTA="/var/www/produccion"
        CONFIRMAR=true
        ;;
    *)
        echo "Entorno desconocido: $ENTORNO"
        exit 1
        ;;
esac

registrar() { echo "[$ENTORNO] $@"; }

if [[ "$CONFIRMAR" == "true" ]]; then
    echo "Acerca de desplegar a produccion: $SERVIDOR"
    read -p "Continuar? (s/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Ss]$ ]] || exit 0
fi

registrar "Iniciando despliegue a $SERVIDOR"

rsync -avz --delete \
    --exclude='.env' \
    ./ "$SERVIDOR:$RUTA/"

ssh "$SERVIDOR" "cd $RUTA && npm install --production"

registrar "Despliegue completado"
EOF
```

---

## 14.5 Ejercicios

1. Escribe un script de despliegue que soporte la opcion `--dry-run`
2. Agrega funcionalidad de respaldo al script de despliegue
3. Escribe un script de despliegue multi-entorno (desarrollo/pruebas/produccion)
4. Crea un script de rollback que liste y permita elegir a que version revertir
