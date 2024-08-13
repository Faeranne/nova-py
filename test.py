import numpy
import hid
from PIL import Image,ImageDraw

VID=0x1038
PID=0x12e0

def parseImageToMessages(img):
    #Image is a 1-bit color image.
    imgBytes = img.tobytes()
    npPack = numpy.frombuffer(imgBytes,dtype=numpy.uint8)
    #because image is 1-bit color, this breaks the uint8 entries into individual bits to work with
    npPixels = numpy.unpackbits(npPack)
    #The next two lines handle swapping the x and y axis of the bits, since the display receives pixels by columns
    npPixelRows = numpy.split(npPixels,64)
    npMergedColumns = numpy.stack(npPixelRows,1)
    #Pillow returns images in big-eiden format, but our display reads in little-eiden format.
    npFixedPack = numpy.packbits(npMergedColumns,bitorder='little')
    imgFixedBytes = npFixedPack.tobytes()
    #Split the bytes into 2 arrays, exactly in half, so we get 2 arrays of 64x64 pixels (4096 bits)
    #This is because the HID message maxes out at 1024 bytes, and 6 of our bytes are eaten up by the magic numbers needed below
    a = list(imgFixedBytes)[:len(imgFixedBytes)//2]
    b = list(imgFixedBytes)[len(imgFixedBytes)//2:]
    #0x06 is the data direction... (I think?  it's HID weirdness)
    #0x93 is the ... command code? for writing to the display... I think... again.
    #0,0 is the x,y to start drawing to the screen.
    #64,64 is the width and height of the block of pixels being sent
    message1 = tuple([0x06,0x93,0,0,64,64]+a)
    message2 = tuple([0x06,0x93,64,0,64,64]+b)
    return (message1,message2)

def drawImageToDev(img,dev):
    message1,message2 = parseImageToMessages(img)
    dev.send_feature_report(message1)
    dev.send_feature_report(message2)

devInput = hid.device()
devOutput = hid.device()

input_path = b''

for dev in hid.enumerate(0x1038,0x12e0):
    #We have to grab the specific endpoints.  endpoint 4 is our transmit, and endpoint 3 is our receive
    if dev['interface_number']==4:
        input_path = dev['path']
    if dev['interface_number']==3:
        output_path = dev['path']

#This is a test case.
print(input_path)
try:
    devInput.open_path(input_path)
    devOutput.open_path(output_path)
    im = Image.new("1",(128,64))
    draw = ImageDraw.Draw(im)
    #draw.line((0,0)+(128,64), fill=128)
    drawImageToDev(im,devInput)
finally:
    devInput.close()
    devOutput.close()
