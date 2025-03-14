import snap7
from snap7.util import *

def cambiar_color(IP_ADDRESS,circulos_adicionales):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)

    # Leer el estado de la salida Q0.3 (byte 0, bit 3)
    byte = 0
    bit = 3
    bit2 = 4
    bit3 = 5

    try:
        salida = plc.read_area(snap7.type.Areas.PA, 0, byte, 1)  # Área de salidas (Q)
        estado_r = get_bool(salida, 0, bit)  # Extraer el estado del bit
        estado_a = get_bool(salida, 0, bit3)
        estado_v = get_bool(salida, 0, bit2)

        # Diccionario de estados y colores
        estados_colores = [
            ("red" if estado_r else "black"),      # Rojo (Q0.3)
            ("yellow" if estado_a else "black"),   # Amarillo (Q0.5)
            ("green" if estado_v else "black")     # Verde (Q0.4)
        ]

        # Aplicar colores a los círculos generados en la lista
        for i, (canvas, circulo) in enumerate(circulos_adicionales):
            canvas.itemconfig(circulo, fill=estados_colores[i])

    except Exception as e:
        print(f"Error al leer salida: {e}")
