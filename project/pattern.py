import math
from PIL import Image

COLOR_BLACK = (0,0,0)
COLOR_GREY = (128, 128, 128)

# Colors an blockSize x blockSize pixel block + outlining grid
def colorBlock(blockSize, blockColor, upperLeft, outImage):
    for i in range(0, blockSize):
	for j in range(0, blockSize):
	    putx = upperLeft[0] + i
	    puty = upperLeft[1] + j
	    if i == blockSize-1 or j == blockSize-1:
		outImage.putpixel((putx, puty), COLOR_GREY)
	    else:
		outImage.putpixel((putx, puty), blockColor)
    # Adjust grid color if tenth block
    tenth = blockSize * 10
    if (upperLeft[0] + blockSize) % tenth == 0:
	putx = upperLeft[0] + blockSize - 1
	for j in range(0, blockSize):
	    puty = upperLeft[1] + j
	    outImage.putpixel((putx, puty), COLOR_BLACK)
    if (upperLeft[1] + blockSize) % tenth == 0:
	puty = upperLeft[1] + blockSize -1
	for i in range(0, blockSize):
	    putx = upperLeft[0] + i
	    outImage.putpixel((putx, puty), COLOR_BLACK)

# Takes in the input and the output Images and colors blocks
# in the output Image based in the input Image. The two images
# may no be the same size
def generatePattern(stitches, blockSize, inImage, outImage):
    inWidth, inHeight = inImage.size
    stitchSize = inWidth / stitches
    midStitch = stitchSize / 2
    inWidth = int(inWidth / stitchSize)
    inHeight = int(inHeight / stitchSize)
    outWidth, outHeight = outImage.size
    for i in range(0, inWidth):
	for j in range(0, inHeight):
	    getx = i * stitchSize + midStitch
	    gety = j * stitchSize + midStitch
	    blockColor = inImage.getpixel((getx, gety))
	    outxy = (i * blockSize, j * blockSize)
	    colorBlock(blockSize, blockColor, outxy, outImage)
	
def processImage(filename='pikachu.png', stitches=60, maxColors=256):
    uploadedImage = Image.open('uploads/' + filename)
    width, height = uploadedImage.size
    width = float(width)
    height = float(height)
    # Resize image according to stitches across
    ratio = width / height
    miniw = stitches * 8
    minih = int(math.ceil(miniw / ratio))
    stitchSize = int(miniw / stitches)
    stitchesh = int(minih / stitchSize)
    miniImage = uploadedImage.resize((int(miniw), int(minih)), Image.ANTIALIAS)
    miniImage = miniImage.convert('P', palette=Image.ADAPTIVE, colors=maxColors)
    miniImage = miniImage.convert('RGB')
    blockSize = 25
    saveImage = Image.new('RGB', (blockSize*stitches, blockSize*stitchesh), COLOR_BLACK)
    generatePattern(stitches, blockSize, miniImage, saveImage)
    filename, ext = filename.split('.', 1)
    saveName = 'images/' + filename + 'pattern.' + ext
    saveImage.save('static/' + saveName)
    return saveName

#processImage('pikachu.png', 50, 9)
