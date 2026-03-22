# 19. Modo de Colaboração IA + Shell

---

## 19.1 Nova Forma de Colaboração Humano-Máquina

Programação tradicional:
- Humanos digitam com teclado
- Humans usam mouse para operar IDE
- Humanos executam e testam

Programação na era da IA:
- Humanos descrevem requisitos
- IA gera comandos e scripts Shell
- Humanos revisam e executam
- Humanos e IA depuram juntos

---

## 19.2 Descrevendo Requisitos para a IA

### Descrições Boas

```bash
# Tarefa clara
"Encontrar todos os arquivos .log maiores que 100MB em /var/log"

# Incluir formato de saída esperado
"Listar todos os arquivos .py, mostrando: line_count filename por linha"

# Declarar restrições
"Compactar todos os arquivos .txt, mas pular qualquer um contendo 'test'"
```

### Descrições Ruins

```bash
# Muito vago
"me ajude a processar logs"

# Irrealista
"me ajude a escrever um sistema operacional"
```

---

## 19.3 Padrões de Comandos Shell Gerados pela IA

### Padrão 1: Comando Único

```bash
# Humano pergunta: encontrar top 10 arquivos Python com mais linhas
find . -name "*.py" -exec wc -l {} + | sort -rn | head -10
```

### Padrão 2: Script Shell

```bash
# Humano pergunta: processar imagens em lote
cat > process_images.sh << 'EOF'
#!/bin/bash
for img in *.jpg; do
    convert "$img" -resize 800x600 "thumb_$img"
done
EOF
```

---

## 19.4 Desenvolvimento Iterativo

### Rodada 1: Gerar Versão Inicial

```bash
# Humano: escrever um script de backup
# IA gera versão inicial, então humano testa, levanta problemas:

# Humano: bom, mas preciso de modo --dry-run
```

### Rodada 2: Adicionar Funcionalidades

```bash
# Humano: também adicionar tratamento de erros e logging
```

### Rodada 3: Depurar

```bash
# Humano: получик erro 'Permission denied' depois de executar
# IA: corrige o problema...
```

---

## 19.5 Deixe a IA Ajudar na Depuração

```bash
# Humano: получик erro depois de executar este comando
$ ./deploy.sh
# Saída: /bin/bash^M: bad interpreter: No such file or directory

# IA: este é um problema de quebra de linha do Windows. Execute:
sed -i 's/\r$//' deploy.sh
```

---

## 19.6 Ferramentas de Colaboração Recomendadas

### Multiplexador de Terminal

```bash
# tmux: dividir janelas
tmux new -s mysession
# Ctrl+b %  # divisão vertical
# Ctrl+b "  # divisão horizontal
```

---

## 19.7 Exercícios

1. Descrever uma tarefa complexa e fazer a IA gerar comandos Shell
2. Fazer a IA revisar um script existente para problemas de segurança
3. Usar iteração para fazer a IA ajudar a escrever uma ferramenta prática
4. Fazer a IA ajudar a explicar código Shell que você não entende