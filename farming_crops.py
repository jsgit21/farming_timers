
from asyncio.windows_events import NULL

# name: crop name
# cycles: number of cycles it takes to fully grow
# cycle_time: how long each cycle is
# label_name: reference to the label that holds crop name
# harvest_label: reference to the label that holds harvest time
# remaining_label: reference to the label that holds remaining growth time
# active: defines whether the timer is active already or not, so that it 
#         cannot be triggered more than once


allotments = [
    {"name":"Potato", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Onion", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Cabbage", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Tomato", "cycles": 4, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Sweetcorn", "cycles": 6, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Strawberry", "cycles": 6, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Watermelon", "cycles": 8, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False},
    {"name":"Snapegrass", "cycles": 7, "cycle_time":10, "label_name":NULL, "harvest_label":NULL, "remaining_label":NULL, "active":False, "reset":False}
]

def get_crop_type(type):
    return type