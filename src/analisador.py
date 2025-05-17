from collections import Counter

def detectar_ips_suspeitos(df, limite=3):
    """
    Detecta IPs que tiveram mais de N ações BLOCK.
    Retorna uma lista de IPs suspeitos.
    """
    bloqueios = df[df['acao'] == 'BLOCK']
    contagem = Counter(bloqueios['ip'])

    suspeitos = {ip: count for ip, count in contagem.items() if count >= limite}
    return suspeitos