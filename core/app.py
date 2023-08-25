import taipy as tp
import pandas as pd

from taipy.gui import notify, State
from config.config import *

scenario = None
df_metrics = None
data_node = None
default_data = {"x":[0], "y":[0]}

def on_init(state):
    maes = []
    names = []

    for scenario in tp.get_scenarios():
        evaluation = scenario.evaluation.read()
        maes.append(evaluation)
        names.append(scenario.name)
    
    state.df_metrics = pd.DataFrame({"Names": names, "MAE": maes})



# ------------------- Scenario Page -------------------

day = None

scenario_md = """
<|1 1|layout|
<|{scenario}|scenario_selector|>

**Day of prediction**
<|{scenario.day.read() if scenario else None}|date|on_change=save|>
|>

<|{scenario}|scenario|>
<|{scenario}|scenario_dag|>
"""


def save(state:State, var, val):
    if state.scenario:
        state.scenario.day.write(val.replace(tzinfo=None))
        notify(state, 's', f"Scenario {state.scenario.name} saved")


# ------------------- Data Node Page -------------------
def is_dataframe(obj):
    if obj is not None:
        return (isinstance(obj.read(), pd.DataFrame) or isinstance(obj.read(), pd.Series))
    return False

def return_dataframe(obj):
    return pd.DataFrame(obj.read()) if is_dataframe(obj) else default_data

def return_text(obj):
    if obj is not None:
        return obj.read() if not is_dataframe(obj) else ''
    return ''

datanode_selector = """
<|{data_node}|data_node_selector|>

------

<|part|render={is_dataframe(data_node)}|
<|layout|columns=1 1|
<|{return_dataframe(data_node)}|table|width=fit-content|rebuild|>

<|{return_dataframe(data_node)}|chart|rebuild|>
|>
|>

<|part|render={not is_dataframe(data_node)}|
<|{return_text(data_node)}|text|>
|>
"""

# ------------------- Comparison Page -------------------
comparison_md = "<|{df_metrics}|chart|x=Names|y=MAE|type=bar|>"


pages = {'/':'<|navbar|> <|toggle|theme|> <br/>',
         'Scenario': scenario_md,
         'Data-Node': datanode_selector,
         "Comparison": comparison_md}


if __name__ == "__main__":
    tp.Core().run()

    tp.Gui(pages=pages).run(port=4999)