# Evaluaci-n-Continua-Patrones-Creacionales-2023_2024
## Ejercicio 1. Análisis Modular de las Activaciones del SAMUR-Protección Civil en Madrid con Abstract Factory
En este ejercicio nos piden que a partir de un CSV sobre el SAMUR que debemos modelizar crear una Abstract Factory en la que cada fábrica hace funciones diferentes. 
Voy a hacer el modelaje del csv y la creación de las clases de la fábrica en el archivo clases.py.
Como no primero importamos:
```from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```
Para empezar modelaremos el csv eliminando valores nulos, creando nuevas columnas con números para poder hacer el análisis estadístico y definiendo la relación de estas columnas con las originales.
El código propueto es el siguiente:
```
URL = "https://datos.madrid.es/egob/catalogo/300178-4-samur-activaciones.csv"

# Leer CSV desde la URL
data = pd.read_csv(URL, sep=';', encoding='ISO-8859-1')
print(data.head())


#2
#Limpar filas con columnas vacias
df = data.dropna(subset=["Hospital"])
df = df.dropna(subset=["Distrito"])
df = df.dropna(subset=["Hora Solicitud"])
print(df.info())  # Mostrar las primeras filas para visualizar los datos
#Creo nuevas columnas con números para poder hacer el análisis estadístico
df["Num_Código"] = pd.factorize(df["Código"])[0]+1
df["Num_Distrito"] = pd.factorize(df["Distrito"])[0]+1
df["Num_Hospital"] = pd.factorize(df["Hospital"])[0]+1
#Guardo la relación de las columnas en una nueva variable en forma de diccionario
relacion_codigo = df.set_index('Num_Código')['Código'].to_dict()
relacion_distrito = df.set_index('Num_Distrito')['Distrito'].to_dict()
```

