import os

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
#Bottom of the chart
bottom = 385

outf = open("Output\mycharms.txt", "w")
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

#A function for correcting incorrect skill names.
def autocorrect(ins):
    ins = "Elderfrost X"    if ins == "Eldertrost X"    else ins
    ins = "Stam Recov"      if ins == "StamRecov"       else ins
    ins = "Endurance"       if ins == "Enduronce"       else ins
    ins = "Maestro"         if ins == "Maestro,"        else ins
    ins = "Artillery"       if ins == "Antilery"        else ins
    ins = "Boltreaver"      if ins == "Bokreaver"       else ins
    ins = "Guard Up"        if ins == "Guard Up,"       else ins
    ins = "Bloodbath"       if ins == "Bloocbath"       else ins
    ins = "Crit Draw"       if ins == "Crit Drow"       else ins
    ins = "Normal Up"       if ins == "Nomol Up"        else ins
    ins = "Carnivore"       if ins == "Comivore"        else ins
    ins = "Pierce Up"       if ins == "Pierce Up."      else ins

    return ins

#Grabs a list of all files in the Input folder and allows the program to run through them all.
dirlist = os.listdir("Input")
for l in range (0,len(dirlist)):
    img = Image.open("Input\\" + dirlist[l])

    #For loop of all 9 rows of the Talisman Menu
    for i in range (0,9):
        #Multiply the counter by 32, the height of each row.
        x = 32 * i

        #Cropping and reading the Slots by checking pixel lightness.
        imgt = img.crop((sl, top + x, sr, bot + x))
        ctrl = sum(imgt.getpixel((0,0)))/3                  #Grabbing color of top left pixel.
        slots = 0
        for k in range (0,3):
            test = sum(imgt.getpixel((9 + (k * 18),8)))/3   #Grabbing colors of pixels that will be
            slots += 1 if (test - ctrl) > 25 else 0         #white if there is a slot there.

        #Initilizing the output string with the slot count.
        outs = str(slots) + ","


        #Cropping and reading the Name of Skill A.
        imgt = img.crop((sanl, top + x, sanr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        outs += autocorrect(out) + ","

        #Cropping and reading the Level of Skill A.
        imgt = img.crop((sall, top + x, salr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        #Sometimes tesseract can't read the numbers... if the regex fails
        #then this Try Catch will ask the user what the image says and save a copy of the copped image.
        try:
            out = re.findall("-*\d+", out)[0]
        except:
            imgt.show()
            imgt.save("Output\\" + str(l) + ".A." + str(i) + ".jpg")
            out = input ("What does this say? ")
            out = re.findall("-*\d+", out)[0]
        outs += out + ","

        #Cropping and reading the Name of Skill B.
        imgt = img.crop((sbnl, top + x, sbnr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        outs += autocorrect(out) + ","

        #Cropping and reading the Level of Skill B.
        imgt = img.crop((sbll, top + x, sblr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        #The same Try Catch as above.
        try:
            out = re.findall("-*\d+", out)[0]
        except:
            imgt.show()
            imgt.save("Output\\" + str(l) + ".B." + str(i) + ".jpg")
            out = input ("What does this say? ")
            out = re.findall("-*\d*", out)[0] if out != "" else ""
        outs += out + "\n"
        outf.write(outs)