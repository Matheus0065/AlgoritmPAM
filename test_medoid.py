from algoritm_pam import AlgoritmoPAM
import math
import random

_BACKUP_MEDOIDS = []


def test_medoids(new_dataset, _MEDOIDS, ponto_inicial, _VALORES_MSE):
    global pausa
    if ponto_inicial == 0:

        # SORTEAR NOVO MEDOID
        nvo_medoid = random.choice(new_dataset)
        print(f"NOVO MEDOID: {nvo_medoid}")

        _CALCULO_DISTANCIA = {}
        # CALCULAR A DISTANCIA DOS MEDOIDS PARA O NOVO MEDOID
        for i in range(len(_MEDOIDS)):
            distancia = math.sqrt((nvo_medoid[0] - _MEDOIDS[i][0]) ** 2 + (nvo_medoid[1] - _MEDOIDS[i][1]) ** 2)
            _CALCULO_DISTANCIA[i] = []
            _CALCULO_DISTANCIA[i].append(distancia)

        menor_distancia, posicao = AlgoritmoPAM.definir_menor(_CALCULO_DISTANCIA)
        print(f"VALOR DA MENOR DISTANCIA: {menor_distancia}")
        print(f"POSIÇÃO DO MEDOID COM MENOR DISTANCIA: {posicao}")

        antigo_medoid = _MEDOIDS[posicao]

        print("___________________________________")
        _BACKUP_MEDOIDS.append(antigo_medoid)
        print(f"ANTIGO MEDOID: {_BACKUP_MEDOIDS}")

        _MEDOIDS[posicao] = nvo_medoid
        print(f"MEDOIDS COM NOVA POSIÇÃO: {_MEDOIDS}")

        # ponto_inicial += 1
        pausa = None

    elif ponto_inicial > 0:

        if _VALORES_MSE[1] < _VALORES_MSE[0]:
            print("MENOR")
            print(_BACKUP_MEDOIDS[0])
            print(_MEDOIDS)

        else:
            print("MAIOR")
            print(_BACKUP_MEDOIDS[0])
            print(_MEDOIDS)

        pausa = 2

    return pausa


if __name__ == "__main__":
    mse = [0, 1]
    inicial = 0
    while True:
        dataset = [[84, 0], [741, 21], [325, 8], [5003, 101], [470, 0], [298, 10], [1763, 0]]
        medoid = [[209, 0], [116, 0], [4264, 41]]

        pausa = test_medoids(dataset, medoid, inicial, mse)

        inicial += 1

        if pausa == 2:
            break
