# 1. Wie die KI Shell verwendet

---

### 1.1 Projekthintergrund: Ein Python + C Hybridprojekt

Stellen Sie sich vor, Sie sind eine KI, die beauftragt wurde, einen hochperformanten HTTP-Client zu schreiben.

Ihre Strategie ist klar: Verwenden Sie **Python** für die obere Logikschicht (wartbar, erweiterbar), und verwenden Sie **C** für die performancekritische Netzwerkschicht (schnell, geringer Speicherverbrauch). Dann lässt Python C über `ctypes` aufrufen.

Dieses Projekt erfordert:
- Eine C-Datei (`curl.c`): implementiert hochperformantes HTTP GET
- Eine Python-Datei (`curl.py`): verpackt es in eine benutzerfreundliche API
- Ein Build-Skript: automatisiert den Kompilierungsprozess
- Testdateien: verifizieren die Funktionalität

In der Welt der KI beginnt alles mit einem einzigen `mkdir`-Befehl.

---

### 1.2 Shell verwenden, um Verzeichnisstrukturen zu erstellen

Wenn die KI ein neues Projekt startet, ist das erste nicht das Schreiben von Code, sondern das Aufbauen einer **sauberen Verzeichnisstruktur**.

```bash
mkdir -p curl-project/src
mkdir -p curl-project/include
mkdir -p curl-project/tests
mkdir -p curl-project/scripts
```

Warum verwendet die KI `mkdir -p`? Weil `-p` sicher ist:
- Wenn das Verzeichnis bereits existiert, kein Fehler
- Kann verschachtelte Verzeichnisse auf einmal erstellen

Menschliche Ingenieure machen oft den Fehler, `mkdir project` und `mkdir project/src` separat auszuführen, und sind dann verwirrt, wenn `src` nicht existiert. Die Gewohnheit der KI ist, **es gleich richtig zu machen**.

Jetzt schreibt die KI diese Befehle in ein `setup.sh`-Skript für die zukünftige Neuerstellung:

```bash
cat > setup.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_NAME="curl-project"

mkdir -p "$PROJECT_NAME/src"
mkdir -p "$PROJECT_NAME/include"
mkdir -p "$PROJECT_NAME/tests"
mkdir -p "$PROJECT_NAME/scripts"

echo "✓ Projektstruktur erstellt: $PROJECT_NAME/"
ls -la "$PROJECT_NAME"
EOF

chmod +x setup.sh
./setup.sh
```

Haben Sie es bemerkt? Die KI hat hier die `cat > file << 'EOF'`-Syntax verwendet - das ist **heredoc**, die Kerntechnik, die die KI verwendet, um Code ohne Editor zu schreiben. Wir werden dies in Kapitel 4 ausführlich untersuchen.

Ausgabe:

```
✓ Projektstruktur erstellt: curl-project/
total 8
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 curl-project/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/include/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/scripts/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:22 curl-project/src/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/tests/
```

---

### 1.3 C-Code mit heredoc schreiben

