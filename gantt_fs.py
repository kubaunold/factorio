#################################################################
# Diagrama de Gantt Básico para Programación de la Producción   #
# Autor: Rodrigo Maranzana                                      #
# Contacto: https://www.linkedin.com/in/rodrigo-maranzana       #
# Fecha: Octubre 2020                                           #
#################################################################

import matplotlib.pyplot as plt
import numpy as np
import random

def inicializar_gantt(maquinas, ht):
    # Parámetros:
    hbar = 10
    tticks = 10
    nmaq = len(maquinas)

    # Creación de los objetos del plot:
    fig, gantt = plt.subplots()

    # Diccionario con parámetros:
    diagrama = {
        "fig": fig,
        "ax": gantt,
        "hbar": hbar,
        "tticks": tticks,
        "maquinas": maquinas,
        "ht": ht,
        "colores": {}
    }

    # Etiquetas de los ejes:
    gantt.set_xlabel("Time")
    gantt.set_ylabel("Machines")

    # Límites de los ejes:
    gantt.set_xlim(0, ht)
    gantt.set_ylim(nmaq*hbar, 0)

    # Divisiones del eje de tiempo:
    gantt.set_xticks(range(0, ht, 1), minor=True)
    # gantt.grid(True, axis='x', which='both')

    # Divisiones del eje de máquinas:
    gantt.set_yticks(range(hbar, nmaq*hbar, hbar), minor=True)
    gantt.grid(True, axis='y', which='minor')

    # Etiquetas de máquinas:
    gantt.set_yticks(np.arange(hbar/2, hbar*nmaq - hbar/2 + hbar,
                            hbar))
    gantt.set_yticklabels(maquinas)

    return diagrama

# Función para armar tareas:
def add_subtask(diagrama, t0, d, maq, job_namesea, color=None):
    maquinas = diagrama["maquinas"]
    hbar = diagrama["hbar"]
    gantt = diagrama["ax"]
    ht = diagrama["ht"]

    # Color:
    if diagrama["colores"].get(job_namesea) == None:
        if color == None:
            r = random.random()
            g = random.random()
            b = random.random()
            color = (r, g, b)

            diagrama["colores"].update({job_namesea: color})
    else:
        color = diagrama["colores"].get(job_namesea)

    # Índice de la máquina:
    imaq = maquinas.index(maq)
    # Posición de la barra:
    gantt.broken_barh([(t0, d)], (hbar*imaq, hbar),
                      facecolors=(color))
    # Posición del texto:
    gantt.text(x=(t0 + d/2), y=(hbar*imaq + hbar/2),
                  s=f"{job_namesea} ({d})", va='center', ha='center', color='white')

def completar_gantt(diagrama, schedule, n_maqs, n_tareas):
    # Agregamos las subtasks:
    for subtask in schedule:

        add_subtask(
            diagrama,
            subtask["t0"],
            subtask["d"],
            n_maqs[subtask["i_machine"]],
            n_tareas[subtask["i_task"]]
        )

def crear_gantt_fs(schedule, n_maqs, n_tareas):
    # Horizonte temporal:
    # ultima_subtask = schedule[-1]
    # ht = ultima_subtask["t0"] + ultima_subtask["d"]
    ht = 10

    for task in schedule:
        end_of_task = task["t0"] + task["d"] 
        ht = max(ht, end_of_task)

    # Creamos el diagrama de gantt:
    diagrama = inicializar_gantt(n_maqs, int(ht))

    # Completamos el gantt:
    completar_gantt(diagrama, schedule, n_maqs, n_tareas)

    # Retornamos el diagrama:
    return diagrama

def crear_y_mostrar_gantt_fs(schedule, n_maqs, n_tareas):
    # Creamos el gantt:
    crear_gantt_fs(schedule, n_maqs, n_tareas)

    # Plotteamos:
    mostrar()

def mostrar():
    plt.show()

def guardar_figura(diagrama):
    diagrama['fig'].savefig('filename.png', dpi=225)