Ahora procedemos a crear las fábricas que devolveran como productos en el caso de la fábrica 1 el analisis estadístico de unos datos del csv y en el caso de la fábrica 2 hara gráficas dependiendo de la exigencia.
Código propuesto:
```
# Creamos las fábricas
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass

class ConcreteFactory1(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()

    def analisis_estadistico(self, df):
        return f"{self.create_product_a().useful_function_a(df)}\n{self.create_product_b().useful_function_b(df)}"

class ConcreteFactory2(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()
    
class AbstractProductA(ABC):
    @abstractmethod
    def useful_function_a(self, df) -> str:
        pass

class AbstractProductB(ABC):
    @abstractmethod
    def useful_function_b(self, df) -> None:
        pass
#Fabrica 1 Producto A es calcular la media, moda y mediana de la hora en la que se solicitan los servicios
class ConcreteProductA1(AbstractProductA):
    def useful_function_a(self, df) -> str:
        # Convertir 'Hora Solicitud' a un formato de hora válido
        df['Hora Solicitud'] = pd.to_datetime(df['Hora Solicitud'])
        
        # Extraer la hora del día
        horas = df['Hora Solicitud'].dt.hour

        # Calcular la media, moda y mediana de las activaciones por día
        media_por_dia = horas.groupby(horas // 24).mean()
        moda_por_dia = horas.groupby(horas // 24).agg(lambda x: x.value_counts().index[0])
        mediana_por_dia = horas.groupby(horas // 24).median()

        return f"Análisis estadístico de la columna 'Hora Solicitud' por día:\n" \
               f"Media por día:\n{media_por_dia}\n\n" \
               f"Moda por día:\n{moda_por_dia}\n\n" \
               f"Mediana por día:\n{mediana_por_dia}\n"
#Ahora con el producto B calcularemos lo mismo sobre la columna Distrito
class ConcreteProductB1(AbstractProductB):
    def useful_function_b(self, df) -> str:
        media_Distrito = df['Num_Distrito'].mean()
        moda_Distrito = df['Num_Distrito'].mode()
        mediana_Distrito = df['Num_Distrito'].median()
        return f"Análisis estadístico de la columna Distrito.\nLa media es {media_Distrito}\nLa moda es {moda_Distrito.iloc[0]}\nLa mediana es {mediana_Distrito}\nEsto significa que la media es CHAMARTIN.\nLa moda es CENTRO.\nY la mediana es CHAMARTIN"
#Ya estamos con la fábrica 2, en este caso una gráfica sobre cuantas veces se repiten los valores en la columna Código
class ConcreteProductA2(AbstractProductA):
    def useful_function_a(self, df) -> str:
        # Generar la gráfica de los diferentes valores de Código
        plt.figure(figsize=(12, 8))
        df['Código'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title("Frecuencia de Motivos de Emergencia")
        plt.xlabel("Motivo de Emergencia")
        plt.ylabel("Frecuencia")
        
        # Guardar la gráfica
        plt.savefig("ej1/frecuencia_codigos.png")

        return "Gráfica de frecuencia de Motivos de Emergencia guardada como 'frecuencia_codigos.png'."

#Ahora haremos un histograma de activaciones por mes
class ConcreteProductB2(AbstractProductB):
    def useful_function_b(self, df) -> str:
        # Calcular la cantidad de activaciones por mes
        activaciones_por_mes = df['Mes'].value_counts().sort_index()

        # Generar el histograma
        plt.figure(figsize=(12, 8))
        plt.hist(df['Mes'], bins=range(0, 13), align='left', rwidth=0.8, color='skyblue', edgecolor='black')
        plt.title("Histograma de Activaciones por Mes")
        plt.xlabel("Mes")
        plt.ylabel("Frecuencia")
        plt.xticks(range(0, 12))

        plt.savefig("ej1/histograma_activaciones.png")
        plt.show()

        return f"Activaciones por mes:\n{activaciones_por_mes}\n\nHistograma de activaciones guardado como 'histograma_activaciones.png'"
```
Como podemos ver las gráficas generadas por la fábrica 2 se guardan en la carpeta actual.
Para hacer funcionar el código pondremos el lanzador en el archivo main.py el cual queda de la siguiente forma:
```
from clases import *
#Diseñamos el lanzador
if __name__ == "__main__":
    factory1 = ConcreteFactory1()
    factory2 = ConcreteFactory2()

    # Utilizar ConcreteFactory1 para el análisis estadístico
    print("Client: Testing client code with the first factory type:")
    print(factory1.create_product_a().useful_function_a(df))
    print(factory1.create_product_b().useful_function_b(df))

    print("\n")

    # Utilizar ConcreteFactory2 para mostrar estadísticas y generar histograma
    print("Client: Testing client code with the second factory type:")
    print(factory2.create_product_a().useful_function_a(df))
    print(factory2.create_product_b().useful_function_b(df))
```
Al ejecutar el código recibimo esto en el terminal:
Primero información sobre el dataset:
```
    Año    Mes Hora Solicitud Hora Intervención                Código       Distrito Hospital
0  2019  ENERO        0:08:09           0:08:15  Intoxicación etílica         CENTRO      NaN
1  2019  ENERO        0:09:13               NaN   Violencia de genero  VALLECAS PTE.      NaN
2  2019  ENERO        0:24:12           0:24:22                 Otros         CENTRO      NaN
3  2019  ENERO        0:28:55               NaN  Intoxicación etílica         CENTRO      NaN
4  2019  ENERO        0:29:11           0:34:02    Casual: caída, etc         CENTRO      NaN
<class 'pandas.core.frame.DataFrame'>
Int64Index: 46739 entries, 5 to 149900
Data columns (total 7 columns):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   Año                46739 non-null  int64
 1   Mes                46739 non-null  object
 2   Hora Solicitud     46739 non-null  object
 3   Hora Intervención  46739 non-null  object
 4   Código             46739 non-null  object
 5   Distrito           46739 non-null  object
 6   Hospital           46739 non-null  object
dtypes: int64(1), object(6)
memory usage: 2.9+ MB
None
```
Ahora se inicia la primera fábrica que nos dara dos análisis sobre diferentes datos, primer analisis:
```
Client: Testing client code with the first factory type:
Análisis estadístico de la columna 'Hora Solicitud' por día:
Media por día:
Hora Solicitud
0    13.316588
Name: Hora Solicitud, dtype: float64

Moda por día:
Hora Solicitud
0    12
Name: Hora Solicitud, dtype: int64

Mediana por día:
Hora Solicitud
0    14.0
Name: Hora Solicitud, dtype: float64
```
Segundo análisis:
```
Análisis estadístico de la columna Distrito.
La media es 9.289415691392627
La moda es 3
La mediana es 9.0
Esto significa que la media es CHAMARTIN.
La moda es CENTRO.
Y la mediana es CHAMARTIN
```
La segunda fábrica como hemos dicho anteriormente proporciona unas gráficas, estas son las siguientes:
La primera sobre la cantidad de activciones que tiene cada mes
![image](https://github.com/alexlomu/Evaluaci-n-Continua-Patrones-Creacionales-2023_2024/assets/91721507/07289bde-066e-4298-b779-14b6a93e9a5a)
Y la segunda sobre el motivo de las activaciones
![image](https://github.com/alexlomu/Evaluaci-n-Continua-Patrones-Creacionales-2023_2024/assets/91721507/434541da-ed2a-480d-b887-1fb706717184)

## Ejercicio 2. Sistema Integral de Creación y Gestión de Pizzas Gourmet con Almacenamiento en CSV utilizando el Patrón Builder
En este ejercicio tenemos que crear una pizzeria siguiendo diversas carcterísticas usando el Patrón Builder.
Para ello usaremos el archivo builder.py en el que primero, obviamente haremos las importacione necesarias:
```
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
import csv
import tkinter as tk
from tkinter import messagebox
```
A continuación diseñaremos clases básicas así como la de Cliente y la de Pizza, el código es el siguiente:
```
#Clase Cliente
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

#Clase Pizza
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
```
Ahora haremos el ConstructorPizza con el formato del builder:
```
#El constructor de pizza
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
```
A continuación declararemos unas variables para evitarnos errores luego y una función que nos permitirá coger los datos personales que nos da el usuario y implementarlos con la clase Cliente:
```
# Declarar las variables como globales
entry_nombre_usuario = None
entry_contraseña = None
entry_nombre_personal = None
entry_correo = None

#Funcion para que el cliente se guarde usando la clase
def obtener_informacion_cliente(entry_nombre_usuario, entry_contraseña, entry_nombre_personal, entry_correo):
    nombre_usuario = entry_nombre_usuario.get()
    contraseña = entry_contraseña.get()
    nombre_personal = entry_nombre_personal.get()
    correo = entry_correo.get()

    cliente = Cliente(nombre_usuario, contraseña, nombre_personal, correo)
    return cliente
```
Ahora inicializaremos la interfaz en la que el usuario introducirá sus datos para a posterior hacer el pedido:
```
#Interfaz del cliente
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
```
Como podemos observar contiene la clase hacer_pedido a la cual llamamos con el botón de hacer pedido la cual cogerá los datos del cliente los meterá en una instancia de Cliente además de guardar los datos en clientes.csv y inicializar la siguiente interfaz que nos permitirá personalizar la pizza además de incluir unas sugerencias para el consumidor:
```
#Creamos la interfaz para pedir la pizza
def crear_interfaz_pizza():
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
```
Cabe mencionar que antes de dicha función hemos definido una lista con ingredientes y otra función guardar_pizza() para acabar con el trabajo:
```
ingredientes_disponibles = [
        "Pepperoni", "Champiñones", "Cebolla", "Salchicha", "Tocino",
        "Queso Extra", "Aceitunas", "Tomates", "Espinacas", "Salchicha italiana",
        "Jamón", "Anchoas", "Piña", "Maíz", "Alcachofas", "Chorizo",
        "Espárragos", "Berenjena", "Rúcula", "Huevo"
]
#Funcion final para guardar la pizza en las variables correspondientes y se guarde el pedido en el csv
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
    
    messagebox.showinfo(title="Pedido Realizado", message= "El pedido se ha envido correctamente")
```
Para ejecutar el código lo haremos desde el archivo main.py usando la función crear_interfaz():
```
from builder import *
#Lanzamos la interfaz
if __name__ == "__main__":
    crear_interfaz()
```
Las diferentes interfaces y mensajes se ven de la siguiente manera:
Interfaz del cliente:
![image](https://github.com/alexlomu/Evaluaci-n-Continua-Patrones-Creacionales-2023_2024/assets/91721507/088c8ede-51c9-4b73-9cbf-a967bf721273)
Interfaz de personalización de la pizza:
![image](https://github.com/alexlomu/Evaluaci-n-Continua-Patrones-Creacionales-2023_2024/assets/91721507/acac267d-a595-4734-8259-04f768fc14c8)
Mensaje conforme se ha enviado correctamente el pedido:
![image](https://github.com/alexlomu/Evaluaci-n-Continua-Patrones-Creacionales-2023_2024/assets/91721507/3b1c9b05-45ae-4d5f-b186-19216116c081)


