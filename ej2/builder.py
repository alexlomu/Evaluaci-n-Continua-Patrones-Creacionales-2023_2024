from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
import csv
import tkinter as tk
from tkinter import messagebox

class Cliente:
    def __init__(self, nombre_usuario, contraseña, nombre_personal, correo):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.nombre_personal = nombre_personal
        self.correo = correo
        self.pedidos = []

    def hacer_pedido(self, pedido):
        self.pedidos.append(pedido)

    def guardar_en_csv(self):
        with open('ej2/clientes.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.nombre_usuario, 
                self.contraseña,
                self.nombre_personal,
                self.correo
                ])

class Pizza:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tamano = None
        self.masa = None
        self.salsa = None
        self.ingredientes = []
        self.tecnica_coccion = None
        self.presentacion = None
        self.maridaje = None
        self.acabado_extra = None

    def set_tamano(self, tamano):
        self.tamano = tamano

    def set_masa(self, masa):
        self.masa = masa

    def set_salsa(self, salsa):
        self.salsa = salsa

    def set_ingredientes(self, ingredientes):
        self.ingredientes = ingredientes

    def set_tecnica_coccion(self, tecnica):
        self.tecnica_coccion = tecnica

    def set_presentacion(self, presentacion):
        self.presentacion = presentacion

    def set_maridaje(self, maridaje):
        self.maridaje = maridaje

    def set_acabado_extra(self, acabado):
        self.acabado_extra = acabado

class ConstructorPizza(ABC):
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def construir_tamano(self):
        pass

    @abstractmethod
    def construir_masa(self):
        pass

    @abstractmethod
    def construir_salsa(self):
        pass
    
    @abstractmethod
    def construir_ingredientes(self):
        pass
    
    @abstractmethod
    def construir_tecnica_coccion(self):
        pass
    
    @abstractmethod
    def construir_presentacion(self):
        pass
    
    @abstractmethod
    def construir_maridaje(self):
        pass
    
    @abstractmethod
    def construir_acabado_extra(self):
        pass

class ConstructorPizzaPersonalizada(ConstructorPizza):
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.pizza = Pizza("Personalizada")

    def construir_tamano(self):
        self.pizza.set_tamano(input("Elije el tamaño (individual, mediana, familiar): "))

    def construir_masa(self):
        self.pizza.set_masa(input("Elije la masa (fina, gruesa, de masa madre): "))
         
    def construir_salsa(self):
        self.pizza.set_salsa(input("Elije la salsa (tomate, barbacoa, crema): "))
        
    def construir_ingredientes(self):
        ingredientes = self.elegir_ingredientes()
        self.pizza.set_ingredientes(ingredientes)
    
    def construir_tecnica_coccion(self):
        self.pizza.set_tecnica_coccion(input("Elije la técnica de cocción (horno de leña, horno tradicional): "))
        
    def construir_presentacion(self):
        self.pizza.set_presentacion(input("Elije la presentación (clásica, artística): "))
        
    def construir_maridaje(self):
        self.pizza.set_maridaje(input("Elije el maridaje (vino tinto, cerveza, refresco): "))
        
    def construir_acabado_extra(self):
        self.pizza.set_acabado_extra(input("Elije el acabado extra (aceite de trufa, glaseado de balsámico): "))
    
    def elegir_ingredientes(self):
        ingredientes_disponibles = ["Pepperoni", "Champiñones", "Cebolla", "Salchicha", "Tocino", "Queso Extra", "Aceitunas", "Tomates", "Espinacas", "Tocino", "Salchicha italiana", "Jamón", "Anchoas", "Piña", "Maíz", "Alcachofas", "Chorizo", "Espárragos", "Berenjena", "Rúcula", "Huevo"]
        print("Elige hasta 5 ingredientes (escribe 'listo' cuando termines):")
        ingredientes_elegidos = []
        while len(ingredientes_elegidos) < 5:
            print(f"Ingredientes disponibles: {ingredientes_disponibles}")
            ingrediente = input("Ingresa el ingrediente: ")
            if ingrediente.lower() == 'listo':
                break
            elif ingrediente in ingredientes_disponibles:
                ingredientes_elegidos.append(ingrediente)
                ingredientes_disponibles.remove(ingrediente)
            else:
                print("Ingrediente inválido. Por favor elige de la lista de ingredientes disponibles.")
        return ingredientes_elegidos

# Declarar las variables como globales
entry_nombre_usuario = None
entry_contraseña = None
entry_nombre_personal = None
entry_correo = None

def obtener_informacion_cliente(entry_nombre_usuario, entry_contraseña, entry_nombre_personal, entry_correo):
    nombre_usuario = entry_nombre_usuario.get()
    contraseña = entry_contraseña.get()
    nombre_personal = entry_nombre_personal.get()
    correo = entry_correo.get()

    cliente = Cliente(nombre_usuario, contraseña, nombre_personal, correo)
    return cliente

