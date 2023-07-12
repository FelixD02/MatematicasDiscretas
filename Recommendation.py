import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from random import sample
import sys

df_movies = pd.read_excel('C:\\Users\\FELIX\\Downloads\\Proyecto MD\\datamovies.xlsx') #Crea un dataframe con el excel de la base de datos
g_movies = nx.Graph() #Creamo el grafo

class movie:
    def __init__(self, name, categoryA, categoryB, director, year, castA, castB):
        self.name = name
        self.categoryA = categoryA
        self.categoryB = categoryB
        self.director = director
        self.year = year
        self.castA = castA
        self.castB = castB

    def imprimir_pelicula(self):
        print("Película:", self.name)
        print("Categoría A:", self.categoryA)
        print("Categoría B:", self.categoryB)
        print("Director:", self.director)
        print("Año:", self.year)

l_movies = []

for index, row in df_movies.iterrows():
    # Obtener los valores de cada columna
    name = row['Name']
    categoryA = row['CategoryA']
    categoryB = row['CategoryB']
    director = row['Director']
    year = row['Year']
    castA = row['CastA']
    castB = row['CastB']

    # Crear una instancia de Pelicula y agregarla a la lista
    pelicula = movie(name, categoryA, categoryB, director, year, castA, castB)
    g_movies.add_node(pelicula)
    l_movies.append(pelicula)

for i in range(len(l_movies)):
    current_movie = l_movies[i]
    
    for j in range(i+1, len(l_movies)):
        next_movie = l_movies[j]
        
        weight = 0
        
        if current_movie.categoryA == next_movie.categoryA or current_movie.categoryA == next_movie.categoryB:
            weight += 1
            
        if current_movie.categoryB == next_movie.categoryA or current_movie.categoryB == next_movie.categoryB:
            weight += 1
                
        if current_movie.director == next_movie.director:
            weight += 1
            
        if current_movie.year == next_movie.year:
            weight += 1
            
        if current_movie.castA == next_movie.castA or current_movie.castA == next_movie.castB:
            weight += 1
        
        if current_movie.castB == next_movie.castA or current_movie.castB == next_movie.castB:
            weight += 1
        
        if weight == 1:
            g_movies.add_edge(current_movie, next_movie, weight=1)
        elif weight == 2:
            g_movies.add_edge(current_movie, next_movie, weight=2)
        elif weight == 3:
            g_movies.add_edge(current_movie, next_movie, weight=3)
        elif weight == 4:
            g_movies.add_edge(current_movie, next_movie, weight=4)
    

def obtener_recomendaciones(pelicula, num_recomendaciones):
    
    # Obtener los vecinos de la película
    vecinos = g_movies.neighbors(pelicula)
    
    # Calcular los pesos de similitud de los vecinos
    pesos_similitud = {}
    for vecino in vecinos:
        peso = g_movies[pelicula][vecino]['weight']
        pesos_similitud[vecino] = peso
    
    # Ordenar los vecinos por peso de similitud (de mayor a menor)
    vecinos_ordenados = sorted(pesos_similitud, key=pesos_similitud.get, reverse=True)
    
    # Obtener las recomendaciones basadas en los vecinos ordenados
    recomendaciones = vecinos_ordenados[:num_recomendaciones]
    
    return recomendaciones

