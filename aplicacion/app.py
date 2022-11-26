from shiny import App, render, ui
from matplotlib import pyplot as plt
from shiny.types import ImgData # Para el logo

app_ui = ui.page_fluid(
    #logo
    ui.output_image("milogo", inline=True),
    # Título y slider
    ui.h2("App shiny para Python!"),
    ui.input_slider("n", "Número", 0, 100, 20),
    ui.output_text_verbatim("txt"),
    # Plot
    ui.output_plot("a_scatter_plot"),
    # Salida de html
    ui.output_ui("unhtml"), #mismo nombre que la función de abajo
)

def server(input, output, session):
    # Logo
    @output
    @render.image
    def milogo():
        from pathlib import Path

        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "yodaperfil.jpg"), "width": "150px"}
        return img

    # Texto de salida
    @output
    @render.text
    def txt():
        return f"n*2 es {input.n() * 2}"

    # Plot 
    @output
    @render.plot
    def a_scatter_plot():
        return plt.scatter([1,2,3], [5, 2, 3])
    
    # html
    @output
    @render.ui
    def unhtml():
        return ui.HTML("<marquee>Hola, me llamo Íñigo Montoya. Tu mataste a mi padre. Prepárate a morir. <<-- Esto es html puro</marquee>")

app = App(app_ui, server)
