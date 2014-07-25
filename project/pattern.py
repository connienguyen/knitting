from PIL import Image

COLOR_BLACK = (0,0,0)
COLOR_GREY = (128, 128, 128)

# Colors an blockSize x blockSize pixel block + outlining grid
# TO DO: Change to take in a color
def colorBlock(blockSize, upperLeft, inImage, outImage):
    midBlock = int(blockSize / 2)
    blockColor = inImage.getpixel((upperLeft[0] + midBlock, upperLeft[1] + midBlock))
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

filename = 'plant.png'
stitches = 30
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
processImage.show()
for i in range(0, width):
    for j in range (0, height):
	if( (i % blockSize == 0) and (j % blockSize == 0)):
	    colorBlock(blockSize, (i,j), processImage, processImage)
processImage.show()
