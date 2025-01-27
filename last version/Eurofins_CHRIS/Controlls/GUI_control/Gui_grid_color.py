# Controls/GUI_control/Gui_grid_color.py

def get_color(state):
    """
    Return the color based on the sample state.

    Args:
        state (str): The state of the sample (e.g., "New_Sample", "Drying_Sample").

    Returns:
        str: The color corresponding to the sample state.
    """
    return {
        "New_Sample": "Orange",
        "Drying_Sample": "Yellow",
        "Dried_Sample": "Blue",
        "Done_Sample": "Green",
        "No_sample": "Red"  # Added No_sample state
    }.get(state, "White")  # Default to white if the state is not recognized
