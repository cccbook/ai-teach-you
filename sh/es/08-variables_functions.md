# 8. Variables y Funciones

---

## 8.1 Fundamentos de Variables

### Asignacion Basica

```bash
# Cadena de texto
nombre="Alicia"
saludo="Hola, Mundo!"

# Numero
edad=25
contador=0

# Vacia
vacia=
vacia2=""
```

### Leer Variables

```bash
echo $nombre
echo ${nombre}    # Forma recomendada, mas explicita

# Entre comillas dobles
echo "Mi nombre es ${nombre}"
```

### Errores Comunes

```bash
# Incorrecto: espacios alrededor de =
nombre = "Alicia"   # Se interpreta como comando

# Incorrecto: sin comillas
saludo=Hola Mundo  # Solo muestra "Hola"

# Correcto:
nombre="Alicia"
saludo="Hola Mundo"
```

---

## 8.2 El Arte de las Comillas

### Comillas Dobles `"`
Expanden variables y sustitucion de comandos

```bash
nombre="Alicia"
echo "Hola, $nombre"           # Hola, Alicia
echo "Hoy es $(date +%Y)"       # Hoy es 2026
```

### Comillas Simples `'`
Salida literal, no expande nada

```bash
nombre="Alicia"
echo 'Hola, $nombre'           # Hola, $nombre
echo 'Hoy es $(date +%Y)'      # Hoy es $(date +%Y)
```

### Sin Comillas
Evitar a menos que este seguro de que la variable no contiene espacios

---

## 8.3 Variables Especiales

```bash
$0          # Nombre del script
$1, $2...   # Parametros posicionales
$#          # Numero de argumentos
$@          # Todos los argumentos (individuales)
$*          # Todos los argumentos (como una cadena)
$?          # Codigo de salida del ultimo comando
$$          # PID del proceso actual
$!          # PID del ultimo proceso en segundo plano
$-          # Opciones actuales del shell
```

---

## 8.4 Arreglos

### Uso Basico

```bash
# Definir arreglo
colores=("rojo" "verde" "azul")

# Leer elementos
echo ${colores[0]}    # rojo
echo ${colores[1]}    # verde

# Leer todos
echo ${colores[@]}    # rojo verde azul

# Longitud del arreglo
echo ${#colores[@]}   # 3
```

### Arreglos Asociativos (Bash 4+)

```bash
declare -A usuario
usuario["nombre"]="Alicia"
usuario["correo"]="alicia@ejemplo.com"

echo ${usuario["nombre"]}    # Alicia
```

---

## 8.5 Fundamentos de Funciones

### Definir Funciones

```bash
# Metodo 1: palabra clave function
function saludar {
    echo "Hola!"
}

# Metodo 2: definicion directa (recomendado)
saludar() {
    echo "Hola!"
}
```

### Parametros de Funciones

```bash
saludar() {
    echo "Hola, $1!"
}

saludar "Alicia"    # Hola, Alicia!
```

### Valores de Retorno

```bash
# return: para codigo de salida (0-255)
verificar() {
    if [[ $1 -gt 10 ]]; then
        return 0  # exito
    else
        return 1  # fallo
    fi
}

if verificar 15; then
    echo "Mayor que 10"
fi
```

---

## 8.6 Variables Locales

```bash
contador() {
    local cuenta=0
    ((cuenta++))
    echo $cuenta
}
```

---

## 8.7 Bibliotecas de Funciones

### Crear Biblioteca

```bash
cat > lib.sh << 'EOF'
#!/bin/bash

registrar() {
    echo "[$(date +%H:%M:%S)] $@"
}

error() {
    echo "[$(date +%H:%M:%S)] ERROR: $@" >&2
}

confirmar() {
    read -p "$1 (s/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Ss]$ ]]
}
EOF
```

### Usar Biblioteca

```bash
#!/bin/bash

source lib.sh

registrar "Iniciando proceso"
error "Algo salio mal"
confirmar "Continuar?" && echo "Continuando"
```

---

## 8.8 Referencia Rapida

| Tema | Sintaxis | Descripcion |
|------|----------|-------------|
| Asignacion | `var=valor` | Sin espacios alrededor de = |
| Leer | `$var` o `${var}` | Usar `${var}` |
| Comillas dobles | `"..."` | Expande variables |
| Comillas simples | `'...'` | Sin expansion |
| Argumentos | `$1`, `$2`, `$@` | Obtener parametros |
| Funcion | `nombre() { }` | definicion recomendada |
| Var local | `local var=valor` | solo en funcion |
| Arreglo | `arr=(a b c)` | indexado y asociativo |
| source | `source archivo.sh` | Cargar biblioteca |

---

## 8.9 Ejercicios

1. Escribe un script que acepte parametros nombre y edad, muestre "Hola Y, tienes X anios!"
2. Crea una biblioteca con funciones `registrar` y `error`, usala en otro script
3. Escribe una funcion recursiva para calcular numeros de Fibonacci
4. Usa `mapfile` para leer un archivo linea por linea a un arreglo, luego muestralo en orden inverso
