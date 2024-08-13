import numpy
import hid
from PIL import Image,ImageDraw

def parseImageToMessages(img):
    imgBytes = img.tobytes()
    npPack = numpy.frombuffer(imgBytes,dtype=numpy.uint8)
    npPixels = numpy.unpackbits(npPack)
    npPixelRows = numpy.split(npPixels,64)
    npMergedColumns = numpy.stack(npPixelRows,1)
    npFixedPack = numpy.packbits(npMergedColumns,bitorder='little')
    imgFixedBytes = npFixedPack.tobytes()
    a = list(imgFixedBytes)[:len(imgFixedBytes)//2]
    b = list(imgFixedBytes)[len(imgFixedBytes)//2:]
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
    if dev['interface_number']==4:
        input_path = dev['path']
    if dev['interface_number']==3:
        output_path = dev['path']

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
