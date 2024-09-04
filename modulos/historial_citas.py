from tkinter import *
from tkinter import ttk, messagebox
from controladores import obtener_historial_clinico_completo, exportar_historial_clinico_excel, eliminar_historial

class PantallaHistoriasClinicas:
    def __init__(self, master):
        self.master = master

    def mostrar(self):
        self.master.limpiar_contenido()

        frame_historial_clinico = Frame(self.master.frame_contenido, bg="#f0f4f7", padx=20, pady=20)
        frame_historial_clinico.pack(fill=BOTH, expand=1)

        etiqueta_titulo = Label(frame_historial_clinico, text="Historias Clínicas", font=("Arial", 24, "bold"), bg="#00acc1", fg="#ffffff")
        etiqueta_titulo.pack(pady=20)

        self.tree_historial_clinico = ttk.Treeview(frame_historial_clinico, columns=("Cedula", "Paciente", "Fecha", "Motivo Consulta"), show='headings')
        self.tree_historial_clinico.heading("Cedula", text="Cédula")
        self.tree_historial_clinico.heading("Paciente", text="Paciente")
        self.tree_historial_clinico.heading("Fecha", text="Fecha")
        self.tree_historial_clinico.heading("Motivo Consulta", text="Motivo Consulta")
        self.tree_historial_clinico.tag_configure('oddrow', background='lightgrey')
        self.tree_historial_clinico.tag_configure('evenrow', background='white')
        self.tree_historial_clinico.pack(fill=BOTH, expand=1)

        historial = obtener_historial_clinico_completo()
        for i, h in enumerate(historial):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree_historial_clinico.insert("", "end", values=(h[1], f"{h[2]} {h[3]}", h[4], h[5]), tags=(tag,))

        frame_botones = Frame(frame_historial_clinico, bg="#f0f4f7")
        frame_botones.pack(pady=10, fill=X)

        boton_crear = Button(frame_botones, text="Crear Historial", command=self.crear_historial, bg="#28a745", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_crear.pack(side=LEFT, padx=10)

        boton_eliminar = Button(frame_botones, text="Eliminar Historial", command=self.eliminar_historial, bg="#dc3545", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_eliminar.pack(side=LEFT, padx=10)

        boton_exportar_todo = Button(frame_botones, text="Exportar Historias", command=self.exportar_historial, bg="#007bff", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_exportar_todo.pack(side=LEFT, padx=10)

        boton_volver = Button(frame_botones, text="Volver", command=self.master.crear_bienvenida, bg="#ffc107", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_volver.pack(side=LEFT, padx=10)

    def crear_historial(self):
        # Aquí deberías abrir una nueva ventana para crear un nuevo historial clínico
        pass

    def eliminar_historial(self):
        selected_item = self.tree_historial_clinico.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un historial para eliminar")
            return

        historia_id = self.tree_historial_clinico.item(selected_item)["values"][0]  # Suponiendo que la Cédula está en la primera columna
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro que desea eliminar este historial?")
        if respuesta:
            try:
                eliminar_historial(historia_id)
                messagebox.showinfo("Éxito", "Historial eliminado correctamente")
                self.mostrar()  # Actualiza la lista de historiales para reflejar la eliminación
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el historial: {str(e)}")

    def exportar_historial(self):
        try:
            exportar_historial_clinico_excel()
            messagebox.showinfo("Éxito", "Historial de historias clínicas exportado correctamente a Excel")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar las historias clínicas: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    root.title("Sistema de Agendamiento de Citas")
    root.geometry("1200x800")
    app = PantallaHistoriasClinicas(root)
    app.mostrar()
    root.mainloop()
