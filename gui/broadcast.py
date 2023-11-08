from taipy.gui import Gui, State, broadcast_callback
from threading import Thread, Event
from time import sleep

counter = 0

# Thread management
thread = None
thread_event = Event()
timer_status = "Timer stopped"

client_index = 1
user_name = ""
button_texts = ["Start", "Stop"]
# Text in the start/stop button (initially "Start")
button_text = button_texts[0]


def on_init(state: State):
    global client_index
    state.user_name = f"Client_{client_index}"
    client_index = client_index+1

# Invoked by the timer
def update_counter(state: State, c):
    # Update all clients
    state.broadcast("counter", c)

def count(event, gui):
    while not event.is_set():
        global counter
        counter = counter + 1
        broadcast_callback(gui, update_counter, [counter])
        sleep(2)


# Start or stop the timer when the button is pressed
def start_or_stop(state):
    status = ""
    global thread
    if thread:  # Timer is running
        thread_event.set()
        thread = None
        status = "stopped"
    else:  # Timer is stopped
        thread_event.clear()
        thread = Thread(target=count, args=[thread_event, state.get_gui()])
        thread.start()
        status = "started"
    # Update statuses.
    with state:
        state.broadcast("timer_status", f"Timer {status} by {state.user_name}")
        state.timer_status = f"You {status} the timer"
        state.button_text = button_texts[1 if thread else 0]


page = """# Broadcasting values

User name: <|{user_name}|input|>

<|{timer_status}|>

Counter: <|{counter}|>

Timer: <|{button_text}|button|on_action=start_or_stop|>
"""

# Declare "button_text" as a shared variable.
# Assigning a value to a state's 'button_text' property is propagated to all clients
Gui.add_shared_variable("button_text")

Gui(page).run()
