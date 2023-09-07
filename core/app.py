import taipy as tp
import pandas as pd

from config.config import *

scenario = None
df_metrics = None
data_node = None

def update_comparison(state):
    maes, names = [], []

    for scenario in tp.get_scenarios():
        evaluation = scenario.evaluation.read()
        maes.append(evaluation)
        names.append(scenario.name)
    
    state.df_metrics = pd.DataFrame({"Names": names, "MAE": maes})


# ------------------- Scenario Page -------------------
jobs = []
day = None

scenario_md = """
<|1 3 4|layout|
<|{scenario}|scenario_selector|>

**Day of prediction**
<|{scenario.day if scenario else None}|data_node|>

**Scenario**
<|{scenario}|scenario|>
|>

<|{jobs}|job_selector|>
<|{scenario}|scenario_dag|>
"""

# ------------------- Data Node Page -------------------
datanode_selector = """
<|1 5|layout|
<|{data_node}|data_node_selector|>

<|{data_node}|data_node|scenario={scenario}|>
|>
"""

# ------------------- Comparison Page -------------------
comparison_md = """
<|{df_metrics}|chart|x=Names|y=MAE|type=bar|>
"""

def on_navigate(state, page_name):
    if page_name == "Comparison":
        update_comparison(state)
    return page_name


pages = {'/':'<|navbar|> <|toggle|theme|> <br/>',
         'Scenario': scenario_md,
         'Data-Node': datanode_selector,
         "Comparison": comparison_md}


if __name__ == "__main__":
    tp.Core().run()

    tp.Gui(pages=pages).run(port=4999)