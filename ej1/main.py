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

    