Jetzt schreibt die KI den Kern-C-Code. Für Menschen ist das Öffnen von Vim oder VS Code natürlich. Aber der Ansatz der KI ist:

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
        fprintf(stderr, "Memory allocation failed\n");
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
        fprintf(stderr, "CURL initialization failed\n");
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
        fprintf(stderr, "Request failed: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        free(chunk.data);
        return 1;
    }
    
    long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    printf("HTTP status code: %ld\n", response_code);
    
    *response = chunk.data;
    *len = chunk.size;
    
    curl_easy_cleanup(curl);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <URL>\n", argv[0]);
        return 1;
    }
    
    char *result = NULL;
    size_t len = 0;
    
    int status = fetch_url(argv[1], &result, &len);
    
    if (status == 0 && result) {
        printf("Response content (%zu bytes):\n%s\n", len, result);
        free(result);
    }
    
    return status;
}
EOF
```

**Was macht dieser Code?**

1. Verwendet libcurl zur Implementierung von HTTP-GET-Anfragen
2. Dynamische Speicherzuweisung zur Speicherung von Antwortinhalten
3. Implementiert eine Callback-Funktion zur Behandlung von Datenströmen
4. Stellt die `fetch_url()`-Funktion für externe Aufrufe bereit
5. Die `main()`-Funktion dient als Kommandozeilenwerkzeug

---

### 1.4 Python-Wrapper mit heredoc schreiben

Jetzt schreibt die KI die Python-Datei, um C aufzurufen:

```bash
cat > src/__init__.py << 'EOF'
"""
curl-py: Python + C Hybrid HTTP Client
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
            raise CurlError(f"Library not found: {lib_path}")
        
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
            raise CurlError(f"Request failed, error code: {result}")
        
        return response.value.decode('utf-8')
EOF
```

Dann eine benutzerfreundliche Schnittstelle schreiben:

```bash
cat > curl.py << 'EOF'
#!/usr/bin/env python3
"""
curl.py - Kommandozeilen-HTTP-Client
Verwendung: python curl.py <URL>
"""

from src import CurlFetcher, CurlError
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        fetcher = CurlFetcher()
        print(f"Requesting: {url}")
        content = fetcher.get(url)
        print(content)
    except CurlError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
EOF
```

---

### 1.5 C-Code mit gcc kompilieren

Die Kompilierung ist einer der sichtbarsten Schritte im Workflow der KI. Die KI macht es so:

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl -Wall -Wextra
```

**Warum schreibt die KI es so?**

- `-shared -fPIC`: erstellt positionsunabhängigen Code, generiert Shared Library
- `-O2`: Optimierungsstufe 2, verbessert die Ausführungseffizienz
- `-lcurl`: verlinkt libcurl-Bibliothek
- `-Wall -Wextra`: aktiviert alle Warnungen, vermeidet versteckte Probleme

Die KI verpackt dies in ein Build-Skript:

```bash
cat > scripts/build.sh << 'EOF'
#!/bin/bash
set -e

LIB_NAME="libcurl_ext.so"
SRC_FILE="src/curl.c"

echo "🔨 Compiling $SRC_FILE ..."

if ! command -v gcc &> /dev/null; then
    echo "Error: gcc not found, please install Xcode Command Line Tools"
    echo "Run: xcode-select --install"
    exit 1
fi

gcc -shared -fPIC -O2 \
    -o "$LIB_NAME" \
    "$SRC_FILE" \
    -lcurl \
    -Wall \
    -Wextra

if [ $? -eq 0 ]; then
    echo "✓ Build erfolgreich: $LIB_NAME"
    ls -lh "$LIB_NAME"
else
    echo "✗ Build fehlgeschlagen"
    exit 1
fi
EOF

chmod +x scripts/build.sh
./scripts/build.sh
```

---

### 1.6 Den gesamten Prozess mit Shell-Skript automatisieren

Dies ist das Wesen der KI: **sich wiederholende Arbeit automatisieren**.

```bash
cat > scripts/dev.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "  curl-project Entwicklungsumgebung"
echo "============================================"

echo ""
echo "🧹 Alte Dateien bereinigen..."
rm -f libcurl_ext.so
rm -rf __pycache__ src/__pycache__

echo ""
echo "🔨 C-Code kompilieren..."
./scripts/build.sh

if [ -f "libcurl_ext.so" ]; then
    echo ""
    echo "🧪 C-Programm testen..."
    gcc -o curl_test src/curl.c -lcurl 2>/dev/null && {
        ./curl_test https://httpbin.org/get || true
        rm -f curl_test
    } || echo "(C-Test überspringen, libcurl-dev fehlt)"
fi

echo ""
echo "🐍 Python-Wrapper testen..."
if [ -f "src/__init__.py" ]; then
    python3 -c "from src import CurlFetcher; print('✓ Python-Modul erfolgreich geladen')" 2>/dev/null || {
        echo "⚠ Python-Modultest erfordert zuerst C-Kompilierung"
    }
fi

echo ""
echo "============================================"
echo "  Bereit!"
echo "  Führen Sie 'python3 curl.py <URL>' aus, um zu starten"
echo "============================================"
EOF

chmod +x scripts/dev.sh
```

Ausführen:

```bash
./scripts/dev.sh
```

```
============================================
  curl-project Entwicklungsumgebung
============================================

🧹 Alte Dateien bereinigen...

🔨 C-Code kompilieren...
✓ Build erfolgreich: libcurl_ext.so
-rwxr-xr-x  1 ai  staff  45032 Mar 22 10:35 libcurl_ext.so

🐍 Python-Wrapper testen...
✓ Python-Modul erfolgreich geladen

============================================
  Bereit!
  Führen Sie 'python3 curl.py <URL>' aus, um zu starten
============================================
```

---

### 1.7 Debugging- und Korrektur-Workflow der KI

#### Ebene 1: Kompilierungsfehler

Angenommen, der erste C-Code der KI hat einen Syntaxfehler:

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl
```

Ausgabe:

```
src/curl.c:15:10: error: unknown type name 'size_t'
```

Die Reaktion der KI: **Sofort korrigieren**. Häufige Probleme:
- `#include <stdlib.h>` vergessen (`size_t`, `malloc`, `free`)
- `#include <string.h>` vergessen (`memcpy`)
- libcurl-Header-Pfad-Probleme

Die Korrektur ist einfach:

```bash
cat > src/curl.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
// ... vollständiger Inhalt ...
EOF
```

#### Ebene 2: Laufzeitfehler

Wenn das Programm kompiliert, aber nicht läuft:

```bash
./curl_test https://example.com
# Ausgabe: Request failed: Couldn't resolve host name
```

Die KI prüft:
1. Funktioniert das Netzwerk: `ping -c 1 8.8.8.8`
2. Ist DNS verfügbar: `nslookup example.com`
3. Blockiert die Firewall

#### Ebene 3: Logikfehler

Logikfehler sind am schwierigsten zu debuggen. Die Methode der KI ist **schrittweise Verifizierung**:

```bash
bash -x ./scripts/build.sh
```

Gibt jeden ausgeführten Befehl und Variablenwerte aus

#### Ebene 4: Speicherprobleme

Wenn das C-Programm Speicherlecks hat, schlägt die KI die Verwendung von `valgrind` vor:

```bash
valgrind --leak-check=full ./curl_test https://example.com
```

---

### 1.8 Vollständige Projektstruktur

```
curl-project/
├── src/
│   ├── curl.c           # C-Implementierung
│   └── __init__.py     # Python-Wrapper
├── include/            # C-Header (reserviert)
├── tests/              # Testdateien (reserviert)
├── scripts/
│   ├── setup.sh        # Verzeichnisse initialisieren
│   ├── build.sh        # Build-Skript
│   └── dev.sh          # Entwicklungsumgebung
├── libcurl_ext.so      # Build-Ausgabe
└── curl.py             # Kommandozeilenwerkzeug
```

---

### 1.9 Shell-Wichtige Erkenntnisse aus diesem Projekt

1. **`mkdir -p`**: Verzeichnisse sicher erstellen, unterstützt verschachtelte Strukturen
2. **`cat > file << 'EOF'`**: Dateien ohne Editor schreiben
3. **`chmod +x`**: Ausführungsberechtigung erteilen
4. **`set -e`**: Skript bei Befehlsfehler stoppen
5. **`&&` und `||`**: Bedingte Befehle kombinieren
6. **`gcc ...`**: Standard-C-Kompilierungsworkflow
7. **`bash -x`**: Skript Schritt für Schritt debuggen

---

### 1.10 Kapitelzusammenfassung

Wenn die KI Code schreibt, **verlässt sie das Terminal niemals**.

Von der Erstellung von Ordnerstrukturen, dem Schreiben von Code, dem Kompilieren, Ausführen bis zum Debuggen - alles auf einem schwarzen Bildschirm mit weißem Text erledigt. Keine VS-Code-Vorschläge, keine Mausklicks, kein WYSIWYG-Editor.

Das ist keine Einschränkung, das ist **Effizienz**.

Nach diesem Kapitel sollten Sie verstehen:
- Wie die KI einzelne Befehle verwendet, um Aufgaben zu erledigen
- Wie heredoc Shell zu einem "Textgenerator" macht
- Warum der Workflow der KI so schnell und wiederholbar ist

In den folgenden Kapiteln werden wir jeden Aspekt vertiefen, von Befehlen zu Skripten, vom Debugging zur Optimierung.
