import argparse
from src.ingestao import carregar_logs
from src.analisador import detectar_ips_suspeitos
from src.alerta import gerar_alertas

def run(caminho_log, limite_alerta=3):
    print(f"[INFO] Lendo log de: {caminho_log}")
    df = carregar_logs(caminho_log)

    print(f"[INFO] Analisando IPs com mais de {limite_alerta} bloqueios...")
    suspeitos = detectar_ips_suspeitos(df, limite=limite_alerta)

    gerar_alertas(suspeitos)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de análise de segurança")
    parser.add_argument("--input", required=True, help="Caminho para o arquivo de log")
    parser.add_argument("--limite", type=int, default=3, help="Limite de bloqueios para alerta")
    args = parser.parse_args()

    run(args.input, args.l