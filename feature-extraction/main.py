import os
import image as img

def main():
    print('Por favor informe o caminho das imagens a serem extraidas as caracteristicas: ')
    path = input()

    image_files = []

    for name in os.listdir(path):
        if os.path.isfile(name):
            image_files.append(name)
    print(image_files)

main()