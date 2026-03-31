# 5. Procesamiento de Texto

---

## 5.1 La Filosofía de Procesamiento de Texto de la IA

En el mundo de la IA, **todo es texto**.

- El código es texto
- Los archivos de configuración son texto
- Los logs son texto
- JSON, HTML, Markdown son todo texto

Así que los comandos de procesamiento de texto son el núcleo del toolkit de la IA.

Cuando los ingenieros humanos encuentran problemas: "Necesito una herramienta para manejar esto..."
Cuando la IA encuentra problemas: "Esto se puede resolver con `grep | sed | awk` en una línea."

---

## 5.2 `cat`: El Arte de Leer Archivos

### Uso Básico

```bash
# Mostrar contenido del archivo
cat file.txt

# Combinar archivos
cat part1.txt part2.txt > whole.txt

# Mostrar números de línea
cat -n script.sh
```

### Propósito Real: Combinar y Crear

```bash
cat << 'EOF' > newfile.txt
Contenido del archivo
Puede escribir muchas líneas
EOF
```

---

## 5.3 `head` y `tail`: Ver Solo lo que Necesitas

### `head`: Mirar el Principio

```bash
# Primeras 10 líneas (por defecto)
head file.txt

# Primeras 5 líneas
head -n 5 file.txt

# Primeros 100 bytes
head -c 100 file.txt
```

### `tail`: Mirar el Final

```bash
# Últimas 10 líneas (por defecto)
tail file.txt

# Últimas 5 líneas
tail -n 5 file.txt

# Seguir archivo en tiempo real (¡más común!)
tail -f /var/log/syslog

# Seguir y filtrar
tail -f app.log | grep --line-buffered ERROR
```

### Ver Rango Específico de Líneas

```bash
# Ver líneas 100-150
tail -n +100 file.txt | head -n 50
```

---

## 5.4 `wc`: Herramienta de Conteo

```bash
# Contar líneas
wc -l file.txt

# Contar líneas de múltiples archivos
wc -l *.py

# Contar archivos en directorio
ls | wc -l
```

---

## 5.5 `grep`: Rey de la Búsqueda de Texto

### Uso Básico

```bash
# Buscar líneas con "error"
grep "error" log.txt

# Ignorar mayúsculas
grep -i "error" log.txt

# Mostrar números de línea
grep -n "error" log.txt

# Solo mostrar nombres de archivos
grep -l "TODO" *.md

# Invertir (líneas sin coincidencia)
grep -v "debug" log.txt

# Coincidencia de palabra completa
grep -w "error" log.txt
```

### Expresiones Regulares

```bash
# Coincidir inicio
grep "^Error" log.txt

# Coincidir final
grep "hecho.$" log.txt

# Cualquier carácter
grep "e.or" log.txt

# Rango
grep -E "[0-9]{3}-" log.txt
```

### Técnicas Avanzadas

```bash
# Búsqueda recursiva
grep -r "TODO" src/

# Solo extensión específica
grep -r "TODO" --include="*.py" src/

# Mostrar contexto de líneas
grep -B 2 -A 2 "ERROR" log.txt

# Múltiples condiciones (O)
grep -E "error|warning|fatal" log.txt
```

---

## 5.6 `sed`: Herramienta de Reemplazo de Texto

### Reemplazo Básico

```bash
# Reemplazar primera coincidencia
sed 's/viejo/nuevo/' file.txt

# Reemplazar todas las coincidencias
sed 's/viejo/nuevo/g' file.txt

# Reemplazo en el lugar
sed -i 's/viejo/nuevo/g' file.txt

# Respaldar luego reemplazar
sed -i.bak 's/viejo/nuevo/g' file.txt
```

### Eliminar Líneas

```bash
# Eliminar líneas vacías
sed '/^$/d' file.txt

# Eliminar líneas de comentario
sed '/^#/d' file.txt

# Eliminar espacios en blanco al final
sed 's/[[:space:]]*$//' file.txt
```

### Ejemplos Prácticos

```bash
# Renombrar en lote extensiones (.txt → .md)
for f in *.txt; do
    mv "$f" "$(sed 's/.txt$/.md/' <<< "$f")"
done

# Eliminar finales de línea Windows
sed -i 's/\r$//' file.txt
```

---

## 5.7 `awk`: Navaja Suiza del Procesamiento de Texto

### Concepto Básico

`awk` procesa texto línea por línea, dividiendo automáticamente en campos ($1, $2, $3...), ejecutando acciones especificadas para cada línea.

### Uso Básico

```bash
# División por espacios en blanco por defecto
awk '{print $1}' file.txt

# Especificar delimitador
awk -F: '{print $1}' /etc/passwd

# Mostrar múltiples campos
awk -F: '{print $1, $3, $7}' /etc/passwd
```

### Procesamiento Condicional

```bash
# Solo procesar líneas coincidentes
awk -F: '$3 > 1000 {print $1}' /etc/passwd

# BEGIN y END
awk 'BEGIN {print "Inicio"} {print} END {print "Hecho"}' file.txt
```

### Ejemplos Prácticos

```bash
# Sumar una columna CSV
awk -F, '{sum += $3} END {print sum}' data.csv

# Encontrar máximo
awk 'NR==1 {max=$3} $3>max {max=$3} END {print max}' data.csv

# Salida formateada
awk '{printf "%-20s %10.2f\n", $1, $2}' data.txt
```

---

## 5.8 Práctica: Combinando Todas las Herramientas

### Escenario: Analizar Logs del Servidor

```bash
# 1. Encontrar mensajes de error
grep -i "error" access.log

# 2. Contar errores
grep -ci "error" access.log

# 3. Encontrar errores más comunes
grep "error" access.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head

# 4. Contar solicitudes por hora
awk '{print $4}' access.log | cut -d: -f2 | sort | uniq -c
```

### Escenario: Modificar Código en Lote

```bash
# Cambiar "print" a "logger.info" en todos los archivos .py
find . -name "*.py" -exec sed -i 's/print(/logger.info(/g' {} +

# Cambiar var a const
find . -name "*.js" -exec sed -i 's/\bvar\b/const/g' {} +
```

---

## 5.9 Referencia Rápida

| Comando | Propósito | Indicadores Comunes |
|---------|-----------|---------------------|
| `cat` | Mostrar/combinar archivos | `-n` números de línea |
| `head` | Ver inicio del archivo | `-n` líneas, `-c` bytes |
| `tail` | Ver final del archivo | `-n` líneas, `-f` seguir |
| `wc` | Conteo | `-l` líneas, `-w` palabras, `-c` bytes |
| `grep` | Búsqueda de texto | `-i` ignorar, `-n` número línea, `-r` recursivo, `-c` contar |
| `sed` | Reemplazo de texto | `s/viejo/nuevo/g`, `-i` en lugar |
| `awk` | Procesamiento de campos | `-F` delimitador, `{print}` acción |

---

## 5.10 Ejercicios

1. Usa `head` y `tail` para ver líneas 100-120
2. Usa `grep` para encontrar todos los usuarios con `/bin/bash` en /etc/passwd
3. Usa `sed` para reemplazar todos `\r\n` con `\n`
4. Usa `awk` para calcular máximo, mínimo y promedio de un archivo numérico
