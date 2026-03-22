# 7. Control de Flujo y Bucles Condicionales

---

## 7.1 Combinar Comandos: La Esencia de Shell

Los comandos individuales tienen capacidad limitada. Solo **combinándolos** puedes completar tareas complejas.

La IA es poderosa en gran parte porque domina estas combinaciones:

```bash
cat access.log | grep "ERROR" | sort | uniq -c | sort -rn | head -10
```

Esto significa: "De access.log, encontrar errores, contar ocurrencias, mostrar top 10"

---

## 7.2 `|` (Tubería): El Arte del Flujo de Datos

La tubería convierte la **salida** del comando anterior en la **entrada** del siguiente.

```bash
# Ordenar contenido de archivo
cat unsorted.txt | sort

# Encontrar comandos más comunes
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# Extraer IPs del log y contar
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```

### Redirigir stderr a la tubería

```bash
# Enviar stderr a la tubería
command1 2>&1 | command2

# O Bash 4+
command1 |& command2
```

---

## 7.3 `&&`: Ejecutar Siguiente Solo Si Éxito

**Solo si `command1` tiene éxito (código de salida = 0) se ejecutará `command2`.**

```bash
# Crear directorio luego entrar
mkdir -p project && cd project

# Compilar luego ejecutar
gcc -o program source.c && ./program

# Descargar luego extraer
curl -L -o archive.tar.gz http://example.com/file && tar -xzf archive.tar.gz
```

---

## 7.4 `||`: Ejecutar Siguiente Solo Si Falla

**Solo si `command1` falla (código de salida ≠ 0) se ejecutará `command2`.**

```bash
# Crear archivo si no existe
[ -f config.txt ] || echo "Config faltante" > config.txt

# Intentar una forma, fallback a otra
cd /opt/project || cd /home/user/project

# Asegurar éxito incluso en fallo (común en makefiles)
cp file.txt file.txt.bak || true
```

### Combinando `&&` y `||`

```bash
# Expresión condicional
[ -f config ] && echo "Encontrado" || echo "No encontrado"

# Equivalente a:
if [ -f config ]; then
    echo "Encontrado"
else
    echo "No encontrado"
fi
```

---

## 7.5 `;`: Ejecutar Sin Condición

```bash
# Los tres se ejecutan
mkdir /tmp/test ; cd /tmp/test ; pwd
```

---

## 7.6 `$()`: Sustitución de Comandos

**Ejecutar comando, reemplazar `$()` con su salida.**

```bash
# Uso básico
echo "Hoy es $(date +%Y-%m-%d)"
# Salida: Hoy es 2026-03-22

# En variables
FILES=$(ls *.txt)

# Obtener nombre de directorio
DIR=$(dirname /path/to/file.txt)
BASE=$(basename /path/to/file.txt)

# Calcular
echo "El resultado es $((10 + 5))"
# Salida: El resultado es 15
```

### vs Backticks

```bash
# Ambos son equivalentes
echo "Hoy es $(date +%Y)"
echo "Hoy es `date +%Y`"

# Pero $() es mejor porque puede anidarse
echo $(echo $(echo anidado))
```

---

## 7.7 `[[ ]]` y `[ ]`: Pruebas Condicionales

### Pruebas de Archivos

```bash
[[ -f file.txt ]]      # Archivo regular existe
[[ -d directory ]]     # Directorio existe
[[ -e path ]]          # Cualquier tipo existe
[[ -L link ]]          # Enlace simbólico existe
[[ -r file ]]          # Legible
[[ -w file ]]          # Escribible
[[ -x file ]]          # Ejecutable
[[ file1 -nt file2 ]]  # file1 es más nuevo que file2
```

### Pruebas de Cadenas

```bash
[[ -z "$str" ]]        # Cadena vacía
[[ -n "$str" ]]        # Cadena no vacía
[[ "$str" == "valor" ]] # Igual
[[ "$str" =~ patrón ]]  # Coincide con regex
```

### Pruebas Numéricas

```bash
[[ $num -eq 10 ]]      # Igual
[[ $num -ne 10 ]]      # Diferente
[[ $num -gt 10 ]]      # Mayor que
[[ $num -lt 10 ]]      # Menor que
```

---

## 7.8 `if`: Declaraciones Condicionales

```bash
if [[ condición ]]; then
    # hacer algo
elif [[ condición2 ]]; then
    # hacer algo más
else
    # fallback
fi
```

### Ejemplo Completo

```bash
#!/bin/bash

FILE="config.yaml"

if [[ ! -f "$FILE" ]]; then
    echo "Error: $FILE no existe"
    exit 1
fi

if [[ -r "$FILE" ]]; then
    echo "El archivo es legible"
else
    echo "El archivo no es legible"
fi
```

---

## 7.9 `for`: Bucles

### Sintaxis Básica

```bash
for variable in lista; do
    # usar $variable
done
```

### Patrones Comunes de la IA

```bash
# Procesar todos los archivos .txt
for file in *.txt; do
    echo "Procesando $file"
done

# Rango numérico
for i in {1..10}; do
    echo "Iteración $i"
done

# Array
for color in rojo verde azul; do
    echo $color
done

# Bucle estilo C (Bash 3+)
for ((i=0; i<10; i++)); do
    echo $i
done
```

---

## 7.10 `while`: Bucles Condicionales

```bash
# Leer líneas
while IFS= read -r line; do
    echo "Leído: $line"
done < file.txt

# Bucle contador
count=0
while [[ $count -lt 10 ]]; do
    echo $count
    ((count++))
done
```

---

## 7.11 `case`: Coincidencia de Patrones

```bash
case $ACTION in
    start)
        echo "Iniciando servicio..."
        ;;
    stop)
        echo "Deteniendo servicio..."
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Uso: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### Patrones con Comodines

```bash
case "$filename" in
    *.txt)
        echo "Archivo de texto"
        ;;
    *.jpg|*.png|*.gif)
        echo "Archivo de imagen"
        ;;
    *)
        echo "Tipo desconocido"
        ;;
esac
```

---

## 7.12 Referencia Rápida

| Símbolo | Nombre | Descripción |
|---------|--------|-------------|
| `\|` | Tubería | Pasar salida a siguiente entrada |
| `&&` | Y | Ejecutar siguiente solo si el anterior tiene éxito |
| `\|\|` | O | Ejecutar siguiente solo si el anterior falla |
| `;` | Punto y coma | Ejecutar sin condición |
| `$()` | Sustitución de comando | Ejecutar, reemplazar con salida |
| `[[ ]]` | Prueba condicional | sintaxis de prueba recomendada |
| `if` | Condicional | rama basada en condición |
| `for` | Bucle contador | iterar a través de lista |
| `while` | Bucle condicional | repetir mientras condición sea verdadera |
| `case` | Coincidencia de patrones | bifurcación múltiple |

---

## 7.13 Ejercicios

1. Usar `|` para combinar `ls`, `grep`, `wc` para contar archivos `.log`
2. Usar `&&` para asegurar que `cd` tenga éxito antes de continuar
3. Usar bucle `for` para crear 10 directorios (dir1 a dir10)
4. Usar `while read` para leer y mostrar /etc/hosts
5. Escribir una calculadora simple con `case` (suma, resta, mult, div)
