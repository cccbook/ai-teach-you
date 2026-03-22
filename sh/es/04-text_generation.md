# 4. Generación y Escritura de Texto

---

## 4.1 Por Qué la IA No Necesita un Editor

El flujo de trabajo de la mayoría de los ingenieros humanos para escribir código:
1. Abrir editor (VS Code, Vim, Emacs...)
2. Escribir código
3. Guardar archivo
4. Cerrar editor

Para la IA:
```
"Escribir un programa Python" = generar algo de texto
"Guardar este programa en un archivo" = escribir texto en disco
```

El proceso de generación de código de la IA es un **proceso de generación de texto**. Así que la IA usa las herramientas de texto de Shell:

- `echo`: salida de una línea de texto
- `printf`: salida formateada
- `heredoc`: salida de texto multilínea (¡el más importante!)

---

## 4.2 `echo`: Salida Más Simple

### Uso Básico

```bash
# Salida de cadena
echo "¡Hola, Mundo!"

# Salida de variable
name="Alice"
echo "¡Hola, $name!"

# Salida de múltiples valores
echo "Hoy es $(date +%Y-%m-%d)"
```

### Trampas de `echo`

```bash
# echo agrega newline por defecto
echo -n "Cargando: "  # Sin newline
```

### Escribir Archivos con `echo`

```bash
# Sobrescribir
echo "¡Hola, Mundo!" > file.txt

# Agregar
echo "Segunda línea" >> file.txt
```

**Nota**: Usar `echo` para archivos multilínea es doloroso, así que la IA casi nunca lo usa para código. `heredoc` es la estrella.

---

## 4.3 `printf`: Salida Formateada Más Poderosa

### Comparación con `echo`

```bash
# printf soporta formato estilo C
printf "Valor: %.2f\n" 3.14159
# Salida: Valor: 3.14

printf "%s\t%s\n" "Nombre" "Edad"
```

### Crear Tablas

```bash
printf "%-15s %10s\n" "Nombre" "Precio"
printf "%-15s %10.2f\n" "iPhone" 999.99
printf "%-15s %10.2f\n" "MacBook" 1999.99
```

---

## 4.4 heredoc: El Arma Principal de la IA para Escribir Código

### ¿Qué es heredoc?

heredoc es una sintaxis especial de Shell para **salida de texto multilínea literalmente**.

```bash
cat << 'EOF'
Todo este contenido
será salida literalmente
incluyendo newlines, espacios
EOF
```

### Escribir Archivos (Uso Más Común de la IA)

```bash
cat > program.py << 'EOF'
#!/usr/bin/env python3

def hello(name):
    print(f"Hola, {name}!")

if __name__ == "__main__":
    hello("Mundo")
EOF
```

### ¿Por Qué Usar `'EOF'` (Comilla Simple)?

```bash
# Comilla simple EOF: no expandir nada
cat << 'EOF'
HOME es: $HOME
Hoy es: $(date)
EOF
# Salida: HOME es: $HOME (no expandido)

# Comilla doble EOF o sin comillas: expandirá
cat << EOF
HOME es: $HOME
EOF
# Salida: HOME es: /home/ai (expandido)
```

**Elección de la IA**: casi siempre usar `'EOF'` (comilla simple). Porque el código generalmente no necesita expansión de variables Shell.

---

## 4.5 La IA Escribe Varios Archivos con heredoc

### Escribir Programa Python

```bash
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""Punto de entrada principal"""

import sys
import os

def main():
    print("Proyecto Híbrido Python + C")
    print(f"Directorio de trabajo: {os.getcwd()}")

if __name__ == "__main__":
    main()
EOF
```

### Escribir Script Shell

```bash
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash
set -e

DEPLOY_HOST="server.example.com"

echo "🚀 Desplegando a $DEPLOY_HOST"
rsync -avz --delete ./dist/ "$DEPLOY_HOST:/var/www/app/"
ssh "$DEPLOY_HOST" "systemctl restart myapp"
echo "✅ ¡Despliegue completo!"
EOF

chmod +x scripts/deploy.sh
```

### Escribir Archivo de Configuración

```bash
cat > config.json << 'EOF'
{
    "site_name": "Mi Blog",
    "author": "Anónimo",
    "theme": "minimal"
}
EOF
```

### Escribir Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "http.server", "8000"]
EOF
```

---

## 4.6 Trampas de heredoc y Soluciones

### Trampa 1: Contiene Comillas Simples

```bash
# Problema: EOF con comilla simple no permite comillas simples
cat << 'EOF'
Él va a ir.
EOF
# Salida: error de sintaxis

# Solución: usar comilla doble EOF
cat << "EOF"
Él va a ir.
EOF
```

### Trampa 2: Contiene `$` (Pero No Quiere Expansión)

```bash
# Problema: EOF con comilla doble expande $
cat << "EOF"
El precio es $100
EOF
# Salida: El precio es (vacío)

# Solución: escapar individualmente
cat << "EOF"
El precio es $$100
EOF
# Salida: El precio es $100
```

---

## 4.7 Práctica: Construyendo un Proyecto Completo desde Cero

```bash
# 1. Crear estructura de directorios
mkdir -p myblog/{src,themes,content}

# 2. Crear archivo de configuración
cat > myblog/config.json << 'EOF'
{
    "site_name": "Mi Blog",
    "author": "Anónimo",
    "theme": "minimal"
}
EOF

# 3. Crear programa principal Python
cat > myblog/src/blog.py << 'EOF'
#!/usr/bin/env python3
"""Generador simple de blog"""
import json
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path) as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config()
    print(f"Generando: {config['site_name']}")
EOF

# 4. Crear script de compilación
cat > myblog/build.sh << 'EOF'
#!/bin/bash
set -e
echo "🔨 Construyendo blog..."
cd "$(dirname "$0")"
python3 src/blog.py
echo "✅ ¡Construcción completa!"
EOF

chmod +x myblog/build.sh

# 5. Verificar estructura
find myblog -type f | sort
```

---

## 4.8 Referencia Rápida

| Herramienta | Propósito | Ejemplo |
|------------|-----------|---------|
| `echo` | Salida de una línea | `echo "Hola"` |
| `echo -n` | Sin newline | `echo -n "Cargando..."` |
| `printf` | Salida formateada | `printf "%s: %d\n" "edad" 25` |
| `>` | Sobrescribir archivo | `echo "hola" > file.txt` |
| `>>` | Agregar a archivo | `echo "hola" >> file.txt` |
| `<< 'EOF'` | heredoc (sin expansión) | preferido para código |
| `<< "EOF"` | heredoc (expandir) | raramente usado |

---

## 4.9 Ejercicios

1. Crear una animación de Carga con `echo -n` y bucle `for`
2. Crear una tabla formateada (nombre, edad, trabajo) con `printf`
3. Escribir un programa Python de 20 líneas con heredoc
4. Escribir un docker-compose.yml con heredoc
