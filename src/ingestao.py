import pandas as pd

def carregar_logs(path_log):
    """
    Lê um arquivo de log de texto e retorna um DataFrame estruturado.
    Suporta logs simples no formato: [DATA] [IP] [ACAO] [PORTA]
    Exemplo de linha: 2025-05-17 12:01:33 192.168.0.10 BLOCK 443
    """
    dados = []

    with open(path_log, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split()
            if len(partes) >= 4:
                data = f"{partes[0]} {partes[1]}"
                ip = partes[2]
                acao = partes[3]
                porta = partes[4] if len(partes) > 4 else "-"
                dados.append((data, ip, acao, porta))

    df = pd.DataFrame(dados, columns=['timestamp', 'ip', 'acao', 'porta'])
    return df