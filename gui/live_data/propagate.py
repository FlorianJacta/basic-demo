from taipy.gui import Gui
from time import sleep
from math import sin

data = {
        "x":[],
        "y":[]
    }

page = """
<|button|label=start|on_action=start_button_pressed|>
<|{data}|chart|x=x|y=y|rebuild=True|propagate|>
"""

def start_button_pressed(state):
    global data
    x = 0
    while True:
        data['x'].append(x)
        data['y'].append(sin(x/3))
        state.refresh("data")
        x+=1
        sleep(0.02)

gui = Gui(page=page)

gui.run(port=4949)