def crear_interfaz():
    global entry_nombre_usuario, entry_contraseña, entry_nombre_personal, entry_correo
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Pizzería Delizioso")

    # Etiquetas y campos de entrada para la información del cliente
    tk.Label(root, text="Nombre de Usuario: ").grid(row=0, column=0)
    entry_nombre_usuario = tk.Entry(root)
    entry_nombre_usuario.grid(row=0, column=1)

    tk.Label(root, text="Contraseña: ").grid(row=1, column=0)
    entry_contraseña = tk.Entry(root, show="*")
    entry_contraseña.grid(row=1, column=1)

    tk.Label(root, text="Nombre Personal: ").grid(row=2, column=0)
    entry_nombre_personal = tk.Entry(root)
    entry_nombre_personal.grid(row=2, column=1)

    tk.Label(root, text="Correo: ").grid(row=3, column=0)
    entry_correo = tk.Entry(root)
    entry_correo.grid(row=3, column=1)

    def hacer_pedido():
        cliente = obtener_informacion_cliente(entry_nombre_usuario, entry_contraseña, entry_nombre_personal, entry_correo)
        root.destroy()  # Cerrar la ventana principal
        cliente.guardar_en_csv()
        crear_interfaz_pizza()

    # Botón para realizar el pedido
    tk.Button(root, text="Hacer Pedido", command=hacer_pedido).grid(row=4, column=0, columnspan=2)
    root.mainloop()
    
ingredientes_disponibles = [
        "Pepperoni", "Champiñones", "Cebolla", "Salchicha", "Tocino",
        "Queso Extra", "Aceitunas", "Tomates", "Espinacas", "Salchicha italiana",
        "Jamón", "Anchoas", "Piña", "Maíz", "Alcachofas", "Chorizo",
        "Espárragos", "Berenjena", "Rúcula", "Huevo"
    ]
def guardar_pizza():
    # Obtener los valores ingresados por el usuario
    tamano = tamano_var.get()
    masa = masa_var.get()
    salsa = salsa_var.get()
    ingredientes_seleccionados = [ingredientes_disponibles[i] for i in lista_ingredientes.curselection()]
    tecnica_coccion = tecnica_coccion_var.get()
    presentacion = presentacion_var.get()
    maridaje = maridaje_var.get()
    acabado_extra = acabado_extra_var.get()

    with open("ej2/Pedidos.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            tamano,
            masa,
            salsa,
            ', '.join(ingredientes_seleccionados),
            tecnica_coccion,
            presentacion,
            maridaje,
            acabado_extra
        ])
    
    messagebox.showinfo("Pedido Realizado")
    

def crear_interfaz_pizza():
    # Crear la ventana para la creación de la pizza
    global tamano_var, masa_var, salsa_var, lista_ingredientes, tecnica_coccion_var, presentacion_var, maridaje_var, acabado_extra_var 
    root_pizza = tk.Tk()
    root_pizza.title("Creación de Pizza Personalizada")
    #Sugerimos las recomendaciones de la casa
    sugerencias = tk.Label(root_pizza, text="Recomendaciones de la casa\nNuestra salsa barbacoa\nEl horno de piedra es el más exitoso de la zona\nNuestra salchica italiana procedente de Venecia")
    sugerencias.pack()
    # Agregar elementos de la interfaz para construir la pizza

    tk.Label(root_pizza, text="Elije el tamaño (individual, mediana, familiar):").pack()
    tamano_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=tamano_var).pack()

    tk.Label(root_pizza, text="Elije la masa (fina, gruesa, de masa madre):").pack()
    masa_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=masa_var).pack()

    tk.Label(root_pizza, text="Elije la salsa (tomate, barbacoa, crema): ").pack()
    salsa_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=salsa_var).pack()

    tk.Label(root_pizza, text="Elige hasta 5 ingredientes:").pack()

    lista_ingredientes = tk.Listbox(root_pizza, selectmode=tk.MULTIPLE, height=len(ingredientes_disponibles))

    for ingrediente in ingredientes_disponibles:
        lista_ingredientes.insert(tk.END, ingrediente)

    lista_ingredientes.pack()

    tk.Label(root_pizza, text="Elije la técnica de cocción (horno de leña, horno tradicional): ").pack()
    tecnica_coccion_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=tecnica_coccion_var).pack()

    tk.Label(root_pizza, text="Elije la presentación (clásica, artística): ").pack()
    presentacion_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=presentacion_var).pack()
 
    tk.Label(root_pizza, text="Elije el maridaje (vino tinto, cerveza, refresco): ").pack()
    maridaje_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=maridaje_var).pack()

    tk.Label(root_pizza, text="Elije el acabado extra (aceite de trufa, glaseado de balsámico): ").pack()
    acabado_extra_var = tk.StringVar()
    tk.Entry(root_pizza, textvariable=acabado_extra_var).pack()

    tk.Button(root_pizza, text="Enviar pedido", command=guardar_pizza).pack()
    root_pizza.mainloop()