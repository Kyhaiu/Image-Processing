import os
import image as img
import PIL as pil

def main():
    print('Por favor informe o caminho das imagens a serem extraidas as caracteristicas: ')
    path = input()

    image_files = []

    for name in os.listdir(path):
        if os.path.isfile(path + '\\' + name):
            image_files.append(name)
    
    #im = pil.Image.open(path + '\\' + image_files[0])

    images = [img.image(path + '\\' + filename) for filename in image_files]

    images[0].getImage().show()

main()