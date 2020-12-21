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
    path = input()
    #path = "C:\\Users\\Sharkb8i\\Documents\\GitHub\\Image-Processing\\feature-extraction\\images\\Entradas"

    image_files = []
    k = 0
    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            image_files.append(name)

    print("Arquivos identificados: ", image_files)

    images = None
    image_ready = []
    df = pd.DataFrame(columns = ['ID Imagem', 'ID Folha', "Perimetro", "Contraste", "Homogeneidade", "Correlacao"])
    for i in image_files:
        images = img.image(path, i)
        print("Arquivo: ", image_files)
        generate_csv_and_save(images.segmentation(images.getBinaryImage(), 0, 0), df)

def generate_csv_and_save(images, df):
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
    id_img = images[0]
    id_folha = images[1]
    per = images[2]
    cont = images[3]
    homo = images[4]
    corel = images[5]
    j = 0
    while j < len(images[1]):
        dicty = {
                 'ID Imagem'     : id_img,
                 'ID Folha'      : id_folha[j],
                 'Perimetro'     : per[j],
                 'Contraste'     : cont[j],
                 'Homogeneidade' : homo[j],
                 'Correlacao'    : corel[j]
                }
        df = df.append(dicty, ignore_index=True)
        j += 1



    df.to_csv("Resultados.csv", index=False, mode='a')
    print("CSV salvo!")

main()