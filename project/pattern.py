from PIL import Image

filename = 'clooney.jpg'
#filename = 'turkey.jpg'
stitches = 50
baseImage = Image.open('uploads/' + filename)
COLOR_BLACK = (0,0,0)
COLOR_GREY = (128, 128, 128)

# Make a function which colors an nxn pixel block of the output image
def colorBlock(blockSize, upperLeft, inImage, outImage):
    midBlock = int(blockSize / 2)
    blockColor = inImage.getpixel((upperLeft[0] + midBlock, upperLeft[1] + midBlock))
    for i in range(0, blockSize):
	for j in range(0, blockSize):
	    if i == blockSize -1 or j == blockSize -1:
		outImage.putpixel((upperLeft[0]+i, upperLeft[1]+j), COLOR_GREY)
	    else:
		outImage.putpixel((upperLeft[0] + i, upperLeft[1] + j), blockColor)

result = baseImage.convert('P', palette=Image.ADAPTIVE, colors=3)
result.putalpha(0)
colors = result.getcolors(3)
width, height = result.size
blockSize = 5
width = int(width / blockSize) * blockSize
height = int(height / blockSize) * blockSize
for i in range(0, width):
    for j in range (0, height):
	if( (i % blockSize == 0) and (j % blockSize == 0)):
	    colorBlock(blockSize, (i,j), result, result)
result.show()

#baseImage.show() #display image
