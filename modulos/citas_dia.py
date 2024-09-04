from tkinter import *
from tkinter import ttk, messagebox
from controladores import obtener_citas_dia, obtener_paciente_por_id

class PantallaCitasDia:
    def __init__(self, master, fecha, ubicacion):
        self.master = master
        self.fecha = fecha
        self.ubicacion = ubicacion

    def mostrar(self):
        self.master.limpiar_contenido()

        frame_citas_dia = Frame(self.master.frame_contenido, bg="#f0f4f7", padx=20, pady=20)
        frame_citas_dia.pack(fill=BOTH, expand=1)

        etiqueta = Label(frame_citas_dia, text="Citas del Día", font=("Arial", 24, "bold"), bg="#f0f4f7", fg="#333333")
        etiqueta.pack(pady=20)

        self.tree_citas_dia = ttk.Treeview(frame_citas_dia, columns=("Paciente", "Fecha", "Hora", "Descripción", "Ubicación"), show='headings')
        self.tree_citas_dia.heading("Paciente", text="Paciente")
        self.tree_citas_dia.heading("Fecha", text="Fecha")
        self.tree_citas_dia.heading("Hora", text="Hora")
        self.tree_citas_dia.heading("Descripción", text="Descripción")
        self.tree_citas_dia.heading("Ubicación", text="Ubicación")
        self.tree_citas_dia.tag_configure('oddrow', background='lightgrey')
        self.tree_citas_dia.tag_configure('evenrow', background='white')
        self.tree_citas_dia.pack(fill=BOTH, expand=1)

        self.cargar_citas_dia()

        boton_volver = Button(frame_citas_dia, text="Volver", command=self.master.crear_bienvenida, bg="#ffc107", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_volver.pack(pady=10, fill=X)

    def cargar_citas_dia(self):
        citas = obtener_citas_dia(self.fecha)
        citas_filtradas = [cita for cita in citas if cita[5].lower() == self.ubicacion.lower()]
        citas_ordenadas = sorted(citas_filtradas, key=lambda x: x[3])  # Ordenar por hora

        for i, cita in enumerate(citas_ordenadas):
            paciente = obtener_paciente_por_id(cita[1])
            if paciente:
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree_citas_dia.insert("", "end", values=(f"{paciente[1]} {paciente[2]}", cita[2], cita[3], cita[4], cita[5]), tags=(tag,))
            else:
                print(f"Paciente con id {cita[1]} no encontrado.")

if __name__ == "__main__":
    root = Tk()
    root.title("Sistema de Agendamiento de Citas")
    root.geometry("1024x768")
    app = PantallaCitasDia(root, "2023-08-07", "consultorio")  # Ejemplo de uso
    app.mostrar()
    root.mainloop()
