#################################################################
# Diagrama de Gantt Básico para Programación de la Producción   #
# Autor: Rodrigo Maranzana                                      #
# Contacto: https://www.linkedin.com/in/rodrigo-maranzana       #
# Fecha: Octubre 2020                                           #
#################################################################

from platform import machine
import matplotlib.pyplot as plt
import numpy as np
import random

from breakdown import Breakdown

def initialize_gantt(maquinas, ht, n, m):
    # Parámetros:
    hbar = 10
    tticks = 10
    nmaq = len(maquinas)

    # Creación de los objetos del plot:
    # plt.figure(figsize=(8,6), dpi=60)
    fig, gantt = plt.subplots()
    fig.set_size_inches(18, 10)

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
    gantt.set_xlabel("Czas", fontsize=16)
    gantt.set_ylabel("Maszyna", fontsize=16)
    gantt.set_title(
        f'Diagram Gantta dla {n=} {m=} ',
        fontsize = 18,
    )
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

def add_subtask(diagrama, t0, d, maq, job_namesea, color=None, suspend_operation_names=False):
    """Function for adding tasks to the diagram"""
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
    if not suspend_operation_names:
        gantt.text( x=(t0 + d/2), y=(hbar*imaq + hbar/2),
                    s=f"{job_namesea} ({d})", va='center', ha='center', color='white')

def add_machinebreakdown(diagrama, breakdown:Breakdown):
    gantt = diagrama["ax"]
    hbar = diagrama["hbar"]
    imaq = breakdown.m
    mb_color = (1, 0, 0)

    # Position machine machine breakdown
    gantt.broken_barh(  xranges=[(breakdown.t0, breakdown.breakdown_duration)],
                        yrange=(hbar*imaq, hbar),
                        facecolors=(mb_color),
                        hatch='/')

    gantt.text( x=(breakdown.t0 + breakdown.breakdown_duration/2),
                y=(hbar*imaq + hbar/2),
                s=f"MB {breakdown.breakdown_duration}",
                color='black',
                va='center', ha='center')

def complete_gantt(diagrama, schedule, machine_names, task_names, breakdown=None, suspend_operation_names=False):
    # Add subtasks:
    for subtask in schedule:
        add_subtask(
            diagrama,
            subtask["t0"],
            subtask["d"],
            machine_names[subtask["i_machine"]],
            task_names[subtask["i_task"]],
            suspend_operation_names=suspend_operation_names
        )

    # Add machine breakdown
    if breakdown is not None:
        add_machinebreakdown(
            diagrama,
            breakdown,
        )

def create_gantt_fs(schedule, machine_names, task_names, breakdown=None, suspend_operation_names=False):
    # Horizonte temporal:
    # ultima_subtask = schedule[-1]
    # ht = ultima_subtask["t0"] + ultima_subtask["d"]
    ht = 10

    for task in schedule:
        end_of_task = task["t0"] + task["d"] 
        ht = max(ht, end_of_task)

    n = len(task_names)
    m = len(machine_names)

    # Creamos el diagrama de gantt:
    diagrama = initialize_gantt(machine_names, int(ht), n, m)

    # Completamos el gantt:
    complete_gantt(diagrama, schedule, machine_names, task_names, breakdown=breakdown, suspend_operation_names=suspend_operation_names)

    # Retornamos el diagrama:
    return diagrama

def create_and_show_gantt_fs(schedule, machine_names, task_names, breakdown=None, suspend_operation_names=False):
    create_gantt_fs(schedule, machine_names, task_names, breakdown=breakdown, suspend_operation_names=suspend_operation_names)
    mostrar()

def mostrar():
    plt.show()

def guardar_figura(diagrama):
    diagrama['fig'].savefig('filename.png', dpi=225)
