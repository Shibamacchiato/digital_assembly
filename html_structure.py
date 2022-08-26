from ctypes import alignment
from turtle import width
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd

from helper_functions import get_3d_fig, make_div_minimizable
from data.mock_data import get_parts, get_steps

def get_main_layout():
    main_div = html.Div(
        children=[
            dbc.Row(
                id="row_header",
                children=[
                    get_top_col_body_left(),
                    get_top_col_body_center(),
                    get_top_col_body_right(),
                ],
                style={"height": "10vh", "min-height": "3em", "margin-top": "0.6em", "margin-left": "0.5em", "display": "flex", "align-items": "center"} # 10 percent of screen          
            ),
            dbc.Row(
                id="row_body",
                children=[
                    get_col_body_left(),
                    get_col_body_center(),
                    get_col_body_right(),
                ],
                style={"height": "85vh"}    # 85 percent of screen
            ),
            dcc.Store(id="current_step", data="step1"),
            dcc.Store(id="minimized_divs", data=[])
        ],
    )
    
    return main_div


def get_3d_graph():
    
    fig = get_3d_fig("step1")
    
    graph = dcc.Graph(
        id="graph",
        figure=fig,
        config={"scrollZoom": True, "responsive": True},
        style={"height": "100%", "width": "100%"}
    )
    
    return graph
   
###############################
# LEFT COLUMN
###############################

def get_col_body_left():
    return dbc.Col(
        id="col_body_left",
        children=[
            *get_div_productmetadata(),
            *get_div_materiallist(),
        ],
        width=3,
        class_name="col-body",
    )
    
def get_div_productmetadata():
    div = html.Div(
        id="div_productmetadata",
        children=[
            html.Table([
                html.Tr([
                    html.Th(html.Span("Bezeichnung")),
                    html.Td(html.Span("Spielzeughund")),
                ]),
                html.Tr([
                    html.Th(html.Span("Variante")),
                    html.Td(
                        dcc.Dropdown(
                            id="dd_product_variant",
                            options=[
                                {"label": "mit Wackelaugen", "value": 1},
                                {"label": "ohne Wackelaugen", "disabled": True, "value": 2},
                            ],
                            value=1,
                            searchable=True,
                            clearable=False,
                        ),
                    ),
                ]),
            ],
                       className="producttable"),
        ]
    )
    
    minimizable_div, minimized_div = make_div_minimizable(div, "left", align="start", div_title="Produkt")
    return minimizable_div, minimized_div

def get_materials_accordion():
    df_parts = get_parts()
    
    accordion_items = []
    for groupname, rows in df_parts.groupby("category"):
        
        table_rows = []

        for _, row in rows.iterrows():
            table_row = html.Tr(
                [
                    html.Td(row["name"]),
                    # html.Td(row["color"], style={"background-color": row["color"]}),
                    html.Td(style={"background-color": row["color"], "width": "3em"}),
                ]
            )
            table_rows.append(table_row)

        table_body = [html.Tbody(table_rows)]
        
        table = dbc.Table(table_body, bordered=True)
        
        accordion_item = dbc.AccordionItem(
            title = groupname,
            children = table
        )
        
        accordion_items.append(accordion_item)

    return dbc.Accordion(accordion_items, style={"width": "100%"}, always_open=True)


def get_materials_table():
    table_header = [
        html.Thead(html.Tr([html.Th(""), html.Th("Material")]))
    ]
    
    df_parts = get_parts()
    
    table_rows = []

    for key, part_row in df_parts.iterrows():
        table_row = html.Tr(
            [
                html.Td(key),
                html.Td(part_row["name"]),
            ],
            id={"type":"tr", "index": key}
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, bordered=True)
    return table

    
def get_div_materiallist():
    div = html.Div(
        id="div_materiallist",
        children=[
            html.Div(
                children=[
                    # get_materials_table()
                    get_materials_accordion(),
                ],
                style={
                    "display": "flex",
                    "overflow-y": "auto",
                    "height": "350px",
                }    
            )
        ],
    )
    
    minimizable_div, minimized_div = make_div_minimizable(div, "left", align="end", div_title="Bauteilliste")
    return minimizable_div, minimized_div


###############################
# CENTERED COLUMN
###############################
def get_col_body_center():
    return dbc.Col(
        id="col_body_center",
        children=dbc.Container(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=dbc.Button(
                                id={"type": "step_nav_button", "index": "step1"}, 
                                # alternative CD
                                children=html.I(className="fa-solid fa-circle-arrow-left", style={"font-size": "3em", "color": "#5D98C5"}),
                                # children=html.I(className="fa-solid fa-circle-arrow-left", style={"font-size": "3em", "color": "#6B4092"}),
                                style={"background-color": "transparent", "border-color": "transparent"}
                            ), 
                            width=1,
                            style= {"display": "flex", "align-items": "center", "justify-content": "center"}
                        ),
                        dbc.Col(
                            children=get_3d_graph(), 
                            width=10
                        ),
                        dbc.Col(
                            children=dbc.Button(
                                id={"type": "step_nav_button", "index": "step99"},
                                # alternative CD 
                                children=html.I(className="fa-solid fa-circle-arrow-right", style={"font-size": "3em", "color": "#5D98C5"}),
                                # children=html.I(className="fa-solid fa-circle-arrow-right", style={"font-size": "3em", "color": "#6B4092"}),
                                style={"background-color": "transparent", "border-color": "transparent"}
                            ), 
                            width=1,
                            style= {"display": "flex", "align-items": "center", "justify-content": "center"}
                        ),
                    ],
                    class_name="flex-fill d-flex justify-content-start" # to flexibly resize the graph row
                ),
                dbc.Row(dbc.Col(
                    children=[
                        *get_div_step_description()
                    ]
                )),
            ],
            fluid=True, 
            class_name="d-flex h-100 flex-column"   # to fill the whole available space
        ),
        width=6,
        class_name="col-body",
    )
    
