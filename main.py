import random
import time
from datetime import datetime

ATTACK_TYPES = {
    "Tentativa de login inválido": 1,
    "IP desconhecido": 2,
    "Acesso não autorizado": 3,
    "Transferência suspeita": 4,
    "Ataque de força bruta": 5
}


def gerar_evento():

    ataque=random.choice(list(ATTACK_TYPES.keys()))
    base=ATTACK_TYPES[ataque]

    score=base+random.uniform(-0.5,0.5)

    if score<2:
        nivel="BAIXO"
    elif score<4:
        nivel="MÉDIO"
    else:
        nivel="ALTO"

    hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"[{hora}] {ataque} | {nivel} ({score:.2f})"


def salvar(evento):

    if not os.path.exists("logs"):
        os.mkdir("logs")

    with open("logs/seguranca.log","a") as f:
        f.write(evento+"\n")


def main():

    print("Rovie IA iniciado...\n")

    for i in range(40):

        e=gerar_evento()
        print(e)
        salvar(e)
        time.sleep(1)

    print("\nFinalizado.")


if __name__=="__main__":
    import os
    main()