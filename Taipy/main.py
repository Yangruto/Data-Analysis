import pandas as pd
from taipy.gui import Gui
import taipy.gui.builder as tgb

""" 
DEMO

value = 10

def compute_data(decay:int)->list:
    return [cos(i / 6) * exp(-i * decay / 600) for i in range(100)]

def slider_moved(state):
    state.data = compute_data(state.value)

with tgb.Page() as page:
    tgb.text(value="# Taipy Getting Started", mode="md")
    tgb.text(value="Value: {value}")
    tgb.slider(value="{value}", on_change=slider_moved)
    tgb.chart(data="{data}")

data = compute_data(value)
"""

def on_change(state, var_name, var_value):
    if var_name == 'start_station':
        state.start_station = var_value 
        if var_value == None:
            state.pivot_mrt_id = station_list
        else:
            state.pivot_mrt_id = [var_value]
    elif var_name == 'destination':
        state.destination = var_value
        if var_value == None:
            state.pivot_mrt_column = ['from'] + partent_pivot_mrt['from'].to_list()
        else:
            state.pivot_mrt_column = ['from', var_value]
    state.child_pivot_mrt = partent_pivot_mrt.loc[partent_pivot_mrt['from'].isin(state.pivot_mrt_id), state.pivot_mrt_column]
    if len(state.pivot_mrt_column) + len(state.pivot_mrt_id) == 3:
        state.route = get_route(state.start_station, state.destination)

def get_route(start, end):
    route  = eval(taipei_mrt.loc[(taipei_mrt['from'] == start) & (taipei_mrt['to'] == end), 'route'].values[0])
    route = pd.DataFrame(route, columns=['station'])
    route['tag'] = 'Station'
    route.loc[route['station']=='換線', 'tag'] = 'Transition'
    route.loc[[0, len(route)-1], 'tag'] = 'Endpoint'
    route['Colors'] = route['tag'].map({'Endpoint':'green', 'Transition':'red', 'Station':'blue'})
    route['y'] = 0
    route['Sizes'] = 45
    route['x'] = route.index
    return route

with tgb.Page() as page:
    tgb.text(value="## Taipy for Taipei MRT", mode="md")
    tgb.text(value="Start Station: {start_station}")
    tgb.selector("{start_station}", lov="{station_list}", dropdown=True, filter=True, width="180px", height="20px", on_change=on_change)
    tgb.text(value="Destination: {destination}")
    tgb.selector("{destination}", lov="{station_list}", dropdown=True, filter=True, width="180px", height="20px", on_change=on_change)
    tgb.text(value="### Travel Time", mode="md")
    tgb.table("{child_pivot_mrt}", rebuild=True)
    tgb.text(value="### Route", mode="md")
    tgb.chart("{route}", mode="markers+text", x="x", y="y", marker="{marker}", layout="{layout}", rebuild=True, text="station")

if __name__ == "__main__":
    taipei_mrt = pd.read_csv('taipei_mrt.csv')
    station_list = taipei_mrt['from'].unique().tolist()
    partent_pivot_mrt = taipei_mrt.pivot_table(index='from', columns='to', values='time').reset_index()
    child_pivot_mrt = partent_pivot_mrt.copy()
    pivot_mrt_column = ['from'] + partent_pivot_mrt['from'].to_list()

    pivot_mrt_id = station_list
    start_station = None
    destination = None
    route = None
    marker = {"color": "Colors", "size":"Sizes"}
    layout = {"showlegend": False,
    "xaxis": {"showticklabels": False, 'title':None},
    "yaxis": {"showticklabels": False, 'title':None}}

    Gui(page=page).run(title="Frank Fancy Chart")