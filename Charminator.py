from PIL import Image
from pytesseract import pytesseract
import re

#Predefined locations on the image
#Skill A Level Left and Right
sall = 1007
salr = 1042
#Skill A Name Left and Right
sanl = 894
sanr = 1004
#Skill B Level Left and Right
sbll = 1157
sblr = 1193
#Skill B Name Left and Right
sbnl = 1045
sbnr = 1154
#Slots Left and Right
sl = 1196
sr = 1251
#Top and bottom of first talisman
top = 100
bot = 129

img = Image.open(r"Input\1.jpg")
outf = open("Output\mycharms.txt", "a")
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

#For loop of all 8 rows of the Talisman Menu
for i in range (0,8):
    #Multiply the counter by 32, the height of each row.
    x = 32 * i

    #Initilizing the output string
    outs = ""

    # Cropping and Grabbing the slots.
    imgt = img.crop((sl, top + x, sr, bot + x))
    imgt.show()
    out = input("How many slots? ")
    outs += out + ","

    #Cropping and reading the Name of Skill A.
    imgt = img.crop((sanl, top + x, sanr, bot + x))
    out = pytesseract.image_to_string(imgt)[:-2]
    outs += out + ","#Cropping and reading the Level of Skill A.
    imgt = img.crop((sall, top + x, salr, bot + x))
    out = pytesseract.image_to_string(imgt)[:-2]
    #Sometimes tesseract can't read the numbers... if the regex fails
    #then this Try Catch will ask the user what the image says
    try:
        out = re.findall("-*\d+", out)[0]
    except:
        imgt.show()
        out = input ("What does this say? ")
        out = re.findall("-*\d+", out)[0]
    outs += out + ","

    #Cropping and reading the Name of Skill B.
    imgt = img.crop((sbnl, top + x, sbnr, bot + x))
    out = pytesseract.image_to_string(imgt)[:-2]
    outs += out + ","

    #Cropping and reading the Level of Skill B.
    imgt = img.crop((sbll, top + x, sblr, bot + x))
    out = pytesseract.image_to_string(imgt)[:-2]
    #The same Try Catch as above.
    try:
        out = re.findall("-*\d+", out)[0]
    except:
        imgt.show()
        out = input ("What does this say? ")
        out = re.findall("-*\d+", out)[0]
    outs += out
    outf.write(outs)
