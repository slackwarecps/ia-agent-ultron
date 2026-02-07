#!/usr/bin/env python3

import subprocess
import re

def executar_comando(comando):
    """Executa um comando no shell e retorna a saída."""
    try:
        # Executa o comando e captura a saída (stdout e stderr)
        resultado = subprocess.run(
            comando,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Se o comando falhar, retorna uma mensagem de erro com o stderr
        return f"Erro ao executar '{comando}':\\n{e.stderr.strip()}"
    except FileNotFoundError:
        # Se o comando não for encontrado (ex: docker não instalado)
        programa = comando.split()[0]
        return f"Erro: O programa '{programa}' não foi encontrado. Ele está instalado e no PATH do sistema?"

def imprimir_titulo(titulo):
    """Imprime um título formatado para as seções do relatório."""
    print("\n" + "="*50)
    print(f"  {titulo}")
    print("="*50)

def get_docker_containers():
    """Lista os contêineres Docker ativos."""
    imprimir_titulo("Contêineres Docker Ativos")
    # Formata a saída do docker ps para ser mais legível
    output = executar_comando('docker ps --format "table {{.Names}}	{{.Image}}	{{.Status}}"')
    print(output)

def get_network_config():
    """Mostra as configurações de rede e DNS."""
    imprimir_titulo("Configurações de Rede (Endereços IP)")
    # 'ip -br a' é um comando moderno e conciso para listar IPs
    output = executar_comando("ip -br a")
    print(output)
    
    imprimir_titulo("Configurações de Rede (Servidores DNS)")
    # O arquivo resolv.conf contém os servidores DNS
    output_dns = executar_comando("cat /etc/resolv.conf")
    print(output_dns)
    print("\nNota: Para ver os domínios configurados no Coolify, é melhor consultar a UI do Coolify,")
    print("pois eles são gerenciados pelo proxy reverso (ex: Traefik) e não pela configuração de rede do host.")


def get_debian_version():
    """Mostra a versão do Debian."""
    imprimir_titulo("Versão do Sistema Operacional")
    # /etc/os-release é o local padrão para informações do SO em sistemas modernos
    output = executar_comando("cat /etc/os-release")
    # Procura pela linha PRETTY_NAME para uma descrição amigável
    for linha in output.splitlines():
        if "PRETTY_NAME" in linha:
            print(linha.split("=")[1].strip('"'))
            return
    print(output) # Fallback caso PRETTY_NAME não exista

def get_server_resources():
    """Mostra o uso de CPU, RAM e Disco."""
    imprimir_titulo("Recursos do Servidor")
    print("\n--- CPU Info ---")
    # nproc mostra o número de processadores
    cpu_cores = executar_comando("nproc")
    # lscpu para o modelo do processador
    cpu_model = executar_comando("lscpu | grep 'Model name:'")
    print(f"Cores/Processadores: {cpu_cores}")
    print(cpu_model.strip())
    
    print("\n--- Memória RAM ---")
    # 'free -h' mostra o uso de memória em formato legível por humanos
    ram_usage = executar_comando("free -h")
    print(ram_usage)

    print("\n--- Uso de Disco ---")
    # 'df -h' mostra o uso do sistema de arquivos
    disk_usage = executar_comando("df -h")
    print(disk_usage)

def get_firewall_status():
    """Verifica e mostra o status do firewall UFW."""
    imprimir_titulo("Status do Firewall (UFW)")
    # O comando 'ufw status' requer sudo
    output = executar_comando("sudo ufw status")
    if "Status: active" in output:
        print("Firewall está ATIVADO.")
    elif "Status: inactive" in output:
        print("Firewall está DESATIVADO.")
    else:
        # Imprime a saída completa em caso de erro ou estado inesperado
        print("Não foi possível determinar o status do firewall. Verifique a saída abaixo:")
    
    print("-" * 20)
    print(output)
    print("-" * 20)
    if "Cannot open" in output:
         print("\nAVISO: Este comando precisa de privilégios de superusuário.")
         print("Execute o script com 'sudo python3 busca-contexto.py' para ver o status do firewall.")


def main():
    """Função principal que orquestra a coleta e exibição dos dados."""
    print("Coletando informações do ambiente da VPS...")
    get_debian_version()
    get_server_resources()
    get_network_config()
    get_docker_containers()
    get_firewall_status()
    print("\n\nRelatório gerado com sucesso!")

if __name__ == "__main__":
    main()
