# 1. Como a IA Usa o Shell

## Um Projeto Real do Zero

---

### 1.1 Contexto do Projeto: Um Projeto Híbrido Python + C

Imagine que você é uma IA tasked with writing a high-performance HTTP client.

Sua estratégia é clara: usar **Python** para a lógica da camada superior (manutenível, extensível), e usar **C** para a camada de rede crítica de desempenho (rápida, baixa memória). Então fazer o Python chamar C via `ctypes`.

Este projeto requer:
- Um arquivo C (`curl.c`): implementa HTTP GET de alto desempenho
- Um arquivo Python (`curl.py`): envolve em uma API amigável
- Um script de build: automatiza o processo de compilação
- Arquivos de teste: verificam a funcionalidade

No mundo da IA, tudo começa com um único comando `mkdir`.

---

### 1.2 Usando Shell para Criar Estrutura de Diretórios

Quando a IA inicia um novo projeto, a primeira coisa não é escrever código, mas estabelecer uma **estrutura de diretórios limpa**.

```bash
mkdir -p curl-project/src
mkdir -p curl-project/include
mkdir -p curl-project/tests
mkdir -p curl-project/scripts
```

Por que a IA usa `mkdir -p`? Porque `-p` é seguro:
- Se o diretório já existe, nenhum erro
- Pode criar diretórios aninhados de uma vez

Engenheiros humanos frequentemente cometem o erro de executar `mkdir project` e `mkdir project/src` separadamente, e depois ficam confusos quando `src` não existe. O hábito da IA é **fazer certo da primeira vez**.

Agora a IA escreve esses comandos em um script `setup.sh` para recriação futura:

```bash
cat > setup.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_NAME="curl-project"

mkdir -p "$PROJECT_NAME/src"
mkdir -p "$PROJECT_NAME/include"
mkdir -p "$PROJECT_NAME/tests"
mkdir -p "$PROJECT_NAME/scripts"

echo "✓ Estrutura do projeto criada: $PROJECT_NAME/"
ls -la "$PROJECT_NAME"
EOF

chmod +x setup.sh
./setup.sh
```

Você notou? A IA usou a sintaxe `cat > arquivo << 'EOF'` aqui—isso é **heredoc**, a técnica central que a IA usa para escrever código sem um editor. Vamos explorar isso profundamente no Capítulo 4.

Saída:

```
✓ Estrutura do projeto criada: curl-project/
total 8
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 curl-project/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/include/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/scripts/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:22 curl-project/src/
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 curl-project/tests/
```

---

### 1.3 Escrevendo Código C com heredoc

Agora a IA escreve o código C central. Para humanos, abrir Vim ou VS Code é natural. Mas a abordagem da IA é:

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
        fprintf(stderr, "Falha na alocação de memória\n");
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
        fprintf(stderr, "Falha na inicialização do CURL\n");
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
        fprintf(stderr, "Requisição falhou: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        free(chunk.data);
        return 1;
    }
    
    long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    printf("Código de status HTTP: %ld\n", response_code);
    
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
        printf("Conteúdo da resposta (%zu bytes):\n%s\n", len, result);
        free(result);
    }
    
    return status;
}
EOF
```

**O que este código faz?**

1. Usa libcurl para implementar requisições HTTP GET
2. Aloca memória dinamicamente para armazenar conteúdo da resposta
3. Implementa uma função de callback para lidar com fluxos de dados
4. Fornece função `fetch_url()` para chamadas externas
5. Função `main()` serve como ferramenta de linha de comando

---

### 1.4 Escrevendo Wrapper Python com heredoc

Agora a IA escreve o arquivo Python para chamar C:

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
            raise CurlError(f"Biblioteca não encontrada: {lib_path}")
        
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
            raise CurlError(f"Requisição falhou, código de erro: {result}")
        
        return response.value.decode('utf-8')
EOF
```

Então escreve uma interface conveniente:

```bash
cat > curl.py << 'EOF'
#!/usr/bin/env python3
"""
curl.py - Cliente HTTP de Linha de Comando
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
        print(f"Requisição: {url}")
        content = fetcher.get(url)
        print(content)
    except CurlError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelado", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
EOF
```

---

### 1.5 Compilando Código C com gcc

Compilação é um dos passos mais "visíveis" no fluxo de trabalho da IA. A IA faz assim:

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl -Wall -Wextra
```

**Por que a IA escreve assim?**

- `-shared -fPIC`: cria código independente de posição, gera biblioteca compartilhada
- `-O2`: otimização nível 2, melhora eficiência de execução
- `-lcurl`: vincula biblioteca libcurl
- `-Wall -Wextra`: habilita todos os avisos, evita problemas ocultos

A IA envolve isso em um script de build:

```bash
cat > scripts/build.sh << 'EOF'
#!/bin/bash
set -e

LIB_NAME="libcurl_ext.so"
SRC_FILE="src/curl.c"

echo "🔨 Compilando $SRC_FILE ..."

if ! command -v gcc &> /dev/null; then
    echo "Erro: gcc não encontrado, por favor instale Xcode Command Line Tools"
    echo "Execute: xcode-select --install"
    exit 1
fi

gcc -shared -fPIC -O2 \
    -o "$LIB_NAME" \
    "$SRC_FILE" \
    -lcurl \
    -Wall \
    -Wextra

if [ $? -eq 0 ]; then
    echo "✓ Build bem-sucedido: $LIB_NAME"
    ls -lh "$LIB_NAME"
