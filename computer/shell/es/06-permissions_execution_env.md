# 6. Permisos, Ejecución, Entorno y Configuración

---

## 6.1 `chmod`: El Arte de los Permisos

### Conceptos Básicos de Permisos en Linux/Unix

```
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 .
-rw-r--r--  1 ai  staff  4096 Mar 22 10:30 README.md
-rwxr-xr-x  1 ai  staff   128 Mar 22 10:30 script.sh
```

Los 9 caracteres están en tres grupos:
- `rwx` (propietario): leer, escribir, ejecutar
- `r-x` (grupo): leer, ejecutar
- `r--` (otros): solo leer

### Dos Representaciones de chmod

**Numérico (octal)**:

```
r = 4, w = 2, x = 1

rwx = 7, r-x = 5, r-- = 4
```

Combinaciones comunes:
- `777` = rwxrwxrwx (¡peligroso!)
- `755` = rwxr-xr-x
- `644` = rw-r--r--
- `700` = rwx------
- `600` = rw-------

**Simbólico**:

```bash
chmod u+x script.sh    # Propietario agrega ejecutar
chmod g-w file.txt     # Grupo elimina escribir
chmod +x script.sh     # Todos agregan ejecutar
```

### Uso Común de chmod de la IA

```bash
# Hacer script ejecutable (casi todo script)
chmod +x script.sh

# Hacer directorio transitable
chmod +x ~/projects

# Directorios con escritura grupal
chmod -R g+w project/
```

---

## 6.2 Ejecutando Scripts Shell

### Métodos de Ejecución

```bash
# Método 1: Ejecución por ruta (necesita permiso de ejecución)
./script.sh

# Método 2: Usando bash (no necesita permiso de ejecución)
bash script.sh

# Método 3: Usando source (ejecuta en shell actual)
source script.sh
```

### ¿Cuándo Usar Cuál?

| Método | Cuándo Usar | Características |
|--------|-------------|-----------------|
| `./script.sh` | Ejecución estándar | necesita `chmod +x`, subshell |
| `bash script.sh` | Especificar shell | no necesita permiso de ejecución |
| `source script.sh` | Configurar entorno | ejecuta en shell actual |

### Diferencia Clave entre `source` y `./script`

```bash
# contenido de script.sh: export MY_VAR="hola"

# Ejecutar con ./
./script.sh
echo $MY_VAR  # Salida: (vacío) ← en subshell, variable perdida

# Ejecutar con source
source script.sh
echo $MY_VAR  # Salida: hola ← en shell actual, variable permanece
```

---

## 6.3 `export`: Variables de Entorno

```bash
# Establecer variable de entorno
export NAME="Alice"
export PATH="$PATH:/nuevo/directorio"

# Mostrar todas las variables de entorno
export

# Variables comunes
echo $HOME      # Directorio home
echo $USER      # Nombre de usuario
echo $PATH      # Ruta de búsqueda
echo $PWD       # Directorio actual
```

### Persistir Variables de Entorno

```bash
# Agregar a ~/.bashrc
echo 'export EDITOR=vim' >> ~/.bashrc

# Aplicar cambios
source ~/.bashrc
```

---

## 6.4 `source`: Cargando Archivos

Equivale a: directamente **pegar** el contenido del archivo en la posición actual y ejecutar.

### Usos Comunes

```bash
# Cargar entorno virtual
source venv/bin/activate

# Cargar archivo .env
source .env

# Cargar biblioteca
source ~/scripts/common.sh
```

### Práctico: Archivos de Configuración Modulares

```bash
# config.sh
export DB_HOST="localhost"
export DB_PORT="5432"

# Usar en otros scripts
source config.sh
psql -h $DB_HOST -p $DB_PORT
```

---

## 6.5 `env`: Gestión de Entorno

```bash
# Mostrar todas las variables de entorno
env

# Ejecutar con entorno limpio
env -i HOME=/tmp PATH=/bin sh

# Establecer variables y ejecutar
env VAR1=valor1 VAR2=valor2 ./mi_programa
```

### Encontrar Comandos

```bash
which python      # Encontrar ubicación del comando
type cd           # Encontrar builtins del shell
whereis gcc       # Encontrar todos los archivos relacionados
```

---

## 6.6 `sudo`: Elevar Privilegios

```bash
# Ejecutar como root
sudo rm /var/log/old.log

# Ejecutar como usuario específico
sudo -u postgres psql

# Mostrar qué puedes hacer
sudo -l
```

### Advertencia de Peligro

```bash
# ¡Nunca ejecutes esto!
sudo rm -rf /

# ¡Nunca hagas esto!
sudo curl http://sitio-desconocido.com | sh
```

---

## 6.7 Referencia Rápida

| Comando | Propósito | Indicadores Comunes |
|---------|-----------|---------------------|
| `chmod` | Cambiar permisos de archivo | `+x` agregar exec, `755` octal, `-R` recursivo |
| `chown` | Cambiar propietario | `usuario:grupo`, `-R` recursivo |
| `./script` | Ejecutar script (necesita x) | - |
| `bash script` | Ejecutar script (no necesita x) | - |
| `source` | Ejecutar en shell actual | - |
| `export` | Establecer variables de entorno | `-n` eliminar |
| `env` | Mostrar/gestionar entorno | `-i` limpiar |
| `sudo` | Ejecutar como root | `-u usuario` especificar usuario |

---

## 6.8 Ejercicios

1. Crea un script, establece permisos con `chmod 755`, luego ejecútalo
2. Ejecuta el mismo script de variable de entorno con `source` y `./`, observa la diferencia
3. Usa `env -i` para crear un entorno limpio, ejecuta `python --version`
4. Crea un archivo `.env`, usa `source` para cargar sus variables
