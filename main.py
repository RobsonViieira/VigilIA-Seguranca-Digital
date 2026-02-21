import random
import time
from datetime import datetime

ATTACK_TYPES = {
    "Tentativa de login inválido": 1,
    "IP desconhecido detectado": 2,
    "Acesso não autorizado": 3,
    "Transferência suspeita": 4,
    "Ataque de força bruta": 5
}

estatisticas = {
    "BAIXO": 0,
    "MÉDIO": 0,
    "CRÍTICO": 0
}

def gerar_evento():
    ataque = random.choice(list(ATTACK_TYPES.keys()))
    nivel = ATTACK_TYPES[ataque]
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if nivel <= 2:
        risco = "BAIXO"
    elif nivel <= 4:
        risco = "MÉDIO"
    else:
        risco = "CRÍTICO"

    estatisticas[risco] += 1

    evento = f"[{horario}] ALERTA: {ataque} | RISCO: {risco}"
    return evento


def salvar_log(evento):
    with open("logs/seguranca.log", "a") as file:
        file.write(evento + "\n")


def gerar_relatorio():
    relatorio = "\n===== RELATÓRIO FINAL =====\n"
    total = sum(estatisticas.values())

    for nivel, qtd in estatisticas.items():
        relatorio += f"{nivel}: {qtd} eventos\n"

    relatorio += f"Total: {total} eventos\n"
    relatorio += "Status: "

    if estatisticas["CRÍTICO"] > 2:
        relatorio += "RISCO ALTO\n"
    elif estatisticas["MÉDIO"] > 3:
        relatorio += "RISCO MODERADO\n"
    else:
        relatorio += "SISTEMA ESTÁVEL\n"

    return relatorio


def main():
    print("VigilIA iniciado...")
    print("Monitoramento Inteligente Ativo\n")

    for i in range(15):
        evento = gerar_evento()
        print(evento)
        salvar_log(evento)
        time.sleep(1)

    relatorio = gerar_relatorio()
    print(relatorio)

    with open("logs/relatorio.txt", "w") as file:
        file.write(relatorio)

    print("Relatório salvo em logs/relatorio.txt")


if __name__ == "__main__":
    main()