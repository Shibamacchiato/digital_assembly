from operator import invert
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from typing import List

from dash_obj_in_3dmesh import geometry_tools

from data.mock_data import get_steps

def make_div_minimizable(div, minimize_to, align, div_title=""):
    """ takes a div and encapsulates it in a div that contains a minimize button
        returns the minimizable div
    """

    if minimize_to == "left":
        minimizable_div = html.Div(
            id={"type": "minimizable_div", "index": div.id},
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(html.Span(div_title, className="divTitle"), width="auto"),
                        dbc.Col(get_minimize_button(div.id, minimize_to), width=2),
                    ],
                    justify="between"   # puts the title on the left and the button on the right
                ),
                dbc.Row(dbc.Col(div))
            ],
            className="windows",
        )
        
        minimized_div = html.Div(
            id={"type": "minimized_div", "index": div.id},
            children=dbc.Row([
                dbc.Col(
                    get_maximize_button(div.id, minimize_to, div_title),
                    width=2,
                    style={"margin-top": "2em", "margin-bottom": "2em"}
                )
            ],
            class_name="justify-content-start"),
            style={"display": "none"}
        )
        
    elif minimize_to == "right":
        minimizable_div = html.Div(
            id={"type": "minimizable_div", "index": div.id},
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(get_minimize_button(div.id, minimize_to), width=2),
                        dbc.Col(html.Span(div_title, className="divTitle"), width="auto"),
                    ], 
                    justify="between"   # puts the title on the right and the button on the left
                ),
                dbc.Row(dbc.Col(div)),
            ],
            className="windows",
        )
        
        minimized_div = html.Div(
            id={"type": "minimized_div", "index": div.id},
            children=dbc.Row([
                dbc.Col(
                    get_maximize_button(div.id, minimize_to, div_title),
                    width=2,
                    style={
                        "margin-top": "2em", 
                        "margin-bottom": "2em",
                        "float": "right",
                        "display": "contents"
                    }
                ),
            ],
            class_name="justify-content-end"),
            style={"display": "none"}
        )
        
    elif minimize_to == "down":
        minimizable_div = html.Div(
            id={"type": "minimizable_div", "index": div.id},    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(html.Span(div_title, className="divTitle"), width="auto"),
                        dbc.Col(get_minimize_button(div.id, minimize_to), width=1),
                    ], 
                    justify="between"   # puts the title on the left and the button on the right
                ),
                dbc.Row(dbc.Col(div))
            ],
            className="windows",
        )
        
        minimized_div = html.Div(
            id={"type": "minimized_div", "index": div.id},
            children=[
                dbc.Row(
                    children=dbc.Col(
                        children=get_maximize_button(div.id, minimize_to, div_title),
                        width=3
                    ),
                    justify="end",    
                ),
            ],
            style={"display": "none"}
        )
        
    return [minimizable_div, minimized_div]
   
def get_minimize_button(button_id, minimize_to):
    """ creates button with id of minimizable div
    """
    
    return dbc.Button(
        id={"type": f"minimize_button", "index": button_id},
        children=[
            html.I(className=f"fa-solid fa-arrow-{minimize_to}")
        ],
        outline=True,
        color="secondary",
        style={}
    )

     
def get_maximize_button(button_id, minimized_to, div_title=""):
    """ creates button with id of maximizable div
    """
    
    if minimized_to == "left":
        # rotate maximize button by 90 degrees
        style = {"transform": "rotate(90deg)", "transform-origin": "bottom left"}
    elif minimized_to == "right":
        style = {"transform": "rotate(270deg)", "transform-origin": "bottom right"}
    elif minimized_to == "down":
        style = {}
        
    maximized_to = invert_direction(minimized_to)
    return dbc.Button(
        id={"type": f"maximize_button", "index": button_id},
        children=[
            html.P(div_title, style={"font-weight": "bold"}),
            # html.I(className=f"fa-solid fa-arrow-{maximize_to}", style={"transform": "rotate(-90deg)"})
        ],
        color="secondary",
        style=style
    )
  
def invert_direction(direction):
    
    if direction == "right":
        return "left"
    if direction == "left":
        return "right"
    if direction == "up":
        return "down"
    if direction == "down":
        return "up"
    

def get_3d_fig(step_id):
    """ define settings of the 3D figure
    """
      
    axis_template = {
        "showbackground": False,
        "visible" : False
    }

    plot_layout = {
        "title": "",
        "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
        "font": {"size": 12, "color": "white"},
        "showlegend": False,
        "legend" : dict(
            x=0,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        ),
        'uirevision':'same_all_the_time', #this keeps camera position etc the same when data changes.
        "scene": {
            "xaxis": axis_template,
            "yaxis": axis_template,
            "zaxis": axis_template,
            "aspectmode" : "data",
            "camera": {
                "eye": {"x": 2, "y": 2, "z": 2},
                "up": {"x": 0, "y": 1, "z": 0},
            },

            "annotations": []
        },
    }
    
    # Get the object names for the step (excel-file)
    df_steps = get_steps()
    object_names = df_steps.loc[step_id]["object_names"]

    figure_data = get_figure_data(object_names)
    
    fig = go.Figure(
        data = figure_data,
        layout=plot_layout
    )
    
    return fig


def get_figure_data(figure_names : List[str]) -> List[go.Mesh3d]:
    """ import obj and mtl-files and sets appearance of each element
    """

    figure_data : List[go.Mesh3d] = geometry_tools.import_geometry(figure_names)
    
    # legend attributes
    for figure, name in zip(figure_data, figure_names):
        figure.showlegend = True
        figure.name=name
        figure.lighting={
            "ambient": 0.8,
            "diffuse": 1,
            "facenormalsepsilon": 0,
            "fresnel": 0,
            "roughness": 0.5,
            "specular": 0.2,
            "vertexnormalsepsilon": 0,
        }

    return figure_data