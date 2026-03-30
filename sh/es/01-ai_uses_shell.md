# 1. Cómo la IA usa Shell

## Un Proyecto Real desde Cero

---

### 1.1 Antecedentes del Proyecto: Un Proyecto Híbrido Python + C

Imagina que eres una IA tasked con escribir un cliente HTTP de alto rendimiento.

Tu estrategia es clara: usar **Python** para la lógica de la capa superior (mantenible, extensible), y usar **C** para la capa de red crítica de rendimiento (rápido, bajo consumo de memoria). Luego dejar que Python llame a C mediante `ctypes`.

Este proyecto requiere:
- Un archivo C (`curl.c`): implementa HTTP GET de alto rendimiento
- Un archivo Python (`curl.py`): lo envuelve en una API fácil de usar
- Un script de compilación: automatiza el proceso de compilación
- Archivos de prueba: verifican la funcionalidad

En el mundo de la IA, todo comienza con un simple comando `mkdir`.

---

### 1.2 Usando Shell para Crear la Estructura de Directorios

Cuando la IA inicia un nuevo proyecto, lo primero no es escribir código, sino establecer una **estructura de directorios limpia**.

```bash
mkdir -p curl-project/src
mkdir -p curl-project/include
mkdir -p curl-project/tests
mkdir -p curl-project/scripts
```

¿Por qué la IA usa `mkdir -p`? Porque `-p` es seguro:
- Si el directorio ya existe, no genera error
- Puede crear directorios anidados de una sola vez

Los ingenieros humanos a menudo cometen el error de ejecutar `mkdir project` y `mkdir project/src` por separado, y luego se confunden cuando `src` no existe. El hábito de la IA es **hacerlo bien la primera vez**.

Ahora la IA escribe estos comandos en un script `setup.sh` para recrearlo en el futuro:

```bash
cat > setup.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_NAME="curl-project"

mkdir -p "$PROJECT_NAME/src"
mkdir -p "$PROJECT_NAME/include"
mkdir -p "$PROJECT_NAME/tests"
mkdir -p "$PROJECT_NAME/scripts"

echo "✓ Estructura del proyecto creada: $PROJECT_NAME/"
ls -la "$PROJECT_NAME"
EOF

chmod +x setup.sh
./setup.sh
```

¿Notaste? La IA usó la sintaxis `cat > file << 'EOF'` aquí—esto es **heredoc**, la técnica central que la IA usa para escribir código sin un editor. Exploraremos esto en profundidad en el Capítulo 4.

Salida:

```
✓ Estructura del proyecto creada: curl-project/
total 8
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 curl-project/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/include/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/scripts/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:22 curl-project/src/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/tests/
```

---

### 1.3 Escribiendo Código C con heredoc

Ahora la IA escribe el código C principal. Para los humanos, abrir Vim o VS Code es natural. Pero el enfoque de la IA es:

```bash
cat > src/curl.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

struct MemoryBuffer {
    char *data;
    size_t size;
};

static size_t write_callback(void *contents, size_t size, 
                             size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryBuffer *mem = (struct MemoryBuffer *)userp;
    
    char *ptr = realloc(mem->data, mem->size + realsize + 1);
    if (!ptr) {
        fprintf(stderr, "Error en asignación de memoria\n");
        return 0;
    }
    
    mem->data = ptr;
    memcpy(&(mem->data[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->data[mem->size] = 0;
    
    return realsize;
}

int fetch_url(const char *url, char **response, size_t *len) {
    CURL *curl;
    CURLcode res;
    struct MemoryBuffer chunk;
    
    chunk.data = malloc(1);
    chunk.size = 0;
    
    curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "Error en inicialización de CURL\n");
        free(chunk.data);
        return 1;
    }
    
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);
    
    res = curl_easy_perform(curl);
    
    if (res != CURLE_OK) {
        fprintf(stderr, "Solicitud fallida: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        free(chunk.data);
        return 1;
    }
    
    long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    printf("Código de estado HTTP: %ld\n", response_code);
    
    *response = chunk.data;
    *len = chunk.size;
    
    curl_easy_cleanup(curl);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <URL>\n", argv[0]);
        return 1;
    }
    
    char *result = NULL;
    size_t len = 0;
    
    int status = fetch_url(argv[1], &result, &len);
    
    if (status == 0 && result) {
        printf("Contenido de respuesta (%zu bytes):\n%s\n", len, result);
        free(result);
    }
    
    return status;
}
EOF
```

**¿Qué hace este código?**

