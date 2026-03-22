# 10. Analisis de Argumentos y Herramientas CLI

---

## 10.1 Fundamentos de Argumentos de Linea de Comandos

```bash
#!/bin/bash

echo "Script: $0"
echo "Primer arg: $1"
echo "Segundo arg: $2"
echo "Tercer arg: ${3:-predeterminado}"  # valor por defecto
echo "Numero de args: $#"
echo "Todos los args: $@"
```

### Ejecucion

```bash
./script.sh foo bar
# Salida:
# Script: ./script.sh
# Primer arg: foo
# Segundo arg: bar
# Tercer arg: predeterminado
# Numero de args: 2
# Todos los args: foo bar
```

---

## 10.2 Analisis Simple de Argumentos

### Parametros Posicionales

```bash
#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Uso: $0 <archivo>"
    exit 1
fi

ARCHIVO="$1"

if [[ ! -f "$ARCHIVO" ]]; then
    echo "Error: el archivo no existe"
    exit 1
fi

echo "Procesando $ARCHIVO..."
```

### Manejo de Argumentos Opcionales

```bash
#!/bin/bash

VERBOSE=false
SALIDA=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -o|--salida)
            SALIDA="$2"
            shift 2
            ;;
        -*)
            echo "Opcion desconocida: $1"
            exit 1
            ;;
        *)
            ARCHIVO="$1"
            shift
            ;;
    esac
done

$VERBOSE && echo "modo verbose activado"
[[ -n "$SALIDA" ]] && echo "Salida a: $SALIDA"
```

---

## 10.3 `getopts`: Analisis Estandar de Opciones

```bash
#!/bin/bash

while getopts "hv:o:" opt; do
    case $opt in
        h)
            echo "Informacion de ayuda"
            exit 0
            ;;
        v)
            echo "modo verbose: $OPTARG"
            ;;
        o)
            echo "archivo de salida: $OPTARG"
            ;;
        \?)
            echo "Opcion invalida: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))

echo "Argumentos restantes: $@"
```

### Referencia de Formato de Opciones

| Formato | Significado |
|---------|-------------|
| `getopts "hv:"` | `-h` sin arg, `-v` necesita arg |
| `OPTARG` | Valor del argumento de la opcion actual |
| `OPTIND` | Indice del siguiente argumento |

---

## 10.4 Entrada Interactiva

### `read`: Leer Entrada del Usuario

```bash
#!/bin/bash

# Lectura basica
read -p "Ingresa tu nombre: " nombre
echo "Hola, $nombre"

# Contrasenia (oculta)
read -sp "Ingresa la contrasenia: " contrasenia
echo

# Leer multiples valores
read -p "Ingresa nombre y edad: " nombre edad
echo "$nombre tiene $edad anios"

# Con tiempo limite
read -t 5 -p "Ingresa en 5 segundos: " valor
```

### Solicitud de Confirmacion

```bash
confirmar() {
    read -p "$1 (s/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Ss]$ ]]
}

if confirmar "Eliminar este archivo?"; then
    echo "Eliminando..."
fi
```

---

## 10.5 Interfaz de Menu

```bash
#!/bin/bash

PS3="Selecciona operacion: "

select opcion in "Crear proyecto" "Eliminar proyecto" "Salir"; do
    case $opcion in
        "Crear proyecto")
            echo "Creando..."
            ;;
        "Eliminar proyecto")
            echo "Eliminando..."
            ;;
        "Salir")
            echo "Adios!"
            exit 0
            ;;
        *)
            echo "Opcion invalida"
            ;;
    esac
done
```

---

## 10.6 Referencia Rapida

| Sintaxis | Descripcion |
|----------|-------------|
| `$0` | Nombre del script |
| `$1`, `$2`... | Parametros posicionales |
| `$#` | Numero de argumentos |
| `${var:-predeterminado}` | Valor por defecto |
| `getopts "hv:" opt` | Analizar opciones |
| `$OPTARG` | Arg de la opcion actual |
| `read -p "prompt:" var` | Leer entrada |
| `read -s var` | Entrada oculta (contrasenia) |
| `read -t 5 var` | Tiempo limite de 5 segundos |
| `select` | Interfaz de menu |

---

## 10.7 Ejercicios

1. Escribe una herramienta CLI que acepte `-n` para cantidad, `-v` para verbose
2. Usa `getopts` para analizar opciones `-h` (ayuda), `-o` (archivo de salida)
3. Escribe una funcion de confirmacion que solo proceda con respuesta s
4. Crea un menu de calculadora simple con `select`
