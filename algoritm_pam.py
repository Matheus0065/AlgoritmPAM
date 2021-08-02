import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import random
import math


df = pd.read_csv('base-covid-19-us.csv')
df2 = df[:10]  # BASE TESTE


class AlgoritmoPAM:
    _LISTA_MEDOIDS = {}
    _MEDOIDS = None
    _VALORES_MSE = []
    _BACKUP_MEDOIDS = []
    _CONTADOR_ALPHA = 0

    @staticmethod
    def definir_menor(lista_medoid):  # Função para identificar o menor valor

        menor = lista_medoid[0]
        posicao = 0

        for idx in range(len(lista_medoid)):
            if idx == 0:
                pass

            elif lista_medoid[idx] < menor:
                menor = lista_medoid[idx]
                posicao = idx

        return menor, posicao

    @staticmethod
    def remove_medoids(dataset, medoids):
        list_remove = []
        for row in range(len(dataset)):
            for idx in range(len(medoids)):
                if dataset[row][0] == medoids[idx][0] and dataset[row][1] == medoids[idx][1]:
                    list_remove.append(row)

        new_dataset = np.delete(dataset, list_remove, axis=0)

        return new_dataset

    def calculo_custo_medoids(self, X, Y, medoids):
        _MEDOIDS_ASSOCIADOS = {}
        for i in range(len(X)):
            print(f"POSIÇÃO DO DADO: {i}")

            # Calculo do custo entre cada ponto e cada medoid
            for m in range(len(medoids)):
                custo_medoid = (medoids[m][0] - X[i]) ** 2 + (medoids[m][1] - Y[i]) ** 2
                self._LISTA_MEDOIDS[m] = custo_medoid

                print(f"CALCULO DA MEDOID POSICAO: {m}")
                print(f"VALOR DO CUSTO: {custo_medoid}")

            # Associar cada medoid a cada ponto
            # verificar menor valor entre os medoids dos pontos
            medoid_menor, posicao = self.definir_menor(self._LISTA_MEDOIDS)
            print(f"VALOR MENOR CUSTO DO MEDOID: {medoid_menor}")

            # associação do medoid ao ponto
            for m in range(len(self._LISTA_MEDOIDS)):
                if medoid_menor == self._LISTA_MEDOIDS[m]:
                    if m in _MEDOIDS_ASSOCIADOS:
                        _MEDOIDS_ASSOCIADOS[m].append(medoid_menor)

                    else:
                        _MEDOIDS_ASSOCIADOS[m] = []
                        _MEDOIDS_ASSOCIADOS[m].append(medoid_menor)

            print("_______________________________________")

        return _MEDOIDS_ASSOCIADOS

    @staticmethod
    def mse_total(medoids_associados):
        soma_mse_total = 0
        for idx in range(len(medoids_associados) + 2):
            if idx not in medoids_associados:
                pass

            elif len(medoids_associados[idx]) == 0:
                pass

            else:
                mse_medoid = sum(medoids_associados[idx]) / len(medoids_associados[idx])
                soma_mse_total += mse_medoid

                print(mse_medoid)

        MSE_TOTAL = soma_mse_total / len(medoids_associados)

        return MSE_TOTAL

    def metodo_sorteio_medoid(self, new_dataset, _MEDOIDS):

        # SORTEAR NOVO MEDOID
        nvo_medoid = random.choice(new_dataset)
        print(f"NOVO MEDOID: {nvo_medoid}")

        _CALCULO_DISTANCIA = {}
        # CALCULAR A DISTANCIA DOS MEDOIDS PARA O NOVO MEDOID
        for i in range(len(_MEDOIDS)):
            distancia = math.sqrt((nvo_medoid[0] - _MEDOIDS[i][0]) ** 2 + (nvo_medoid[1] - _MEDOIDS[i][1]) ** 2)
            _CALCULO_DISTANCIA[i] = []
            _CALCULO_DISTANCIA[i].append(distancia)

        menor_distancia, posicao = self.definir_menor(_CALCULO_DISTANCIA)
        print(f"VALOR DA MENOR DISTANCIA: {menor_distancia}")
        print(f"POSIÇÃO DO MEDOID COM MENOR DISTANCIA: {posicao}")

        return posicao, nvo_medoid

    def fit_pam(self, pontos, K, alpha):

        # RECEBER OS VALORES DE ENTRADAS DO DATASET
        global set_posicao
        dataset = pontos.values

        # SORTEAR OS VALORES ALEATORIAMENTE, K PONTOS DOS DADOS COMO MEDOIDS
        posicao_medoids = random.sample(list(dataset), k=K)
        _MEDOIDS = np.array(posicao_medoids)  # Transformando os medoids em array

        # print(f"POSIÇÕES INICIAIS DOS MEDOIDS 00: {_MEDOIDS[0]}")
        # print(f"POSIÇÕES INICIAIS DOS MEDOIDS 01: {_MEDOIDS[1]}")
        # print(f"POSIÇÕES INICIAIS DOS MEDOIDS 02: {_MEDOIDS[2]}")
        # print("_______________________________________")
        # self._BACKUP_MEDOIDS.append(_MEDOIDS)
        ponto_inicial = 0
        while True:

            # ATRIBUINDOS OS VALORES AS VARIAVEIS X E Y
            new_dataset = self.remove_medoids(dataset, _MEDOIDS)
            print(_MEDOIDS)

            X = new_dataset.T[0]
            Y = new_dataset.T[1]

            print(X)
            print(Y)
            print("_______________________________________")

            # CALCULAR O CUSTOS DE CADA MEDOIDS COM CADA DADOS E ASSOCIAR OS MEDOIDS AOS PONTOS
            ASSOCIADOS_MEDOIDS = self.calculo_custo_medoids(X, Y, medoids=_MEDOIDS)
            print(f"MEDOIDS ASSOCIADOS VALORES: {ASSOCIADOS_MEDOIDS}")

            # CALCULAR O CUSTO TOTAL (MSE) PARA CADA MEDOID
            TOTAL_MSE = self.mse_total(ASSOCIADOS_MEDOIDS)
            print(f"TOTAL MSE: {TOTAL_MSE}")
            self._VALORES_MSE.append(TOTAL_MSE)

            if ponto_inicial == 0:
                set_posicao, novo_medoid = self.metodo_sorteio_medoid(new_dataset, _MEDOIDS)

                # antigo_medoid = np.array(_MEDOIDS[posicao])
                self._BACKUP_MEDOIDS.append(np.array(_MEDOIDS[set_posicao]))  # antigo medoid adicionado em uma lista

                _MEDOIDS[set_posicao] = novo_medoid
                print(f"ANTIGO MEDOID: {self._BACKUP_MEDOIDS}")
                print(f"NOVOS MEDOID: {_MEDOIDS}")

                ponto_inicial += 1

            elif ponto_inicial > 0:
                print(self._VALORES_MSE)
                if self._VALORES_MSE[1] < self._VALORES_MSE[0]:
                    print("MENOR")
                    print(self._BACKUP_MEDOIDS[0])
                    print(_MEDOIDS)
                    self._VALORES_MSE.remove(self._VALORES_MSE[0])
                    self._BACKUP_MEDOIDS.remove(self._BACKUP_MEDOIDS[0])

                    set_posicao, novo_medoid = self.metodo_sorteio_medoid(new_dataset, _MEDOIDS)

                    self._BACKUP_MEDOIDS.append(np.array(_MEDOIDS[set_posicao]))

                    _MEDOIDS[set_posicao] = novo_medoid
                    print(f"ANTIGO MEDOID: {self._BACKUP_MEDOIDS}")
                    print(f"NOVOS MEDOID: {_MEDOIDS}")

                    self._CONTADOR_ALPHA = 0

                else:
                    print("MAIOR")
                    print(self._BACKUP_MEDOIDS[0], set_posicao)
                    print(_MEDOIDS)
                    self._CONTADOR_ALPHA += 1

                    if self._CONTADOR_ALPHA == alpha:
                        print(f"ATINGIU A CONTAGEM MÁXIMA DE ALPHA: {self._CONTADOR_ALPHA}")
                        _MEDOIDS[set_posicao] = self._BACKUP_MEDOIDS[0]
                        self._VALORES_MSE.remove(self._VALORES_MSE[1])
                        print(f"ULTIMA POSIÇÃO COM MELHOR MSE: {_MEDOIDS} | MSE FINAL: {self._VALORES_MSE}")
                        break

                    else:
                        _MEDOIDS[set_posicao] = self._BACKUP_MEDOIDS[0]
                        self._VALORES_MSE.remove(self._VALORES_MSE[1])
                        self._BACKUP_MEDOIDS.remove(self._BACKUP_MEDOIDS[0])

                        set_posicao, novo_medoid = self.metodo_sorteio_medoid(new_dataset, _MEDOIDS)

                        self._BACKUP_MEDOIDS.append(np.array(_MEDOIDS[set_posicao]))

                        _MEDOIDS[set_posicao] = novo_medoid
                        print(f"ANTIGO MEDOID: {self._BACKUP_MEDOIDS}")
                        print(f"NOVOS MEDOID: {_MEDOIDS}")


pam = AlgoritmoPAM()
pam.fit_pam(df[['cases', 'deaths']], 3, 3)
