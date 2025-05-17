def gerar_alertas(suspeitos):
    """
    Exibe no console os IPs suspeitos detectados.
    """
    if not suspeitos:
        print("[INFO] Nenhum comportamento suspeito detectado.")
        return

    print("\n[ALERTA] IPs com comportamento suspeito detectados:")
    for ip, qtd in suspeitos.items():
        print(f" - {ip} teve {qtd} bloqueios.")