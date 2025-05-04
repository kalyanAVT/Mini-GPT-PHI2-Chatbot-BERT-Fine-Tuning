import ipywidgets as widgets
from IPython.display import display

def update_value(value):
    print(f"Slider Value: {value}")

slider = widgets.FloatSlider(value=7.5, min=0, max=10, step=0.1)
interactive_widget = widgets.interactive(update_value, value=slider)
display(interactive_widget)
