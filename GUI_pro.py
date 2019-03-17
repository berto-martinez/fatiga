import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from vida_class import vida
from tkinter import *
from tkinter import ttk, font
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import asksaveasfilename
import threading


LARGE_FONT= ("Verdana 12 bold")


class fatiga(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Vida a fatiga")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
          
        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self,*args)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="INPUTS", font=LARGE_FONT)
        label.grid(row=0,column=0)
        self.controller = controller
        
        self.mecanica = tk.StringVar() #Propiedades mecanicas
        self.fatiga = tk.StringVar()
        self.solucion_nodal = tk.StringVar() #Propiedades mecanicas
        self.fichero_temperatura = tk.StringVar()
        self.output = tk.StringVar()
        self.tension_manual = tk.StringVar()
        self.temperatura_manual = tk.StringVar()
        self.seguridad = tk.StringVar()
        
        label = tk.Label(self, text="Parametros R-O")
        label.grid(row=1,column=0)
        label = tk.Label(self, text="Parametros S-N")
        label.grid(row=2,column=0)
        label = tk.Label(self, text="Fichero solucion nodal")
        label.grid(row=3,column=0)
        label = tk.Label(self, text="Fichero temperaturas")
        label.grid(row=4,column=0)
        
        self.ctext1 = ttk.Entry(self, textvariable=self.mecanica, width=30)
        self.ctext1.grid(row=1,column=1)
        self.ctext2 = ttk.Entry(self, textvariable=self.fatiga, width=30)
        self.ctext2.grid(row=2,column=1)
        self.ctext3 = ttk.Entry(self, textvariable=self.solucion_nodal, width=30)
        self.ctext3.grid(row=3,column=1)
        self.ctext4 = ttk.Entry(self, textvariable=self.fichero_temperatura, width=30)
        self.ctext4.grid(row=4,column=1)
        
        
        self.boton1 = ttk.Button(self, text="Buscar...", command=self.buscar_mecanica)
        self.boton2 = ttk.Button(self, text="Buscar...", command=self.buscar_fatiga)
        self.boton1.grid(row=1, column=2)
        self.boton2.grid(row=2, column=2)
        self.boton3 = ttk.Button(self, text="Buscar...", command=self.buscar_nodal)
        self.boton4 = ttk.Button(self, text="Buscar...", command=self.buscar_temp)
        self.boton3.grid(row=3, column=2)
        self.boton4.grid(row=4, column=2)


        button5 = ttk.Button(self, text="Mostrar curvas",command=lambda: controller.show_frame(PageThree))
        button5.grid(row=1,column=3)
        
        button6 = ttk.Button(self, text="Mostrar curvas",command=lambda: controller.show_frame(PageTwo))
        button6.grid(row=2,column=3)
        
        label = tk.Label(self, text="OUTPUT", font=LARGE_FONT)
        label.grid(row=5,column=0)
        
        label = tk.Label(self, text="Fichero de resultados")
        label.grid(row=6,column=0)

        self.ctext5 = ttk.Entry(self, textvariable=self.output, width=30)
        self.ctext5.grid(row=6,column=1)

        label = tk.Label(self, text="Coef. Seguridad")
        label.grid(row=7,column=0)

        self.ctext12 = ttk.Entry(self, textvariable=self.seguridad, width=30)
        self.ctext12.grid(row=7,column=1)

        self.boton7 = ttk.Button(self, text="Guardar como...", command=self.definir_output)
        self.boton7.grid(row=6, column=2)

        self.boton8 = ttk.Button(self, text="GENERAR FICHERO DE RESULTADOS", command=self.interm)
        self.boton8.grid(row=8, column=0)
        
        label = tk.Label(self, text="CURVA DE NEUBER MANUAL", font=LARGE_FONT)
        label.grid(row=9,column=0)
        
        label = tk.Label(self, text="Tension [MPa]")
        label.grid(row=10,column=0)
        label = tk.Label(self, text="Temperatura [ºC]")
        label.grid(row=11,column=0)
        
        self.ctext10 = ttk.Entry(self, textvariable=self.tension_manual, width=30)
        self.ctext10.grid(row=10,column=1)

        self.ctext11 = ttk.Entry(self, textvariable=self.temperatura_manual, width=30)
        self.ctext11.grid(row=11,column=1)

        button10 = ttk.Button(self, text="Mostrar corrección",command=lambda: controller.show_frame(PageOne))
        button10.grid(row=12,column=3)

        
    def buscar_mecanica(self):
        archivo_mecanica = askopenfilename()
        self.mecanica.set(archivo_mecanica)
    def buscar_fatiga(self):
        archivo_fatiga = askopenfilename()
        self.fatiga.set(archivo_fatiga)
    def buscar_nodal(self):
        archivo_nodal = askopenfilename()
        self.solucion_nodal.set(archivo_nodal)
    def buscar_temp(self):
        archivo_temp = askopenfilename()
        self.fichero_temperatura.set(archivo_temp)
    def definir_output(self):
        archivo_out = asksaveasfilename()
        self.output.set(archivo_out)
    def interm(self):
        label = tk.Label(self, text="Generando...")
        label.grid(row=8,column=1)
        threading.Thread(target=self.generar_fichero).start() #Threading para mostrar el aviso de generando

    def generar_fichero(self):

        x = vida(self.mecanica.get(),self.fatiga.get(),self.seguridad.get())
        x.incluir_temperatura(self.fichero_temperatura.get(),self.solucion_nodal.get(),self.output.get())
        label = tk.Label(self, text="HECHO")
        label.grid(row=8,column=2)



