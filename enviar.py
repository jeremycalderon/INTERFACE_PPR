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

#Función para enviar datos desde la HMI
#Int
def enviar_entero(IP_ADDRESS,nume1):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    nume1_int = int(nume1.get())
    data = bytearray(4)
    set_int(data, 0, nume1_int)
    plc.db_write(DB_NUM_INT, OFFSET_INT, data)

#Real
def enviar_real(IP_ADDRESS,nume2):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    nume2_real = float(nume2.get())
    data = bytearray(4)
    set_real(data, 0, nume2_real)
    plc.db_write(DB_NUM_REAL, OFFSET_REAL, data)

#Word
def enviar_word(IP_ADDRESS,nume3):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    nume3_word = int(nume3.get())
    data = bytearray(2)  # Un WORD ocupa 2 bytes
    set_int(data, 0, nume3_word)
    plc.db_write(DB_NUM_WORD, OFFSET_WORD, data)

#Bool
def enviar_bool(IP_ADDRESS,nume4):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    bool_value = bool(int(nume4.get()))
    byte_data = plc.db_read(DB_NUM_BOOL, BYTE_OFFSET_BOOL, 1)
    set_bool(byte_data, 0, BIT_OFFSET_BOOL, bool_value)
    plc.db_write(DB_NUM_BOOL, BYTE_OFFSET_BOOL, byte_data)

#Dint
def enviar_dint(IP_ADDRESS,nume5):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    nume5_dint = int(nume5.get())
    data = bytearray(4)
    set_dint(data, 0, nume5_dint)
    plc.db_write(DB_NUM_DINT, OFFSET_DINT, data)

#DWord
def enviar_dword(IP_ADDRESS,nume6):
    plc=snap7.client.Client()
    plc.connect(IP_ADDRESS,0,1)
    nume6_dword = int(nume6.get())
    data = bytearray(4)  # Un DWORD ocupa 4 bytes
    set_dword(data, 0, nume6_dword)
    plc.db_write(DB_NUM_DWORD, OFFSET_DWORD, data)

#Función para llamar a las funciones anteriores a la vez
def enviar(IP_ADDRESS,nume1,nume2,nume3,nume4,nume5,nume6):
    enviar_entero(IP_ADDRESS,nume1)
    enviar_real(IP_ADDRESS,nume2)
    enviar_word(IP_ADDRESS,nume3)
    enviar_bool(IP_ADDRESS,nume4)
    enviar_dint(IP_ADDRESS,nume5)
    enviar_dword(IP_ADDRESS,nume6)
