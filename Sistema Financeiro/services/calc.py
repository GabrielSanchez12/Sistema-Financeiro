
class CalculadoraFinanceira:

    @staticmethod
    def juros_simples(capital, taxa, tempo):
        return capital * (1 + (taxa / 100) * tempo)

    @staticmethod
    def juros_compostos(capital, taxa, tempo):
        return capital * (1 + taxa / 100) ** tempo