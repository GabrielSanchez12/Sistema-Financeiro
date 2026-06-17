import tkinter as tk
from tkinter import messagebox

from models.movimentacao import Movimentacao
from models.carteira import CarteiraFinanceira
from services.calc import CalculadoraFinanceira


class SistemaFinanceiroGUI:
    def __init__(self):
        self.carteira = CarteiraFinanceira()

        self.janela = tk.Tk()
        self.janela.title("Sistema Financeiro")
        self.janela.geometry("600x800")

        self.criar_widgets()
        self.atualizar_saldo()
        self.atualizar_historico()

    def criar_widgets(self):
        titulo = tk.Label(self.janela, text="Sistema Financeiro", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        tk.Label(self.janela, text="Descrição:").pack()
        self.entrada_descricao = tk.Entry(self.janela, width=40)
        self.entrada_descricao.pack()

        tk.Label(self.janela, text="Valor:").pack()
        self.entrada_valor = tk.Entry(self.janela, width=40)
        self.entrada_valor.pack()

        tk.Button(self.janela, text="Adicionar Receita", command=self.adicionar_receita).pack(pady=5)
        tk.Button(self.janela, text="Adicionar Despesa", command=self.adicionar_despesa).pack(pady=5)

        self.label_saldo = tk.Label(self.janela, text="Saldo: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_saldo.pack(pady=10)

        tk.Label(self.janela, text="Histórico:").pack()
        self.lista_historico = tk.Listbox(self.janela, width=60, height=10)
        self.lista_historico.pack()

        tk.Button(self.janela, text="Remover Selecionado", command=self.remover_movimentacao).pack(pady=10)

        tk.Label(self.janela, text="Calculadora de Juros", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(self.janela, text="Capital inicial:").pack()
        self.entrada_capital = tk.Entry(self.janela, width=40)
        self.entrada_capital.pack()

        tk.Label(self.janela, text="Taxa de juros (% ao período):").pack()
        self.entrada_taxa = tk.Entry(self.janela, width=40)
        self.entrada_taxa.pack()

        tk.Label(self.janela, text="Tempo (nº de períodos):").pack()
        self.entrada_tempo = tk.Entry(self.janela, width=40)
        self.entrada_tempo.pack()

        tk.Button(self.janela, text="Calcular Juros Simples", command=self.calcular_juros_simples).pack(pady=5)
        tk.Button(self.janela, text="Calcular Juros Compostos", command=self.calcular_juros_compostos).pack(pady=5)

        self.label_resultado_juros = tk.Label(self.janela, text="Resultado: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_resultado_juros.pack(pady=10)

    def adicionar_receita(self):
        self.adicionar_movimentacao("receita")

    def adicionar_despesa(self):
        self.adicionar_movimentacao("despesa")

    def adicionar_movimentacao(self, tipo):
        descricao = self.entrada_descricao.get()
        valor_texto = self.entrada_valor.get()

        if descricao == "":
            messagebox.showerror("Erro", "Digite uma descrição.")
            return

        try:
            valor = float(valor_texto)
            if valor <= 0:
                messagebox.showerror("Erro", "Digite um valor maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
            return

        movimentacao = Movimentacao(descricao, valor, tipo)
        self.carteira.adicionar_movimentacao(movimentacao)

        self.entrada_descricao.delete(0, tk.END)
        self.entrada_valor.delete(0, tk.END)

        self.atualizar_saldo()
        self.atualizar_historico()

        messagebox.showinfo("Sucesso", "Movimentação adicionada com sucesso!")

    def atualizar_saldo(self):
        saldo = self.carteira.calcular_saldo()
        self.label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")

    def atualizar_historico(self):
        self.lista_historico.delete(0, tk.END)

        for mov in self.carteira.listar_movimentacoes():
            texto = f"{mov.tipo.capitalize()} - {mov.descricao}: R$ {mov.valor:.2f}"
            self.lista_historico.insert(tk.END, texto)

    def remover_movimentacao(self):
        selecionado = self.lista_historico.curselection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma movimentação para remover.")
            return

        indice = selecionado[0]

        if self.carteira.remover_movimentacao(indice):
            self.atualizar_saldo()
            self.atualizar_historico()
            messagebox.showinfo("Sucesso", "Movimentação removida com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível remover a movimentação.")
    
    def calcular_juros_simples(self):
        self.calcular_juros("simples")


    def calcular_juros_compostos(self):
        self.calcular_juros("compostos")


    def calcular_juros(self, tipo):
        try:
            capital = float(self.entrada_capital.get())
            taxa = float(self.entrada_taxa.get())
            tempo = int(self.entrada_tempo.get())

            if capital <= 0 or taxa < 0 or tempo < 0:
                messagebox.showerror("Erro", "Digite valores válidos.")
                return

        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números nos campos de juros.")
            return

        if tipo == "simples":
            resultado = CalculadoraFinanceira.juros_simples(capital, taxa, tempo)
        else:
            resultado = CalculadoraFinanceira.juros_compostos(capital, taxa, tempo)

        self.label_resultado_juros.config(text=f"Resultado: R$ {resultado:.2f}")

    def executar(self):
        self.janela.mainloop()