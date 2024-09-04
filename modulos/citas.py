from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controladores import agregar_cita, obtener_paciente_por_cedula, obtener_proximas_citas, obtener_paciente_por_id

class PantallaCitas:
    def __init__(self, master):
        self.master = master

    def mostrar(self):
        self.master.limpiar_contenido()

        frame_agendar_cita = Frame(self.master.frame_contenido, bg="#e0f7fa", padx=20, pady=20)
        frame_agendar_cita.pack(fill=BOTH, expand=1)

        etiqueta_titulo = Label(frame_agendar_cita, text="Agendar Cita", font=("Arial", 24, "bold"), bg="#00acc1", fg="#ffffff")
        etiqueta_titulo.pack(pady=20, fill=X)

        etiquetas_campos = [
            ("Cédula del Paciente:", 'cedula_paciente_entry'),
            ("Fecha (YYYY-MM-DD):", 'fecha_entry'),
            ("Hora (HH:MM):", 'hora_entry'),
            ("Ubicación:", 'ubicacion_entry'),
            ("Descripción:", 'descripcion_entry')
        ]

        for texto, var in etiquetas_campos:
            frame = Frame(frame_agendar_cita, bg="#e0f7fa")
            frame.pack(fill=X, pady=5)
            label = Label(frame, text=texto, bg="#e0f7fa", fg="#00796b", font=("Arial", 14), width=20, anchor="w")
            label.pack(side=LEFT, padx=5)
            if texto.startswith("Fecha"):
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd', font=("Arial", 14), bg="#ffffff", fg="#00796b")
            elif texto.startswith("Hora"):
                entry = ttk.Combobox(frame, values=[f"{str(h).zfill(2)}:00" for h in range(24)], font=("Arial", 14))
            elif texto.startswith("Descripción"):
                entry = Text(frame, font=("Arial", 14), bg="#ffffff", fg="#00796b", height=5, wrap=WORD)
            else:
                entry = Entry(frame, font=("Arial", 14), bg="#ffffff", fg="#00796b")
            setattr(self, var, entry)
            entry.pack(side=LEFT, fill=X, expand=YES, padx=5)

        frame_botones = Frame(frame_agendar_cita, bg="#e0f7fa")
        frame_botones.pack(pady=20)

        boton_guardar = Button(frame_botones, text="Guardar Cita", command=self.guardar_cita, bg="#00acc1", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5)
        boton_guardar.pack(side=LEFT, padx=10)

        boton_volver = Button(frame_botones, text="Volver", command=self.master.crear_bienvenida, bg="#fbc02d", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5)
        boton_volver.pack(side=LEFT, padx=10)

        self.mostrar_historial_citas()

    def guardar_cita(self):
        cedula_paciente = self.cedula_paciente_entry.get()
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get()
        ubicacion = self.ubicacion_entry.get().lower()
        descripcion = self.descripcion_entry.get("1.0", END).strip().lower()

        if cedula_paciente and fecha and hora:
            try:
                paciente = obtener_paciente_por_cedula(cedula_paciente)
                if not paciente:
                    messagebox.showerror("Error", "Paciente no encontrado")
                    return
                paciente_id = paciente[0]

                agregar_cita(paciente_id, fecha, hora, descripcion, ubicacion)
                messagebox.showinfo("Éxito", "Cita agregada correctamente")
                self.master.crear_bienvenida()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la cita: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def mostrar_historial_citas(self):
        frame_historial = Frame(self.master.frame_contenido, bg="#e0f7fa", padx=20, pady=20)
        frame_historial.pack(fill=BOTH, expand=1)

        etiqueta_historial = Label(frame_historial, text="Historial de Citas Agendadas", font=("Arial", 20, "bold"), bg="#00acc1", fg="#ffffff")
        etiqueta_historial.pack(pady=10, fill=X)

        tree_frame = Frame(frame_historial, bg="#e0f7fa")
        tree_frame.pack(fill=BOTH, expand=1)

        tree_scroll_vertical = Scrollbar(tree_frame, orient="vertical")
        tree_scroll_vertical.pack(side=RIGHT, fill=Y)

        tree_scroll_horizontal = Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_horizontal.pack(side=BOTTOM, fill=X)

        self.tree_historial_citas = ttk.Treeview(tree_frame, columns=("Paciente", "Fecha", "Hora", "Descripción", "Ubicación"), show='headings',
                                                 yscrollcommand=tree_scroll_vertical.set, xscrollcommand=tree_scroll_horizontal.set)
        self.tree_historial_citas.heading("Paciente", text="Paciente")
        self.tree_historial_citas.heading("Fecha", text="Fecha")
        self.tree_historial_citas.heading("Hora", text="Hora")
        self.tree_historial_citas.heading("Descripción", text="Descripción")
        self.tree_historial_citas.heading("Ubicación", text="Ubicación")
        self.tree_historial_citas.tag_configure('oddrow', background='lightblue')
        self.tree_historial_citas.tag_configure('evenrow', background='white')
        self.tree_historial_citas.pack(side=LEFT, fill=BOTH, expand=1)

        tree_scroll_vertical.config(command=self.tree_historial_citas.yview)
        tree_scroll_horizontal.config(command=self.tree_historial_citas.xview)

        historial_citas = obtener_proximas_citas()
        for i, cita in enumerate(historial_citas):
            paciente = obtener_paciente_por_id(cita[1])
            if paciente:
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree_historial_citas.insert("", "end", values=(paciente[1] + " " + paciente[2], cita[2], cita[3], cita[4], cita[5]), tags=(tag,))
            else:
                print(f"Paciente con id {cita[1]} no encontrado.")

        # Ajustar el ancho de la columna "Descripción" según el contenido
        self.ajustar_ancho_columna_descripcion()

    def ajustar_ancho_columna_descripcion(self):
        max_len = 0
        for item in self.tree_historial_citas.get_children():
            descripcion = self.tree_historial_citas.item(item, 'values')[3]  # Obtener el valor de la columna "Descripción"
            max_len = max(max_len, len(descripcion))

        # Ajustar el ancho de la columna según el contenido
        new_width = max_len * 10  # Ajustar el multiplicador según sea necesario
        self.tree_historial_citas.column("Descripción", width=new_width)

if __name__ == "__main__":
    root = Tk()
    root.title("Sistema de Agendamiento de Citas")
    root.geometry("1024x768")
    app = PantallaCitas(root)
    app.mostrar()
    root.mainloop()
