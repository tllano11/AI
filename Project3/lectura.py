""" INSTALACION
sudo -H pip install setuptools                                                  
sudo -H pip install pyexcel                                                     
sudo -H pip install pyexcel-xlsx                                                
"""

# -*- coding: utf-8 -*-

import pyexcel as pe

"""Funcion para la lectura del archivo de excel con el campo texto predefinido"""

def lectura(nombreArchivo):
    listaTweets = []
    excel = pe.iget_records(file_name=nombreArchivo)
    for tweet in excel:
        listaTweets.append(tweet['Texto'])          #Creacion de una lista con los tweets
    print(listaTweets)

def main(archivo):
    lectura(archivo)

if __name__ == "__main__":
    main("Todos.xlsx")
