def createNewImage(self, width, height):
        newImage = np.zeros((height, width))
        i = 0
        j = 0

        while (i < width):
            j = 0
            while (j < height):
                newImage[i][j] = 255
                j = j + 1
            i = i + 1
        
        print(newImage)

def floodFillRecur(self, binaryImage, rgbImage, newImage, x, y):
        if (x < 0 or x >= binaryImage.shape[0] or y < 0 or y >= binaryImage.shape[1] or binaryImage[x][y] != 0):
            return

        binaryImage[x][y] = 255
        newImage[x][y] = rgbImage[x][y]
    
        self.floodFillRecur(binaryImage, rgbImage, newImage, x + 1, y)
        self.floodFillRecur(binaryImage, rgbImage, newImage, x - 1, y)
        self.floodFillRecur(binaryImage, rgbImage, newImage, x, y + 1)
        self.floodFillRecur(binaryImage, rgbImage, newImage, x, y - 1)

def floodFill(self, binaryImage, x, y):
        self.floodFillRecur(binaryImage, rgbImage, newImage, x, y)

