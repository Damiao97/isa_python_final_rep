##bibliotecas necessárias##
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

## Definir classe Tempestade ##
class Tempestade:

# define os objetos da classe ( sobre-elevação da tempestade, pressão atmosférica, data, hora) e o caminho para o arquivo tempestades.csv #
    def __init__(self, sobre_elevacao, pressao_atmosferica, csv_path='tempestades.csv'): 

        # parâmetros da tempestade, variáveis
        self.sobre_elevacao = sobre_elevacao
        self.pressao_atmosferica = pressao_atmosferica

        # hora atual e a data atual para registo
        self.hora_registo = datetime.now().strftime("%H:%M:%S") #("%H:%M:%S") hora em HH-MM_SS
        self.data_registo = datetime.now().strftime("%Y-%m-%d") #("%Y-%m-%d") data em formato YYYY-MM-DD

        # Define o caminho do arquivo tempestades.csv para a classe da tempestade
        self.csv_path = csv_path

        # Intervalo de valores, biblio np, para a pressão atmosférica entre 900 e 1100 , 100.
        self.pressao_atmosferica_reta = np.linspace(900, 1100, 100)

        # Calcula a sobre-elevação linear associada à pressão atmosférica
        self.sobre_elevacao_reta = 0.4 * (self.pressao_atmosferica_reta - 1000)


