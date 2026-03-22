# 1. Comment l'IA utilise Shell

## Un vrai projet de zéro

---

### 1.1 Contexte du projet : un projet hybride Python + C

Imaginez que vous êtes une IA chargée d'écrire un client HTTP haute performance.

Votre stratégie est claire : utiliser **Python** pour la couche supérieure (maintenable, extensible), et **C** pour la couche réseau critique en performances (rapide, faible mémoire). Ensuite, faire appel à C depuis Python via `ctypes`.

Ce projet nécessite :
- Un fichier C (`curl.c`) : implémente HTTP GET haute performance
- Un fichier Python (`curl.py`) : l'enveloppe dans une API conviviale
- Un script de compilation : automatise le processus de compilation
- Des fichiers de test : vérifie la fonctionnalité

Dans le monde de l'IA, tout commence par une simple commande `mkdir`.

---

### 1.2 Utiliser Shell pour créer la structure de répertoires

Quand l'IA démarre un nouveau projet, la première chose n'est pas d'écrire du code, mais d'établir une **structure de répertoires propre**.

```bash
mkdir -p curl-project/src
mkdir -p curl-project/include
mkdir -p curl-project/tests
mkdir -p curl-project/scripts
```

Pourquoi l'IA utilise-t-elle `mkdir -p` ? Parce que `-p` est sûr :
- Si le répertoire existe déjà, pas d'erreur
- Peut créer des répertoires imbriqués en une seule fois

Les ingénieurs humains font souvent l'erreur de lancer `mkdir project` et `mkdir project/src` séparément, puis sont confus quand `src` n'existe pas. L'habitude de l'IA est de **le faire correctement du premier coup**.

Maintenant, l'IA écrit ces commandes dans un script `setup.sh` pour une recreation future :

```bash
cat > setup.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_NAME="curl-project"

mkdir -p "$PROJECT_NAME/src"
mkdir -p "$PROJECT_NAME/include"
mkdir -p "$PROJECT_NAME/tests"
mkdir -p "$PROJECT_NAME/scripts"

echo "✓ Structure du projet créée : $PROJECT_NAME/"
ls -la "$PROJECT_NAME"
EOF

chmod +x setup.sh
./setup.sh
```

Avez-vous remarqué ? L'IA a utilisé la syntaxe `cat > fichier << 'EOF'` ici — c'est le **heredoc**, la technique fondamentale que l'IA utilise pour écrire du code sans éditeur. Nous explorerons cela en détail au Chapitre 4.

Sortie :

```
✓ Structure du projet créée : curl-project/
total 8
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 curl-project/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/include/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/scripts/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:22 curl-project/src/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/tests/
```

---

### 1.3 Écrire du code C avec heredoc

