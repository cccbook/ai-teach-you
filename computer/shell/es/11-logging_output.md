# 11. Registro y Salida

---

## 11.1 Por Que Es Importante el Registro

Sin registro:
- No sabes donde esta el script
- No sabes por que fallo
- No sabes lo que hizo en caso de exito

Con registro:
- Puedes seguir el progreso
- Tienes suficiente informacion para depurar fallos
- Puedes auditar el historial de ejecucion

---

## 11.2 Niveles de Log Basicos

```bash
#!/bin/bash

DEBUG=0
INFO=1
WARN=2
ERROR=3

NIVEL_LOG=${NIVEL_LOG:-$INFO}

registrar() {
    local nivel=$1
    shift
    local mensaje="$@"
    local marca_tiempo=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [[ $nivel -ge $NIVEL_LOG ]]; then
        echo "[$marca_tiempo] $mensaje"
    fi
}

registrar $DEBUG "Esto es depuracion"
registrar $INFO "Esto es informacion"
registrar $WARN "Esto es advertencia"
registrar $ERROR "Esto es error"
```

---

## 11.3 Salida con Colores

```bash
#!/bin/bash

ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
NC='\033[0m'  # Sin Color

registrar_info() { echo -e "${VERDE}[INFO]${NC} $@"; }
registrar_aviso() { echo -e "${AMARILLO}[AVISO]${NC} $@"; }
registrar_error() { echo -e "${ROJO}[ERROR]${NC} $@" >&2; }

registrar_info "Instalacion completada"
registrar_aviso "Usando valores predeterminados"
registrar_error "Conexion fallida"
```

---

## 11.4 Salida a Archivo

```bash
#!/bin/bash

ARCHIVO_LOG="/var/log/miapp.log"

registrar() {
    local mensaje="[$(date '+%Y-%m-%d %H:%M:%S')] $@"
    echo "$mensaje"
    echo "$mensaje" >> "$ARCHIVO_LOG"
}

registrar "Aplicacion iniciada"
```

---

## 11.5 `tee`: Salida a Pantalla y Archivo

```bash
# Mostrar y guardar simultaneamente
echo "Hola" | tee salida.txt

# Modo agregar
echo "Mundo" | tee -a salida.txt

# Capturar stderr tambien
./script.sh 2>&1 | tee salida.log
```

---

## 11.6 Indicadores de Progreso

### Puntos Simples

```bash
echo -n "Procesando"
for i in {1..10}; do
    echo -n "."
    sleep 0.2
done
echo " Listo"
```

### Barra de Progreso

```bash
dibujar_progreso() {
    local actual=$1
    local total=$2
    local ancho=40
    local porcentaje=$((actual * 100 / total))
    local caracteres=$((ancho * actual / total))
    
    printf "\r[%s%s] %3d%%" \
        "$(printf '%*s' $caracteres | tr ' ' '=')" \
        "$(printf '%*s' $((ancho - caracteres)) | tr ' ' '-')" \
        "$porcentaje"
    
    [[ $actual -eq $total ]] && echo
}
```

---

## 11.7 Explicacion de `2>&1`

```bash
# 1 = stdout, 2 = stderr

# Redirigir stderr a stdout
comando 2>&1

# Redirigir stdout a archivo, stderr a pantalla
comando > salida.txt

# Redirigir ambos a archivo
comando > salida.txt 2>&1

# Redirigir ambos a /dev/null (ocultar)
comando > /dev/null 2>&1
```

---

## 11.8 Referencia Rapida

| Sintaxis | Descripcion |
|----------|-------------|
| `echo "texto"` | Salida basica |
| `echo -e "\033[31m"` | Salida con color |
| `2>&1` | Redirigir stderr a stdout |
| `> archivo` | Sobrescribir archivo |
| `>> archivo` | Agregar a archivo |
| `tee archivo` | Mostrar y guardar |
| `tee -a archivo` | Modo agregar |
| `/dev/null` | Descartar salida |

---

## 11.9 Ejercicios

1. Escribe un script que muestre mensajes INFO, AVISO, ERROR en diferentes colores
2. Usa `tee` para mostrar y guardar la salida en un archivo de log simultaneamente
3. Crea un script de procesamiento de archivos con una barra de progreso
4. Construye una biblioteca de registro que soporte salida a archivo y niveles de log
