
# INSTRUCOES

# Vá para o diretório do projeto
cd ~/services/ultron-engine

# Crie o ambiente virtual
python3 -m venv venv

# Ative o venv
```
source venv/bin/activate


$ pip install flask python-dotenv google-generativeai requests
```
## DEPLOY

# Build da imagem
docker compose build

# Subir o container em background
docker compose up -d

# Validar se o container está saudável
docker ps | grep ultron

## TESTES 1. Preparação da Conectividade (O Pulo do Gato SRE)
Como definimos no docker-compose.yml que a porta 5005 está mapeada apenas para 127.0.0.1, ela não está aberta para a internet.

Opção A (Recomendada): Túnel SSH No terminal do seu Mac, abra um túnel para "trazer" a porta da VPS para o seu localhost:

Bash
ssh -L 5005:localhost:5005 bikini-bottom-server
Agora, quando você enviar algo para localhost:5005 no Mac, ele cairá direto no container na VPS.

# Configura o nome do bot
git config --global user.name "Ultron"

# Configura o email oficial
git config --global user.email "ia-ultron@fabao.eng.br"

## REDPLOY
$ docker compose down && docker compose up -d --build

## ANALISE DOS LOGS
$ docker logs -f ultron-engine