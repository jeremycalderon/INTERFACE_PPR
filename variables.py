import snap7
from snap7.util import *
import tkinter as tk

#DB_NUM y OFFSET
#Int
DB_NUM_INT = 5  # Número del DB
OFFSET_INT = 0  # Dirección del entero

#Real
DB_NUM_REAL = 5  # Número del DB
OFFSET_REAL = 2  # Dirección del REAL

#Word
DB_NUM_WORD = 5  # Número del DB
OFFSET_WORD = 6  # Dirección del WORD

#Bool
DB_NUM_BOOL = 5  # Número del DB
BYTE_OFFSET_BOOL = 8  # Byte donde se encuentra el BOOL
BIT_OFFSET_BOOL = 0  # Bit específico dentro del byte

#Int
DB_NUM_DINT = 5  # Número del DB
OFFSET_DINT = 10  # Dirección del Dint

#Word
DB_NUM_DWORD = 5  # Número del DB
OFFSET_DWORD = 14  # Dirección del DWord

#Función para actualizar las variables
#Int
def refres_int(IP_ADDRESS,label_int):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    Salida_Enterop=plc.db_read(DB_NUM_INT,OFFSET_INT,2) #Cantidad de bits = 2
    Salida_Enterop=get_int(Salida_Enterop,0)
    label_int.config(text=f"La variable Entera es: {Salida_Enterop}")

#Real
def refres_real(IP_ADDRESS,label_real):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    Salida_Realp=plc.db_read(DB_NUM_REAL,OFFSET_REAL,4) #Cantidad de bits = 4
    Salida_Realp=get_real(Salida_Realp,0)
    label_real.config(text=f"La variable Real es: {Salida_Realp}")

#Word
def refres_Word(IP_ADDRESS,label_word):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    Salida_Wordp=plc.db_read(DB_NUM_WORD,OFFSET_WORD,2) #Cantidad de bits = 2
    Salida_Wordp=get_word(Salida_Wordp,0)
    label_word.config(text=f"La variable Word es: {Salida_Wordp}")

#Bool
def refres_bool(IP_ADDRESS,label_bool):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    Salida_Boolp = plc.db_read(DB_NUM_BOOL, BYTE_OFFSET_BOOL, 1)  # Leer 1 byte
    Salida_Boolp = get_bool(Salida_Boolp, 0, BIT_OFFSET_BOOL)  # Obtener el bit deseado
    label_bool.config(text=f"La variable Booleana es: {Salida_Boolp}")

#Dint
def refres_dint(IP_ADDRESS,label_dint):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    Salida_Dintp=plc.db_read(DB_NUM_DINT,OFFSET_DINT,4) #Cantidad de bits = 4
    Salida_Dintp=get_dint(Salida_Dintp,0)
    label_dint.config(text=f"La variable Dint es: {Salida_Dintp}")

#DWord
def refres_DWord(IP_ADDRESS,label_dword):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    Salida_DWordp=plc.db_read(DB_NUM_DWORD,OFFSET_DWORD,4) #Cantidad de bits = 4
    Salida_DWordp=get_dword(Salida_DWordp,0)
    label_dword.config(text=f"La variable DWord es: {Salida_DWordp}")

#Función para llamar a las funciones anteriores a la vez
def REFRESH(IP_ADDRESS, label_int, label_real, label_word, label_bool, label_dint, label_dword):
    refres_int(IP_ADDRESS, label_int)
    refres_real(IP_ADDRESS, label_real)
    refres_Word(IP_ADDRESS, label_word)
    refres_bool(IP_ADDRESS, label_bool)
    refres_dint(IP_ADDRESS, label_dint)
    refres_DWord(IP_ADDRESS, label_dword)
