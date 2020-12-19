import os
import image as img


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
    

    images = [img.image(path, filename) for filename in image_files]
    
    t = images[0].segmentation(images[0].getBinaryImage(), 0, 0)
    #print(t)


main()