import tkinter as Tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class app(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry("1150x500")
        self.title("Interfaz")
        self.configure(bg="peachpuff")

        Label(text="Bienvenido a ---", font=("Arial 12 bold"), bg="peachpuff").place(x=20, y=20)
        
        self.note = ttk.Notebook(self)
        self.note.pack()
        self.note.config(width="1100", height="400")
        self.note.place(x=20, y=50)

        self.tab1 = ttk.Frame(self.note)
        self.tab2 = ttk.Frame(self.note)
        self.tab3 = ttk.Frame(self.note)

        self.note.add(self.tab1, text="Descubrir nuevos Animes")
        self.note.add(self.tab2, text="Favoritos")
        self.note.add(self.tab3, text="Recomendaciones")

#----------Busqueda

        Label(self.tab1, text="Ingrese datos", font=("Arial 12 bold")).place(x=20, y=20)


        self.busqueda2=ttk.Combobox(self.tab1, width=10, values=["Serie", "Película"])
        self.busqueda2.place(x=150, y=55)

        self.busqueda3=Entry(self.tab1, width=10)
        self.busqueda3.place(x=250, y=55)

        self.busqueda2=Entry(self.tab1, width=10)
        self.busqueda2.place(x=350, y=55)

        self.busqueda4=Entry(self.tab1, width=10)
        self.busqueda4.place(x=450, y=55)

        self.busqueda7=ttk.Combobox(self.tab1, width=10, values=["Si", "No"])
        self.busqueda7.place(x=850, y=55)

        self.buscar=Button(self.tab1, text="Buscar")
        self.buscar.place(x=1050, y=55)

        self.addFavorite=Button(self.tab1, text="Agregar a favoritos")
        self.addFavorite.place(x=800, y=340)

        self.busqueda2=ttk.Combobox(self.tab1, width=10, values=[""])
        self.busqueda2.place(x=950, y=350)

        columnas = ('no','sp','g','e','y','a','va','m','f')
        self.tree = ttk.Treeview(self.tab1, columns=columnas, show='headings', height=9)

        self.tree.heading('no', text="Nombre")
        self.tree.heading('sp', text="Serie/Película")
        self.tree.heading('g', text="Género")
        self.tree.heading('e', text="Estudio")
        self.tree.heading('y', text="Año")
        self.tree.heading('a', text="Aceptación")
        self.tree.heading('va', text="Actores de voz")
        self.tree.heading('m', text="Manga")
        self.tree.heading('f', text="Favorito")

        self.tree.column('no', width=110)
        self.tree.column('sp', width=100)
        self.tree.column('g', width=100)
        self.tree.column('e', width=100)
        self.tree.column('y', width=100)
        self.tree.column('a', width=100)
        self.tree.column('va', width=200)
        self.tree.column('m', width=100)
        self.tree.column('f', width=100)
        

        self.tree.place(x=20, y=100)

        #-----Favoritos

        columnas = ('no','sp','g','e','y','a','va','m',)
        self.tree2 = ttk.Treeview(self.tab2, columns=columnas, show='headings', height=9)

        self.tree2.heading('no', text="Nombre")
        self.tree2.heading('sp', text="Serie/Película")
        self.tree2.heading('g', text="Género")
        self.tree2.heading('e', text="Estudio")
        self.tree2.heading('y', text="Año")
        self.tree2.heading('a', text="Aceptación")
        self.tree2.heading('va', text="Actores de voz")
        self.tree2.heading('m', text="Manga")

        self.tree2.column('no', width=110)
        self.tree2.column('sp', width=100)
        self.tree2.column('g', width=100)
        self.tree2.column('e', width=100)
        self.tree2.column('y', width=100)
        self.tree2.column('a', width=100)
        self.tree2.column('va', width=200)
        self.tree2.column('m', width=100)

        self.tree2.place(x=20, y=80)

        self.RemoveFavorite=Button(self.tab2, text="Eliminar de favoritos")
        self.RemoveFavorite.place(x=800, y=340)

        self.busqueda3=ttk.Combobox(self.tab2, width=10, values=[""])
        self.busqueda3.place(x=950, y=350)

    #----------Recomendaciones

        columnas = ('no','sp','g','e','y','a','va','m')
        self.tree3 = ttk.Treeview(self.tab3, columns=columnas, show='headings', height=9)

        self.tree3.heading('no', text="Nombre")
        self.tree3.heading('sp', text="Serie/Película")
        self.tree3.heading('g', text="Género")
        self.tree3.heading('e', text="Estudio")
        self.tree3.heading('y', text="Año")
        self.tree3.heading('a', text="Aceptación")
        self.tree3.heading('va', text="Actores de voz")
        self.tree3.heading('m', text="Manga")

        self.tree3.column('no', width=110)
        self.tree3.column('sp', width=100)
        self.tree3.column('g', width=100)
        self.tree3.column('e', width=100)
        self.tree3.column('y', width=100)
        self.tree3.column('a', width=100)
        self.tree3.column('va', width=200)
        self.tree3.column('m', width=100)

        self.tree3.place(x=20, y=80)

        self.addFavorite3=Button(self.tab3, text="Agregar a favoritos")
        self.addFavorite3.place(x=800, y=340)

        self.busqueda4=ttk.Combobox(self.tab3, width=10, values=[""])
        self.busqueda4.place(x=950, y=350)

app().mainloop()