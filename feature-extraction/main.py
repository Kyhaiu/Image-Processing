import os
import cv2 as cv
import numpy as np
import image as img
import pandas as pd
from matplotlib import pyplot as plt


def main():
    """
        As funções possuem descrição, então basta colocar o mouse em cima de cada, que vai ser que nem se fosse função de biblioteca
        Executa todo o programa, se quiser deixar constante a execução vc pode passar via prametro na main
    """
    print('Por favor informe o caminho das imagens a serem extraidas as caracteristicas: ')
    #path = input()
    path = "C:\\Users\\Sharkb8i\\Documents\\GitHub\\Image-Processing\\feature-extraction\\images\\Entradas"

    image_files = []
    k = 6
    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            if name ==  "Teste" + str(k).zfill(2) + ".png":
                image_files.append(name)
                k += 1

    print("Arquivos identificados: ", image_files)

    images = None
    image_ready = []
    for i in image_files:
        images = img.image(path, i)
        print("Arquivo: ", image_files)
        image_ready.append(images.segmentation(images.getBinaryImage(), 0, 0))

    return image_ready

def generate_csv_and_save(images):
    """
    No arquivo .csv, cada imagem, folha e propriedades dela extraídas serão
    gravadas em uma linhado arquivo. Sugerimos o seguinte formato:
        - ID  Imagem(mesmo  nome  do  arquivo  de  entrada);
        - ID  Folha(Inteiro sequencial, reiniciado para cada nova imagem de entrada);
        - Propriedade 1, Propriedade 2, ..., Propriedade N.
    
    O perímetro também é propriedade a ser armazenada  no  arquivo  .csv,  bem
    como as propriedades especificadas para cada uma das equipes, de acordo com
    a lista abaixo.

    Os campos devem, necessariamente serem separados por vírgula.
    Valores fracionários devem usar o “.” como separador decimal.
    """

    import csv
    print("Gerando CSV...")
    count = True
    for i in images:
        field_names = ["ID Imagem", "ID Folha", "Perimetro", "Contraste", "Homogeneidade", "Correlacao"]
        dict = {"ID Imagem": i[0], "ID Folha": i[1], "Perimetro": i[2], "Contraste": i[3], "Homogeneidade": i[4], "Correlacao": i[5]}

        with open('Resultados.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            if(count):
                writer.writeheader()
                count = False
            writer.writerows(dict)


    print("CSV salvo!")

images = main()
generate_csv_and_save(images)