# https://github.com/RamiKrispin/shinylive
# Dependencies
from shiny import App, render, ui
from numpy import random 
import pandas as pd
import matplotlib.pyplot as plt

# Functions
def random_steps(steps = 16, type = "float", low = -1, high = 1):
    if type == "int":
        r = random.randint(low = low, high=high, size= steps, dtype=int).tolist()
        r = [high if i == 0 else i for i in r]
    elif type == "float":
        r = (high - low) * random.random_sample(size = steps) + low
    else:
        print("The type argument is not valid")
        return
    return r

def cumsum(l):
    c = []
    t = 0
    for i in range(0, len(l)):
        t += l[i]
        c.append(t)
    return(c)

def sim_steps(sim_number = 10, steps = 16, type = "float"):
    s = []
    d = pd.DataFrame()
    for i in range(0, sim_number):
        v1 = [0]
        v2 = random_steps(steps = steps, type = type)
        if not isinstance(v2, list):
            v2 = v2.tolist()
        v = cumsum(v1 + v2)
        d_temp = pd.DataFrame({"sim": i, "step": range(0, len(v)), "y": v})
        d = pd.concat([d, d_temp])
    return d


# UI
app_ui = ui.page_fluid(
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.h2("Porqué las distribuciones son normales"),
                ui.input_slider("sample_size", "Tamaño de la muestra", 1, 1000, 500),
                ui.input_slider("steps", "Número de pasos", 1, 20, 16),
                ui.input_select("step", "Tipo de paso", {"float": "Float", "int": "Integer"}),
                ui.input_slider("alpha", "Opacidad", 0, 1, 0.2)
            ),
        ui.panel_main(
            ui.output_plot("plot"),
            ui.markdown(
        """
        ### Por qué las distribuciones normales son normales

        El capítulo 3 de [Statistical Rethinking's] (https://xcelab.net/rm/statistical-rethinking/) del Prof. Richard McElreath se centra en la distribución normal
        y sus características. Ilustra cómo generar una distribución normal utilizando el experimento del campo de fútbol:

        - Coloca un grupo de personas en la línea central de un campo de fútbol
        - Cada persona lanza una moneda y se mueve un paso a la derecha o a la izquierda según el resultado (cara o cruz)
        - Repita este proceso varias veces
        Después de un par de iteraciones, notará que la distribución de las distancias de las personas en el campo se volverá gaussiana o normal (por ejemplo, forma de campana).

        La aplicación anterior simula esta experiencia al establecer el tamaño de la muestra (es decir, la cantidad de personas) y la cantidad de iteraciones. 
        Donde en cada iteración, dibujamos un número aleatorio entre -1 y 1 (puede elegir entre pasos enteros flotantes con el menú desplegable 'Tipo de paso'). La gráfica anterior muestra la suma acumulada de cada experimento en cada paso de la experiencia. Puede notar cómo la distribución se vuelve más Gaussin a medida que aumenta el número de pasos.

        """
    ),
        )
    )
)

# Server
def server(input, output, session):
    @output
    @render.plot(alt="Simulación")
    def plot():
        type = input.step()
        color = "lightblue"
        alpha = input.alpha()
        sim_number = input.sample_size()
        steps = input.steps()
        sim_df = sim_steps(sim_number = sim_number, steps = steps, type = type)
        fig, ax = plt.subplots()
        for i in sim_df.sim.unique():
            df = sim_df[sim_df["sim"] == i]
            ax.plot(df["step"], df["y"], color = color, alpha= alpha)

        ax.set_title(label = "Simulación de un camino aleatorio")
        ax.set_xlabel("Número de pasos")
        ax.set_ylabel("Posición")
        return fig


app = App(app_ui, server)

# TODO Solucionar el utf-8 o latin1
