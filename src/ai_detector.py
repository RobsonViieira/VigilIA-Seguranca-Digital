import statistics

class AIDetector:

    def __init__(self):
        self.valores = []
        self.min_dados = 15  # mínimo pra começar a analisar

    def registrar(self, valor):
        self.valores.append(valor)

    def detectar_anomalia(self, valor_atual):

        if len(self.valores) < self.min_dados:
            return False, "Em fase de aprendizado"

        media = statistics.mean(self.valores)
        desvio = statistics.stdev(self.valores)

        limite = media + (2 * desvio)

        if valor_atual > limite:
            motivo = f"Acima do padrão (limite={limite:.2f})"
            return True, motivo

        return False, "Comportamento normal"