Maintenant, l'IA écrit le code C principal. Pour les humains, ouvrir Vim ou VS Code est naturel. Mais l'approche de l'IA est :

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
        fprintf(stderr, "Échec de l'allocation mémoire\n");
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
        fprintf(stderr, "Échec de l'initialisation CURL\n");
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
        fprintf(stderr, "Échec de la requête : %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        free(chunk.data);
        return 1;
    }
    
    long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    printf("Code de statut HTTP : %ld\n", response_code);
    
    *response = chunk.data;
    *len = chunk.size;
    
    curl_easy_cleanup(curl);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage : %s <URL>\n", argv[0]);
        return 1;
    }
    
    char *result = NULL;
    size_t len = 0;
    
    int status = fetch_url(argv[1], &result, &len);
    
    if (status == 0 && result) {
        printf("Contenu de la réponse (%zu octets) :\n%s\n", len, result);
        free(result);
    }
    
    return status;
}
EOF
```

**Que fait ce code ?**

1. Utilise libcurl pour implémenter les requêtes HTTP GET
2. Alloue dynamiquement la mémoire pour stocker le contenu de la réponse
3. Implémente une fonction de rappel pour gérer les flux de données
4. Fournit la fonction `fetch_url()` pour les appels externes
5. La fonction `main()` sert d'outil en ligne de commande

---

### 1.4 Écrire le wrapper Python avec heredoc

Maintenant, l'IA écrit le fichier Python pour appeler C :

```bash
cat > src/__init__.py << 'EOF'
"""
curl-py : Client HTTP hybride Python + C
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
            raise CurlError(f"Bibliothèque introuvable : {lib_path}")
        
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
            raise CurlError(f"Échec de la requête, code d'erreur : {result}")
        
        return response.value.decode('utf-8')
EOF
```

Puis écrire une interface pratique :

```bash
cat > curl.py << 'EOF'
#!/usr/bin/env python3
"""
curl.py - Client HTTP en ligne de commande
Utilisation : python curl.py <URL>
"""

from src import CurlFetcher, CurlError
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Utilisation : {sys.argv[0]} <URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        fetcher = CurlFetcher()
        print(f"Requête vers : {url}")
        content = fetcher.get(url)
        print(content)
    except CurlError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAnnulé", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
EOF
```

---

### 1.5 Compiler le code C avec gcc

La compilation est l'une des étapes les plus "visibles" du flux de travail de l'IA. L'IA fait comme ceci :

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl -Wall -Wextra
```

**Pourquoi l'IA l'écrit-elle ainsi ?**

- `-shared -fPIC` : crée du code indépendant de la position, génère une bibliothèque partagée
- `-O2` : optimisation de niveau 2, améliore l'efficacité d'exécution
- `-lcurl` : lie la bibliothèque libcurl
- `-Wall -Wextra` : active tous les avertissements, évite les problèmes cachés

L'IA enveloppe ceci dans un script de compilation :

```bash
cat > scripts/build.sh << 'EOF'
#!/bin/bash
set -e

LIB_NAME="libcurl_ext.so"
SRC_FILE="src/curl.c"

echo "🔨 Compilation de $SRC_FILE ..."

if ! command -v gcc &> /dev/null; then
    echo "Erreur : gcc introuvable, veuillez installer Xcode Command Line Tools"
    echo "Exécuter : xcode-select --install"
    exit 1
fi

gcc -shared -fPIC -O2 \
    -o "$LIB_NAME" \
    "$SRC_FILE" \
    -lcurl \
    -Wall \
    -Wextra

if [ $? -eq 0 ]; then
    echo "✓ Build réussi : $LIB_NAME"
    ls -lh "$LIB_NAME"
else
    echo "✗ Build échoué"
    exit 1
fi
EOF

chmod +x scripts/build.sh
./scripts/build.sh
```

---

### 1.6 Automatiser tout le processus avec un script Shell

C'est l'essence de l'IA : **automatiser le travail répétitif**.

```bash
cat > scripts/dev.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "  curl-project Environnement de Développement"
echo "============================================"

echo ""
echo "🧹 Nettoyage des anciens fichiers..."
rm -f libcurl_ext.so
rm -rf __pycache__ src/__pycache__

echo ""
echo "🔨 Compilation du code C..."
./scripts/build.sh

if [ -f "libcurl_ext.so" ]; then
    echo ""
    echo "🧪 Test du programme C..."
    gcc -o curl_test src/curl.c -lcurl 2>/dev/null && {
        ./curl_test https://httpbin.org/get || true
        rm -f curl_test
    } || echo "(Test C ignoré, libcurl-dev manquant)"
fi

echo ""
echo "🐍 Test du wrapper Python..."
if [ -f "src/__init__.py" ]; then
    python3 -c "from src import CurlFetcher; print('✓ Module Python chargé avec succès')" 2>/dev/null || {
        echo "⚠ Le test du module Python nécessite d'abord la compilation C"
    }
fi

echo ""
echo "============================================"
echo "  Prêt !"
echo "  Exécutez 'python3 curl.py <URL>' pour démarrer"
echo "============================================"
EOF

chmod +x scripts/dev.sh
```

Exécuter :

```bash
./scripts/dev.sh
```

```
============================================
  curl-project Environnement de Développement
============================================

🧹 Nettoyage des anciens fichiers...

🔨 Compilation du code C...
✓ Build réussi : libcurl_ext.so
-rwxr-xr-x  1 ai  staff  45032 Mar 22 10:35 libcurl_ext.so

🐍 Test du wrapper Python...
✓ Module Python chargé avec succès

============================================
  Prêt !
  Exécutez 'python3 curl.py <URL>' pour démarrer
============================================
```

---

### 1.7 Flux de travail de débogage et correction de l'IA

#### Couche 1 : Erreurs de compilation

Supposez que le premier code C de l'IA contient une erreur de syntaxe :

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl
```

Sortie :

```
src/curl.c:15:10: error: unknown type name 'size_t'
```

Réponse de l'IA : **Corriger immédiatement**. Problèmes courants :
- Oubli de `#include <stdlib.h>` (`size_t`, `malloc`, `free`)
- Oubli de `#include <string.h>` (`memcpy`)
- Problèmes de chemin d'accès au header libcurl

La correction est simple :

```bash
cat > src/curl.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
// ... contenu complet ...
EOF
```

#### Couche 2 : Erreurs d'exécution

Si le programme compile mais échoue à l'exécution :

```bash
./curl_test https://example.com
# Sortie : Échec de la requête : Impossible de résoudre le nom d'hôte
```

L'IA vérifie :
1. Le réseau fonctionne : `ping -c 1 8.8.8.8`
2. Le DNS est disponible : `nslookup example.com`
3. Le pare-feu bloque

#### Couche 3 : Erreurs de logique

Les erreurs de logique sont les plus difficiles à déboguer. La méthode de l'IA est la **vérification étape par étape** :

```bash
bash -x ./scripts/build.sh
```

Affiche chaque commande exécutée et les valeurs des variables

#### Couche 4 : Problèmes de mémoire

Si le programme C a des fuites mémoire, l'IA suggère d'utiliser `valgrind` :

```bash
valgrind --leak-check=full ./curl_test https://example.com
```

---

### 1.8 Structure complète du projet

```
curl-project/
├── src/
│   ├── curl.c           # Implémentation C
│   └── __init__.py     # Wrapper Python
├── include/             # Headers C (réservé)
├── tests/               # Fichiers de test (réservé)
├── scripts/
│   ├── setup.sh        # Initialisation des répertoires
│   ├── build.sh         # Script de compilation
│   └── dev.sh           # Environnement de développement
├── libcurl_ext.so       # Sortie de compilation
└── curl.py              # Outil en ligne de commande
```

---

### 1.9 Points clés sur Shell à retenir de ce projet

1. **`mkdir -p`** : créer des répertoires en toute sécurité, prend en charge les structures imbriquées
2. **`cat > fichier << 'EOF'`** : écrire des fichiers sans éditeur
3. **`chmod +x`** : donner la permission d'exécution
4. **`set -e`** : arrêter le script en cas d'échec de commande
5. **`&&` et `||`** : combiner des commandes conditionnelles
6. **`gcc ...`** : flux de travail standard de compilation C
7. **`bash -x`** : déboguer le script étape par étape

---

### 1.10 Résumé du chapitre

Quand l'IA écrit du code, elle **ne quitte jamais le Terminal**.

De la création des structures de dossiers, à l'écriture du code, la compilation, l'exécution, jusqu'au débogage — tout se fait dans un écran noir avec du texte blanc. Pas de suggestions VS Code, pas de clics de souris, pas d'éditeur WYSIWYG.

Ce n'est pas une limitation, c'est **l'efficacité**.

Après avoir lu ce chapitre, vous devriez comprendre :
- Comment l'IA utilise des commandes uniques pour accomplir des tâches
- Comment heredoc fait de Shell un "générateur de texte"
- Pourquoi le flux de travail de l'IA est si rapide et reproductible

Dans les chapitres suivants, nous approfondirons chaque aspect, des commandes aux scripts, du débogage à l'optimisation.
