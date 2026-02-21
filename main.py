import random
import time
from datetime import datetime
from src.ai_detector import AIDetector

ATTACK_TYPES = {
    "Tentativa de login inválido": 1,
    "IP desconhecido detectado": 2,
    "Acesso não autorizado": 3,
    "Transferência suspeita": 4,
    "Ataque de força bruta": 5
}

detector = AIDetector()

def gerar_evento():
    ataque = random.choice(list(ATTACK_TYPES.keys()))
    nivel = ATTACK_TYPES[ataque]

    detector.registrar(nivel)

    anomalia = detector.detectar_anomalia(nivel)

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alerta = ""

    if anomalia:
        alerta = " ⚠️ ANOMALIA DETECTADA"

    evento = f"[{horario}] {ataque} | NIVEL {nivel}{alerta}"

    return evento


def salvar_log(evento):
    with open("logs/seguranca.log", "a") as file:
        file.write(evento + "\n")


def main():
    print("VigilIA + IA iniciado...\n")

    for i in range(20):
        evento = gerar_evento()
        print(evento)
        salvar_log(evento)
        time.sleep(1)

    print("\nMonitoramento finalizado.")


if __name__ == "__main__":
    main()