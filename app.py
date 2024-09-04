from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from controladores import *
from modulos.calendario import PantallaCalendario
from modulos.citas import PantallaCitas
from modulos.pacientes import PantallaPacientes
from modulos.historias_clinicas import PantallaHistoriasClinicas

# Configuración de usuario y contraseña
USERNAME = "usuario"
PASSWORD = "contrasena"

class Aplicacion(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Agendamiento de Citas")
        self.geometry("1200x800")
        self.configure(bg="#E0F7FA")

        self.frame_contenido = Frame(self, bg="#E0F7FA", padx=20, pady=20)
        self.frame_contenido.pack(side=LEFT, fill=BOTH, expand=1)

        self.crear_pantalla_login()

    def crear_pantalla_login(self):
        self.limpiar_contenido()

        frame_login = Frame(self.frame_contenido, bg="#FFFFFF", padx=20, pady=20, bd=5, relief=RIDGE)
        frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

        etiqueta_titulo = Label(frame_login, text="Bienvenido", font=("Arial", 24, "bold"), bg="#FFFFFF", fg="#007bff")
        etiqueta_titulo.pack(pady=10)

        etiqueta_login = Label(frame_login, text="Inicio de Sesión", font=("Arial", 20, "bold"), bg="#FFFFFF", fg="#333333")
        etiqueta_login.pack(pady=10)

        Label(frame_login, text="Usuario:", bg="#FFFFFF", fg="#333333", font=("Arial", 14)).pack(pady=5)
        self.usuario_entry = Entry(frame_login, font=("Arial", 14), bg="#F0F0F0", fg="#333333", relief=FLAT)
        self.usuario_entry.pack(pady=5, ipady=5, ipadx=5)

        Label(frame_login, text="Contraseña:", bg="#FFFFFF", fg="#333333", font=("Arial", 14)).pack(pady=5)
        self.contrasena_entry = Entry(frame_login, font=("Arial", 14), bg="#F0F0F0", fg="#333333", relief=FLAT, show="*")
        self.contrasena_entry.pack(pady=5, ipady=5, ipadx=5)

        boton_login = Button(frame_login, text="Iniciar Sesión", command=self.verificar_credenciales, bg="#007bff", fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5)
        boton_login.pack(pady=20)

    def verificar_credenciales(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if usuario == USERNAME and contrasena == PASSWORD:
            self.crear_bienvenida()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def crear_bienvenida(self):
        self.limpiar_contenido()

        frame_bienvenida = Frame(self.frame_contenido, bg="#E0F7FA", padx=20, pady=20)
        frame_bienvenida.pack(side=LEFT, fill=Y)

        etiqueta_bienvenida = Label(frame_bienvenida, text="Bienvenida", font=("Arial", 24, "bold"), bg="#E0F7FA", fg="#333333")
        etiqueta_bienvenida.pack(pady=20)

        botones = [
            ("Registrar Paciente", self.crear_pantalla_registrar_paciente, "#007bff"),
            ("Agendar Cita", self.crear_pantalla_agendar_cita, "#28a745"),
            ("Calendario", self.crear_pantalla_calendario, "#17a2b8"),
            ("Registro de Pacientes", self.crear_pantalla_ver_pacientes, "#6c757d"),
            ("Historias Clínicas", self.crear_pantalla_historias_clinicas, "#ff5722"),
            ("Salir", self.quit, "#dc3545")
        ]

        for texto, comando, color in botones:
            Button(frame_bienvenida, text=texto, command=comando, bg=color, fg="white", font=("Arial", 16, "bold"), relief=RAISED, bd=5, width=20).pack(pady=10, ipadx=20, ipady=10)

        self.mostrar_proximas_citas()

    def mostrar_proximas_citas(self):
        frame_proximas_citas = Frame(self.frame_contenido, bg="#FFFFFF")
        frame_proximas_citas.pack(fill=BOTH, expand=1)

        etiqueta = Label(frame_proximas_citas, text="Próximas Citas", font=("Arial", 20, "bold"), bg="#FFFFFF", fg="#333333")
        etiqueta.pack(pady=20)

        tree_frame = Frame(frame_proximas_citas, bg="#FFFFFF")
        tree_frame.pack(fill=BOTH, expand=1)

        tree_scroll_vertical = Scrollbar(tree_frame, orient="vertical")
        tree_scroll_vertical.pack(side=RIGHT, fill=Y)

        tree_scroll_horizontal = Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_horizontal.pack(side=BOTTOM, fill=X)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 12))
        style.configure("mystyle.Treeview.Heading", font=('Arial', 14, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tree_proximas_citas = ttk.Treeview(tree_frame, columns=("Paciente", "Fecha", "Hora"), show='headings', style="mystyle.Treeview",
                                                yscrollcommand=tree_scroll_vertical.set, xscrollcommand=tree_scroll_horizontal.set)
        self.tree_proximas_citas.heading("Paciente", text="Paciente")
        self.tree_proximas_citas.heading("Fecha", text="Fecha")
        self.tree_proximas_citas.heading("Hora", text="Hora")
        self.tree_proximas_citas.tag_configure('oddrow', background='#B2EBF2')
        self.tree_proximas_citas.tag_configure('evenrow', background='#E0F7FA')
        self.tree_proximas_citas.pack(fill=BOTH, expand=1)

        tree_scroll_vertical.config(command=self.tree_proximas_citas.yview)
        tree_scroll_horizontal.config(command=self.tree_proximas_citas.xview)

        citas = obtener_proximas_citas()
        citas_ordenadas = sorted(citas, key=lambda x: (x[2], x[3]))  # Ordenar por fecha y hora
        next_appointment_id = None

        for i, cita in enumerate(citas_ordenadas):
            paciente = obtener_paciente_por_id(cita[1])
            if paciente:
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                item_id = self.tree_proximas_citas.insert("", "end", values=(f"{paciente[1]} {paciente[2]}", cita[2], cita[3]), tags=(tag,))
                if next_appointment_id is None:
                    next_appointment_id = item_id

        if next_appointment_id:
            self.tree_proximas_citas.selection_set(next_appointment_id)
            self.tree_proximas_citas.see(next_appointment_id)

    def crear_pantalla_registrar_paciente(self):
        PantallaPacientes(self).mostrar()

    def crear_pantalla_agendar_cita(self):
        PantallaCitas(self).mostrar()

    def crear_pantalla_calendario(self):
        PantallaCalendario(self).mostrar()

    def crear_pantalla_ver_pacientes(self):
        PantallaPacientes(self).mostrar_registro()

    def crear_pantalla_historias_clinicas(self):
        PantallaHistoriasClinicas(self).mostrar()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