else
    echo "✗ Build falhou"
    exit 1
fi
EOF

chmod +x scripts/build.sh
./scripts/build.sh
```

---

### 1.6 Automatizando Todo o Processo com Script Shell

Esta é a essência da IA: **automatizar trabalho repetitivo**.

```bash
cat > scripts/dev.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "  curl-project Ambiente de Desenvolvimento"
echo "============================================"

echo ""
echo "🧹 Limpando arquivos antigos..."
rm -f libcurl_ext.so
rm -rf __pycache__ src/__pycache__

echo ""
echo "🔨 Compilando código C..."
./scripts/build.sh

if [ -f "libcurl_ext.so" ]; then
    echo ""
    echo "🧪 Testando programa C..."
    gcc -o curl_test src/curl.c -lcurl 2>/dev/null && {
        ./curl_test https://httpbin.org/get || true
        rm -f curl_test
    } || echo "(Pulando teste C, faltando libcurl-dev)"
fi

echo ""
echo "🐍 Testando wrapper Python..."
if [ -f "src/__init__.py" ]; then
    python3 -c "from src import CurlFetcher; print('✓ Módulo Python carregado com sucesso')" 2>/dev/null || {
        echo "⚠ Teste do módulo Python requer compilação C primeiro"
    }
fi

echo ""
echo "============================================"
echo "  Pronto!"
echo "  Execute 'python3 curl.py <URL>' para começar"
echo "============================================"
EOF

chmod +x scripts/dev.sh
```

Execute:

```bash
./scripts/dev.sh
```

```
============================================
  curl-project Ambiente de Desenvolvimento
============================================

🧹 Limpando arquivos antigos...

🔨 Compilando código C...
✓ Build bem-sucedido: libcurl_ext.so
-rwxr-xr-x  1 ai  staff  45032 Mar 22 10:35 libcurl_ext.so

🐍 Testando wrapper Python...
✓ Módulo Python carregado com sucesso

============================================
  Pronto!
  Execute 'python3 curl.py <URL>' para começar
============================================
```

---

### 1.7 Fluxo de Trabalho de Depuração e Correção da IA

#### Camada 1: Erros de Compilação

Suponha que o primeiro código C da IA tenha um erro de sintaxe:

```bash
gcc -shared -fPIC -o libcurl_ext.so src/curl.c -lcurl
```

Saída:

```
src/curl.c:15:10: error: unknown type name 'size_t'
```

Resposta da IA: **Corrigir imediatamente**. Problemas comuns:
- Esqueceu `#include <stdlib.h>` (`size_t`, `malloc`, `free`)
- Esqueceu `#include <string.h>` (`memcpy`)
- Problemas de caminho do header do libcurl

Correção é simples:

```bash
cat > src/curl.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
// ... conteúdo completo ...
EOF
```

#### Camada 2: Erros de Execução

Se o programa compila mas falha ao executar:

```bash
./curl_test https://example.com
# Saída: Request failed: Couldn't resolve host name
```

IA verifica:
1. Rede está funcionando: `ping -c 1 8.8.8.8`
2. DNS disponível: `nslookup example.com`
3. Firewall bloqueando

#### Camada 3: Erros de Lógica

Erros de lógica são os mais difíceis de depurar. O método da IA é **verificação passo a passo**:

```bash
bash -x ./scripts/build.sh
```

Mostra cada comando executado e valores de variáveis

#### Camada 4: Problemas de Memória

Se o programa C tem vazamentos de memória, IA sugere usar `valgrind`:

```bash
valgrind --leak-check=full ./curl_test https://example.com
```

---

### 1.8 Estrutura Completa do Projeto

```
curl-project/
├── src/
│   ├── curl.c           # Implementação C
│   └── __init__.py     # Wrapper Python
├── include/            # Headers C (reservado)
├── tests/              # Arquivos de teste (reservado)
├── scripts/
│   ├── setup.sh        # Inicializar diretórios
│   ├── build.sh        # Script de build
│   └── dev.sh          # Ambiente de desenvolvimento
├── libcurl_ext.so      # Saída do build
└── curl.py             # Ferramenta de linha de comando
```

---

### 1.9 Conclusões Chave do Shell deste Projeto

1. **`mkdir -p`**: criar diretórios com segurança, suporta estrutura aninhada
2. **`cat > arquivo << 'EOF'`**: escrever arquivos sem um editor
3. **`chmod +x`**: dar permissão de execução
4. **`set -e`**: parar script em qualquer falha de comando
5. **`&&` e `||`**: combinar comandos condicionais
6. **`gcc ...`**: fluxo de trabalho padrão de compilação C
7. **`bash -x`**: depurar script passo a passo

---

### 1.10 Resumo do Capítulo

Quando a IA escreve código, ela **nunca sai do Terminal**.

Desde criar estruturas de pastas, escrever código, compilar, executar, até depurar—tudo feito em uma tela preta com texto branco. Sem sugestões do VS Code, sem cliques de mouse, sem editor WYSIWYG.

Isso não é uma limitação, isso é **eficiência**.

Após ler este capítulo, você deve entender:
- Como a IA usa comandos únicos para realizar tarefas
- Como heredoc faz do Shell um "gerador de texto"
- Por que o fluxo de trabalho da IA é tão rápido e repetível

Nos capítulos seguintes, vamos mergulhar profundamente em cada aspecto, de comandos a scripts, de depuração a otimização.
