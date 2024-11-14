import numpy as np
import matplotlib.pyplot as plt

# número de ciclos a simular
num_ciclos = 5 

#funcion que me genera lpm variados para la arritmia y fibrilacion
def generar_lpm_variado(base_lpm, num_ciclos, variacion=10):
    # Genera una lista de LPMs que varían aleatoriamente en cada ciclo
    return base_lpm + np.random.randint(-variacion, variacion, size=num_ciclos)


# Definición de las funciones para cada fase de la PRESION
def p1(x, est): #"x" es el tiempo relativo
        pres_media = (est["P_sist"] + est["P_diast"]) / 2
        pres_amplitud = (est["P_diast"] - est["P_sist"]) / 2

        return pres_media + pres_amplitud * np.sin(3 / 2 * np.pi * (est["Lpm"] / (60 * 3 / 8)) * x - 1 / 2 * np.pi)

def p2(x, est):
        pres_media = (est["P_sist"] + est["P_diast"]) / 2
        pres_amplitud = (est["P_diast"] - est["P_sist"]) / 2

        return pres_media + (pres_amplitud / 2) * np.sin(3 / 2 * np.pi * (est["Lpm"] / (60 * (3 / 8))) * x - 1 / 2 * np.pi)

def p3(x, est):
        pres_media = (est["P_sist"] + est["P_diast"]) / 2
        pres_amplitud = (est["P_diast"] - est["P_sist"]) / 2

        return pres_media + pres_amplitud * np.sin(-np.pi * (est["Lpm"] / (60 * (5 / 8))) * x - np.pi)

# Función para calcular la presión aórtica en cada instante de tiempo
def PRESION_AORT(est, T, F, ax):
        if est["Estado"] == "Arritmia":
                presion_aortica = []
                tiempo_total = []
        
                lpm_variado = generar_lpm_variado(est["Lpm"], num_ciclos)
        
                for ciclo, lpm in enumerate(lpm_variado):
                        T = 60 / lpm  # recalcular T para cada LPM
                        tiempo_ciclo = np.linspace(ciclo * T, (ciclo + 1) * T, 1000)

                        for t in tiempo_ciclo:
                                t_relativo = t % T
                                if 0 <= t_relativo < T * (3 / 8):
                                        presion_aortica.append(p1(t_relativo, est))
                                elif T * (3 / 8) <= t_relativo < T * (5 / 8):
                                        presion_aortica.append(p2(t_relativo, est))
                        else:
                                presion_aortica.append(p3(t_relativo, est))
                        tiempo_total.append(t)
                
                ax.plot(tiempo_total, presion_aortica, color="blue", linewidth=2, label="Presión Aórtica (Simulada con Arritmia)")
                # Cambia el color de fondo
                ax.set_facecolor("#F5F5DC")
                # Personaliza los textos con color y tamaño
                ax.set_xlabel("Tiempo (s)", fontsize=14, color="#008B8B") 
                ax.set_ylabel("Presión (mmHg)", fontsize=14, color="#008B8B")
                ax.set_title("Simulación de la Presión Aórtica con Arritmia", fontsize=14, color = "#800080")
                ax.legend(loc="upper right", fontsize=10)
                ax.grid(True, linestyle="--", color="#cfd8dc", alpha=0.7)
                ax.set_ylim(0, 200)

        else:
                # Tiempo total para la simulación
                tiempo_total = np.linspace(0, num_ciclos * T, num_ciclos * 1000)
                
                # Inicializo el array de la presión aórtica
                presion_aortica = np.zeros_like(tiempo_total)

                # Lleno el array 'presion_aortica' de acuerdo con cada fase en cada ciclo
                for i in range(len(tiempo_total)):

                # Ajuste del tiempo relativo al ciclo actual
                        t_relativo = tiempo_total[i] % T
                
                        if 0 <= t_relativo < T * 3 / 8:
                                presion_aortica[i] = p1(t_relativo, est)

                        elif T * 3 / 8 <= t_relativo < T * 5 / 8:
                                presion_aortica[i] = p2(t_relativo, est)

                        else:
                                presion_aortica[i] = p3(t_relativo, est)


                # Graficar en el eje dado
                ax.plot(tiempo_total, presion_aortica, color="blue", linewidth=2, label="Presión Aórtica (Simulada)")
                ax.set_xlabel("Tiempo (s)", fontsize=12)
                ax.set_ylabel("Presión (mmHg)", fontsize=12)
                ax.set_title("Simulación de la Presión Aórtica en Varios Ciclos", fontsize=14)
                ax.legend(loc="upper right", fontsize=10)
                ax.grid(True, linestyle="--", alpha=0.7)
                ax.set_ylim(0, 200)



# Definición de las funciones para cada fase del VOLUMEN
def v1(x, est, T):
        vol_medio = est["V_diast"] - est["V_sist"]

        return vol_medio + (est["V_sist"] * np.sin((3 / 4) * np.pi * (est["Lpm"] / (60 * (2/8))) * x))

