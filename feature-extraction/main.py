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
    k = 1
    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            if name ==  "Teste" + str(k).zfill(2) + ".png":
                image_files.append(name)
                k += 1

    print("Arquivos identificados: ", image_files)

    images = None
    for i in image_files:
        images = img.image(path, i)
        print("Arquivo: ", image_files)
        seg_image = images.segmentation(images.getBinaryImage(), 0, 0)
        gray_image = images.grayscale(seg_image)
        glmc = images.glmc(gray_image, 1, 0, levels=8)
        contrast = image_files[i].glcmprops(glmc, 'contrast')
        homogeneity = image_files[i].glcmprops(glmc, 'homogeneity')
        correlation = image_files[i].glcmprops(glmc, 'correlation')

        print("Grayscale: ", gray_image)
        print("GLMC: ", glmc)
        print("Contrast: ", contrast)
        print("Homogeneity: ", homogeneity)
        print("Correlation: ", correlation)


    #t = images[0].segmentation(images[0].getBinaryImage(), 0, 0)
    #print(t)

    """
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

        contraste = images[0].glcmprops(result, 'contrast')
        uniformidade = images[0].glcmprops(result, 'homogeneity')
        correlacao = images[0].glcmprops(result, 'correlation')
        
        print("Contraste: ", contraste)
        print("Uniformidade: ", uniformidade)
        print("Correlação: ", correlacao)

        #images[0].generate_csv_and_save(result)
    """

main()