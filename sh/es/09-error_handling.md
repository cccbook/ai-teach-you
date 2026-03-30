# 9. Manejo de Errores

---

## 9.1 Por Que Es Importante el Manejo de Errores

Sin manejo de errores:
- Despues de que un comando falla, se continua con operaciones incorrectas
- Puede eliminar archivos equivocados
- Puede sobrescribir datos importantes
- Puede dejar el sistema en estado inconsistente

Con manejo de errores:
- Detener inmediatamente en caso de error
- Proporcionar mensajes de error significativos
- Limpiar antes de salir

---

## 9.2 Codigos de Salida

Cada comando devuelve un codigo de salida despues de ejecutarse:

- `0`: exito
- `non-zero`: fallo

```bash
# Verificar el codigo de salida del ultimo comando
ls /tmp
echo $?  # Salida: 0 (si fue exitoso)

ls /inexistente
echo $?  # Salida: 2 (si fallo)
```

---

## 9.3 `set -e`: Detener en Caso de Error

```bash
#!/bin/bash
set -e

mkdir -p respaldo
cp importante.txt respaldo/  # Si esto falla, el script se detiene aqui
rm importante.txt          # No llegara aqui
```

### Cuando Usarlo

Casi todos los scripts deberian usar `set -e`:
- Scripts de inicializacion
- Scripts de despliegue
- Scripts de pruebas automatizadas

---

## 9.4 `set -u`: Error en Variables No Definidas

```bash
#!/bin/bash
set -u

echo $variable_indefinida
# Salida: bash: variable_indefinida: variable sin asignar
```

### Uso Combinado

```bash
#!/bin/bash
set -euo pipefail

# -e: detener en error
# -u: error en variable no definida
# -o pipefail: la tuberia falla si cualquier comando falla
```

**Este es el encabezado estandar de scripts para IA!**

---

## 9.5 `trap`: Manejo Elegante de Errores

### Uso Basico

```bash
#!/bin/bash
set -euo pipefail

limpiar() {
    echo "Limpiando..."
    rm -f /tmp/archivo_temporal
}

trap limpiar EXIT

# Programa principal
echo "Iniciando proceso..."
```

### Capturar Errores

```bash
#!/bin/bash
set -euo pipefail

manejador_error() {
    local codigo_salida=$?
    echo "X El script fallo en la linea $1, codigo de salida: $codigo_salida"
    exit $codigo_salida
}

trap 'manejador_error $LINENO' ERR
```

---

## 9.6 Funciones Personalizadas de Error

```bash
#!/bin/bash
set -euo pipefail

morir() {
    echo "X $@" >&2
    exit 1
}

advertir() {
    echo "ADVERTENCIA: $@"
}

necesita_comando() {
    command -v "$1" &>/dev/null || morir "Comando requerido: $1"
}

necesita_archivo() {
    [[ -f "$1" ]] || morir "Archivo requerido: $1"
}
```

---

## 9.7 Referencia Rapida

| Comando | Descripcion |
|---------|-------------|
| `$?` | Codigo de salida del ultimo comando |
| `set -e` | Detener en error |
| `set -u` | Error en variable no definida |
| `set -o pipefail` | La tuberia falla si cualquier comando falla |
| `set -euo pipefail` | Combinado (recomendado) |
| `trap 'func' EXIT` | Ejecutar al salir |
| `trap 'func' ERR` | Ejecutar en error |
| `trap 'func' INT` | Ejecutar con Ctrl+C |
| `exit 1` | Salir con codigo de error 1 |

---

## 9.8 Ejercicios

1. Escribe un script con `set -euo pipefail` que muestre "Ocurrio un error" en caso de fallo
2. Crea una funcion `morir()` que imprima un mensaje y salga
3. Usa `trap` para mostrar "Adios" cuando el script termine
4. Escribe un script de despliegue con reversión automatica en caso de fallo
