from PIL import Image as Img
from PIL import ImageTk as Imgtk
from pytesseract import pytesseract
from difflib import get_close_matches
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from functools import partial
import os, re, threading

skillList = ["Ammo Saver",
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
if not os.path.exists("Input"): os.mkdir("Input")
if not os.path.exists("Output"): os.mkdir("Output")
if not os.path.exists("Pages"): os.mkdir("Pages")
pgs = []
pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"


# A function for correcting incorrect skill names. Contains a list of all valid skills. Chonkier than intended.
def getskill(ins):
    return get_close_matches(ins, skillList, 1)[0]


# Called by the browse button on the input page of the gui. Gets the input directory and overwrites the existing field.
def getinfile():
    gui.infile = filedialog.askdirectory(title="Select Input Directory", mustexist=True, initialdir="Input")
    start[1].config(text=gui.infile)


# This is the correction center, it'll allow people to compare the results to the inputed images. I hope it looks cool!
class Tome:
    def __init__(nya, results, contents):
        nya.results = results
        nya.contents = contents

    def rescribe(nya, page, diff):
        global pgs
        for g in range(9):
            for h in range(5):
                nya.results[page][g][h] = pgs[(h + 1) + (5 * g)].get()
        for i in range(len(pgs)): pgs[i].destroy()
        nya.page(page + diff)

    def finale(nya, page):
        nya.rescribe(page, 0)
        outfile = open(filedialog.askdirectory(title="Export Charm List",
                                               mustexist=True,
                                               initialdir="Output") + "/mycharms.txt",
                       mode="w")
        for k in nya.results:
            for a in k:
                outfile.write(a[0] + "," + a[1] + "," + a[2] + "," + a[3] + "," + a[4] + "\n")
        outfile.close()
        gui.destroy()

    def page(nya, pg):
        global pgs
        pgs = []
        pagey = Imgtk.PhotoImage(Img.open("Pages/Page" + str(pg) + ".jpg"))
        pgs.append(Label(gui, image=pagey))
        # noinspection PyUnresolvedReferences
        pgs[0].image = pagey
        pgs[0].grid(column=0, columnspan=3, row=1, rowspan=9, sticky="news")
        for p in range(9):
            pgs.append(Combobox(gui, values=["0", "1", "2", "3"], width=1, justify=CENTER))
            pgs[1 + (5 * p)].set(nya.results[pg][p][0])
            pgs[1 + (5 * p)].grid(column=7, row=(1 + p))
            pgs.append(Combobox(gui, values=skillList, width=15, justify=LEFT))
            pgs[2 + (5 * p)].set(nya.results[pg][p][1])
            pgs[2 + (5 * p)].grid(column=3, row=(1 + p))
            pgs.append(Combobox(gui, width=3, justify=RIGHT))
            pgs[3 + (5 * p)].set(nya.results[pg][p][2])
            pgs[3 + (5 * p)].grid(column=4, row=(1 + p))
            pgs.append(Combobox(gui, values=skillList, width=15, justify=LEFT))
            pgs[4 + (5 * p)].set(nya.results[pg][p][3])
            pgs[4 + (5 * p)].grid(column=5, row=(1 + p))
            pgs.append(Combobox(gui, width=3, justify=RIGHT))
            pgs[5 + (5 * p)].set(nya.results[pg][p][4])
            pgs[5 + (5 * p)].grid(column=6, row=(1 + p))
        pgs.append(Button(gui, text="Prev", command=partial(nya.rescribe, pg, -1)))
        if pg == 0: pgs[46].config(state="disabled")
        pgs[46].grid(column=0, row=10, sticky="w")
        pgs.append(Button(gui, text="Next", command=partial(nya.rescribe, pg, 1)))
        if pg == nya.contents: pgs[47].config(state="disabled")
        pgs[47].grid(column=5, columnspan=3, row=10, sticky="e")
        pgs.append(Label(gui, text="Source Image"))
        pgs[48].grid(column=0, columnspan=3, row=0)
        pgs.append(Label(gui, text="Editable Results"))
        pgs[49].grid(column=3, columnspan=5, row=0)
        pgs.append(Button(gui, text="Finish", command=partial(nya.finale, pg)))
        pgs[50].grid(column=1, columnspan=4, row=10)


# Grabs a list of all files in the Input folder and allows the program to run through them all.
def core():
    # Predefined locations on the image
    # Skill A Level Left and Right
    sall = 1007
    salr = 1042
    # Skill A Name Left and Right
    sanl = 894
    sanr = 1004
    # Skill B Level Left and Right
    sbll = 1157
    sblr = 1193
    # Skill B Name Left and Right
    sbnl = 1045
    sbnr = 1154
    # Slots Left and Right
    sl = 1196
    sr = 1251
    # Top and bottom of first talisman
    top = 100
    bot = 129
    # Bottom of the chart
    bottom = 385

    # outcore will be a multidimensional array containing images and the output of the core of the program.
    # [
    #  [[skillA, levelA, skillB, levelB, slots], [skillA, levelA, skillB, levelB, slots]]
    #  [[skillA, levelA, skillB, levelB, slots], [skillA, levelA, skillB, levelB, slots]]
    #  [[skillA, levelA, skillB, levelB, slots], [skillA, levelA, skillB, levelB, slots]]
    # ]
    dirlist = os.listdir(gui.infile)
    outcore = []
    for switcher in start: switcher.destroy()
    progress = Progressbar(maximum=((len(dirlist) * 45) + 1), length=500)
    progress.grid(column=0, row=0)
    for l in range(len(dirlist)):
        outcore.append([])
        img = Img.open(gui.infile + "\\" + dirlist[l])
        img.crop((sanl, top, sr, bottom)).save("Pages\\Page" + str(l) + ".jpg")

        # For loop of all 9 rows of the Talisman Menu
        for i in range(9):
            outcore[l].append([])
            # Multiply the counter by 32, the height of each row.
            x = 32 * i

            # Cropping and reading the Slots by checking pixel lightness.
            imgt = img.crop((sl, top + x, sr, bot + x))
            ctrl = sum(imgt.getpixel((0, 0))) / 3  # Grabbing color of top left pixel.
            slots = 0
            for k in range(3):
                test = sum(imgt.getpixel((9 + (k * 18), 8))) / 3  # Grabbing colors of pixels that will be
                slots += 1 if (test - ctrl) > 25 else 0  # white if there is a slot there.

            outcore[l][i].append(str(slots))
            progress.step()

            # Cropping and reading the Name of Skill A.
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
            outcore[l][i].append(getskill(out))
            progress.step()

            # Cropping and reading the Level of Skill A.
            imgt = img.crop((sall, top + x, salr, bot + x))
            out = pytesseract.image_to_string(imgt)[:-2]
            # Sometimes tesseract can't read the numbers... if the regex fails
            # then this Try Catch will attempt to use single pixels to get the
            # correct output.
            try:
                out = re.findall("\d+", out)[0]
                out = "3" if out == "43" else out
            except:
                ctrl = sum(imgt.getpixel((0, 0))) / 3  # Another color test. Control.
                test1 = sum(imgt.getpixel((12, 15))) / 3  # Test for +10
                test2 = sum(imgt.getpixel((31, 14))) / 3  # Test for +5
                if (test1 - ctrl) > 25:
                    out = "10"
                elif (test2 - ctrl) > 25:
                    out = "5"
                else:
                    out = ""
            outcore[l][i].append(out)
            progress.step()

            # Cropping and reading the Name of Skill B.
            imgt = img.crop((sbnl, top + x, sbnr, bot + x))
            out = pytesseract.image_to_string(imgt)[:-2]
            ctrl = sum(imgt.getpixel((0, 0))) / 3
            test1 = sum(imgt.getpixel((9, 11))) / 3
            test2 = sum(imgt.getpixel((3, 10))) / 3
            test3 = sum(imgt.getpixel((2, 10))) / 3
            if (out == "" or out == " ") and (test1 - ctrl) > 30:
                out = "Status"
            elif (out == "" or out == " ") and (test2 - ctrl) > 30:
                out = "Sense"
            elif (out == "" or out == " ") and (test3 - ctrl) > 30:
                out = "Unscathed"
            elif out == "" or out == " ":
                out = ""
            outcore[l][i].append(getskill(out))
            progress.step()
            # if (out == "" or out == " "):
            #    imgt.save("Output\Bace." + str(l) + "." + str(i) + ".jpg")

            # Cropping and reading the Level of Skill B.
            imgt = img.crop((sbll, top + x, sblr, bot + x))
            out = pytesseract.image_to_string(imgt)[:-2]
            # The same Try Catch as above.
            try:
                out = re.findall("-*\d+", out)[0]
            except:
                ctrl = sum(imgt.getpixel((0, 0))) / 3
                test1 = sum(imgt.getpixel((10, 14))) / 3
                test2 = sum(imgt.getpixel((29, 8))) / 3
                test3 = sum(imgt.getpixel((32, 11))) / 3
                test4 = sum(imgt.getpixel((28, 21))) / 3
                test5 = sum(imgt.getpixel((21, 19))) / 3
                test6 = sum(imgt.getpixel((31, 15))) / 3
                test7 = sum(imgt.getpixel((32, 20))) / 3
                test8 = sum(imgt.getpixel((29, 10))) / 3
                test9 = sum(imgt.getpixel((31, 11))) / 3
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
            outcore[l][i].append(out)
            progress.step()
    progress.destroy()
    Tome(outcore, len(dirlist) - 1).page(0)


def corethread():
    threading.Thread(target=core).start()


gui = Tk()
gui.title("Mini's Charm List Image Transcriber for MHGU")
gui.infile = ""
start = [Label(gui, text="Input directory:"), Label(gui, relief=SUNKEN, width=60),
         Button(gui, text="Browse", command=getinfile), Button(gui, text="Start", command=corethread)]
start[0].grid(column=0, row=0, sticky=W)
start[1].grid(column=0, row=1)
start[2].grid(column=1, row=1)
start[3].grid(column=0, row=2, sticky="news", columnspan=2)
gui.mainloop()

