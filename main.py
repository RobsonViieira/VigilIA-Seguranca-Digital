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
    nivel_base = ATTACK_TYPES[ataque]

    # Score suave e realista
    score = nivel_base + random.uniform(-0.5, 0.5)

    detector.registrar(score)
    anomalia, motivo = detector.detectar_anomalia(score)

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Classificação executiva
    if score < 2:
        nivel_risco = "BAIXO"
    elif score < 4:
        nivel_risco = "MÉDIO"
    else:
        nivel_risco = "ALTO"

    if anomalia:
        alerta = f"⚠️ {nivel_risco} ({score:.2f}) - {motivo}"
    else:
        alerta = f"{nivel_risco} ({score:.2f})"

    evento = f"[{horario}] {ataque} | {alerta}"
    return evento


def salvar_log(evento):
    with open("logs/seguranca.log", "a") as f:
        f.write(evento + "\n")


def main():
    print("Rovie IA iniciado...\n")

    for _ in range(30):
        evento = gerar_evento()
        print(evento)
        salvar_log(evento)
        time.sleep(1)

    print("\nMonitoramento finalizado.")


if __name__ == "__main__":
    main()