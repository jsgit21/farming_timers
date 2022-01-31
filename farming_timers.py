from ast import Raise
from asyncio.windows_events import NULL
from doctest import master
from re import X
from textwrap import fill
import tkinter as tk
import time as tm
from turtle import back, width
from PIL import ImageTk, Image
from functools import partial
import datetime

allotments = [
    {"name":"Potato", "value":40, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Onion", "value":40, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Cabbage", "value":40, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Tomato", "value":40, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Sweetcorn", "value":60, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Strawberry", "value":60, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Watermelon", "value":80, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL},
    {"name":"Snapegrass", "value":70, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL}
]

label_dict = {}
# {0: {"label_name":Potato, "label_time":label_time}}
btn_list = []

# create the window
window = tk.Tk()
window.title("Farming timers")

icon_path = "D:\\Joe\\PythonWorkspace\\farming_timer_project\\farming_icons\\"

time_now = datetime.datetime.now()
current_time = time_now.strftime('%I:%M %p')


def update_time():
    time_now = datetime.datetime.now()
    current_time = time_now.strftime('%I:%M %p')
    time_label.config(text=current_time)
    time_label.after(60000, update_time)

def flatten_time():
    time_now = datetime.datetime.now()
    if time_now.second != 0:
        time_label.after(1000, flatten_time)
    else:
        time_label.config(text=current_time)
        update_time()

def calc_harvest_time(crop_growtime):
    time_change = datetime.timedelta(minutes=crop_growtime)
    time_now = datetime.datetime.now()
    harvest_time = time_now + time_change
    harvest_time = harvest_time.replace(second=0)
    
    # Round down the harvest time to account for cycles,
    # My allotment cycles occur every :05 :15 :25 :35 :45 :55
    while harvest_time.minute % 5 != 0 or harvest_time.minute % 10 == 0:
        harvest_time = harvest_time.replace(minute=harvest_time.minute-1)
    
    return harvest_time

def growth_countdown(n, remaining):
    hmmss = str(remaining).split(":")
    if hmmss[2] == 0:
        allotments[n]["remaining_label"].after(1000, )

def calc_growth_time(n, harvest_time):
    time_now = datetime.datetime.now()
    remaining_time = harvest_time - time_now
    allotments[n]["remaining_label"].configure(text=remaining_time, font='ariel 12', foreground="black")
    growth_countdown(n, remaining_time)

def plant(n):
    btn_name = (btn_list[n])
    allotments[n]["label_name"].configure(background="#d12424")
    harvest_time = calc_harvest_time(allotments[n]["value"])
    strharvest_time = harvest_time.strftime('%I:%M %p')
    allotments[n]["harvest_label"].configure(text=strharvest_time, font='ariel 12', foreground="black")
    calc_growth_time(n, harvest_time)


# Holding the time frame
time_frame = tk.Frame(master = window)
time_label = tk.Label(
    master = time_frame, 
    text = current_time,
    font='ariel 16',
    borderwidth=1,
    background="#75aaff"
)
time_label.pack(fill=tk.X)
time_frame.pack(fill=tk.X)
time_label.after(10, flatten_time)

# Holding the titles / column headers
title_frame = tk.Frame(master = window, background="purple")
crop_lbl = tk.Label(
    master = title_frame,
    text = "Crops",
    font='ariel 14',
    width=25
)
crop_lbl.pack(side=tk.LEFT)
crop_lbl = tk.Label(
    master = title_frame,
    text = "Harvest",
    font='ariel 14',
)
crop_lbl.pack(side=tk.LEFT)
title_frame.pack()

# Holding the grid for the allotments
main_frame = tk.Frame(master = window)
main_frame.pack()

for i in range(len(allotments)):

        # FRAME for holding image and name
        name_frame = tk.Frame(
            master = main_frame,
            relief = tk.FLAT,
            borderwidth = 1
            #,background="red"
        )
        name_frame.grid(row=i, column=0, padx=5, pady=5)

        # ---------------- CHILDREN OF name_frame ---------------- V
        pic = Image.open(icon_path + allotments[i]["name"] + ".png")
        #resized_image= pic.resize((55,45), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(pic)
        img = tk.Label(
            master = name_frame, 
            image = icon,
            anchor="n"
        )
        # keep image reference
        img.image = icon
        img.pack(side=tk.LEFT, padx=5)

        label = tk.Label(
            master = name_frame, 
            text = allotments[i]["name"],
            width=10,
            font='ariel 12'
        )
        label.pack(side=tk.LEFT, padx=5, pady=5)

        # assign label name identifier
        allotments[i]["label_name"] = label
        # ---------------- CHILDREN OF name_frame ---------------- A

        # FRAME for holding buttons
        btn_frame = tk.Frame(
            master = main_frame,
            relief = tk.FLAT
            #,background="blue"
        )
        btn_frame.grid(row=i, column=1, padx=5, pady=5)

        # ---------------- CHILDREN OF btn_frame ---------------- V
        btn_plant = tk.Button(
            master = btn_frame, 
            text="Plant", 
            width=8, height=2, 
            background="grey",
            command = partial(plant, i)    
        )
        btn_plant.pack(side=tk.LEFT, padx=5, pady=5)
        btn_list.append(btn_plant)
        # ---------------- CHILDREN OF btn_frame ---------------- A

        # FRAME for holding harvest timers
        harvest_time_frame = tk.Frame(
            master = main_frame,
            relief=tk.FLAT,
            #,background="yellow"
        )
        harvest_time_frame.grid(row=i, column=2, padx=5, pady=5)

        # ---------------- CHILDREN OF btn_frame ---------------- V
        harvest_time_label = tk.Label(
            master = harvest_time_frame,
            text = "--:--",
            foreground = "grey",
            width=8,
            font='ariel 12'
        )
        harvest_time_label.pack(side=tk.LEFT, padx=5, pady=5)

        # assign label name identifier
        allotments[i]["harvest_label"] = harvest_time_label

        elapsed_time_label = tk.Label(
            master = harvest_time_frame,
            text = "--:--",
            foreground = "grey",
            width=8,
            font='ariel 12'
        )
        elapsed_time_label.pack(side=tk.LEFT, padx=5, pady=5)
        allotments[i]["remaining_label"] = elapsed_time_label
        # ---------------- CHILDREN OF btn_frame ---------------- A





window.mainloop()