import snap7
from snap7.util import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from collections import deque
from grafica import crear_grafica, iniciar_animacion, update_graph
from variables import REFRESH
from enviar import enviar
from crear_excel import guardar_datos_excel
from salidas import cambiar_color

#Conexión PLC
IP_ADDRESS="192.168.1.13"

try:
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    conectado_plc="Conectado"
    print(conectado_plc)

except Exception as e:
    conectado_plc="Error de conexión: ", str(e)
    print(conectado_plc)

#Definir el tamaño de las listas
lista = 30

#Variables
x_data = deque(maxlen=lista)
y_data = [deque(maxlen=lista) for _ in range(4)]
cont=0
delay=1

#Función para cambiar el estado de las variables del PLC
#I0.2 e I0.1
def Start_b():
    start_plc=plc.eb_read(0,1)
    set_bool(start_plc,0,2,True)
    plc.eb_write(0,1,start_plc)
    stop_plc=plc.eb_read(0,1)
    set_bool(stop_plc,0,1,False)
    plc.eb_write(0,1,stop_plc)

#Función para cambiar el estado de las variables del PLC
#I0.2 e I0.1
def Stop_b():
    stop_plc=plc.eb_read(0,1)
    set_bool(stop_plc,0,1,True)
    plc.eb_write(0,1,stop_plc)
    start_plc=plc.eb_read(0,1)
    set_bool(start_plc,0,2,False)
    plc.eb_write(0,1,start_plc)

#Función para cambiar de página o frame
def ir_pagina(pagina):
    for p in paginas:
        p.pack_forget()
    paginas[pagina].pack()
    resaltar_botones(pagina)

def resaltar_botones(pagina_actual):
    for i, boton in enumerate(botones):
        if i==pagina_actual:
            boton.config(bg='#663399')
        else:
            boton.config(bg='#6666CC')

#Función para subir configuración del sensor
def cargar():
    min = int(analog1.get())
    data_min = bytearray(4)
    set_real(data_min, 0, min)
    plc.db_write(6, 4, data_min)

    max = int(analog2.get())
    data_max = bytearray(4)
    set_real(data_max, 0, max)
    plc.db_write(6, 0, data_max)

#Función para leer variables analógicas
def read_analog_value(db_number, start):
        data = plc.db_read(db_number, start, 4)  # Leer 4 bytes
        return snap7.util.get_real(data, 0)  # Convertir a float

def read_plc_values():
        global cont, delay
        try:
            # Leer 4 valores analógicos desde DB1 (direcciones ajustables según PLC)
            values = [
                read_analog_value(db_number=6, start=8),   # Dirección DB{number}.DBD{start}
                read_analog_value(db_number=6, start=12),
                read_analog_value(db_number=6, start=4),
                read_analog_value(db_number=6, start=16)
            ]
            print(f"Lecturas del PLC: {values}")
            cont=cont+1
            if cont==delay:
                guardar_datos_excel(values)
                cont=0
            return values
        except Exception as e:
            print(f"Error de conexión: {e}")
            guardar_datos_excel(values)
            return None

#Interfaz gráfica
ventana=tk.Tk()
ventana.geometry("1000x700")
ventana.config(padx=40,pady=40,bg="#17202A")
ventana.title("Python-PLC")
Label_plc=tk.Label(ventana,text="Python-PLC",font=("ITALIC",50,),bg="#003333",fg="#00CC99")
Label_plc.pack(padx=0,pady=0)
conectado_ventana=tk.Label(ventana,text=(conectado_plc),font=("Arial",15,),bg="#003333",fg="#00FF66")
conectado_ventana.pack(padx=0,pady=10)

#Frames
frame_st=tk.Frame(ventana,width=1000,height=300,bg="#17202A")
frame_int=tk.Frame(ventana,width=400,height=300,bg="#17202A")
frame_var=tk.Frame(ventana,width=400,height=300,bg="#17202A")
frame_sensor=tk.Frame(ventana,width=400,height=300,bg="#17202A")
frame_graf=tk.Frame(ventana,width=400,height=300,bg="#17202A")

