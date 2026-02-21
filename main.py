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

    evento = f"[{horario}] ALERTA: {ataque} | RISCO: {risco}"
    return evento


def salvar_log(evento):
    with open("logs/seguranca.log", "a") as file:
        file.write(evento + "\n")


def main():
    print("VigilIA iniciado...")
    print("Sistema Inteligente de Monitoramento\n")

    for i in range(10):
        evento = gerar_evento()
        print(evento)
        salvar_log(evento)
        time.sleep(1)

    print("\nSimulação finalizada.")
    print("Logs salvos com classificação de risco.")


if __name__ == "__main__":
    main()