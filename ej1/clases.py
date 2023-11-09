from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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