label_st=tk.Label(frame_st,text="Start/Stop",font=("Arial",20),bg="#17202A",fg="#66FFCC")
label_st.pack(padx=0,pady=0)
label_var=tk.Label(frame_int,text="Enviar variables",font=("Arial",20),bg="#17202A",fg="#66FFCC")
label_var.pack(padx=0,pady=0)
label_mon=tk.Label(frame_var,text="Monitoreo de variables",font=("Arial",20),bg="#17202A",fg="#66FFCC")
label_mon.pack(padx=0,pady=0)
label_sensor=tk.Label(frame_sensor,text="Configuración de sensores",font=("Arial",20),bg="#17202A",fg="#66FFCC")
label_sensor.pack(padx=0,pady=0)
label_graf=tk.Label(frame_graf,text="Gráfica de Analógicos",font=("Arial",20),bg="#17202A",fg="#66FFCC")
label_graf.pack(padx=0,pady=0)
label_a=tk.Label(frame_graf,text="",font=("Arial",15),bg="#17202A",fg="#66FFCC")
label_a.pack(padx=0,pady=0)
contenedor_botones=tk.Frame(ventana)

#Botones para cambiar de pag
botones=[]
botones.append(tk.Button(contenedor_botones,text="Start/Stop",command=lambda:ir_pagina(0),bg="#6666CC",fg="#99FFFF"))
botones.append(tk.Button(contenedor_botones,text="Enviar variables",command=lambda:ir_pagina(1),bg="#6666CC",fg="#99FFFF"))
botones.append(tk.Button(contenedor_botones,text="Monitoreo de variables",command=lambda:ir_pagina(2),bg="#6666CC",fg="#99FFFF"))
botones.append(tk.Button(contenedor_botones,text="Sensores",command=lambda:ir_pagina(3),bg="#6666CC",fg="#99FFFF"))
botones.append(tk.Button(contenedor_botones,text="Gráfica",command=lambda:ir_pagina(4),bg="#6666CC",fg="#99FFFF"))
contenedor_botones.pack(side=tk.BOTTOM)

for boton in botones:
    boton.pack(side=tk.LEFT)

#Almacenamiento de páginas
paginas=[frame_st,frame_int,frame_var,frame_sensor,frame_graf]

#Redimensionamiento de la ventana
ventana.resizable(True,True)
canvas=tk.Canvas(frame_st,bg="#17202A",width=100,height=100)
canvas.pack(side=tk.RIGHT, padx=20, pady=40)
circulo=canvas.create_oval(10,10,90,90,fill="red")

# Frame para los círculos debajo de los botones
frame_circulos = tk.Frame(frame_st, bg="#17202A")
frame_circulos.pack(side=tk.BOTTOM, pady=10)  # Ubicar el frame debajo de los botones

# Crear Canvas para cada círculo con sus etiquetas
colores = ["Rojo", "Amarillo", "Verde"]
circulos_adicionales = []
for i, color in enumerate(colores):
    frame_individual = tk.Frame(frame_circulos, bg="#17202A")
    frame_individual.grid(row=0, column=i, padx=15)

    etiqueta = tk.Label(frame_individual, text=color, font=("Arial", 10), fg="white", bg="#17202A")
    etiqueta.pack()

    canvas_ind = tk.Canvas(frame_individual, width=50, height=50, bg="#17202A", highlightthickness=0)
    canvas_ind.pack()
    circulo_ind = canvas_ind.create_oval(5, 5, 45, 45, fill="black")
    circulos_adicionales.append((canvas_ind, circulo_ind))

