import random
import time
from datetime import datetime

# Simulação de eventos suspeitos

ATTACK_TYPES = [
    "Tentativa de login inválido",
    "Acesso não autorizado",
    "Transferência suspeita",
    "Ataque de força bruta",
    "IP desconhecido detectado"
]

def gerar_evento():
    ataque = random.choice(ATTACK_TYPES)
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    evento = f"[{horario}] ALERTA: {ataque}"
    return evento


def salvar_log(evento):
    with open("logs/seguranca.log", "a") as file:
        file.write(evento + "\n")


def main():
    print("VigilIA iniciado...")
    print("Monitoramento ativo...\n")

    for i in range(10):  # Simula 10 eventos
        evento = gerar_evento()
        print(evento)
        salvar_log(evento)
        time.sleep(1)

    print("\nSimulação finalizada.")
    print("Logs salvos em logs/seguranca.log")


if __name__ == "__main__":
    main()