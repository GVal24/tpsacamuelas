import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from models.paciente import Paciente
from models.tratamiento import Tratamiento
from models.turno import Turno

class FormularioOdontologico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultorio Odontológico - Panel de Control")
        self.geometry("750x520")

        # Notebook con pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.pestana_pacientes = ttk.Frame(self.notebook)
        self.pestana_turnos = ttk.Frame(self.notebook)
        self.pestana_tratamientos = ttk.Frame(self.notebook)

        self.notebook.add(self.pestana_pacientes, text="Pacientes")
        self.notebook.add(self.pestana_turnos, text="Turnos")
        self.notebook.add(self.pestana_tratamientos, text="Tratamientos")

        # Construcción de interfaces
        self._inicializar_modulo_pacientes()
        self._inicializar_modulo_turnos()
        self._inicializar_modulo_tratamientos()

    # --- PACIENTES ---
    def _inicializar_modulo_pacientes(self):
        frame = self.pestana_pacientes
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="DNI:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txtDni = ttk.Entry(frame, justify="center")
        self.txtDni.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(frame, text="Buscar", command=self.buscarPaciente).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.txtNombre = ttk.Entry(frame, justify="center")
        self.txtNombre.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(frame, text="Apellido:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.txtApellido = ttk.Entry(frame, justify="center")
        self.txtApellido.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(frame, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.txtTelefono = ttk.Entry(frame, justify="center")
        self.txtTelefono.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        f_botones = ttk.Frame(frame)
        f_botones.grid(row=4, column=0, columnspan=3, pady=20)
        ttk.Button(f_botones, text="Guardar", command=self.registrarPaciente).pack(side="left", padx=5)
        ttk.Button(f_botones, text="Modificar", command=self.modificarPaciente).pack(side="left", padx=5)
        ttk.Button(f_botones, text="Eliminar", command=self.eliminarPaciente).pack(side="left", padx=5)

    def registrarPaciente(self):
        p = Paciente(self.txtDni.get(), self.txtNombre.get(), self.txtApellido.get(), self.txtTelefono.get())
        if p.guardar():
            messagebox.showinfo("Éxito", "Paciente registrado exitosamente.")
            self._limpiar_formulario_paciente()
        else:
            messagebox.showerror("Error", "No se pudo registrar (DNI duplicado o datos incorrectos).")

    def modificarPaciente(self):
        p = Paciente(self.txtDni.get(), self.txtNombre.get(), self.txtApellido.get(), self.txtTelefono.get())
        if p.modificar():
            messagebox.showinfo("Éxito", "Ficha modificada con éxito.")
        else:
            messagebox.showerror("Error", "Error al intentar actualizar la información.")

    def eliminarPaciente(self):
        p = Paciente(self.txtDni.get(), "", "", "")
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta ficha de paciente?"):
            if p.eliminar():
                messagebox.showinfo("Éxito", "Eliminado correctamente.")
                self._limpiar_formulario_paciente()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro.")

    def buscarPaciente(self):
        p = Paciente.buscarPorDni(self.txtDni.get())
        if p:
            self.txtNombre.delete(0, tk.END); self.txtNombre.insert(0, p.nombre)
            self.txtApellido.delete(0, tk.END); self.txtApellido.insert(0, p.apellido)
            self.txtTelefono.delete(0, tk.END); self.txtTelefono.insert(0, p.telefono)
        else:
            messagebox.showwarning("Atención", "No se encontró ningún paciente asociado a ese DNI.")

    def _limpiar_formulario_paciente(self):
        self.txtDni.delete(0, tk.END)
        self.txtNombre.delete(0, tk.END)
        self.txtApellido.delete(0, tk.END)
        self.txtTelefono.delete(0, tk.END)

    # --- TURNOS ---
    def _inicializar_modulo_turnos(self):
        frame = self.pestana_turnos
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Fecha:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.calendario = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Hora (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txtHora = ttk.Entry(frame, justify="center")
        self.txtHora.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="DNI Paciente:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txtTurnoDni = ttk.Entry(frame, justify="center")
        self.txtTurnoDni.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Tratamiento:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.cboTratamientos = ttk.Combobox(frame, state="readonly", justify="center")
        self.cboTratamientos.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Agendar Turno", command=self.agendarTurno).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Consultar Agenda", command=self.consultarAgendaDiaria).grid(row=0, column=2, padx=10)

        self.tabla_turnos = ttk.Treeview(frame, columns=("ID", "Hora", "Paciente", "Tratamiento"), show="headings", height=7)
        self.tabla_turnos.heading("ID", text="ID")
        self.tabla_turnos.heading("Hora", text="Hora")
        self.tabla_turnos.heading("Paciente", text="Paciente")
        self.tabla_turnos.heading("Tratamiento", text="Tratamiento")
        self.tabla_turnos.column("ID", width=50, anchor="center")
        self.tabla_turnos.column("Hora", anchor="center")
        self.tabla_turnos.column("Paciente", anchor="center")
        self.tabla_turnos.column("Tratamiento", anchor="center")
        self.tabla_turnos.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ttk.Button(frame, text="Cancelar Turno Seleccionado", command=self.cancelarTurno).grid(row=6, column=0, columnspan=3, pady=5)

        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._cargar_desplegable_tratamientos())

    def _cargar_desplegable_tratamientos(self):
        self.lista_cache_tratamientos = Tratamiento.obtenerTodos()
        self.cboTratamientos['values'] = [t.nombre for t in self.lista_cache_tratamientos]

    def agendarTurno(self):
        # 1. Buscamos el paciente usando el DNI
        paciente = Paciente.buscarPorDni(self.txtTurnoDni.get())
        
        # 2. Obtenemos la posición elegida en el combobox de tratamientos
        seleccion = self.cboTratamientos.current()

        # Validaciones de seguridad
        if not paciente:
            messagebox.showerror("Error", "Primero debe dar de alta al paciente con ese DNI.")
            return
        if seleccion == -1:
            messagebox.showerror("Error", "Debe seleccionar un tratamiento de la lista.")
            return

        # 3. Traemos el objeto del tratamiento de la lista que guardaste en caché
        tratamiento_seleccionado = self.lista_cache_tratamientos[seleccion]
        
        # --- CORRECCIÓN CLAVE AQUÍ ---
        # Le pedimos la fecha directamente a tu objeto 'calendario' usando get_date()
        fecha_turno = self.calendario.get_date() 
        hora_turno = self.txtHora.get()
        
        # 4. Instanciamos la clase Turno respetando tu diagrama
        t = Turno(fecha_turno, hora_turno, paciente.id, tratamiento_seleccionado.id)
        
        # 5. Guardamos en SQLite y refrescamos la grilla
        if t.agendar():
            messagebox.showinfo("Éxito", "Turno cargado correctamente.")
            self.consultarAgendaDiaria()  # Llama a tu función para recargar la tabla
        else:
            messagebox.showerror("Error", "No se pudo agendar el turno en la base de datos.")


    def consultarAgendaDiaria(self):
        for elemento in self.tabla_turnos.get_children():
            self.tabla_turnos.delete(elemento)

        turnos = Turno.obtenerAgendaDiaria(self.calendario.get_date())
        if not turnos:
            messagebox.showinfo("Agenda", f"No hay turnos reservados para {self.calendario.get_date()}")
            return

        for fila in turnos:
            # SELECT devuelve: (id, fecha, hora, nombre_paciente, nombre_tratamiento)
            self.tabla_turnos.insert("", "end", values=(fila[0], fila[2], fila[3], fila[4]))

    def cancelarTurno(self):
        seleccion = self.tabla_turnos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un turno de la grilla.")
            return

        valores = self.tabla_turnos.item(seleccion[0], "values")
        id_turno = valores[0]

        t = Turno("", "", 0, 0, id=id_turno)
        if t.cancelar():
            messagebox.showinfo("Éxito", "Turno cancelado de manera correcta.")
            self.consultarAgendaDiaria()
        else:
            messagebox.showerror("Error", "No se pudo procesar la cancelación.")

    # --- TRATAMIENTOS ---
    def _inicializar_modulo_tratamientos(self):
        frame = self.pestana_tratamientos
        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

        ttk.Label(frame, text="Nombre del Tratamiento:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txtTratNombre = ttk.Entry(frame, justify="center")
        self.txtTratNombre.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(frame, text="Precio ($):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.txtTratPrecio = ttk.Entry(frame, justify="center")
        self.txtTratPrecio.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Button(frame, text="Agregar Tratamiento", command=self.gestionarTratamientos).grid(row=2, column=0, columnspan=2, pady=10)

    def gestionarTratamientos(self):
        """Alta de nuevos tratamientos validando el tipo de dato."""
        try:
            nombre = self.txtTratNombre.get()
            precio = float(self.txtTratPrecio.get())
            t = Tratamiento(nombre, precio)
            if t.insertar():
                messagebox.showinfo("Éxito", "Tratamiento registrado.")
                self.txtTratNombre.delete(0, tk.END)
                self.txtTratPrecio.delete(0, tk.END)
                self._cargar_desplegable_tratamientos()
            else:
                messagebox.showerror("Error", "No se pudo guardar el tratamiento.")
        except ValueError:
            messagebox.showerror("Error", "El precio ingresado debe ser un número válido.")
