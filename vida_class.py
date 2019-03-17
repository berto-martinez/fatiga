import numpy as np
import matplotlib.pyplot as plot
import scipy as sci

class vida():
    
    def __init__(self,material,fatiga,seguridad):

        a = self.leer_material(material)
        
        self.E = a[0]
        self.Rp02 = a[1] 
        self.n = a[2]
        self.Vcycl = a[3]
        self.nu = a[4]
        self.T = a[5]
        
        self.eps_range_st18 = self.leer_fatiga(fatiga)
        self.coef_seguridad = int(seguridad)

    def interpolacion(self,T_calc):

        self.E_T = np.interp(T_calc,self.T,self.E)
        self.Rp02_T = np.interp(T_calc,self.T,self.Rp02)
        self.n_T = np.interp(T_calc,self.T,self.n)
        self.Vcycl_T = np.interp(T_calc,self.T,self.Vcycl)
        self.nu_T = np.interp(T_calc,self.T,self.nu)
        
    def deformacion_plastica(self,sigma_vm,T_calc,K_t): # Devuelve el punto de corte de Neuber con RO [sigma,epsilon]
        
        self.interpolacion(T_calc)
        sigma = np.linspace(0,800,5000) # Vector de tensiones
        b = 2/3*(1+self.nu_T)*sigma/self.E_T + 0.002 * (sigma/(self.Vcycl_T*self.Rp02_T))**self.n_T - 2/3*(1+self.nu_T)*((sigma_vm*self.coef_seguridad)*K_t)**2/(self.E_T*sigma) # Vector Ramberg-Osgood - Curva Neuber para obtener deformacion
        idx = (np.abs(b - 0)).argmin() # Buscar minimo de b (corte)
        deformacion = 2/3*(1+self.nu_T)*((sigma_vm*self.coef_seguridad)*K_t)**2/(self.E_T*sigma[idx]) #Deformacion 3D
        deformacion_1d = sigma[idx]/self.E_T+ 0.002 * (sigma[idx]/(self.Vcycl_T*self.Rp02_T))**(self.n_T)
        return sigma[idx],deformacion_1d,deformacion
    
    def interp_logaritmica(self,dictio,epsilon,T):
        a = [[] for i in range(len(dictio["range"]))]
        i=0
        for r in dictio["range"]:
            for t in dictio["temp"]:
                a[i].append(dictio[str(t)][i])
            i = i+1
        b = []
        for x in a:
            b.append(np.interp(T,dictio["temp"],x))
        
        m = []
        r = dictio["range"]
        for y in range(len(b)-1):
            m.append((b[y]-b[y+1])/(np.log10(r[y])-np.log10(r[y+1])))
        
        for i in range(len(b)):
            if epsilon > b[0]:
                num = 0
            elif epsilon <= b[len(b)-1]:
                num = len(b)-2
            elif epsilon < b[i]:
                num = i
        life = r[num+1]*10**((epsilon-b[num+1])/m[num])
        return life
    
    def incluir_temperatura(self,temp_file,stress_file,output_file):
        try:
            temperature = open(temp_file,"r")
            fem = open(stress_file,"r")
            output = open(output_file,"w")
            
            flag1 = 0
            sep = '.'
            temperature_dict = {}
            for lines in temperature: # Create TEMP dictionary
                if flag1 == 0:
                    flag1 = 1
                else:
                    words = lines.split()
                    temperature_dict[words[0]] = words[1]
                    
            for lines in fem:
                words = lines.split()
                if words[4] != '0.0000000': # Eliminar nodos con sigma 0
                    only_integer = words[0].split(sep,1)[0] # Obtiene el nodo para buscar la temperatura en el diccionario
                    temp_search = str(temperature_dict[only_integer])
                    temp_search_dot = temp_search.replace(',','.') # Cambiar , por .
                    a = self.deformacion_plastica(float(words[4])/2,float(temp_search_dot)-273,1)
                    life = self.interp_logaritmica(self.eps_range_st18,a[1]*100,float(temp_search_dot)-273)
                    output_line = words[0]+','+words[1]+','+words[2]+','+words[3]+','+words[4]+','+temp_search_dot+','+str(life)+'\n'
                    output.write(output_line)
            
            temperature.close()
            fem.close()
            output.close()
        except ValueError:
            temperature.close()
            fem.close()
            output.close()

    
    def deformacion_plastica_manual(self,S,E_T,nu_T,Rp02_T,Vcycl_T,n_T,K_t):
         
        sigma = np.linspace(0,800,10000) # Vector de tensiones
        b = 2/3*(1+nu_T)*sigma/E_T + 0.002 * (sigma/(Vcycl_T*Rp02_T))**n_T - 2/3*(1+nu_T)*(sigma_vm*K_t)**2/(E_T*sigma) # Vector Ramberg-Osgood - Curva Neuber para obtener deformacion
        idx = (np.abs(b - 0)).argmin() # Buscar minimo de b (corte)
        deformacion = 2/3*(1+nu_T)*(sigma_vm*K_t)**2/(E_T*sigma[idx]) #Deformacion 3D
        return sigma[idx],deformacion
    
    def graficas(self,sigma_vm,T,K_t):
        
        self.interpolacion(T)
        #print(self.E_T)
        sigma = np.linspace(0,1400,100000)
        
        RO_3D = 2/3*(1+self.nu_T)*sigma/self.E_T + 0.002 * (sigma/(self.Vcycl_T*self.Rp02_T))**self.n_T
        elastic = 2/3*(1+self.nu_T)*sigma/self.E_T
        neuber = 2/3*(1+self.nu_T)*(sigma_vm*K_t)**2/(self.E_T*sigma)
        
        return RO_3D,elastic,neuber,sigma

    def graficas1d(self,sigma_vm,T,K_t):
        
        self.interpolacion(T)
        sigma = np.linspace(0,1400,100000)
        
        RO_3D = sigma/self.E_T + 0.002 * (sigma/(self.Vcycl_T*self.Rp02_T))**self.n_T
        elastic = sigma/self.E_T
        neuber = (sigma_vm*K_t)**2/(self.E_T*sigma)

        plot.plot(RO_3D,sigma,label='RO 3D')
        plot.plot(elastic,sigma,label='Elastic')
        plot.plot(neuber,sigma,label='neuber')
        axes = plot.gca()
        plot.legend()
        axes.set_xlim([0 , 0.0025])
        axes.set_ylim([0 , 250])
        plot.show()
        
        return RO_3D,sigma
    
    def graficas_mecanica(self,E,V,Rp,n):
        sigma = np.linspace(0,800,1000)
        RO_3D = sigma/E + 0.002 * (sigma/(V*Rp))**n

        return RO_3D,sigma
    
    def graficas_vida(self,dictio,T):
        epsilon = np.linspace(0.0001,0.1,1000)
        a = []
        for i in epsilon:
            a.append(self.interp_logaritmica(dictio,i*100,T))

        return a,epsilon
    
    def leer_material(self,archivo):
        E = []
        Rp02 = []
        n = []
        Vcycl = []
        nu = []
        T = []
        material_file = open(archivo,"r")
        cont = 0
        for line in material_file:
            if cont == 0:
                for words in line.split():
                    E.append(float(words))
            if cont == 1:
                for words in line.split():
                    Rp02.append(float(words))
            if cont == 2:
                for words in line.split():
                    n.append(float(words))
            if cont == 3:
                for words in line.split():
                    Vcycl.append(float(words))
            if cont == 4:
                for words in line.split():
                    nu.append(float(words))
            if cont == 5:
                for words in line.split():
                    T.append(float(words))
            cont += 1
        material_file.close()
        return E,Rp02,n,Vcycl,nu,T

    def leer_fatiga(self,archivo):
        dic_fatiga = {} #Diccionario para fatiga
        valores = []
        T = [] #Guarda las temperaturas
        n = [] #Guarda el rango de fatiga (n)
        a = [] #Temporal para guardar valores de strain
        fatiga_file = open(archivo,"r")
        cont = 0
        for line in fatiga_file:
            if cont == 0:
                for words in line.split():
                    n.append(int(words))
            if cont == 1:
                for words in line.split():
                    T.append(int(words))
            if cont > 1:
                for words in line.split():
                    a.append(float(words.split("*")[0])*float(words.split("*")[1]))
                valores.append(a)
                a = [] #Reset variable a para guardar los siguientes datos
            cont += 1
        dic_fatiga["range"]=n
        dic_fatiga["temp"]=T
        for i in range(len(T)):
            dic_fatiga[str(T[i])]=valores[i]
            
        fatiga_file.close()
        return dic_fatiga
