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
import os

allotments = [
    {"name":"Potato", "cycles": 1, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Onion", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Cabbage", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Tomato", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Sweetcorn", "cycles": 6, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Strawberry", "cycles": 6, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Watermelon", "cycles": 8, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False},
    {"name":"Snapegrass", "cycles": 7, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False}
]

label_dict = {}
# {0: {"label_name":Potato, "label_time":label_time}}
btn_list = []

# create the window
window = tk.Tk()
window.title("Farming timers")

cwd = os.getcwd()
icon_path = cwd + "\\farming_icons\\"

time_now = datetime.datetime.now()
current_time = time_now.strftime('%I:%M %p')


def update_time():
    # Update time every minute
    time_now = datetime.datetime.now()
    current_time = time_now.strftime('%I:%M %p')
    time_label.config(text=current_time)
    time_label.after(60000, update_time)

def flatten_time():
    # Wait for time to hit 00 seconds then update every minute
    time_now = datetime.datetime.now()
    if time_now.second != 0:
        time_label.after(1000, flatten_time)
    else:
        time_label.config(text=current_time)
        update_time()

def calc_harvest_time(crop):
    # Eventually this offset must be recieved from the user on the GUI (0-15)
    player_offset = 5

    offset_mins = datetime.timedelta(minutes=player_offset)
    cycle_time = crop["cycle_time"]
    num_cycles = crop["cycles"]

    #print("Crop: " + str(crop))
    crop_growtime = num_cycles*cycle_time
    #print("crop_growtime: " + str(crop_growtime))
    time_change = datetime.timedelta(minutes=crop_growtime)
    plant_time = datetime.datetime.now()

    # Calculate harvest duration
    adj_plant_time = plant_time + offset_mins
    #print("adj_plant_time = plant_time + offset_mins: " + str(plant_time) + " + " + str(offset_mins) + " = " + str(adj_plant_time))
    adj_harvest_time = adj_plant_time + time_change
    #print("adj_harvest_time = adj_harvest_time + time_change: " + str(adj_harvest_time) + " + " + str(time_change) + " = " + str(adj_harvest_time))
    
    # Round down the harvest time to account for cycles
    one_min = datetime.timedelta(minutes=1)
    # cycle_time 10 for allotments :00 :10 :20 :30 :40 :50
    if cycle_time == 10:
        while adj_harvest_time.minute % 10 != 0:
            adj_harvest_time = adj_harvest_time - one_min
    adj_harvest_time = adj_harvest_time.replace(second=0, microsecond=0)
    #print("Rounded adj_harvest_time: " + str(adj_harvest_time))

    actual_growtime = adj_harvest_time - adj_plant_time
    #print("actual_growtime = adj_harvest_time - adj_plant_time: " + str(adj_harvest_time) + " - " + str(adj_plant_time) + " = " + str(actual_growtime))
    harvest_time = plant_time + actual_growtime
    #print("harvest_time = plant_time + actual_growtime: " + str(plant_time) + " + " + str(actual_growtime) + " = " + str(harvest_time))
    return harvest_time

def handle_growth_time(n, harvest_time):
    time_now = datetime.datetime.now()
    time_now = time_now.replace(microsecond=0)

    if harvest_time >= time_now:
        remaining_time = harvest_time - time_now
        allotments[n]["remaining_label"].configure(text=remaining_time, font='ariel 12', foreground="black")
        allotments[n]["remaining_label"].after(1000, handle_growth_time, n, harvest_time)
    else:
        allotments[n]["label_name"].configure(background="#86d474")
        allotments[n]["active"] = False

        

def plant(n):
    btn_name = (btn_list[n])
    if allotments[n]["active"] is False:
        allotments[n]["active"] = True
        allotments[n]["label_name"].configure(background="#d12424")
        harvest_time = calc_harvest_time(allotments[n])
        harvest_time = harvest_time.replace(microsecond=0) # flatten harvest time
        strharvest_time = harvest_time.strftime('%I:%M %p')
        allotments[n]["harvest_label"].configure(text=strharvest_time, font='ariel 12', foreground="black")
        handle_growth_time(n, harvest_time)


# Holding the time frame
time_frame = tk.Frame(master = window)
time_label = tk.Label(
    master = time_frame, 
    text = current_time,
    font='ariel 16',
    borderwidth=1,
    background="#86d474"
)
time_label.pack(fill=tk.X)
time_frame.pack(fill=tk.X)
time_label.after(10, flatten_time)

# # Holding the titles / column headers
# title_frame = tk.Frame(master = window, background="purple")
# crop_lbl = tk.Label(
#     master = title_frame,
#     text = "Crops",
#     font='ariel 14',
#     width=25
# )
# crop_lbl.pack(side=tk.LEFT)
# crop_lbl = tk.Label(
#     master = title_frame,
#     text = "Harvest",
#     font='ariel 14',
# )
# crop_lbl.pack(side=tk.LEFT)
# title_frame.pack()

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

        remaining_time_label = tk.Label(
            master = harvest_time_frame,
            text = "--:--",
            foreground = "grey",
            width=8,
            font='ariel 12'
        )
        remaining_time_label.pack(side=tk.LEFT, padx=5, pady=5)
        allotments[i]["remaining_label"] = remaining_time_label
        # ---------------- CHILDREN OF btn_frame ---------------- A





window.mainloop()