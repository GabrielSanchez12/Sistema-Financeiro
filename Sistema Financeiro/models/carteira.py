from services.armazenamento import Armazenamento


class CarteiraFinanceira:
    def __init__(self):
        self.armazenamento = Armazenamento()
        self.movimentacoes = self.armazenamento.carregar()

    def adicionar_movimentacao(self, movimentacao):
        self.movimentacoes.append(movimentacao)
        self.armazenamento.salvar(self.movimentacoes)

    def calcular_saldo(self):
        saldo = 0

        for mov in self.movimentacoes:
            if mov.tipo == "receita":
                saldo += mov.valor
            else:
                saldo -= mov.valor

        return saldo

    def listar_movimentacoes(self):
        return self.movimentacoes

    def remover_movimentacao(self, indice):
        if 0 <= indice < len(self.movimentacoes):
            self.movimentacoes.pop(indice)
            self.armazenamento.salvar(self.movimentacoes)
            return True
        return False