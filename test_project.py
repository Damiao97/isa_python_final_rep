## importar modulos e classes necessarias ao teste do projet.py##
import unittest
import csv
from project import Tempestade
from datetime import datetime
import os

class TestTempestade(unittest.TestCase):

    # Testa se estão a ser guardados corretamente os dados no ficheiro tempestade.csv #
    def test_registo_tempestade_csv(self):

        # parametros para o teste
        sobre_elevacao = 30
        pressao_atmosferica = 1001

        # cria um caminho e um arquivo teste para verificação das funções do projeto
        test_csv_path = 'test_tempestades.csv'

        # aplica os parametros e o caminho para o arquivo test_tempestade.csv para a relização do teste
        tempestade = Tempestade(sobre_elevacao, pressao_atmosferica, csv_path=test_csv_path)

        # guarda a informação 
        tempestade.registo_tempestade()

        try:
            
            # lê a ultima linha do arquivo test_tempestade.csv
            with open(test_csv_path, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)

           # verifica se corresponde aos valores esperados
            last_line = lines[-1]
            expected_values = [tempestade.hora_registo, tempestade.data_registo, str(tempestade.sobre_elevacao), str(tempestade.pressao_atmosferica)]
            self.assertListEqual(last_line, expected_values, "valor registado não está a ser guardado corretamente")

        finally:
            
            os.remove(test_csv_path) # remove o arquivo do sistema de arquivos, através do caminho test_csv_path
       
    # teste para ver se está a determinar o risco alto de tempestade #
    def test_risco_tempestade_alto_risco(self):
        # Valores padrão para um alto risco de tempestade 
        sobre_elevacao = 60
        pressao_atmosferica = 1000

        # Aplica os parametros de tempestade
        tempestade = Tempestade(sobre_elevacao, pressao_atmosferica)
        # Determina risco de tempestade
        result = tempestade.risco_tempestade()

        # verifica se o risco calculado corresponde ao esperado
        self.assertEqual(result, "Alto risco de tempestade", "nível de risco incorreto")

    # teste para ver se está a determinar bem o risco medio de tempestade #
    def test_risco_tempestade_medio_risco(self):

        # Valores padrão para um medio risco de tempestade 
        sobre_elevacao = 40
        pressao_atmosferica = 1010

        # Aplica os parametros de tempestade
        tempestade = Tempestade(sobre_elevacao, pressao_atmosferica)
        # Determina risco
        result = tempestade.risco_tempestade()

        # verifica se o risco calculado corresponde ao esperado
        self.assertEqual(result, "Médio risco de tempestade", "nível de risco incorreto")

    # teste para ver se está a determinar bem o risco baixo de tempestade #
    def test_risco_tempestade_baixo_risco(self):

        # Valores padrão para um baixo risco de tempestade 
        sobre_elevacao = 20
        pressao_atmosferica = 1016

        # Aplica os parametros
        tempestade = Tempestade(sobre_elevacao, pressao_atmosferica)
        # Determina resultado de risco
        result = tempestade.risco_tempestade()

        # verifica se o risco calculado corresponde ao esperado
        self.assertEqual(result, "Baixo risco de tempestade", "nível de risco incorreto")


    # teste para a correta leitura dos dados, aplicado ao arquivo do test_tempestade.csv #
    def test_ler_dados_csv(self):
        # parametros do teste
        csv_path = 'test_tempestade.csv'
        sobre_elevacao_values = [30.0, 40.0, 20.0]
        pressao_atmosferica_values = [1001.0, 1002.0, 1003.0]

        # escreve os parametros no arquivo test_tempestades.csv
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Hora', 'Data', 'Sobre_Elevacao', 'Pressao_Atmosferica'])
            for i in range(len(sobre_elevacao_values)):
                writer.writerow(['00:00:00', '2024-01-17', sobre_elevacao_values[i], pressao_atmosferica_values[i]])

        # cria uma instância da classe Tempestade com os parâmetros do teste e o caminho do test_tempestade.csv
        tempestade = Tempestade(0, 0, csv_path)

        # lê os dados do arquivo teste
        sobre_elevacao_data = tempestade.ler_dados_csv(coluna=2)
        pressao_atmosferica_data = tempestade.ler_dados_csv(coluna=3)

        # verifica se correspondem ao esperado
        self.assertEqual(sobre_elevacao_data, sobre_elevacao_values, "Valor de sobre_elevacao errado")
        self.assertEqual(pressao_atmosferica_data, pressao_atmosferica_values, "Valor de  pressao_atmosferica errado")

    # Testa as medias calculadas #
    def test_calcular_media(self):
        
        # valores usados para cálculo da média 
        csv_path = 'test_tempestade.csv'
        sobre_elevacao_values = [30.0, 40.0, 20.0]
        pressao_atmosferica_values = [1001.0, 1002.0, 1003.0]

        # escreve os parametros no arquivo teste csv
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Hora', 'Data', 'Sobre_Elevacao', 'Pressao_Atmosferica'])
            for i in range(len(sobre_elevacao_values)):
                writer.writerow(['00:00:00', '2024-01-17', sobre_elevacao_values[i], pressao_atmosferica_values[i]])

        # cria uma instância da classe Tempestade com os parâmetros do teste e o caminho do arquivo test_tempestade.csv
        tempestade = Tempestade(0, 0, csv_path)

        # calculo dos valores médios das colunas onde estão as variaveis de sobre-elevação e pressão atmosférica
        sobre_elevacao_media = tempestade.calcular_media(2)
        pressao_atmosferica_media = tempestade.calcular_media(3)

        # verifica se corresponde ao valor da média 
        self.assertAlmostEqual(sobre_elevacao_media, sum(sobre_elevacao_values) / len(sobre_elevacao_values), delta=0.001, msg="media de sobre_elevacao errada")
        self.assertAlmostEqual(pressao_atmosferica_media, sum(pressao_atmosferica_values) / len(pressao_atmosferica_values), delta=0.001, msg="media de pressao_atmosferica errada")


    # testar a criação do gráfico (ex: alto risco) #
    def test_gerar_grafico_alto_risco(self):
        
        sobre_elevacao_values = [55.0, 60.0, 70.0]
        pressao_atmosferica_values = [1004.0, 1003.0, 1002.0]
        risco = "Alto Risco"

        tempestade = Tempestade(0, 0)

        # gera grafico
        tempestade.gerar_grafico(sobre_elevacao_values, pressao_atmosferica_values, risco)

        #se cria ficheiro 
        self.assertTrue(os.path.exists('grafico_tempestade.png'), "Erro na criação do gráfico")

## corre os testes ##
if __name__ == '__main__':
    unittest.main()