def v2(x, est, T):
        return v1(T * (2/8), est, T)

def v3(x, est, T):
        vol_medio = est["V_diast"] - est["V_sist"]

        return est["V_sist"] + (vol_medio + est["V_sist"] * np.sin(3 / 4 * np.pi * (est["Lpm"] / (60 * 2/8)) * (T * (2/8))) - est["V_sist"]) * np.exp(-30 * (x - T * (2.5/8)))

def v4(x, est, T):
        vol_medio = est["V_diast"] - est["V_sist"]

        return vol_medio - (v3(T * (5/8), est, T) + 80) * np.exp(-30 * (x - T * (4.5/8)))


#Funcion para calcular el volumen ventricular en cada instante de tiempo
def VOLUMEN_VENT(est, T, F, ax):

        if est["Estado"] == "Arritmia":
                volumen_ventricular = []
                tiempo_total = []
        
                lpm_variado = generar_lpm_variado(est["Lpm"], num_ciclos)

                for ciclo, lpm in enumerate(lpm_variado):
                        T = 60 / lpm  # calcular T para el LPM de cada ciclo
                        tiempo_ciclo = np.linspace(ciclo * T, (ciclo + 1) * T, 1000)
                
                        # Calcular el volumen para cada fase del ciclo
                        for t in tiempo_ciclo:
                                t_relativo = t % T
                                if 0 <= t_relativo < T * (2/8):
                                        volumen_ventricular.append(v1(t_relativo, est, T))
                                elif T * (2/8) <= t_relativo < T * (2.5/8):
                                        volumen_ventricular.append(v2(t_relativo, est, T))
                                elif T * (2.5/8) <= t_relativo < T * (5/8):
                                        volumen_ventricular.append(v3(t_relativo, est, T))
                                else:
                                        volumen_ventricular.append(v4(t_relativo, est, T))
                
                                tiempo_total.append(t)

                ax.plot(tiempo_total, volumen_ventricular, color="purple", linewidth=2, label="Volumen Ventricular (Simulado)")
                ax.set_xlabel("Tiempo (s)", fontsize=12)
                ax.set_ylabel("Volumen (mL)", fontsize=12)
                ax.set_title("Simulación del Volumen Ventricular con Arritmia", fontsize=14)
                ax.legend(loc="upper right", fontsize=10)
                ax.grid(True, linestyle="--", alpha=0.7)
                ax.set_ylim(0, 180)
        else:
        
                # tiempo total para la simulacion
                tiempo_total = np.linspace(0, num_ciclos * T, num_ciclos * 1000)
                
                #Inicializar el array del volumen ventricular
                volumen_ventricular = np.zeros_like(tiempo_total)
                
                # Llenar el array 'volumen_ventricular' de acuerdo con cada fase en cada ciclo
                for i in range(len(tiempo_total)):
                        # Calcular el tiempo en el ciclo actual (modulo T)
                        tiempo_ciclo = tiempo_total[i] % T

                        if 0 <= tiempo_ciclo < T * (2/8):
                                volumen_ventricular[i] = v1(tiempo_ciclo, est, T)

                        elif T * (2/8) <= tiempo_ciclo < T * (2.5/8):
                                volumen_ventricular[i] = v2(tiempo_ciclo, est, T)

                        elif T * (2.5/8) <= tiempo_ciclo < T * (5/8):
                                volumen_ventricular[i] = v3(tiempo_ciclo, est, T)

                        elif T * (5/8) <= tiempo_ciclo < T:
                                volumen_ventricular[i] = v4(tiempo_ciclo, est, T)
                
                # Graficar en el eje dado
                ax.plot(tiempo_total, volumen_ventricular, color="purple", linewidth=2, label="Volumen Ventricular (Simulado)")
                # Cambia el color de fondo
                ax.set_facecolor("#F5F5DC")
                # Personaliza los textos con color y tamaño
                ax.set_xlabel("Tiempo (s)", fontsize=14, color="#008B8B") 
                ax.set_ylabel("Volumen (mL)", fontsize=14, color="#008B8B")
                ax.set_title("Simulación del Volumen Ventricular - 5 Ciclos", fontsize=16, color = "#800080")
                ax.legend(loc="upper right", fontsize=10, frameon=True, facecolor="#e8eaf6")
                ax.grid(True, linestyle="--", color="#cfd8dc", alpha=0.7)
                ax.set_ylim(0, 180)




def Principal(est):
    #Parámetros
    if est["Estado"] == "Muerte":
            T= 60/60
    else:
            T = 60 / est["Lpm"]  # periodo total en segundos
    F = est["Lpm"] / 60  # frecuencia en hz

    # Crear figura y subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Llamar a las funciones de presión y volumen, pasando cada eje
    PRESION_AORT(est, T, F, ax1)
    VOLUMEN_VENT(est, T, F, ax2)
    
    # Ajustar el diseño y mostrar la figura completa
    plt.tight_layout()  # Asegurarse de que la distribución de los subgráficos no se solape
    plt.show()  # Mostrar los gráficos de forma correcta