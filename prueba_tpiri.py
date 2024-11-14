import numpy as np
import matplotlib.pyplot as plt
from funciones import Principal

est1 = {
     "Estado" : "Reposo",
     "Lpm" : 75,
     "P_diast" : 120,
     "P_sist" : 80,
     "V_diast" : 130,
     "V_sist" : 50,
}

est2 = {
     "Estado" : "Trotando",
     "Lpm" : 135,
     "P_diast" : 140,
     "P_sist" : 90,
     "V_diast" : 150,
     "V_sist" : 70,
}

est3 ={
     "Estado" : "Corriendo",
     "Lpm" : 165,
     "P_diast" : 160,
     "P_sist" : 100,
     "V_diast" : 170,
     "V_sist" : 80,
}

est4 = {
     "Estado" : "Fibrilacion",
     "Lpm" :  np.random.randint(160,180),
     "P_diast" : 170,
     "P_sist" : 100,
     "V_diast" : 170,
     "V_sist" : 80,
}

est5 = {
     "Estado" : "Arritmia",
     "Lpm" : np.random.randint(35,50),
     "P_diast" : 100,
     "P_sist" : 50,
     "V_diast" : 110,
     "V_sist" : 50,
}

est6= {
    "Estado" : "Durmiendo",
    "Lpm" : 50,
     "P_diast" : 100,
     "P_sist" : 50,
     "V_diast" : 110,
     "V_sist" : 50,
}

est7 = {
     "Estado" : "Muerte",
     "Lpm" : 0,
     "P_diast" : 0,
     "P_sist" : 0,
     "V_diast" : 0,
     "V_sist" : 0,
}


print("\n VAMOS A GRAFICAR TU PRESION Y VOLUMEN VENTRICULAR:")
while True:
        print("Elija el estado del paciente")
        print("1. Reposo ")
        print("2. Trotando")
        print("3. Corriendo")
        print("4. Fibrilacion")
        print("5. Arritmia (bradicardia)")
        print("6. Durmiendo")
        print("7. Muerte")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            Principal(est1)
        elif opcion == "2":
            Principal(est2)
        elif opcion == "3":
            Principal(est3)
        elif opcion == "4":
            Principal(est4)
        elif opcion == "5":
            Principal(est5)
        elif opcion == "6":
            Principal(est6)
        elif opcion == "7":
            Principal(est7)            
        elif opcion == "":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor intente de nuevo.")