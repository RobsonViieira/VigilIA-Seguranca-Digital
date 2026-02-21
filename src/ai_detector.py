import statistics
from collections import deque

class AIDetector:

    def __init__(self):
        self.valores = deque(maxlen=50)  # guarda só os últimos 50
        self.min_dados = 20

    def registrar(self, valor):
        self.valores.append(valor)

    def detectar_anomalia(self, valor_atual):

        if len(self.valores) < self.min_dados:
            return False, "Em treinamento"

        media = statistics.mean(self.valores)
        desvio = statistics.stdev(self.valores)

        limite = media + (2.5 * desvio)  # mais tolerante

        if valor_atual > limite:
            return True, f"Fora do padrão (limite={limite:.2f})"

        return False, "Normal"