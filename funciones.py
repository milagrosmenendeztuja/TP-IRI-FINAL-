import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# número de ciclos a simular
num_ciclos = 5
# paso para los graficos
paso = 50

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


#Grafico las funciones de presion y volumen

def Graficar(i, est, T, ax1, ax2, tiempo_total, presion_aortica, volumen_ventricular):
    
    # se usa un "paso" para saltar algunos puntos y reducir la carga
    indice_inicio = i * paso
    indice_fin = (i + 1) * paso

    # Calculo presión aórtica y volumen solo para el intervalo actual
    for j in range(indice_inicio, indice_fin):
        if j < len(tiempo_total):
            t_relativo = tiempo_total[j] % T
            
            # Presión aórtica
            if 0 <= t_relativo < T * 3 / 8:
                presion_aortica[j] = p1(t_relativo, est)
            elif T * 3 / 8 <= t_relativo < T * 5 / 8:
                presion_aortica[j] = p2(t_relativo, est)
            else:
                presion_aortica[j] = p3(t_relativo, est)

            # Volumen ventricular
            tiempo_ciclo = tiempo_total[j] % T
            if 0 <= tiempo_ciclo < T * (2/8):
                volumen_ventricular[j] = v1(tiempo_ciclo, est, T)
            elif T * (2/8) <= tiempo_ciclo < T * (2.5/8):
                volumen_ventricular[j] = v2(tiempo_ciclo, est, T)
            elif T * (2.5/8) <= tiempo_ciclo < T * (5/8):
                volumen_ventricular[j] = v3(tiempo_ciclo, est, T)
            else:
                volumen_ventricular[j] = v4(tiempo_ciclo, est, T)

    
    ax1.clear()
    ax1.set_facecolor("#f0f0f0") 
    ax1.plot(tiempo_total[:indice_fin], presion_aortica[:indice_fin], color="blue", linewidth=2, label="Presión Aórtica")
    ax1.set_xlabel("Tiempo (s)", color="darkblue")
    ax1.set_ylabel("Presión (mmHg)", color="darkblue")  
    ax1.set_title("Simulación de la Presión Aórtica", color="darkblue") 
    ax1.legend(loc="upper right")
    ax1.grid(True, linestyle="--", alpha=0.7)
    ax1.set_ylim(0, 200)
    
    ax2.clear()
    ax2.set_facecolor("#fff4e0")  
    ax2.plot(tiempo_total[:indice_fin], volumen_ventricular[:indice_fin], color="purple", linewidth=2, label="Volumen Ventricular")
    ax2.set_xlabel("Tiempo (s)", color="purple")  
    ax2.set_ylabel("Volumen (mL)", color="purple") 
    ax2.set_title("Simulación del Volumen Ventricular", color="purple") 
    ax2.legend(loc="upper right")
    ax2.grid(True, linestyle="--", alpha=0.7)
    ax2.set_ylim(0, 180)

# funcion principal donde se llaman los graficos
def Principal(est):

    if est["Estado"] == "Muerte":
        T = 60/60
    else:
        T = 60 / est["Lpm"]  # Periodo total en segundos

    tiempo_total = np.linspace(0, num_ciclos * T, num_ciclos * 1000)

    presion_aortica = np.zeros_like(tiempo_total)
    volumen_ventricular = np.zeros_like(tiempo_total)

    # Creo figura y subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Imprimo que estado se esta graficando
    fig.text(0.5, 0.95, f"Estado: {est['Estado']}", ha='center', va='top', fontsize=14, color="Lightblue")

    # Configurar animación
    anim = FuncAnimation(
        fig,
        Graficar,
        frames=len(tiempo_total) // paso,  # Dividir en intervalos de 10 para avanzar más rápido
        fargs=(est, T, ax1, ax2, tiempo_total, presion_aortica, volumen_ventricular),
        interval=30,
        repeat=False
    )

    plt.tight_layout()
    plt.show()

    