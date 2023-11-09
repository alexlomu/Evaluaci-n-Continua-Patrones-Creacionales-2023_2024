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