#Ingreso de datos de variables
nume1=tk.StringVar()
label_inta=tk.Label(frame_int,text="Ingresa un número entero: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_inta.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada1=tk.Entry(frame_int,width=20,font=("Arial",15),textvariable=nume1)
entrada1.pack()

nume2=tk.StringVar()
label_intb=tk.Label(frame_int,text="Ingresa un número real: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_intb.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada2=tk.Entry(frame_int,width=20,font=("Arial",15),textvariable=nume2)
entrada2.pack()

nume3=tk.StringVar()
label_intc=tk.Label(frame_int,text="Ingresa un número word: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_intc.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada3=tk.Entry(frame_int,width=20,font=("Arial",15),textvariable=nume3)
entrada3.pack()

nume4=tk.StringVar()
label_intd=tk.Label(frame_int,text="Ingresa un booleano: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_intd.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada4=tk.Entry(frame_int,width=20,font=("Arial",15),textvariable=nume4)
entrada4.pack()

nume5=tk.StringVar()
label_inte=tk.Label(frame_int,text="Ingresa un número dint: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_inte.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada5=tk.Entry(frame_int,width=20,font=("Arial",15),textvariable=nume5)
entrada5.pack()

nume6=tk.StringVar()
label_intf=tk.Label(frame_int,text="Ingresa un número dword: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_intf.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada6=tk.Entry(frame_int,width=20,font=("Arial",15),textvariable=nume6)
entrada6.pack()

#Ingreso de datos analógicos
analog1=tk.StringVar()
label_analog1=tk.Label(frame_sensor,text="Ingresa el valor mínimo (real): ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_analog1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada7=tk.Entry(frame_sensor,width=20,font=("Arial",15),textvariable=analog1)
entrada7.pack()

analog2=tk.StringVar()
label_analog2=tk.Label(frame_sensor,text="Ingresa el valor máximo (real): ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_analog2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
entrada8=tk.Entry(frame_sensor,width=20,font=("Arial",15),textvariable=analog2)
entrada8.pack()

#Labels
label_int=tk.Label(frame_var,text="La variable Entera es: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_int.pack()

label_real=tk.Label(frame_var,text="La variable Real es: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_real.pack()

label_word=tk.Label(frame_var,text="La variable Word es: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_word.pack()

label_bool=tk.Label(frame_var,text="La variable Booleana es: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_bool.pack()

label_dint=tk.Label(frame_var,text="La variable Dint es: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_dint.pack()

label_dword=tk.Label(frame_var,text="La variable DWord es: ",font=("Arial",15),bg="#17202A",fg="#CCFFFF")
label_dword.pack()

#Gráfica
figure, ax, lines, text_labels = crear_grafica()

#Incrustar la gráfica en la interfaz
canvasgraf = FigureCanvasTkAgg(figure, master=frame_graf)
canvasgraf.get_tk_widget().pack()

#Iniciar animación de la gráfica
anim = iniciar_animacion(figure, ax, x_data, y_data, lines, text_labels, lambda: read_plc_values())

#Botones
Boton_Start=tk.Button(frame_st,text="Start",command=Start_b,fg="#B2DFDB",width=10,height=1,font=("Arial",13),bg="#17202A")
Boton_Start.pack(padx=100,pady=10)

Boton_stop=tk.Button(frame_st,text="Stop",command=Stop_b,fg="#B2DFDB",width=10,height=1,font=("Arial",13),bg="#17202A")
Boton_stop.pack(padx=0,pady=20)

Boton_refresh=tk.Button(frame_var,text="Actualizar",command=lambda: REFRESH(IP_ADDRESS, label_int, label_real, label_word, label_bool, label_dint, label_dword),fg="#B2DFDB",width=10,height=1,font=("Arial",13),bg="#17202A")
Boton_refresh.pack(side=tk.BOTTOM)

Boton_suma=tk.Button(frame_int,text="Enviar",command=lambda: enviar(IP_ADDRESS,nume1,nume2,nume3,nume4,nume5,nume6),fg="#B2DFDB",width=20,height=1,font=("Arial",13),bg="#17202A")
Boton_suma.pack()

Boton_sensor=tk.Button(frame_sensor,text="Subir",command=cargar,fg="#B2DFDB",width=20,height=1,font=("Arial",13),bg="#17202A")
Boton_sensor.pack()

#Bucle principal
def cerrar_aplicacion():
    try:
        plc.disconnect()
        print("PLC desconectado correctamente.")
    except:
        pass
    ventana.destroy()
    exit()

while True:
    #Lectura periódica del PLC7
    time.sleep(1)
    try:
        byte=11 #M11.0
        bit=0
        resultado = plc.read_area(snap7.type.Areas.MK, 0, byte, 1)  # Leer 1 byte de la memoria M
        salida_plc = (resultado[0] >> bit) & 1  # Extraer el bit deseado
        print(salida_plc)
        if salida_plc==True:
            color='green'
        elif salida_plc==False:
            color='red'
        canvas.itemconfig(circulo, fill=color)
        cambiar_color(IP_ADDRESS,circulos_adicionales)
    
    except Exception as e:
        print("Error al leer el PLC: ",e)
    
    #Permitir que Tkinter procese eventos
    ventana.update()
    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
