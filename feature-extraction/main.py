import os
import image as img
import PIL as pil

def main():
    """
        As funções possuem descrição, então basta colocar o mouse em cima de cada, que vai ser que nem se fosse função de biblioteca
        Executa todo o programa, se quiser deixar constante a execução vc pode passar via prametro na main
    """
    print('Por favor informe o caminho das imagens a serem extraidas as caracteristicas: ')
    path = "C:\\Users\\Sharkb8i\\Documents\\GitHub\\Image-Processing\\feature-extraction\\images\\Entradas"

    image_files = []

    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            image_files.append(name)
    
    #im = pil.Image.open(path + '\\' + image_files[0])

    images = [img.image(path + '\\' + filename) for filename in image_files]

    t = images[0].segmentation(images[0].getImage())


main()