import os
import image as img
import numpy as np


def main():
    """
        As funções possuem descrição, então basta colocar o mouse em cima de cada, que vai ser que nem se fosse função de biblioteca
        Executa todo o programa, se quiser deixar constante a execução vc pode passar via prametro na main
    """
    #print('Por favor informe o caminho das imagens a serem extraidas as caracteristicas: ')
    path = "C:\\Users\\Sharkb8i\\Documents\\GitHub\\Image-Processing\\feature-extraction\\images\\Entradas"

    image_files = []

    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            image_files.append(name)

    """
            |  0   1   2   3   4   5   6
            ------------------------------
            0|   
            1|          1   1   1   1
            2|      1           1
            3|          1       1
            4|      1           1
            5|      1   1   1   1
            6|  
    
    im = [
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [0, 0, 0]      , [0, 0, 0]      , [0, 0, 0]      , [0, 0, 0]      , [255, 255, 255]],
            [[255, 255, 255], [0, 0, 0]      , [255, 255, 255], [255, 255, 255], [0, 0, 0]      , [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [0, 0, 0]      , [255, 255, 255], [0, 0, 0]      , [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [0, 0 ,0]      , [255, 255, 255], [255, 255, 255], [0, 0, 0]      , [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [0, 0, 0]      , [0, 0, 0]      , [0, 0, 0]      , [0, 0, 0]      , [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
         ]
    """

    images = [img.image(path + '\\' + filename) for filename in image_files]

    #t = images[0].segmentation(images[0].getImage())
    #print(t)
    #images[0].grayscale(images[0].getImage())
    
    im = np.array([[0, 0, 1, 1],
                   [0, 0, 1, 1],
                   [0, 2, 2, 2],
                   [2, 2, 3, 3]], dtype=np.uint8)

    # O resultado é esse, tem esse quantidade de zero, porque
    # o level utilizado para tons de cinza foi 8, logo (8x8).
    # [
    #   [[[2]],[[2]],[[1]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[2]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[0]],[[3]],[[1]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[0]],[[0]],[[1]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    #   [[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    # ]

    result = images[0].glmc(im, 1, 0, levels=8)

    #contraste = images[0].glcmprops(result, 'contrast')
    #uniformidade = images[0].glcmprops(result, 'homogeneity')
    #correlacao = images[0].glcmprops(result, 'correlation')

    images[0].generate_csv_and_save(result)


main()