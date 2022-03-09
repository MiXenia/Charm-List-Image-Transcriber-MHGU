import os

from PIL import Image
from pytesseract import pytesseract
import re
from difflib import get_close_matches as findSkill

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

skilllist = ["Ammo Saver",
             "Amplify",
             "Anti-Chameleos",
             "Anti-Kushala",
             "Anti-Teostra",
             "Anti-Theft",
             "Artillery",
             "Attack",
             "Avarice",
             "Bherna",
             "Bind Res",
             "Biology",
             "Bladescale",
             "Blast C+",
             "Bleeding",
             "Blight Res",
             "Bloodbath",
             "Bloodbath X",
             "Blunt",
             "Boltreaver",
             "Boltreaver X",
             "Bomb Boost",
             "Botany",
             "Brawn",
             "Brutality",
             "Bubble",
             "C.beard",
             "C.Range C+",
             "Capturer",
             "Carnivore",
             "Carving",
             "Chain Crit",
             "Chance",
             "Charmer",
             "Clust S+",
             "Cold Res",
             "ColdBlooded",
             "Combo Plus",
             "Combo Rate",
             "Constitution",
             "Covert",
             "Crag S+",
             "Crisis",
             "Crit Draw",
             "Crit Element",
             "Crit Status",
             "Critical Up",
             "Crystalbeard X",
             "D. Fencing",
             "Dead Eye",
             "Deadeye",
             "Deadeye X",
             "Def Lock",
             "Defense",
             "Destroyer",
             "Distance Runner",
             "Dragon Atk",
             "Dragon Res",
             "Dragon Spirit",
             "Dreadking",
             "Dreadking X",
             "Dreadqueen",
             "Dreadqueen X",
             "Drilltusk",
             "Drilltusk X",
             "Eating",
             "Edge Lore",
             "Edgemaster",
             "Elderfrost",
             "Elderfrost X",
             "Elem C+",
             "Elemental",
             "Endurance",
             "Evade Dist",
             "Evasion",
             "Exhaust C+",
             "Expert",
             "FastCharge",
             "Fate",
             "Fencing",
             "Fire Atk",
             "Fire Res",
             "Flying Pub",
             "Frenzy Res",
             "Furor",
             "Fury",
             "Gathering",
             "Gloves Off",
             "Gluttony",
             "Grimclaw",
             "Grimclaw X",
             "Grinder",
             "Guard",
             "Guard Up",
             "Guts",
             "Handicraft",
             "Haphazard",
             "Health",
             "Hearing",
             "Heat Res",
             "Heavy Up",
             "Hellblade",
             "Hellblade X",
             "Hero Shield",
             "Hoarding",
             "Honey",
             "HotBlooded",
             "Hunger",
             "Ice Atk",
             "Ice Res",
             "Insight",
             "KO",
             "Kokoto",
             "Lasting Pwr",
             "Light Eater",
             "Loading",
             "Maestro",
             "Mechanic",
             "Mounting",
             "Mycology",
             "Negative Crit",
             "Nightcloak",
             "Nightcloak X",
             "Nimbleness",
             "Normal S+",
             "Normal Up",
             "Para C+",
             "Paralysis",
             "Pellet S+",
             "Pellet Up",
             "Perception",
             "Pierce S+",
             "Pierce Up",
             "Poison",
             "Poison C+",
             "Pokke",
             "Potential",
             "Power C+",
             "PowerEater",
             "Prayer",
             "Precision",
             "Prolong SP",
             "Protection",
             "Prudence",
             "Psychic",
             "Punish Draw",
             "Ranger",
             "Rapid Fire",
             "Readiness",
             "Rec Level",
             "Rec Speed",
             "Recoil",
             "Redhelm",
             "Redhelm X",
             "Reload Spd",
             "Resilience",
             "Rustrazor",
             "Rustrazor X",
             "Secret Arts",
             "Sense",
             "Sharpener",
             "Sharpness",
             "Sheathe Sharpen",
             "Sheathing",
             "Silverwind",
             "Silverwind X",
             "Sleep",
             "Sleep C+",
             "Snowbaron",
             "Snowbaron X",
             "Soaratorium",
             "Soulseer",
             "Soulseer X",
             "Speed Setup",
             "Spirit",
             "Stalwart",
             "Stam Drain",
             "Stam Recov",
             "Stamina",
             "Status",
             "Status Res",
             "SteadyHand",
             "Stonefist",
             "Stonefist X",
             "Stun",
             "Survivor",
             "Talisman Boost",
             "Team Player",
             "TeamLeader",
             "Tenderizer",
             "Thunder Atk",
             "Thunder Res",
             "Thunderlord",
             "Thunderlord X",
             "Transporter",
             "Tremor Res",
             "Unscathed",
             "Vault",
             "Water Atk",
             "Water Res",
             "Whim",
             "Wide-Range",
             "Wind Res",
             "Yukumo",
             ""
             ]

