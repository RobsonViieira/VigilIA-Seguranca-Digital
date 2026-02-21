import random
import time
from datetime import datetime
from src.ai_detector import AIDetector

# Tipos de ataque e nível base
ATTACK_TYPES = {
    "Tentativa de login inválido": 1,
    "IP desconhecido detectado": 2,
    "Acesso não autorizado": 3,
    "Transferência suspeita": 4,
    "Ataque de força bruta": 5
}

# Inicializa detector
detector = AIDetector()


def gerar_evento():
    ataque = random.choice(list(ATTACK_TYPES.keys()))
    nivel_base = ATTACK_TYPES[ataque]

    # Score suave (variação pequena)
    score = nivel_base + random.uniform(-0.5, 0.5)

    # Registra no modelo
    detector.registrar(score)

    # Detecta anomalia
    anomalia, motivo = detector.detectar_anomalia(score)

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if anomalia:
        alerta = f"⚠️ RISCO ALTO ({score:.2f}) - {motivo}"
    else:
        alerta = f"RISCO {score:.2f}"

    evento = f"[{horario}] {ataque} | {alerta}"

    return evento


def salvar_log(evento):
    with open("logs/seguranca.log", "a") as file:
        file.write(evento + "\n")


def main():
    print("VigilIA + IA iniciado...\n")
    print("Monitoramento Inteligente Ativo\n")

    for _ in range(30):
        evento = gerar_evento()
        print(evento)
        salvar_log(evento)
        time.sleep(1)

    print("\nMonitoramento finalizado.")
    print("Logs salvos em logs/seguranca.log")


if __name__ == "__main__":
    main()