# 12. Procesamiento por Lotes de Archivos

---

## 12.1 Renombrar en Lote

### Reemplazo Simple de Extension

```bash
# Cambiar todos los .txt a .md
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

### Agregar Prefijo

```bash
# Agregar prefijo thumb_ a todas las imagenes
for f in *.jpg *.png *.gif; do
    [[ -f "$f" ]] || continue
    mv "$f" "thumb_$f"
done
```

### Eliminar Espacios

```bash
# Reemplazar espacios en nombres de archivos con guiones bajos
for f in *\ *; do
    [[ -f "$f" ]] || continue
    mv "$f" "${f// /_}"
done
```

### Agregar Numeros

```bash
# Numerar archivos 001, 002, 003...
i=1
for f in *.jpg; do
    [[ -f "$f" ]] || continue
    mv "$f" "$(printf '%03d.jpg' $i)"
    ((i++))
done
```

---

## 12.2 Procesamiento de Imagenes en Lote

```bash
#!/bin/bash
set -euo pipefail

TAMANO=${1:-800}

for img in *.jpg *.png; do
    [[ -f "$img" ]] || continue
    
    echo "Procesando: $img"
    
    if command -v convert &>/dev/null; then
        # Crear miniatura
        convert "$img" -resize "${TAMANO}x${TAMANO}>" "thumb_$img"
        
        # Crear version grande
        convert "$img" -resize 1920x1080 "large_$img"
        
        echo "Hecho: thumb_$img, large_$img"
    fi
done
```

---

## 12.3 Buscar y Reemplazar en Lote

```bash
#!/bin/bash

# Reemplazar "foo" con "bar" en todos los archivos .txt
for f in *.txt; do
    [[ -f "$f" ]] || continue
    sed -i.bak 's/foo/bar/g' "$f"
done
```

---

## 12.4 Compresion en Lote

```bash
#!/bin/bash

# Comprimir cada archivo
for f in *.txt; do
    [[ -f "$f" ]] || continue
    gzip "$f"
done

# Descomprimir todos
gunzip *.gz
```

---

## 12.5 Descarga en Lote

```bash
#!/bin/bash
set -euo pipefail

while read -r url; do
    nombre_archivo=$(basename "$url")
    echo "Descargando: $url"
    curl -L -o "$nombre_archivo" "$url"
done < urls.txt
```

---

## 12.6 Referencia Rapida

| Tarea | Comando |
|------|---------|
| Cambiar extension | `mv "$f" "${f%.old}.new"` |
| Agregar prefijo | `mv "$f" "prefijo_$f"` |
| Eliminar espacios | `mv "$f" "${f// /_}"` |
| Agregar numeros | `mv "$f" "$(printf '%03d' $i)"` |
| Reemplazo en lote | `for f in *.txt; do sed -i 's/a/b/g' "$f"; done` |
| Comprimir en lote | `for f in *.txt; do gzip "$f"; done` |
| Descargar en lote | `while read url; do curl -LO "$url"; done < urls.txt` |

---

## 12.7 Ejercicios

1. Renombrar en lote 10 archivos de `.txt` a `.md`
2. Agregar prefijo `thumb_` a todas las imagenes y crear miniaturas
3. Reemplazar `sitio-antiguo.com` con `sitio-nuevo.com` en todos los archivos `.html`
4. Crear un script de limpieza que elimine todos los archivos `__pycache__`, `.pyc` y `.log`
