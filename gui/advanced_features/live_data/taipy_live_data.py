import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
from taipy.gui import Gui, invoke_long_callback, notify

# read csv from a github repo
dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# read csv from a URL
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()
count_married = 0

selected_job = df.loc[0, "job"]
df_job = df[df["job"] == selected_job]
df_job["age_new"] = df_job["age"] * np.random.choice(range(1, 5))
df_job["balance_new"] = df_job["balance"] * np.random.choice(range(1, 5))

page = """
<|container|
# Real-Time / Live Data Science Dashboard

<|{selected_job}|selector|lov={pd.unique(df["job"])}|dropdown|class_name=fullwidth|label=Select the Job|on_change=change_job|>

<|1 1 1|layout|
Age ⏳
<|{int(np.mean(df_job["age_new"]))}|text|class_name=h2|>

Married Count 💍
<|{count_married}|text|class_name=h2|>

A/C Balance 💲
<|{f'$ ' + str(round(np.mean(df_job['balance_new']),2))}|text|class_name=h2|>
|>

<|1 1|layout|gap=50px|
<| 
### First Chart

<|{df_job}|chart|type=histogram2d|y=age_new|x=marital|>
|>

<| 
### Second Chart 📊

<|{df_job}|chart|type=histogram|x=age_new|>
|>
|>

### Detailed Data View
<|{df_job}|table|>
|>
"""

     
def change_job(state):
    notify(state, "info", f'Changing to {state.selected_job}...')
    state.df_job = state.df[state.df["job"] == state.selected_job]
    notify(state, "success", f'Changed to {state.selected_job}!')

def update(state):
    with state as s:
        s.df_job["age_new"] = s.df_job["age"] * np.random.choice(range(1, 5))
        s.df_job["balance_new"] = s.df_job["balance"] * np.random.choice(range(1, 5))

        s.count_married = int(
            s.df_job.loc[(s.df_job["marital"] == "married"),"marital"].count()
            + np.random.choice(range(1, 30))
        )
        s.refresh("df_job")

def iddle():
     while True:
          time.sleep(1)

def on_init(state):
    invoke_long_callback(state, iddle, [], update, [], 1000)

Gui(page).run(title="Real-Time Data Science Dashboard", port=4840)