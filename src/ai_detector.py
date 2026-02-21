import statistics

class AIDetector:

    def __init__(self):
        self.valores = []

    def registrar(self, valor):
        self.valores.append(valor)

    def detectar_anomalia(self, valor_atual):

        if len(self.valores) < 5:
            return False, "Dados insuficientes"

        media = statistics.mean(self.valores)
        desvio = statistics.stdev(self.valores)

        limite = media + (2 * desvio)

        if valor_atual > limite:
            motivo = f"Valor acima do padrão (limite={limite:.2f})"
            return True, motivo

        return False, "Dentro do padrão"