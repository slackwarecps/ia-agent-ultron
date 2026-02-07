#!/bin/bash
# Este script executa o busca-contexto.py com sudo e salva a saída em um arquivo.

# Encontra o diretório onde o script está localizado para que possa ser executado de qualquer lugar
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Executa o script python com sudo e redireciona a saída (stdout) e erros (stderr) para o arquivo de log
sudo python3 "$DIR/busca-contexto.py" > "$DIR/status_servidor.log" 2>&1

# Opcional: Imprime uma mensagem de confirmação no terminal
echo "✅ Contexto do servidor salvo em status_servidor.log"