# Registo das variáveis: hora; data; elevação ; pressão atmosférica no arquivo tempestades.csv #
    def registo_tempestade(self):
        #abre o arquivo csv e prepara o registo dos valores
        with open(self.csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # adiciona nova linha no arquivo tempestades.csv 
            writer.writerow([self.hora_registo, self.data_registo, self.sobre_elevacao, self.pressao_atmosferica]) 


# Calculo do nivel de risco de tempestade #
    def risco_tempestade(self):
        if int(self.sobre_elevacao) >= 50 or int(self.pressao_atmosferica) <= 1005:
            return "Alto risco de tempestade"
        elif 30 <= int(self.sobre_elevacao) < 50 and 1005 < int(self.pressao_atmosferica) <= 1015:
            return "Médio risco de tempestade"
        else:
            return "Baixo risco de tempestade"
        
# Cria uma lista de dados para a leitura do arquivo tempestades.csv que premite que estes sejam lidos por outras funções#
    def ler_dados_csv(self, coluna):
        dados = []
        with open(self.csv_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            try:
                next(reader)
                for row in reader:
                    dados.append(float(row[coluna]))
            except StopIteration:
                pass
        return dados
    
# Calculo dos valores médios apartir do arquivo tempestades.csv 
    def calcular_media(self, coluna):
        dados = self.ler_dados_csv(coluna)# vai selecionar uma coluna corresponde a uma variavel 
        if not dados:
            return 0
        return sum(dados) / len(dados)
    
# Calculo medio da elevação 
    def calcular_media_sobre_elevacoes(self):
        return self.calcular_media(2) #calcular média da coluna 2 , sobre-elevação
    
# Calculo medio da pressão
    def calcular_media_pressao_atmosferica(self):
        return self.calcular_media(3) #calcula média da coluna 3, pressao atmosférica
     
# gera o grafico com o Matplotlib, relacionando as variaveis de sobre-elevação e pressão atmosférica #
    def gerar_grafico(self, sobre_elevacao_values, pressao_atmosferica_values, risco):
        plt.plot(sobre_elevacao_values, pressao_atmosferica_values, 'o-', label=f'Dados - Risco: {risco}') # 'o-' simbologia no grafico, marcadores redondos ligados por uma linha
        plt.plot(self.sobre_elevacao_reta, self.pressao_atmosferica_reta, '--', label='Reta de Regressão', color='red') #reta de regressão
        plt.scatter([50, 30, 10, sobre_elevacao_values[0]], [1005, 1015, 1013.25, pressao_atmosferica_values[0]],
                    color=['red', 'yellow', 'green', 'blue'], label=['Alto Risco', 'Médio Risco', 'Baixo Risco', 'Seu Ponto']) #pontos
        
        #Legendas dos eixos x e y; título do gráfico; grelha
        plt.xlabel('Sobre-elevacao (cm)')
        plt.ylabel('Pressao Atmosferica')
        plt.title(f'Gráfico de Sobre-elevacao vs Pressao Atmosferica - Risco: {risco}')
        plt.legend()
        plt.grid(True)

        # Salva e exibe o gráfico
        plt.savefig('grafico_tempestade.png')
        plt.show()


## lê os dados do tempestades.csv e recolhe dados da coluna para uma nova lista ##
def ler_dados_csv_alternativo(csv_path, coluna):
    dados = [] #cria uma lista vazia para armazenar novos dados
    
    #abre e lê os dados da coluna da sobre-elevação e da pressão atmosférica do arquivo tempestades.csv
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        try:
            next(reader)
            for row in reader:
                dados.append(float(row[coluna])) # Extrai o valor da coluna e converte-o em float; acrescenta a lista
        except StopIteration:
            pass
    return dados # devolve os dados recolhidos


## Calculo da mediana apartir dos dados recolhidos do arquivo tempestades.csv após 3 medições ##
def calcular_mediana(coluna):
    dados = ler_dados_csv_alternativo('tempestades.csv', coluna)
    if not dados:
        return 0 
    sorted_data = sorted(dados) # ordena os dados da classe para fazer a mediana
    n = len(sorted_data) #n é igual ao número de elementos de dados da lista, tem que ser maior que 2 para fazer o cálculo da mediana
    if n % 2 == 0:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        return sorted_data[n // 2]


## Calculo do desvio padrão apartir do ficheiro tempestades.csv ##
def calcular_desvio_padrao(coluna):
    dados = ler_dados_csv_alternativo('tempestades.csv', coluna)
    if not dados:
        return 0
    media = sum(dados) / len(dados)
    desvio = sum((x - media) ** 2 for x in dados) / len(dados) #variancia
    return desvio ** 0.5  

## Função Main vai por em prática todas as funções acima trabalhadas; ##
def main():

    # Correção de bugs nos inputs do user
    while True:
        try:
            sobre_elevacao = float(input("Digite a sobre_elevacao (em cm): "))
            pressao_atmosferica = float(input("Digite a pressao atmosferica(em hpa): "))
            break
        except ValueError:
            print("Por favor, insira valores numéricos válidos.")

    # Agrega as variaveis em tempestade para se poder determinar o risco
    tempestade = Tempestade(sobre_elevacao, pressao_atmosferica)
    risco = tempestade.risco_tempestade() # determina risco de tempestade, alto médio ou baixo

    # realiza o Cálculo da media das duas variaveis
    media_sobre_elevacoes = tempestade.calcular_media_sobre_elevacoes()
    media_pressao_atmosferica = tempestade.calcular_media_pressao_atmosferica()

    # Visualização dos resultados no terminal
    print(f"Média das sobre-elevações: {media_sobre_elevacoes}")
    print(f"Média da pressão atmosférica: {media_pressao_atmosferica}")
    print(f"Risco de tempestade: {risco}")

    # Regista a informação da tempestade e dá o path para o ficheiro tempestades.csv
    tempestade.registo_tempestade()
    print(f"Tempestade registada com sucesso em: {tempestade.csv_path}")

    # Extrai as variaveis para as estatisticas e indica as colunas das variaveis no arquivo estatísticas_tempestades.csv. 
    with open('estatisticas_tempestades.csv', mode='a', newline='') as stats_file:
        stats_writer = csv.writer(stats_file)
        stats_writer.writerow([media_sobre_elevacoes, calcular_mediana(2), calcular_desvio_padrao(2),
                               media_pressao_atmosferica, calcular_mediana(3), calcular_desvio_padrao(3)])
        
    # Valores apresentados no grafico
    sobre_elevacao_values = [float(sobre_elevacao)]
    pressao_atmosferica_values = [float(pressao_atmosferica)]

    # Gera o grafico
    tempestade.gerar_grafico(sobre_elevacao_values, pressao_atmosferica_values, risco)


if __name__ == "__main__":
    
    # Vizualização da mediana e desvio padrão da pressao atmosferica no terminal
    mediana_sobre_elevacoes = calcular_mediana(2)
    desvio_padrao_pressao_atmosferica = calcular_desvio_padrao(3)
    print(f"Mediana das sobre-elevações: {mediana_sobre_elevacoes}")
    print(f"Desvio padrão da pressão atmosférica: {desvio_padrao_pressao_atmosferica}")

    
    main()