1. Usa libcurl para implementar solicitudes HTTP GET
2. Asigna memoria dinámicamente para almacenar el contenido de la respuesta
3. Implementa una función de callback para manejar flujos de datos
4. Proporciona la función `fetch_url()` para llamadas externas
5. La función `main()` sirve como herramienta de línea de comandos

---

### 1.4 Escribiendo el Wrapper de Python con heredoc

Ahora la IA escribe el archivo Python para llamar a C:

```bash
cat > src/__init__.py << 'EOF'
"""
curl-py: Cliente HTTP Híbrido Python + C
"""

import ctypes
import os
from pathlib import Path

class CurlError(Exception):
    pass

class CurlFetcher:
    def __init__(self, lib_path=None):
        if lib_path is None:
            base_dir = Path(__file__).parent
            lib_path = base_dir / "libcurl_ext.so"
        
        if not os.path.exists(lib_path):
            raise CurlError(f"Biblioteca no encontrada: {lib_path}")
        
        self.lib = ctypes.CDLL(str(lib_path))
        self.lib.fetch_url.argtypes = [ctypes.c_char_p, 
                                       ctypes.POINTER(ctypes.c_char_p),
                                       ctypes.POINTER(ctypes.c_size_t)]
        self.lib.fetch_url.restype = ctypes.c_int
    
    def get(self, url):
        response = ctypes.c_char_p()
        length = ctypes.c_size_t()
        
        if isinstance(url, str):
            url = url.encode('utf-8')
        
        result = self.lib.fetch_url(url, ctypes.byref(response), 
                                     ctypes.byref(length))
        
        if result != 0:
            raise CurlError(f"Solicitud fallida, código de error: {result}")
        
        return response.value.decode('utf-8')
EOF
```

Luego escribir una interfaz conveniente:

```bash
cat > curl.py << 'EOF'
#!/usr/bin/env python3
"""
curl.py - Cliente HTTP de Línea de Comandos
Uso: python curl.py <URL>
"""

from src import CurlFetcher, CurlError
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        fetcher = CurlFetcher()
        print(f"Solicitando: {url}")
        content = fetcher.get(url)
        print(content)
    except CurlError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelado", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
EOF
```

---

### 1.5 Compilando Código C con gcc

La compilación es uno de los pasos más "visibles" en el flujo de trabajo de la IA. La IA lo hace así:

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl -Wall -Wextra
```

**¿Por qué la IA lo escribe así?**

- `-shared -fPIC`: crea código independiente de posición, genera biblioteca compartida
- `-O2`: optimización nivel 2, mejora la eficiencia de ejecución
- `-lcurl`: enlaza la biblioteca libcurl
- `-Wall -Wextra`: activa todas las advertencias, evita problemas ocultos

La IA lo envuelve en un script de compilación:

```bash
cat > scripts/build.sh << 'EOF'
#!/bin/bash
set -e

LIB_NAME="libcurl_ext.so"
SRC_FILE="src/curl.c"

echo "🔨 Compilando $SRC_FILE ..."

if ! command -v gcc &> /dev/null; then
    echo "Error: gcc no encontrado, por favor instale Xcode Command Line Tools"
    echo "Ejecute: xcode-select --install"
    exit 1
fi

gcc -shared -fPIC -O2 \
    -o "$LIB_NAME" \
    "$SRC_FILE" \
    -lcurl \
    -Wall \
    -Wextra

if [ $? -eq 0 ]; then
    echo "✓ Compilación exitosa: $LIB_NAME"
    ls -lh "$LIB_NAME"
else
    echo "✗ Compilación fallida"
    exit 1
fi
EOF

chmod +x scripts/build.sh
./scripts/build.sh
```

---

### 1.6 Automatizando Todo el Proceso con Script Shell

Esta es la esencia de la IA: **automatizar el trabajo repetitivo**.

```bash
cat > scripts/dev.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "  curl-project Entorno de Desarrollo"
echo "============================================"

echo ""
echo "🧹 Limpiando archivos antiguos..."
rm -f libcurl_ext.so
rm -rf __pycache__ src/__pycache__

echo ""
echo "🔨 Compilando código C..."
./scripts/build.sh

if [ -f "libcurl_ext.so" ]; then
    echo ""
    echo "🧪 Probando programa C..."
    gcc -o curl_test src/curl.c -lcurl 2>/dev/null && {
        ./curl_test https://httpbin.org/get || true
        rm -f curl_test
    } || echo "(Saltando prueba C, falta libcurl-dev)"
fi

