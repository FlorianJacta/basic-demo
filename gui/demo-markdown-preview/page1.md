# Taipy Studio Gui Markdown Preview Demo

<|menu|lov={taipy_lov}|>

<|navbar|lov={navbar}|>

<|toggle|theme|>
## Table

### With Mock JSON data

<|{data_mock}|table|columns=firstName;lastName;age|>

### With external JSON files

<|{data_json}|table|>

### With external CSV files

<|{data_csv}|table|>

### Chart

<|{data_mock}|chart|x=id|y=age|title=Age line chart|>
