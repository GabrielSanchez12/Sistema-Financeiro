import json
import os
from models.movimentacao import Movimentacao


class Armazenamento:
    def __init__(self, arquivo="dados.json"):
        self.arquivo = arquivo

    def salvar(self, movimentacoes):
        dados = []

        for mov in movimentacoes:
            dados.append({
                "descricao": mov.descricao,
                "valor": mov.valor,
                "tipo": mov.tipo
            })

        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return []

        with open(self.arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        movimentacoes = []

        for item in dados:
            movimentacao = Movimentacao(
                item["descricao"],
                item["valor"],
                item["tipo"]
            )
            movimentacoes.append(movimentacao)

        return movimentacoes