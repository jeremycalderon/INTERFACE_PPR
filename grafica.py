import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patheffects as path_effects
import matplotlib.colors as mcolors

def es_color_claro(color):
    rgb = mcolors.to_rgb(color)  # Convierte el color a valores RGB normalizados (0-1)
    luminancia = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]  # Fórmula de luminancia
    return luminancia > 0.5  # Si es mayor a 0.5, es un color claro

def crear_grafica(lista=30):
    figure, ax = plt.subplots()
    figure.subplots_adjust(top=0.85, left=0.1, right=0.8)
    
    line1, = ax.plot([], [], "r-", label="Sensor 1")
    line2, = ax.plot([], [], "b-", label="Sensor 2")
    line3, = ax.plot([], [], "g-", label="Sensor 3")
    line4, = ax.plot([], [], "y-", label="Sensor 4")

    # Posicionar la leyenda en la parte superior
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.75), edgecolor='black', frameon=True)
    
    # Etiquetas de valores actuales
    text_values = []
    for i, color in enumerate(["red", "blue", "green", "yellow", "white", "cyan"]):
        borde = [path_effects.withStroke(linewidth=2, foreground='black')]if es_color_claro(color) else []
        text = ax.text(1.015, 0.5 - i * 0.05, '', transform=ax.transAxes, fontsize=10, color=color, path_effects=borde)
        text_values.append(text)

    ax.set_title("Lectura de sensores con un PLC")
    ax.set_xlabel(f"Últimos {lista} datos")
    ax.set_ylabel("Valor")
    ax.relim()
    ax.autoscale_view()
    
    return figure, ax, [line1, line2, line3, line4], text_values

def update_graph(frame, x_data, y_data, lines, text_values, ax, read_plc_values):
    valores = read_plc_values()
    if valores:
        # Agregar el nuevo índice con desplazamiento de 30 datos
        if x_data:
            x_data.append(x_data[-1] + 1)
        else:
            x_data.append(0)
        
        for i in range(4):
            y_data[i].append(valores[i])

    for i, line in enumerate(lines):
        line.set_data(list(x_data), list(y_data[i]))  # Convertir deque a lista para matplotlib
        text_values[i].set_text(f"Sensor {i+1}: {y_data[i][-1]:.2f}")  # Mostrar el último valor
    
    ax.relim()
    ax.autoscale_view()
    return lines + text_values

def iniciar_animacion(figure, ax, x_data, y_data, lines, text_values, read_plc_values):
    anim = FuncAnimation(figure, update_graph, fargs=(x_data, y_data, lines, text_values, ax, read_plc_values), interval=1000, cache_frame_data=False)
    return anim
