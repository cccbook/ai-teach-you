# 3. Operaciones de Archivos

---

## 3.1 El Modelo Mental de la IA del Sistema de Archivos

Antes de profundizar en cada comando, entiende cómo la IA ve el sistema de archivos.

Los ingenieros humanos típicamente ven el sistema de archivos **visualmente**—como el Explorador de Windows o el Finder de macOS, entendiendo a través de iconos y formas de carpetas.

La vista de la IA es completamente diferente:

```
path          = ubicación absoluta /home/user/project/src/main.py
relative      = caminar hacia abajo desde la ubicación actual
nodes         = cada archivo o directorio es un "nodo"
attributes    = permisos, tamaño, marcas de tiempo, propietario
type          = archivo regular(-), directorio(d), enlace(l), dispositivo(b/c)
```

Cuando la IA ejecuta `ls -la`, ve:

```
drwxr-xr-x  5 ai  staff  170 Mar 22 10:30 .
drwxr-xr-x  3 ai  staff  102 Mar 22 09:00 ..
-rw-r--r--  1 ai  staff  4096 Mar 22 10:30 .env
-rw-r--r--  1 ai  staff  8192 Mar 22 10:31 README.md
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 src
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 tests
-rw-r--r--  1 ai  staff  2048 Mar 22 10:32 package.json
```

La IA puede leer inmediatamente de esto:
- Cuáles son directorios (`d`)
- Cuáles son archivos ocultos (que comienzan con `.`)
- Quién tiene qué permisos
- Tamaños de archivos (determinando si son grandes)
- Última hora de modificación

---

## 3.2 `ls`: El Primer Comando Más Usado por la IA

Casi antes de cada operación, la IA ejecuta `ls` para confirmar el estado actual.

### Combinaciones Comunes de `ls` de la IA

```bash
# Lista básica
ls

# Mostrar archivos ocultos (¡muy importante!)
ls -a

# Formato largo (info detallada)
ls -l

# Formato largo + archivos ocultos (más común)
ls -la

# Ordenar por tiempo de modificación (más nuevo primero)
ls -lt

# Ordenar por tiempo de modificación (más antiguo primero)
ls -ltr

# Tamaños legibles por humanos (K, M, G)
ls -lh

# Solo mostrar directorios
ls -d */

# Mostrar todos los archivos recursivamente
ls -R

# Mostrar números de inodo (útil para enlaces duros)
ls -li
```

### Flujo de Trabajo Real de la IA

```bash
cd ~/project && ls -la

# Resultado:
# drwxr-xr-x  5 ai  staff  170 Mar 22 10:30 .
# drwxr-xr-x  3 ai  staff  102 Mar 22 09:00 ..
# -rw-r--r--  1 ai  staff  4096 Mar 22 10:30 .env
# -rw-r--r--  1 ai  staff  8192 Mar 22 10:31 README.md
# drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 src
# drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 tests
# -rw-r--r--  1 ai  staff  2048 Mar 22 10:32 package.json

# Análisis de la IA: hay un archivo .env, directorios src y tests, package.json
# Esto es un proyecto Node.js
```

---

## 3.3 `cd`: El Directorio que la IA Nunca Olvida

### Hábitos de `cd` de la IA

```bash
# Ir al directorio home
cd ~

# Ir al directorio anterior (¡muy útil!)
cd -

# Ir al directorio padre
cd ..

# Entrar a un subdirectorio
cd src

# Navegar rutas profundas (gracias a Tab completion)
cd ~/project/backend/api/v2/routes
```

### El Patrón `cd` + `&&` de la IA

Este es uno de los patrones más comunes de la IA:

```bash
# Primero cd, solo ejecutar el siguiente comando después de confirmar éxito
cd ~/project && ls -la
```

### Errores Comunes

```bash
# Error: no confirmar que el directorio existe
cd nonexistent
# Salida: bash: cd: nonexistent: No such file or directory

# Enfoque de la IA: verificar primero
[ -d "nonexistent" ] && cd nonexistent || echo "El directorio no existe"
```

---

## 3.4 `mkdir`: El Arte de Crear Directorios

### Uso Básico

```bash
# Crear un solo directorio
mkdir myproject

# Crear múltiples directorios
mkdir src tests docs

# Crear directorios anidados (-p es la clave!)
mkdir -p project/src/components project/tests
```

### Por Qué la IA Casi Siempre Usa `-p`

El indicador `-p` (parents) significa:
1. Si el directorio existe, **sin error**
2. Si el padre no existe, **crearlo automáticamente**

### Patrón Típico de Creación de Proyecto de la IA

```bash
# Crear una estructura de proyecto estándar
mkdir -p project/{src,tests,docs,scripts,config}
```

---

## 3.5 `rm`: El Arte de la Eliminación

**Advertencia**: Este es uno de los comandos más peligrosos en Shell.

### Uso Básico

```bash
# Eliminar archivo
rm file.txt

# Eliminar directorio (necesita -r)
rm -r directory/

# Eliminar directorio y todo (¡peligroso!)
rm -rf directory/
```

### El Peligro de `rm -rf`

```bash
# ¡Nunca ejecutes esto como root!
# rm -rf /

# Si accidentalmente agregas un espacio extra:
rm -rf * 
# (espacio) = rm -rf elimina todo en el directorio actual
```

---

## 3.6 `cp`: Copiar Archivos y Directorios

### Uso Básico

```bash
# Copiar archivo
cp source.txt destination.txt

# Copiar directorio (necesita -r)
cp -r source_directory/ destination_directory/

# Mostrar progreso durante copia (-v verbose)
cp -v large_file.iso /backup/

# Modo interactivo (preguntar antes de sobrescribir)
cp -i *.py src/
```

### Poder de los Comodines

```bash
# Copiar todos los archivos .txt
cp *.txt backup/

# Copiar todos los archivos de imagen
cp *.{jpg,png,gif,webp} images/
```

---

## 3.7 `mv`: Mover y Renombrar

### Uso Básico

```bash
# Mover archivo
mv file.txt backup/

# Mover y renombrar
mv oldname.txt newname.txt

# Renombrar en lote
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

---

## 3.8 Referencia Rápida

| Comando | Uso Básico | Indicadores Comunes | Nota de la IA |
|---------|------------|---------------------|---------------|
| `ls` | `ls [ruta]` | `-l` largo, `-a` oculto, `-h` humano | `ls -la` siempre es bueno |
| `cd` | `cd [ruta]` | `-` anterior, `..` padre | `cd xxx &&` es buen hábito |
| `mkdir` | `mkdir [dir]` | `-p` anidado | casi siempre usar `-p` |
| `rm` | `rm [archivo]` | `-r` recursivo, `-f` forzar | cuidado con `rm -rf /*` |
| `cp` | `cp [src] [dst]` | `-r` directorio, `-i` preguntar, `-p` preservar | usar `-i` por seguridad |
| `mv` | `mv [src] [dst]` | `-i` preguntar, `-n` no-sobrescribir | es renombrar |

---

## 3.9 Ejercicios

1. Usa `mkdir -p` para crear un directorio anidado de tres niveles, luego confirma con `tree` o `find`
2. Copia un archivo grande con `cp -v` y ve la salida
3. Renombra en lote 10 archivos `.txt` a `.md` con `mv`
4. Elimina un archivo de prueba con `rm -i` para experimentar el prompt
