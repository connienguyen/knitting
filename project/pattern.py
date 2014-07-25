from PIL import Image

filename = 'clooney.jpg'
#filename = 'turkey.jpg'
stitches = 50
baseImage = Image.open('uploads/' + filename)
COLOR_BLACK = (0,0,0)
COLOR_GREY = (128, 128, 128)
COLOR_RED = (255, 0, 0)

# Colors an blockSize x blockSize pixel block + outlining grid
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

result = baseImage.convert('P', palette=Image.ADAPTIVE, colors=3)
result.putalpha(0)
colors = result.getcolors(3)
width, height = result.size
blockSize = 25
width = int(width / blockSize) * blockSize
height = int(height / blockSize) * blockSize
for i in range(0, width):
    for j in range (0, height):
	if( (i % blockSize == 0) and (j % blockSize == 0)):
	    colorBlock(blockSize, (i,j), result, result)
result.show()

#baseImage.show() #display image