echo ""
echo "🐍 Probando wrapper Python..."
if [ -f "src/__init__.py" ]; then
    python3 -c "from src import CurlFetcher; print('✓ Módulo Python cargado exitosamente')" 2>/dev/null || {
        echo "⚠ La prueba del módulo Python requiere compilación C primero"
    }
fi

echo ""
echo "============================================"
echo "  ¡Listo!"
echo "  Ejecute 'python3 curl.py <URL>' para comenzar"
echo "============================================"
EOF

chmod +x scripts/dev.sh
```

Ejecutarlo:

```bash
./scripts/dev.sh
```

```
============================================
  curl-project Entorno de Desarrollo
============================================

🧹 Limpiando archivos antiguos...

🔨 Compilando código C...
✓ Compilación exitosa: libcurl_ext.so
-rwxr-xr-x  1 ai  staff  45032 Mar 22 10:35 libcurl_ext.so

🐍 Probando wrapper Python...
✓ Módulo Python cargado exitosamente

============================================
  ¡Listo!
  Ejecute 'python3 curl.py <URL>' para comenzar
============================================
```

---

### 1.7 Flujo de Trabajo de Depuración y Corrección de la IA

#### Nivel 1: Errores de Compilación

Supongamos que el primer código C de la IA tiene un error de sintaxis:

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl
```

Salida:

```
src/curl.c:15:10: error: tipo desconocido 'size_t'
```

Respuesta de la IA: **Corregir inmediatamente**. Problemas comunes:
- Olvidó `#include <stdlib.h>` (`size_t`, `malloc`, `free`)
- Olvidó `#include <string.h>` (`memcpy`)
- Problemas de ruta del header de libcurl

La corrección es simple:

```bash
cat > src/curl.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
// ... contenido completo ...
EOF
```

#### Nivel 2: Errores de Ejecución

Si el programa compila pero falla al ejecutarse:

```bash
./curl_test https://example.com
# Salida: Solicitud fallida: No se pudo resolver el nombre del host
```

La IA verifica:
1. ¿La red funciona: `ping -c 1 8.8.8.8`
2. ¿DNS disponible: `nslookup example.com`
3. ¿El firewall está bloqueando

#### Nivel 3: Errores de Lógica

Los errores de lógica son los más difíciles de depurar. El método de la IA es **verificación paso a paso**:

```bash
bash -x ./scripts/build.sh
```

Muestra cada comando ejecutado y los valores de las variables

#### Nivel 4: Problemas de Memoria

Si el programa C tiene fugas de memoria, la IA sugiere usar `valgrind`:

```bash
valgrind --leak-check=full ./curl_test https://example.com
```

---

### 1.8 Estructura Completa del Proyecto

```
curl-project/
├── src/
│   ├── curl.c           # Implementación C
│   └── __init__.py     # Wrapper Python
├── include/            # Headers C (reservado)
├── tests/              # Archivos de prueba (reservado)
├── scripts/
│   ├── setup.sh        # Inicializar directorios
│   ├── build.sh        # Script de compilación
│   └── dev.sh          # Entorno de desarrollo
├── libcurl_ext.so      # Resultado de compilación
└── curl.py             # Herramienta de línea de comandos
```

---

### 1.9 Puntos Clave de Shell de Este Proyecto

1. **`mkdir -p`**: crear directorios de forma segura, soporta estructura anidada
2. **`cat > file << 'EOF'`**: escribir archivos sin un editor
3. **`chmod +x`**: dar permiso de ejecución
4. **`set -e`**: detener script ante cualquier fallo de comando
5. **`&&` y `||`**: combinar comandos condicionales
6. **`gcc ...`**: flujo de trabajo estándar de compilación C
7. **`bash -x`**: depurar script paso a paso

---

### 1.10 Resumen del Capítulo

Cuando la IA escribe código, **nunca abandona la Terminal**.

Desde crear estructuras de carpetas, escribir código, compilar, ejecutar, hasta depurar—todo hecho en una pantalla negra con texto blanco. Sin sugerencias de VS Code, sin clics de ratón, sin editor WYSIWYG.

Esto no es una limitación, esto es **eficiencia**.

Después de leer este capítulo, deberías entender:
- Cómo la IA usa comandos individuales para completar tareas
- Cómo heredoc convierte a Shell en un "generador de texto"
- Por qué el flujo de trabajo de la IA es tan rápido y repetible

En los siguientes capítulos, profundizaremos en cada aspecto, desde comandos hasta scripts, desde depuración hasta optimización.
