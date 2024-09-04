from tkinter import *
from tkinter import ttk, messagebox
from controladores import agregar_paciente, obtener_pacientes, eliminar_paciente, exportar_historial_pacientes_excel
from datetime import datetime
import os

class PantallaPacientes:
    def __init__(self, master):
        self.master = master

    def mostrar(self):
        self.master.limpiar_contenido()

        frame_registro_paciente = Frame(self.master.frame_contenido, bg="#e0f7fa", padx=20, pady=20)
        frame_registro_paciente.pack(fill=BOTH, expand=1)

        etiqueta = Label(frame_registro_paciente, text="Registrar Paciente", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#007bff")
        etiqueta.pack(pady=20)

        etiquetas_campos = [
            ("Nombre:", 'nombre_entry'),
            ("Apellido:", 'apellido_entry'),
            ("Cédula:", 'cedula_entry'),
            ("Email:", 'email_entry'),
            ("Teléfono:", 'telefono_entry')
        ]

        for texto, var in etiquetas_campos:
            frame = Frame(frame_registro_paciente, bg="#e0f7fa")
            frame.pack(fill=X, pady=5)
            label = Label(frame, text=texto, bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=15, anchor="w")
            label.pack(side=LEFT)
            entry = Entry(frame, font=("Arial", 14), bg="#ffffff", fg="#333333")
            setattr(self, var, entry)
            entry.pack(side=LEFT, fill=X, expand=YES, padx=5)

        frame_otro_datos = Frame(frame_registro_paciente, bg="#e0f7fa")
        frame_otro_datos.pack(pady=10, fill=X)

        Label(frame_otro_datos, text="Edad:", bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=10, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.edad_entry = Entry(frame_otro_datos, font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.edad_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(frame_otro_datos, text="Sexo:", bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=10, anchor="w").grid(row=0, column=2, padx=5, pady=5)
        self.sexo_entry = Entry(frame_otro_datos, font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.sexo_entry.grid(row=0, column=3, padx=5, pady=5)

        Label(frame_otro_datos, text="Estado Civil:", bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=15, anchor="w").grid(row=0, column=4, padx=5, pady=5)
        self.estado_civil_entry = Entry(frame_otro_datos, font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.estado_civil_entry.grid(row=0, column=5, padx=5, pady=5)

        frame_ocupacion = Frame(frame_registro_paciente, bg="#e0f7fa")
        frame_ocupacion.pack(pady=10, fill=X)

        Label(frame_ocupacion, text="Ocupación:", bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=15, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.ocupacion_entry = Entry(frame_ocupacion, font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.ocupacion_entry.grid(row=0, column=1, padx=5, pady=5)

        frame_residencia = Frame(frame_registro_paciente, bg="#e0f7fa")
        frame_residencia.pack(pady=10, fill=X)

        Label(frame_residencia, text="Residencia Actual:", bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=15, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.residencia_actual_entry = Entry(frame_residencia, font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.residencia_actual_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(frame_residencia, text="Residencia Anterior:", bg="#e0f7fa", fg="#333333", font=("Arial", 14), width=15, anchor="w").grid(row=0, column=2, padx=5, pady=5)
        self.residencia_anterior_entry = Entry(frame_residencia, font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.residencia_anterior_entry.grid(row=0, column=3, padx=5, pady=5)

        frame_botones = Frame(frame_registro_paciente, bg="#e0f7fa")
        frame_botones.pack(pady=20)

        boton_guardar = Button(frame_botones, text="Guardar Paciente", command=self.guardar_paciente, bg="#28a745", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5)
        boton_guardar.pack(side=LEFT, padx=10)

        boton_volver = Button(frame_botones, text="Volver", command=self.master.crear_bienvenida, bg="#ffc107", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5)
        boton_volver.pack(side=LEFT, padx=10)

    def guardar_paciente(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        cedula = self.cedula_entry.get()
        email = self.email_entry.get()
        telefono = self.telefono_entry.get()
        edad = self.edad_entry.get()
        sexo = self.sexo_entry.get()
        estado_civil = self.estado_civil_entry.get()
        ocupacion = self.ocupacion_entry.get()
        residencia_actual = self.residencia_actual_entry.get()
        residencia_anterior = self.residencia_anterior_entry.get()

        if nombre and apellido and cedula and email:
            try:
                agregar_paciente(nombre, apellido, email, telefono, cedula, edad, sexo, estado_civil, ocupacion, residencia_actual, residencia_anterior)
                messagebox.showinfo("Éxito", "Paciente registrado correctamente")
                self.master.crear_bienvenida()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el paciente: {e}")
        else:
            messagebox.showerror("Error", "Los campos de Nombre, Apellido, Cédula y Email son obligatorios.")

    def mostrar_registro(self):
        self.master.limpiar_contenido()

        frame_registro_pacientes = Frame(self.master.frame_contenido, bg="#e0f7fa", padx=20, pady=20)
        frame_registro_pacientes.pack(fill=BOTH, expand=1)

        etiqueta = Label(frame_registro_pacientes, text="Registro de Pacientes", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#007bff")
        etiqueta.pack(pady=20)

        tree_frame = Frame(frame_registro_pacientes, bg="#e0f7fa")
        tree_frame.pack(fill=BOTH, expand=1, pady=10)

        tree_scroll_vertical = Scrollbar(tree_frame, orient="vertical")
        tree_scroll_vertical.pack(side=RIGHT, fill=Y)

        tree_scroll_horizontal = Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_horizontal.pack(side=BOTTOM, fill=X)

        self.tree_pacientes = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Apellido", "Email", "Teléfono", "Cédula", "Edad"), show='headings',
                                           yscrollcommand=tree_scroll_vertical.set, xscrollcommand=tree_scroll_horizontal.set)
        self.tree_pacientes.heading("ID", text="ID")
        self.tree_pacientes.heading("Nombre", text="Nombre")
        self.tree_pacientes.heading("Apellido", text="Apellido")
        self.tree_pacientes.heading("Email", text="Email")
        self.tree_pacientes.heading("Teléfono", text="Teléfono")
        self.tree_pacientes.heading("Cédula", text="Cédula")
        self.tree_pacientes.heading("Edad", text="Edad")
        self.tree_pacientes.tag_configure('oddrow', background='#d1ecf1')
        self.tree_pacientes.tag_configure('evenrow', background='#ffffff')
        self.tree_pacientes.pack(side=LEFT, fill=BOTH, expand=1)

        tree_scroll_vertical.config(command=self.tree_pacientes.yview)
        tree_scroll_horizontal.config(command=self.tree_pacientes.xview)

        pacientes = obtener_pacientes()
        for i, paciente in enumerate(pacientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree_pacientes.insert("", "end", values=paciente, tags=(tag,))

        frame_botones = Frame(frame_registro_pacientes, bg="#e0f7fa")
        frame_botones.pack(pady=20, fill=X)

        boton_eliminar = Button(frame_botones, text="Eliminar Paciente", command=self.confirmar_eliminacion_paciente, bg="#dc3545", fg="white", font=("Arial", 14, "bold"), relief=RAISED, bd=5)
        boton_eliminar.pack(side=LEFT, padx=10)

        boton_exportar = Button(frame_botones, text="Exportar Historial", command=self.exportar_historial_pacientes, bg="#007bff", fg="white", font=("Arial", 14, "bold"), relief=RAISED, bd=5)
        boton_exportar.pack(side=LEFT, padx=10)

        boton_volver = Button(frame_botones, text="Volver", command=self.master.crear_bienvenida, bg="#ffc107", fg="white", font=("Arial", 14, "bold"), relief=RAISED, bd=5)
        boton_volver.pack(side=LEFT, padx=10)

    def confirmar_eliminacion_paciente(self):
        seleccionado = self.tree_pacientes.focus()
        valores = self.tree_pacientes.item(seleccionado, 'values')
        if valores:
            respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro que desea eliminar este paciente?")
            if respuesta:
                self.eliminar_paciente(valores[0])
        else:
            messagebox.showerror("Error", "Seleccione un paciente para eliminar")

    def eliminar_paciente(self, paciente_id):
        try:
            eliminar_paciente(paciente_id)
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
            self.mostrar_registro()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el paciente: {e}")

    def exportar_historial_pacientes(self):
        try:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"exportaciones/historial_pacientes_{timestamp}.xlsx"

            if not os.path.exists('exportaciones'):
                os.makedirs('exportaciones')

            exportar_historial_pacientes_excel(filename)
            messagebox.showinfo("Éxito", f"Historial de pacientes exportado correctamente a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar el historial de pacientes: {str(e)}")
