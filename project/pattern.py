from PIL import Image

COLOR_BLACK = (0,0,0)
COLOR_GREY = (128, 128, 128)

# Colors an blockSize x blockSize pixel block + outlining grid
# TO DO: Change to take in a color
def colorBlock(blockSize, blockColor, upperLeft, outImage):
    midBlock = int(blockSize / 2)
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
def generatePattern(stitchSize, blockSize, inImage, outImage):
    midStitch = int(stitchSize / 2)
    inWidth, inHeight = inImage.size
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

filename = 'plant.png'
stitches = 60
maxColors = 10
uploadedImage = Image.open('uploads/' + filename)
width, height = uploadedImage.size
blockSize = int(width / stitches)
width = int(width / blockSize) * blockSize
height = int(height / blockSize) * blockSize
processImage = uploadedImage.resize((width, height), Image.ANTIALIAS)
processImage = processImage.convert('P', palette=Image.ADAPTIVE, colors=maxColors)
#adjustedImage = uploadedImage.convert('P', palette=Image.ADAPTIVE, colors=maxColors)
processImage.putalpha(0)
colors = processImage.getcolors(maxColors)
#processImage = adjustedImage.resize((width, height), Image.ANTIALIAS)
patternImage = processImage.resize((int(width/blockSize) * 25, int(height/blockSize) * 25), Image.ANTIALIAS)
generatePattern(blockSize, 25, processImage, patternImage)
patternImage.show()