def get_div_step_description():
    div = html.Div(
        id="div_step_description",
        children=[
            html.Span(id="div_step_description_stepname", style={"font-size": "24px"}),
            # alternative CD
            html.I(className="fa-solid fa-pen", id="tooltip-target", style={"font-size": "1.5em", "color": "#59C9A5", "margin-left": "0.5em"}),
            # html.I(className="fa-solid fa-pen", id="tooltip-target", style={"font-size": "1.5em", "color": "#F59C1B", "margin-left": "0.5em"}),
            html.P(id="div_step_description_steptext"),
            dbc.Tooltip(
                "Funktion zum Hinzufügen persönlicher Kommentare. "
                "(Noch nicht implementiert)",
                target="tooltip-target",
            ),
        ],
    )
    
    minimizable_div, minimized_div = make_div_minimizable(div, "down", align="end", div_title="Aktueller Schritt")
    return minimizable_div, minimized_div


###############################
# RIGHT COLUMN
###############################
def get_col_body_right():
    return dbc.Col(
        id="col_body_right",
        children=[
            *get_div_tools(),
            *get_div_steplist(),   
        ],
        width=3,
        class_name="col-body",
    )

    
def get_div_tools():
    div = html.Div(
        id="div_tools",
        children=[
            html.Table(
                html.Tr([
                    html.Td(html.Img(id="div_tools_img", style={"max-width": "100%", "max-height": "4em" })),
                    html.Td(html.P(id="div_tools_name"))
                ], style={"display": "flex", "align-items": "baseline"}),
                style={"display": "flex", "justify-content": "space-around"}
            )
        ],
        style={"display": "flex", "justify-content": "center"}
    )
    
    minimizable_div, minimized_div = make_div_minimizable(div, "right", align="start", div_title="Werkzeug")
    return minimizable_div, minimized_div

    
def get_div_steplist():
    div = html.Div(
        id="div_steplist",
        children=[
            html.Div(
                children=[get_steplist_table()],
                style={                    
                    "display": "flex",
                    "overflow-y": "auto",
                    "height": "350px",
                }
            )
        ],
    )
    
    minimizable_div, minimized_div = make_div_minimizable(div, "right", align="end", div_title="Schritte")
    return minimizable_div, minimized_div
    

def get_steplist_table():

    df_steps = get_steps()
    
    table_rows = []

    for key, step_row in df_steps.iterrows():
        
        # define button content
        button_content = [
            html.Span(step_row["name"])
        ]
        
        if not pd.isna(step_row["notifications"]):
            # alternative CD
            button_content.insert(0, html.I(className="fa-solid fa-triangle-exclamation", style={"color": "#59C9A5"}))
            # button_content.insert(0, html.I(className="fa-solid fa-triangle-exclamation", style={"color": "#F59C1B"}))
        
        table_row = html.Tr(
            [
                # html.Td(key),
                html.Td(
                    dbc.Button(
                        id={"type": "step_button", "index": key},
                        children=button_content,
                        style={"width": "100%"},
                        color="secondary",
                        outline=True,
                    ),
                ),
            ],
            id={"type":"tr", "index": key}
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_body, bordered=True)
    return table  


###############################
# TOP ROW LEFT
###############################

def get_top_col_body_left():
    return dbc.Col(
        id="top_col_body_left",
        children=[         
            # alternative CD   
            html.I(className="fa-solid fa-arrow-left", style={"font-size": "2.5em", "color": "#5D98C5", "margin-right": "0.3em"}),
            html.I(className="fa-solid fa-house", style={"font-size": "3em", "color": "#5D98C5"}),
            # html.I(className="fa-solid fa-arrow-left", style={"font-size": "2.5em", "color": "#6B4092", "margin-right": "0.3em"}),
            # html.I(className="fa-solid fa-house", style={"font-size": "3em", "color": "#6B4092"}),
        ],
        width=3,
        class_name="top-col-body",
    )
    
###############################
# TOP ROW CENTER
###############################

def get_top_col_body_center():
    return dbc.Col(
        id="top_col_body_center",
        children=[            
            html.Div(
                className="border_div_notifs",
                id="div_notifs",
                children=[            
                    html.I(
                        className="fa-solid fa-triangle-exclamation",
                        id="i_notifs",
                        # alternative CD
                        style={"text-align": "center", "font-size": "1.5em", "color": "#59C9A5"}
                        # style={"text-align": "center", "font-size": "1.5em", "color": "#F59C1B", "margin-right": "0.1em"}
                    ),
                    html.Span(
                        id="p_notifs",
                        style={"text-align": "center", "font-variant": "all-small-caps", "font-family": "Spartan Semibold"}
                    )
                ]
            )
        ],
        width=6,
        class_name="top-col-body",
        style={"display": "flex", "justify-content": "center"},
    )
    
    
###############################
# TOP ROW RIGHT
###############################

def get_top_col_body_right():
    return dbc.Col(
        id="top_col_body_right",
        children=[            
            html.Img(id="div_danger_img", style={"width": "85%"},),
        ],
        width=3,
        class_name="top-col-body",
        style={"display": "flex", "justify-content": "center"},
    )