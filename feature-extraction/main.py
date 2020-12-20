import os
import image as img
import cv2 as cv
from matplotlib import pyplot as plt


def main():
    """
        As funções possuem descrição, então basta colocar o mouse em cima de cada, que vai ser que nem se fosse função de biblioteca
        Executa todo o programa, se quiser deixar constante a execução vc pode passar via prametro na main
    """
    print('Por favor informe o caminho das imagens a serem extraidas as caracteristicas: ')
    path = input()

    image_files = []

    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            image_files.append(name)
    """
    for i in image_files:
        mask = cv.imread(path+"\\"+i)
        plt.imshow(mask)
    plt.show()
    """

    images = [img.image(path, filename) for filename in image_files]

    for i in images:
        i.segmentation(i.getBinaryImage(), 0, 0)

    #t = images[0].segmentation(images[0].getBinaryImage(), 0, 0)
    #print(t)


main()