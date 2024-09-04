from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from controladores import obtener_citas_dia, exportar_historial_citas_excel, eliminar_cita, obtener_nombre_paciente
import os
class PantallaCalendario:
    def __init__(self, master):
        self.master = master
        self.frame_calendario = None

    def mostrar(self):
        self.limpiar_contenido()

        self.frame_calendario = Frame(self.master.frame_contenido, bg="#e0f7fa", padx=20, pady=20)
        self.frame_calendario.pack(fill=BOTH, expand=1)

        etiqueta = Label(self.frame_calendario, text="Calendario de Citas", font=("Arial", 24, "bold"), bg="#00acc1", fg="#ffffff")
        etiqueta.pack(pady=10)

        self.calendario = Calendar(self.frame_calendario, selectmode='day', date_pattern='yyyy-mm-dd', font=("Arial", 14),
                                   background="#00acc1", foreground='white', bordercolor='gray', headersbackground='#00acc1',
                                   normalbackground='white', normalforeground='black', weekendbackground='lightgray', weekendforeground='black',
                                   othermonthbackground='white', othermonthforeground='gray', othermonthwebackground='lightgray', othermonthweforeground='gray')
        self.calendario.pack(pady=20, fill=BOTH, expand=1)

        botones_frame = Frame(self.frame_calendario, bg="#e0f7fa")
        botones_frame.pack(fill=X, pady=10)

        boton_ver_citas = Button(botones_frame, text="Ver Citas", command=self.mostrar_citas, bg="#00acc1", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=15)
        boton_ver_citas.pack(side=LEFT, padx=10, pady=10)

        boton_exportar = Button(botones_frame, text="Exportar Citas a Excel", command=self.exportar_citas, bg="#00acc1", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_exportar.pack(side=LEFT, padx=10, pady=10)

        boton_eliminar = Button(botones_frame, text="Eliminar Cita", command=self.confirmar_eliminacion_cita, bg="#dc3545", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=15)
        boton_eliminar.pack(side=LEFT, padx=10, pady=10)

        boton_volver = Button(botones_frame, text="Volver", command=self.master.crear_bienvenida, bg="#ffc107", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=15)
        boton_volver.pack(side=RIGHT, padx=10, pady=10)

        self.citas_frame = Frame(self.frame_calendario, bg="#e0f7fa")
        self.citas_frame.pack(fill=BOTH, expand=1)

    def mostrar_citas(self):
        fecha = self.calendario.get_date()
        citas = obtener_citas_dia(fecha)

        for widget in self.citas_frame.winfo_children():
            widget.destroy()

        if citas:
            tree_frame = Frame(self.citas_frame, bg="#e0f7fa")
            tree_frame.pack(fill=BOTH, expand=1, pady=10)

            tree_scroll_vertical = Scrollbar(tree_frame, orient="vertical")
            tree_scroll_vertical.pack(side=RIGHT, fill=Y)

            tree_scroll_horizontal = Scrollbar(tree_frame, orient="horizontal")
            tree_scroll_horizontal.pack(side=BOTTOM, fill=X)

            self.tree = ttk.Treeview(tree_frame, columns=("Nombre", "Fecha", "Hora", "Descripción"), show='headings', height=8,
                                     yscrollcommand=tree_scroll_vertical.set, xscrollcommand=tree_scroll_horizontal.set)
            self.tree.heading("Nombre", text="Nombre")
            self.tree.heading("Fecha", text="Fecha")
            self.tree.heading("Hora", text="Hora")
            self.tree.heading("Descripción", text="Descripción")
            self.tree.pack(side=LEFT, fill=BOTH, expand=1)

            tree_scroll_vertical.config(command=self.tree.yview)
            tree_scroll_horizontal.config(command=self.tree.xview)

            for cita in citas:
                nombre_paciente = obtener_nombre_paciente(cita[1])  # Obtener el nombre del paciente usando el paciente_id
                self.tree.insert("", "end", values=(nombre_paciente, cita[2], cita[3], cita[4]))

            self.tree.pack(side=LEFT, fill=BOTH, expand=1)

            # Ajustar el ancho de la columna "Descripción" según el contenido
            self.ajustar_ancho_columna_descripcion()
        else:
            etiqueta = Label(self.citas_frame, text="No hay citas para esta fecha.", font=("Arial", 14), bg="#e0f7fa", fg="#333333")
            etiqueta.pack(pady=20)

    def ajustar_ancho_columna_descripcion(self):
        max_len = 0
        for item in self.tree.get_children():
            descripcion = self.tree.item(item, 'values')[3]  # Obtener el valor de la columna "Descripción"
            max_len = max(max_len, len(descripcion))

        # Ajustar el ancho de la columna según el contenido
        new_width = max_len * 10  # Ajustar el multiplicador según sea necesario
        self.tree.column("Descripción", width=new_width)

    def confirmar_eliminacion_cita(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una cita para eliminar")
            return

        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro que desea eliminar esta cita?")
        if respuesta:
            self.eliminar_cita()

    def eliminar_cita(self):
        selected_item = self.tree.selection()
        cita_fecha = self.tree.item(selected_item)["values"][1]  # Suponiendo que la fecha de la cita está en la segunda columna
        cita_hora = self.tree.item(selected_item)["values"][2]   # Suponiendo que la hora de la cita está en la tercera columna
        try:
            eliminar_cita(cita_fecha, cita_hora)
            messagebox.showinfo("Éxito", "Cita eliminada correctamente")
            self.mostrar_citas()  # Actualiza la lista de citas para reflejar la eliminación
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la cita: {str(e)}")

    def exportar_citas(self):
        try:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"exportaciones/historial_citas_{timestamp}.xlsx"
            if not os.path.exists('exportaciones'):
                os.makedirs('exportaciones')
            exportar_historial_citas_excel(filename)
            messagebox.showinfo("Éxito", f"Historial de citas exportado correctamente a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar las citas: {str(e)}")

    def limpiar_contenido(self):
        for widget in self.master.frame_contenido.winfo_children():
            widget.destroy()

# Aplicacion principal para ejecutar
class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.frame_contenido = Frame(master, bg="#e0f7fa")
        self.frame_contenido.pack(fill=BOTH, expand=1)

        self.crear_bienvenida()

    def crear_bienvenida(self):
        self.limpiar_contenido()
        frame_bienvenida = Frame(self.frame_contenido, bg="#e0f7fa", padx=20, pady=20)
        frame_bienvenida.pack(fill=BOTH, expand=1)

        etiqueta = Label(frame_bienvenida, text="Bienvenida", font=("Arial", 24, "bold"), bg="#00acc1", fg="#ffffff")
        etiqueta.pack(pady=20)

        boton_calendario = Button(frame_bienvenida, text="Calendario", command=self.mostrar_calendario, bg="#00acc1", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20)
        boton_calendario.pack(pady=10)

    def mostrar_calendario(self):
        PantallaCalendario(self).mostrar()

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Sistema de Agendamiento de Citas")
    root.geometry("1024x768")
    app = Aplicacion(root)
    root.mainloop()
