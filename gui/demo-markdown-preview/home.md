# Taipy Studio Gui Markdown Preview Demo

<|menu|lov={taipy_lov}|>

<|navbar|lov={navbar}|>

<|toggle|theme|>

## Basic Visual Elements

<|{text1}|> <| From Taipy |>

<|This is a button|button|>

<|{text2}|input|label=Editable Text|>

<|{x}|number|label=Editable Number|>

<|{mood}|toggle|lov={mood_lov}|>


### Slider

<|{x}|slider|min=1|max=50|>

<|{mood}|slider|lov={mood_lov}|labels|>

<|0|slider|lov={taipy_lov}|labels|orientation=v|>

### Selector

<|Item 2|selector|lov=Item 1;Item 2;Item 3|>

<|{mood}|selector|lov={mood_lov}|dropdown|>

<|Favorite Colors|>

<|Green|selector|lov=Red;Green;Blue;Orange;Pink;Purple|dropdown|multiple|>

<|Favorite Snacks|>

<|selector|lov=Chaussons aux Pommes;Les Fraises Tagada;Canistrelli;Pissaladière|filter|multiple|>

<|Best Taipy Product|>

<|selector|lov={taipy_lov}|>

### Date

<|date|not editable|>

<|date|not editable|with_time|>

<|{dob}|date|>

<|{dob}|date|with_time|>

### Indicator

<|10|indicator|format=%.2f|value={x}|min=0|max=20|>

<|This number is too large|indicator|min=0|max=9|value={x}|>

### An Image of Taipy

<|{taipy_image_path}|image|label=Taipy Image|>

<|file_download|label=File Download|>

<|file_selector|label=File Selector|drop_message=Drop Here|>

