# 12. Processamento em Lote de Arquivos

---

## 12.1 Renomeacao em Lote

### Substituicao Simples de Extensao

```bash
# Mudar todos .txt para .md
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

### Adicionar Prefixo

```bash
# Adicionar prefixo thumb_ a todas as imagens
for f in *.jpg *.png *.gif; do
    [[ -f "$f" ]] || continue
    mv "$f" "thumb_$f"
done
```

### Remover Espacos

```bash
# Substituir espacos em nomes de arquivo por sublinhados
for f in *\ *; do
    [[ -f "$f" ]] || continue
    mv "$f" "${f// /_}"
done
```

### Adicionar Numeros

```bash
# Numerar arquivos 001, 002, 003...
i=1
for f in *.jpg; do
    [[ -f "$f" ]] || continue
    mv "$f" "$(printf '%03d.jpg' $i)"
    ((i++))
done
```

---

## 12.2 Processamento de Imagens em Lote

```bash
#!/bin/bash
set -euo pipefail

TAMANHO=${1:-800}

for img in *.jpg *.png; do
    [[ -f "$img" ]] || continue
    
    echo "Processando: $img"
    
    if command -v convert &>/dev/null; then
        # Criar miniatura
        convert "$img" -resize "${TAMANHO}x${TAMANHO}>" "thumb_$img"
        
        # Criar versao grande
        convert "$img" -resize 1920x1080 "large_$img"
        
        echo "✓ Feito: thumb_$img, large_$img"
    fi
done
```

---

## 12.3 Busca e Substituicao em Lote

```bash
#!/bin/bash

# Substituir "foo" por "bar" em todos os arquivos .txt
for f in *.txt; do
    [[ -f "$f" ]] || continue
    sed -i.bak 's/foo/bar/g' "$f"
done
```

---

## 12.4 Compressao em Lote

```bash
#!/bin/bash

# Comprimir cada arquivo
for f in *.txt; do
    [[ -f "$f" ]] || continue
    gzip "$f"
done

# Descomprimir todos
gunzip *.gz
```

---

## 12.5 Download em Lote

```bash
#!/bin/bash
set -euo pipefail

while read -r url; do
    nome_arquivo=$(basename "$url")
    echo "Baixando: $url"
    curl -L -o "$nome_arquivo" "$url"
done < urls.txt
```

---

## 12.6 Referencia Rapida

| Tarefa | Comando |
|--------|---------|
| Mudar extensao | `mv "$f" "${f%.old}.new"` |
| Adicionar prefixo | `mv "$f" "prefixo_$f"` |
| Remover espacos | `mv "$f" "${f// /_}"` |
| Adicionar numeros | `mv "$f" "$(printf '%03d' $i)"` |
| Substituir em lote | `for f in *.txt; do sed -i 's/a/b/g' "$f"; done` |
| Comprimir em lote | `for f in *.txt; do gzip "$f"; done` |
| Baixar em lote | `while read url; do curl -LO "$url"; done < urls.txt` |

---

## 12.7 Exercicios

1. Renomear em lote 10 arquivos de `.txt` para `.md`
2. Adicionar prefixo `thumb_` a todas as imagens e criar miniaturas
3. Substituir `site-antigo.com` por `site-novo.com` em todos os arquivos `.html`
4. Criar um script de limpeza que delete todos os arquivos `__pycache__`, `.pyc` e `.log`