outf = open("Output\mycharms.txt", "w")
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

#A function for correcting incorrect skill names.
#def autocorrect(ins):
#    ins = "Elderfrost X"    if ins == "Eldertrost X"    else ins
#    ins = "Stam Recov"      if ins == "StamRecov"       else ins
#    ins = "Endurance"       if ins == "Enduronce"       else ins
#    ins = "Maestro"         if ins == "Maestro,"        else ins
#    ins = "Artillery"       if ins == "Antilery"        else ins
#    ins = "Boltreaver"      if ins == "Bokreaver"       else ins
#    ins = "Guard Up"        if ins == "Guard Up,"       else ins
#    ins = "Bloodbath"       if ins == "Bloocbath"       else ins
#    ins = "Crit Draw"       if ins == "Crit Drow"       else ins
#    ins = "Normal Up"       if ins == "Nomol Up"        else ins
#    ins = "Carnivore"       if ins == "Comivore"        else ins
#    ins = "Pierce Up"       if ins == "Pierce Up."      else ins
#    ins = "Defense"         if ins == "Defense:"        else ins
#    ins = "Heavy Up"        if ins == "Heavy Up."       else ins
#    ins = "Nightcloak"      if ins == "Nightclock"      else ins
#    ins = "Punish Draw"     if ins == "Punish Drow"     else ins
#    ins = "Wide-Range"      if ins == "Wide-Ronge"      else ins
#    ins = "TeamLeader"      if ins == "TeamLeoder"      else ins
#    ins = "Charmer"         if ins == "Chamer"          else ins
#    ins = "Dead Eye"        if ins == "DeadEye"         else ins
#    ins = "Redhelm"         if ins == "Redheim"         else ins
#    ins = "Sheathing"       if ins == "Shecthing"       else ins
#    ins = "TeamLeader"      if ins == "Teomleader"      else ins
#    ins = "Ammo Saver"      if ins == "Ammo Saver:"     else ins
#    ins = "TeamLeader"      if ins == "Teomleoder"      else ins
#    ins = "TeamLeader"      if ins == "TeomLeader"      else ins
#    ins = "Wind Res"        if ins == "Vind Res"        else ins
#    ins = "Crit Status"     if ins == "Crit Status,"    else ins
#    ins = "Tremor Res"      if ins == "Tremor Res,"     else ins
#    ins = "Ice Atk"         if ins == "ke Atk"          else ins
#    ins = "Normal S+"       if ins == "Nomol $+"        else ins
#    ins = "Pierce S+"       if ins == "Pierce St"       else ins
#    ins = "Clust S+"        if ins == "Chst $+"         else ins
#    ins = "Carnivore"       if ins == "Comnivore"       else ins
#    ins = "Lasting Pwr"     if ins == "Lasting Per"     else ins
#    ins = "Haphazard"       if ins == "Hophazard)"      else ins
#    ins = "Crag S+"         if ins == "CragS+"          else ins
#    ins = "Bind Res"        if ins == "BindRes"         else ins
#    ins = "Maestro"         if ins == "Moestro"         else ins
#    ins = "Prolong SP"      if ins == "Prolong SP."     else ins
#    ins = "Transporter"     if ins == "Tronsporter"     else ins
#    ins = "Haphazard"       if ins == "Hophazard"       else ins
#    ins = "Botany"          if ins == "Botony"          else ins
#    ins = "Stun"            if ins == "stun"            else ins
#    ins = "Whim"            if ins == "whim"            else ins
#    ins = "Ice Res"         if ins == "IceRes"          else ins
#    ins = "Rec Level"       if ins == "Rec Level,"      else ins
#    ins = "Health"          if ins == "Heath"           else ins
#    ins = "Mounting"        if ins == "Mounting,"       else ins
#    return ins

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
        ctrl = sum(imgt.getpixel((0, 0))) / 3
        test1 = sum(imgt.getpixel((50, 13))) / 3
        test2 = sum(imgt.getpixel((44, 13))) / 3
        test3 = sum(imgt.getpixel((3, 14))) / 3
        if (out == "" or out == " ") and (test1 - ctrl) > 30:
            out = "Blight Res"
        elif (out == "" or out == " ") and (test2 - ctrl) > 30:
            out = "Charmer"
        elif (out == "" or out == " ") and (test3 - ctrl) > 30:
            out = "KO"
        elif out == "" or out == " ":
            out = ""
        outs += findSkill(out, skilllist, 1)[0] + ","

        #Cropping and reading the Level of Skill A.
        imgt = img.crop((sall, top + x, salr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        #Sometimes tesseract can't read the numbers... if the regex fails
        #then this Try Catch will attempt to use single pixels to get the
        #correct output.
        try:
            out = re.findall("\d+", out)[0]
            out = "3" if out == "43" else out
        except:
            ctrl = sum(imgt.getpixel((0, 0)))/3     #Another color test. Control.
            test1 = sum(imgt.getpixel((12,15)))/3   #Test for +10
            test2 = sum(imgt.getpixel((31,14)))/3   #Test for +5
            if (test1 - ctrl) > 25:
                out = "10"
            elif (test2 - ctrl) > 25:
                out = "5"
            else:
                out = ""
        outs += out + ","

        #Cropping and reading the Name of Skill B.
        imgt = img.crop((sbnl, top + x, sbnr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        ctrl = sum(imgt.getpixel((0,0)))/3
        test1 = sum(imgt.getpixel((9,11)))/3
        test2 = sum(imgt.getpixel((3,10)))/3
        test3 = sum(imgt.getpixel((2,10)))/3
        if (out == "" or out == " ") and (test1 - ctrl) > 30:
            out = "Status"
        elif (out == "" or out == " ") and (test2 - ctrl) > 30:
            out = "Sense"
        elif (out == "" or out == " ") and (test3 - ctrl) > 30:
            out = "Unscathed"
        elif (out == "" or out == " "):
            out = ""
        outs += findSkill(out, skilllist, 1)[0] + ","
        if (out == "" or out == " "):
            imgt.save("Output\Bace." + str(l) + "." + str(i) + ".jpg")

        #Cropping and reading the Level of Skill B.
        imgt = img.crop((sbll, top + x, sblr, bot + x))
        out = pytesseract.image_to_string(imgt)[:-2]
        #The same Try Catch as above.
        try:
            out = re.findall("-*\d+", out)[0]
        except:
            ctrl = sum(imgt.getpixel((0,0)))/3
            test1 = sum(imgt.getpixel((10,14)))/3
            test2 = sum(imgt.getpixel((29,8)))/3
            test3 = sum(imgt.getpixel((32,11)))/3
            test4 = sum(imgt.getpixel((28,21)))/3
            test5 = sum(imgt.getpixel((21,19)))/3
            test6 = sum(imgt.getpixel((31,15)))/3
            test7 = sum(imgt.getpixel((32,20)))/3
            test8 = sum(imgt.getpixel((29,10)))/3
            test9 = sum(imgt.getpixel((31,11)))/3
            if (test1 - ctrl) > 30:
                out = "10"
            elif (test2 - ctrl) > 30:
                if (test3 - ctrl) > 30:
                    out = "-3"
                else:
                    out = "-5"
            elif (test4 - ctrl) > 30:
                out = "-2"
            elif (test5 - ctrl) > 30:
                out = "1"
            elif (test6 - ctrl) > 30:
                if (test7 - ctrl) > 30:
                    out = "-1"
                else:
                    out = "-9"
            elif (test8 - ctrl) > 30:
                out = "-8"
            elif (test9 - ctrl) > 30:
                out = "-6"
            else:
                out = ""
        outs += out + "\n"
        if outs != "0,,,,\n":
            outf.write(outs)