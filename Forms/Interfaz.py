import tkinter as tk
from tkinter import ttk, messagebox
from Persistence.Consultas import ConsultasDB, FuncionesJuntas
from Persistence.SentenciasRut import SentenciasRUT

class EstiloTkinter:
    def __init__(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure(
            'Custom.TEntry',
            borderwidth=2,
            relief='flat',
            font=('Onix', 11),
            padding=(5, 5)
        )

        self.style.theme_use("clam")

        self.style.configure("Custom.TButton",
                        foreground="white",
                        background="black",
                        font=("Onix", 11),
                        relief="raised")

class InterfazConsultaRut:
    def __init__(self, root, estilo):
        self.root = root
        self.root.title("Consulta Rut")
        self.window_width = 550
        self.window_height = 450
        self.resultados_combinados = None
        

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_position = (screen_width - self.window_width) // 2
        y_position = (screen_height - self.window_height) // 2

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)

        self.estilo = estilo
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="Consulta RUT sin DV", font=("Onix", 14))
        label.pack()

        validate_cmd = self.root.register(self.validar_input)
        self.entry_identificacion = ttk.Entry(self.root, width=23, style='Custom.TEntry', foreground='gray', validate="key", validatecommand=(validate_cmd, '%P'))
        self.entry_identificacion.insert(0, "Ingrese ID sin DV")
        self.entry_identificacion.bind('<FocusIn>', self.on_entry_click)
        self.entry_identificacion.bind('<FocusOut>', self.on_focus_out)
        self.entry_identificacion.pack()

        self.estilo.style.theme_use("clam")

        self.boton_ver_consultas = ttk.Button(self.root, text="Ver Consultas del ID", style="Custom.TButton", command=self.ver_consultas_identificacion_db, width=20)
        self.boton_ver_consultas.pack(padx=10, pady=15)

        self.boton_ver_info_proveedor = ttk.Button(self.root, text="Ver Info de Proveedor", style="Custom.TButton", command=self.ver_info_proveedor, width=20)
        self.boton_ver_info_proveedor.pack(padx=10, pady=15)

        self.boton_mostrar_tabla = ttk.Button(self.root, text="Mostrar Tabla consultas", style="Custom.TButton", command=self.mostrar_tabla_completa, width=20)
        self.boton_mostrar_tabla.pack(padx=10, pady=15)

        self.boton_consultar_rut_headless = ttk.Button(self.root, text="Consultar RUES y RUT", style="Custom.TButton", command=self.funciones_juntas, width=20)
        self.boton_consultar_rut_headless.pack(padx=10, pady=15)
        
    
    def mostrar_resultados(self, resultados, title):
        consultas_db = SentenciasRUT()
        consultas_db.mostrar_resultados(resultados, title)

    def on_entry_click(self, event):
        if self.entry_identificacion.get() == "Ingrese ID sin DV":
            self.entry_identificacion.delete(0, tk.END)
            self.entry_identificacion.config(fg='black')

    def on_focus_out(self, event):
        if self.entry_identificacion.get() == "":
            self.entry_identificacion.insert(0, "Ingrese ID sin DV")
            self.entry_identificacion.config(fg='gray')

    def validar_input(self, new_value):
        return new_value.isdigit() or new_value == ""

    def ver_consultas_identificacion_db(self):
        identificacion_limpia = self.entry_identificacion.get()
        consultas_db = ConsultasDB()
        resultados = consultas_db.ver_consultas_identificacion_db(identificacion_limpia)

        # Verifica si resultados es None o vacío
        if resultados is None or not resultados:
            messagebox.showinfo("Información", f"No hay consultas registradas para el ID {identificacion_limpia}")
        else:
            self.mostrar_resultados(resultados, "Resultados de Consulta")


    def funciones_juntas(self):
        identificacion_limpia = self.entry_identificacion.get()
        funciones_juntas = FuncionesJuntas()
        funciones_juntas.funciones_juntas(identificacion_limpia)

    def mostrar_tabla_completa(self):
        consultas_db = SentenciasRUT()
        resultados_completos = consultas_db.obtener_todos_los_resultados_rut()
        self.mostrar_resultados(resultados_completos, "Consultas")


    def ver_info_proveedor(self):
        identificacion_limpia = self.entry_identificacion.get()

        try:
            # Crear una instancia de la clase SentenciasRUT
            sentencias_rut = SentenciasRUT()

            # Llamada a la función para obtener la información del proveedor
            resultados_combinados = sentencias_rut.obtener_info_proveedor(identificacion_limpia)

            # Mostrar la información en una nueva ventana
            if resultados_combinados and ('proveedorrut' in resultados_combinados or 'proveedorrues' in resultados_combinados):
                self.mostrar_resultados_en_textbox(resultados_combinados)
            else:
                messagebox.showinfo("No hay resultados", "No se encontró proveedor para esta identificación.")

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

    def mostrar_resultados_en_textbox(self, resultados_combinados):
        ventana_resultados = tk.Toplevel()
        ventana_resultados.title("Información del Proveedor")

        text_widget = tk.Text(ventana_resultados, wrap="none", height=20, width=80)
        text_widget.pack(expand=True, fill="both")

        mensaje = "Información del Proveedor:\n\n"
        

        if 'proveedorrut' in resultados_combinados and resultados_combinados['proveedorrut']:
            mensaje += "ProveedorRUT:\n"
            for resultado in resultados_combinados['proveedorrut']:
                mensaje += f"ID: {resultado[0]}\nNombre: {resultado[1]}\nDv: {resultado[2]}\nEstado: {resultado[3]}\n\n"

        if 'proveedorrues' in resultados_combinados and resultados_combinados['proveedorrues']:
            mensaje += "ProveedorRUES:\n"
            for resultado in resultados_combinados['proveedorrues']:
                mensaje += f"NIT: {resultado[0]}\nNombre: {resultado[1]}\n"
                mensaje += f"Estado: {resultado[4]}\nCamaraComercio: {resultado[5]}\nMatricula: {resultado[6]}\n"
                mensaje += f"OrganizacionJuridica: {resultado[7]}:\n"
                mensaje += f"Categoria: {resultado[8]}\nActividadesEconomicas: {resultado[9]}\n\n"

        text_widget.insert("1.0", mensaje)

        # Agrega la funcionalidad de copiar al portapapeles
        text_widget.bind("<Control-a>", lambda e: text_widget.tag_add(tk.SEL, "5.0", tk.END))
        text_widget.tag_configure(tk.SEL, background="light gray")

        # Agrega un botón para cerrar la ventana
        boton_cerrar = tk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy)
        boton_cerrar.pack()

        ventana_resultados.mainloop()