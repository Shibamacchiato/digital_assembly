from tkinter import font
import dash
from dash import html
import dash_bootstrap_components as dbc
from html_structure import get_3d_fig, get_main_layout
import pandas as pd

from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate

from data.mock_data import get_steps

app = dash.Dash(
    external_stylesheets=[
        "assets/bootstrap.css",
        dbc.icons.BOOTSTRAP, 
        dbc.icons.FONT_AWESOME,
    ]
)
# create html
app.layout = get_main_layout()



# =======================
# CALLBACKS
# =======================

# the callback block always refers to the function below
@app.callback(
    Output({"type": "minimizable_div", "index": MATCH}, "style"),
    Output({"type": "minimized_div", "index": MATCH}, "style"),
    Input({"type": "minimize_button", "index": MATCH}, "n_clicks"),
    Input({"type": "maximize_button", "index": MATCH}, "n_clicks"),
    State({"type": "minimizable_div", "index": MATCH}, "id"),
    State({"type": "minimizable_div", "index": MATCH}, "style"),
    State({"type": "minimized_div", "index": MATCH}, "style"),
    prevent_initial_call=True
)
def on_showhide_divs(n_clicks_minimize, n_clicks_maximize, id_minimizable, style_minimizable, style_minimized):
    """ triggered by minimize_buttons
        hides the div to minimizes and shows the minimized div
    """ 
    event_button_id = dash.callback_context.triggered_id
    # if event_button_id is None:
    #     raise PreventUpdate("")
    
    # Check if the minimize button or the maximize button was clicked
    if event_button_id["type"] == "minimize_button":
        # Hide the minimizable div
        if style_minimizable is None:
            style_minimizable = {"display": "none"}
        else:
            style_minimizable.update({"display": "none"})
            
        # Show the minimized div
        if style_minimized is None:
            style_minimized = {}
        else:
            del style_minimized["display"]
    
    elif event_button_id["type"] == "maximize_button":
        # Show the minimizable div
        if style_minimizable is None:
            style_minimizable = {}
        else:
            del style_minimizable["display"]
            
        # Hide the minimized div
        if style_minimized is None:
            style_minimized = {"display": "none"}
        else:
            style_minimized.update({"display": "none"})
            
    return style_minimizable, style_minimized

@app.callback(
    Output("col_body_left", "width"),
    Output("col_body_center", "width"),
    Output("col_body_right", "width"),
    Input({"type": "minimizable_div", "index": ALL}, "style"),
    State({"type": "minimizable_div", "index": ALL}, "id"),
    prevent_initial_call=True
)
def on_div_minimized(minimizable_divs_styles, minimizable_divs_ids):
    """ triggered after minimizable_div was opened oder closed
        sets the column size to strech the visualization
    """
    
    indices = [id["index"] for id in minimizable_divs_ids]
    index_style_dict = {idx: style for idx, style in zip(indices, minimizable_divs_styles)}
    
    # Now we have a dict of
    # { 
    #   'div_1': { 'display': 'none', ...},
    #   'div_2': { 'display': 'none', ...},
    #   'div_3': { 'display': 'block', ...},
    #   ...
    # } 
    
    if index_style_dict["div_productmetadata"] is not None and "display" in index_style_dict["div_productmetadata"] and index_style_dict["div_productmetadata"]["display"] == "none" \
        and index_style_dict["div_materiallist"] is not None and "display" in index_style_dict["div_materiallist"] and index_style_dict["div_materiallist"]["display"] == "none":
        width_col_left = 1
    else:
        width_col_left = 3
        
    if index_style_dict["div_tools"] is not None and "display" in index_style_dict["div_tools"] and index_style_dict["div_tools"]["display"] == "none" \
        and index_style_dict["div_steplist"] is not None and "display" in index_style_dict["div_steplist"] and index_style_dict["div_steplist"]["display"] == "none":
        width_col_right = 1
    else:
        width_col_right = 3
        
    width_col_center = 12 - width_col_left - width_col_right
    
    return width_col_left, width_col_center, width_col_right


@app.callback(
    Output("graph", "figure"),
    Output("current_step", "data"),
    Input({"type": "step_button", "index": ALL}, "n_clicks"),
    Input({"type": "step_nav_button", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def onclick_step_button(n_clicks1, n_clicks2):
    """ triggered by clicking any step button or the step arrows
        updates graph and current step variable
    """
    event_button_id = dash.callback_context.triggered_id
    # if event_button_id is None:
    #     raise PreventUpdate("")
    
    step_id = event_button_id["index"]
    fig = get_3d_fig(step_id)
    
    return fig, step_id


@app.callback(
    Output("div_step_description_stepname", "children"),
    Output("div_step_description_steptext", "children"),
    Output("div_tools_name", "children"),
    Output("div_tools_img", "src"),
    Output("div_danger_img", "src"),
    Output("p_notifs", "children"),
    Output("i_notifs", "className"),
    Output("div_notifs", "className"),
    Input("current_step", "data")
)
def on_step_changed(current_step_id):
    """ triggered by the change to a new step
        defines the new updated changes which (can) occur by switching to another step
        e.g. show critical hints and update step description
    """
    # Display step name and text in box under the graph
    df_steps = get_steps()
    step_name = df_steps.loc[current_step_id]["name"]
    step_description = df_steps.loc[current_step_id]["description"]
    
    step_tools_name = df_steps.loc[current_step_id]["tools"]
    step_tools_img = df_steps.loc[current_step_id]["tools_img_path"]
    notifs = df_steps.loc[current_step_id]["notifications"]
    
    if not pd.isna(notifs):
        i_notifs_class = "fa-solid fa-triangle-exclamation"
        div_notifs_class = "border_div_notifs"
    else:
        i_notifs_class = ""
        div_notifs_class = "no_border_div_notifs"
    
    
    if not pd.isna(step_tools_img):
        step_tools_img = "assets/img/" + step_tools_img
    else:
        step_tools_img = ""
        
    if current_step_id == "step14":
        danger_img = "assets/img/danger.png"
    else:
        danger_img = ""
        
    
    return step_name, step_description, step_tools_name, step_tools_img, danger_img, notifs, i_notifs_class, div_notifs_class

@app.callback(
    Output({"type": "step_button", "index": ALL}, "color"),
    Output({"type": "step_nav_button", "index": ALL}, "id"),
    Input("current_step", "data"),
    State({"type": "step_button", "index": ALL}, "id"),
    State({"type": "step_nav_button", "index": ALL}, "id"),
)
def on_step_changed_2(current_step_id, step_button_ids, tmp):
    """ triggered by the change to a new step
        sets step button color and re-calculates which step occurs after the step-nav-arrows
    """
    
    # Extract the index from the id 
    button_indices = [id["index"] for id in step_button_ids]
    
    button_colors_new = []
    for button_index in button_indices:
        if button_index == current_step_id:
            button_colors_new.append("primary")
        else:
            button_colors_new.append("secondary")
            
    # Change step navigation button ID.
    # Set the ID of the back navigation button to the previous step
    
    # Extract the index from the id 
    button_indices = [id["index"] for id in step_button_ids]
    
    i = button_indices.index(current_step_id)
    previous_button_index = {"type": "step_nav_button", "index": button_indices[i-1]}
    next_button_index = {"type": "step_nav_button", "index": button_indices[i+1]}
    
    return button_colors_new, [previous_button_index, next_button_index]
    

# ===================
# END OF CALLBACKS
# ===================

if __name__ == "__main__": 
    app.run_server(debug=True)