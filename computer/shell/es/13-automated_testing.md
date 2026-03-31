# 13. Pruebas Automatizadas

---

## 13.1 Por Que Usar Shell para Pruebas

- Ejecucion rapida de verificaciones simples
- Probar comandos del sistema y scripts
- Pruebas de integracion en CI/CD
- Pruebas de regresion de scripts existentes

---

## 13.2 Framework Basico de Pruebas

```bash
#!/bin/bash
set -euo pipefail

PRUEBAS_EJECUTADAS=0
PRUEBAS_APROBADAS=0
PRUEBAS_FALLIDAS=0

prueba() {
    local nombre=$1
    local comando=$2
    local esperado=$3
    
    ((PRUEBAS_EJECUTADAS++))
    
    local resultado
    resultado=$(eval "$comando" 2>/dev/null)
    
    if [[ "$resultado" == "$esperado" ]]; then
        echo "✓ $nombre"
        ((PRUEBAS_APROBADAS++))
    else
        echo "✗ $nombre"
        echo "  Esperado: $esperado"
        echo "  Resultado: $resultado"
        ((PRUEBAS_FALLIDAS++))
    fi
}

prueba "Suma" "echo \$((1 + 1))" "2"
prueba "Cadena igual" "echo hola" "hola"

echo ""
echo "Resultados: $PRUEBAS_APROBADAS/$PRUEBAS_EJECUTADAS aprovadas"
[[ $PRUEBAS_FALLIDAS -eq 0 ]] || exit 1
```

---

## 13.3 Probar Archivos y Directorios

```bash
#!/bin/bash

probar_archivo_existe() {
    local archivo=$1
    [[ -f "$archivo" ]] || { echo "✗ Archivo no encontrado: $archivo"; return 1; }
}

probar_directorio_existe() {
    local dir=$1
    [[ -d "$dir" ]] || { echo "✗ Directorio no encontrado: $dir"; return 1; }
}

probar_archivo_contiene() {
    local archivo=$1
    local patron=$2
    grep -q "$patron" "$archivo" || { echo "✗ Archivo sin: $patron"; return 1; }
}
```

---

## 13.4 Probar Salida de Comandos

```bash
#!/bin/bash

probar_exito() {
    local nombre=$1
    shift
    if "$@"; then
        echo "✓ $nombre"
    else
        echo "✗ $nombre (codigo de salida: $?)"
        return 1
    fi
}

probar_fallo() {
    local nombre=$1
    shift
    if ! "$@" 2>/dev/null; then
        echo "✓ $nombre (fallo correcto)"
    else
        echo "✗ $nombre (deberia fallar pero tuvo exito)"
        return 1
    fi
}

probar_salida() {
    local nombre=$1
    local esperado=$2
    shift 2
    
    local salida=$("$@" 2>/dev/null)
    if [[ "$salida" == *"$esperado"* ]]; then
        echo "✓ $nombre"
    else
        echo "✗ $nombre"
        return 1
    fi
}
```

---

## 13.5 Script de Pruebas Compatible con CI

```bash
cat > scripts/probar.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ROJO='\033[0;31m'
VERDE='\033[0;32m'
NC='\033[0m'

FALLIDAS=0

ejecutar_prueba() {
    local nombre=$1
    local cmd=$2
    
    echo -n "Prueba: $nombre ... "
    if eval "$cmd" &>/dev/null; then
        echo -e "${VERDE}✓${NC}"
    else
        echo -e "${ROJO}✗${NC}"
        ((FALLIDAS++))
    fi
}

ejecutar_prueba "Script init existe" "[[ -x scripts/iniciar-proyecto.sh ]]"
ejecutar_prueba "Script build existe" "[[ -f scripts/compilar.sh ]]"
ejecutar_prueba "Script deploy existe" "[[ -f scripts/desplegar.sh ]]"

echo ""
if [[ $FALLIDAS -eq 0 ]]; then
    echo -e "${VERDE}Todas las pruebas pasaron${NC}"
    exit 0
else
    echo -e "${ROJO}$FALLIDAS pruebas fallaron${NC}"
    exit 1
fi
EOF

chmod +x scripts/probar.sh
```

---

## 13.6 Ejercicios

1. Escribe un framework de pruebas con funciones `probar_igual`, `probar_contiene`, `probar_exito`
2. Escribe 5 casos de prueba para uno de tus scripts
3. Crea un script de pruebas compatible con CI que genere salida en formato TAP
4. Prueba un script de procesamiento por lotes para asegurar que maneja todos los archivos correctamente
