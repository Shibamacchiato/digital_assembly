import pandas as pd

def get_parts():
    df_parts = pd.read_csv("./data/materials.csv", sep=";", encoding="ISO-8859-1")
    return df_parts
    
    # return pd.DataFrame(
    #     [
    #         ["comp1", "Holzmaterialien",],
    #         ["comp2", "Holzwürfel",],
    #         ["comp3", "Holzquader S",],
    #         ["comp4", "Holzquader L",],
    #         ["comp5", "Holzzylinder",],
    #         ["comp6", "Verbindungen",],
    #         ["comp7", "Verbindungsstück S",],
    #         ["comp8", "Verbindungsstück L",],
    #         ["comp9", "Dekoration",],
    #         ["comp10", "Wackelauge",],
    #     ], columns=["key", "name"],
    # ).set_index("key")
    
def get_steps():
    df_steps = pd.read_csv("./data/step_data.csv", sep=";", encoding="ISO-8859-1").set_index("key")
    
    # Split the comma-separated object_names string into a list
    df_steps["object_names"] = df_steps["object_names"].str.replace(" ", "").str.split(",")
    return df_steps