class MainWindow(QMainWindow): #IMPLEMENTACION DE LA INTERFAZ GRAFICA DE USUARIO
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SISTEMA DE RECOMENDACIÓN DE PELÍCULAS")
        
        self.movie_labels = []
        self.selected_movie = None
        
        self.create_movie_labels()
        self.create_subtitle()
        
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        
        # Agregar subtítulo al layout
        layout.addWidget(self.subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        # Agregar filas de imágenes al layout
        rows = [self.movie_labels[i:i+5] for i in range(0, len(self.movie_labels), 5)]
        for row in rows:
            row_layout = QHBoxLayout()
            for widget in row:
                row_layout.addWidget(widget)
            layout.addLayout(row_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.resize(1000, 350)  # Tamaño de la ventana: 1000 x 350

    def create_movie_labels(self):
        movie_names = [movie.name for movie in l_movies]
        selected_movies = sample(movie_names, 10)  # Obtener 10 películas al azar

        for movie_name in selected_movies:
            image_path = f"C:\\Users\\FELIX\\Downloads\\Proyecto MD\\Posters\\{movie_name}.jpg"  # Ruta a la imagen de la película
            print(movie_name)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(185, 285, Qt.AspectRatioMode.KeepAspectRatio)  # Ajustar tamaño de la imagen

            movie_label = QLabel(self)
            movie_label.setPixmap(pixmap)
            movie_label.setAlignment(Qt.AlignCenter)  # Centrar imagen
            movie_label.mousePressEvent = lambda event, movie=movie_name: self.select_movie(movie)

            movie_name_label = QLabel(self)
            movie_name_label.setText(movie_name)
            movie_name_label.setAlignment(Qt.AlignCenter)  # Centrar texto
            movie_name_label.setStyleSheet("font-size: 11pt;")  # Ajustar el tamaño de la fuente aquí

            layout = QVBoxLayout()
            layout.addWidget(movie_label)
            layout.addWidget(movie_name_label)

            container_widget = QWidget()
            container_widget.setLayout(layout)
            self.movie_labels.append(container_widget)

    def create_subtitle(self):
        self.subtitle_label = QLabel(self)
        self.subtitle_label.setText("Selecciona una Película:")
        self.subtitle_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        
    def mostrar_recomendaciones(self, movie):
        num_recomendaciones = 10
        recomendaciones = obtener_recomendaciones(movie, num_recomendaciones)
        print("Recomendaciones para", movie.name, ":")
        for recomendacion in recomendaciones:
            print(recomendacion.name)
        
        self.mostrar_recomendaciones_imagenes(recomendaciones)

    
    def select_movie(self, movie_name):
        self.selected_movie = movie_name
        print("Película seleccionada:", movie_name)
        
        # Buscar el objeto movie correspondiente al nombre
        selected_movie = next((movie for movie in l_movies if movie.name == movie_name), None)
        
        if selected_movie:
            self.mostrar_recomendaciones(selected_movie)
        else:
            print("No se encontró la película en la lista.")
            
    def mostrar_recomendaciones_imagenes(self, recomendaciones):
        layout = QVBoxLayout()

        # Agregar subtítulo al layout
        subtitle_label = QLabel(self)
        subtitle_label.setText("Películas Recomendadas:")
        subtitle_label.setFont(QFont("Helvetica", 16, QFont.Bold))
        layout.addWidget(subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        for i in range(0, len(recomendaciones), 5):
            row_layout = QHBoxLayout()
            for recomendacion in recomendaciones[i:i+5]:
                container_widget = QWidget()
                container_layout = QVBoxLayout()
                
                image_path = f"C:\\Users\\FELIX\\Downloads\\Proyecto MD\\Posters\\{recomendacion.name}.jpg"  # Ruta a la imagen de la película recomendada
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(185, 285, Qt.AspectRatioMode.KeepAspectRatio)  # Ajustar tamaño de la imagen

                movie_label = QLabel(self)
                movie_label.setPixmap(pixmap)
                movie_label.setAlignment(Qt.AlignCenter)  # Centrar imagen

                movie_name_label = QLabel(self)
                movie_name_label.setText(recomendacion.name)
                movie_name_label.setAlignment(Qt.AlignCenter)  # Centrar texto
                movie_name_label.setStyleSheet("font-size: 11pt;")
                
                
                container_layout.addWidget(movie_label)
                container_layout.addWidget(movie_name_label)
                
                container_widget.setLayout(container_layout)
                row_layout.addWidget(container_widget)
            
            layout.addLayout(row_layout)
        
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    