class PageOne(tk.Frame):

    def __init__(self, parent, controller,*args):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Corrección de Neuber manual", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.control = controller

        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.set_xlim([0 , 10000])
        self.a.set_ylim([0 , 0.1])
        self.a.spines['right'].set_visible(False)
        self.a.spines['top'].set_visible(False)

        button1 = ttk.Button(self, text="Página inicio",command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Mostrar corrección de Neuber",command=lambda: self.pintar_grafica())
        button2.pack()
        
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def pintar_grafica(self):
        pagina_inicio = self.control.get_page(StartPage)

        if  len(pagina_inicio.tension_manual.get()) != 0 and len(pagina_inicio.temperatura_manual.get()) != 0 and len(pagina_inicio.mecanica.get()) != 0 and len(pagina_inicio.fatiga.get()) != 0: #Comprobar que la cadena es mayor que 0
            self.a.clear()
            x = vida(pagina_inicio.mecanica.get(),pagina_inicio.fatiga.get(),1)
            res = x.graficas(float(pagina_inicio.tension_manual.get()),float(pagina_inicio.temperatura_manual.get()),1)
            deform = x.deformacion_plastica(float(pagina_inicio.tension_manual.get()),float(pagina_inicio.temperatura_manual.get()),1)
            self.a.set_xlim([0 , deform[1]*2])
            self.a.set_ylim([0 , float(pagina_inicio.tension_manual.get())+150])
            res = x.graficas(float(pagina_inicio.tension_manual.get()),float(pagina_inicio.temperatura_manual.get()),1)
            self.a.plot(res[0],res[3],label='RO 3D')
            self.a.plot(res[1],res[3],label='Elastic')
            self.a.plot(res[2],res[3],label='Neuber')
            self.a.plot(deform[2], deform[0], 'ro')
            self.a.annotate("(%s,%s)" %(round(deform[2],3), round(deform[0],1)),xy=(deform[1], deform[0]), xycoords='data',backgroundcolor="silver")
            self.a.legend(shadow=True)
            self.a.set_title("Tension %s MPa. Temperatura %s ºC"% (pagina_inicio.tension_manual.get(),pagina_inicio.temperatura_manual.get()))
            self.canvas.draw()
        else:
            self.a.clear()
            self.canvas.draw()
            print("Error")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller,*args):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Curvas S-N", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.control = controller

        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.set_xlim([0 , 10000])
        self.a.set_ylim([0 , 0.1])

        button1 = ttk.Button(self, text="Página inicio",command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Mostrar grafica",command=lambda: self.pintar_grafica())
        button2.pack()

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def pintar_grafica(self):
        pagina_inicio = self.control.get_page(StartPage)

        if  len(pagina_inicio.mecanica.get()) != 0 and len(pagina_inicio.fatiga.get()) != 0: #Comprobar que la cadena es mayor que 0
            self.a.clear()
            x = vida(pagina_inicio.mecanica.get(),pagina_inicio.fatiga.get(),1)
            self.a.set_xlim([0 , 10000])
            self.a.set_ylim([0 , 0.1])
            self.a.set_xlabel('Vida[ciclos]')
            self.a.set_ylabel('Deformacion [mm/mm]')
            for i in range(len(x.eps_range_st18["temp"])):
                res = x.graficas_vida(x.eps_range_st18,x.eps_range_st18["temp"][i]) 
                self.a.plot(res[0],res[1],label=str(x.eps_range_st18["temp"][i])) 
            self.a.legend(shadow=True)
            self.canvas.draw()
        else:
            self.a.clear()
            self.canvas.draw()
            print("Error")


class PageThree(tk.Frame):

    def __init__(self, parent, controller,*args):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Curvas Ramberg-Osgood", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.control = controller

        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.set_xlim([0 , 0.1])
        self.a.set_ylim([0 , 800])

        button1 = ttk.Button(self, text="Página inicio",command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Mostrar gráfica",command=lambda: self.pintar_grafica())
        button2.pack()

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def pintar_grafica(self):
        pagina_inicio = self.control.get_page(StartPage)

        if  len(pagina_inicio.mecanica.get()) != 0 and len(pagina_inicio.fatiga.get()) != 0: #Comprobar que la cadena es mayor que 0
            self.a.clear()
            self.a.set_xlabel('Deformacion [mm/mm]')
            self.a.set_ylabel('Tension [MPa]')
            x = vida(pagina_inicio.mecanica.get(),pagina_inicio.fatiga.get(),1)
            self.a.set_xlim([0 , 0.1])
            self.a.set_ylim([0 , 800])
            for i in range(len(x.T)):
                datos = x.graficas_mecanica(x.E[i],x.Vcycl[i],x.Rp02[i],x.n[i])
                self.a.plot(datos[0],datos[1],label=str(x.T[i]))            
            self.a.legend(shadow=True)
            self.canvas.draw()
        else:
            self.a.clear()
            self.canvas.draw()
            print("Error")

app = fatiga()
app.mainloop()