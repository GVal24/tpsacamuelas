import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from models.paciente import Paciente
from models.tratamiento import Tratamiento
from models.turno import Turno
from database.consultorio import Consultorio
db = Consultorio()


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

        # --- Tabla de pacientes ---
        self.tabla_pacientes = ttk.Treeview(
            frame, 
            columns=("ID", "DNI", "Nombre", "Apellido", "Teléfono"), 
            show="headings", 
            height=7)
        
        for col in ("ID", "DNI", "Nombre", "Apellido", "Teléfono"):
            self.tabla_pacientes.heading(col, text=col)
            self.tabla_pacientes.column(col, anchor="center", width=100)
        self.tabla_pacientes.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ttk.Button(frame, text="Ver todos los pacientes", command=self.mostrarPacientes).grid(row=6, column=0, columnspan=3, pady=5)
       
        self.tabla_pacientes.bind("<<TreeviewSelect>>", self.seleccionarPaciente)

    def seleccionarPaciente(self, event):
        seleccion = self.tabla_pacientes.selection()
        if not seleccion:
            return
        valores = self.tabla_pacientes.item(seleccion[0], "values")

        # Copiar datos al formulario
        self.txtDni.delete(0, tk.END)
        self.txtDni.insert(0, valores[1])

        self.txtNombre.delete(0, tk.END)
        self.txtNombre.insert(0, valores[2])

        self.txtApellido.delete(0, tk.END)
        self.txtApellido.insert(0, valores[3])

        self.txtTelefono.delete(0, tk.END)
        self.txtTelefono.insert(0, valores[4])

        # Guardar ID del paciente seleccionado
        self.paciente_seleccionado_id = valores[0]

    def registrarPaciente(self):
        p = Paciente(self.txtDni.get(), self.txtNombre.get(), self.txtApellido.get(), self.txtTelefono.get())
        if p.guardar():
            messagebox.showinfo("Éxito", "Paciente registrado exitosamente.")
            self._limpiar_formulario_paciente()
        else:
            messagebox.showerror("Error", "No se pudo registrar (DNI duplicado o datos incorrectos).")

    def modificarPaciente(self):
        if not hasattr(self, "paciente_seleccionado_id"):
            messagebox.showwarning("Atención", "Seleccione un paciente primero.")
            return
        p = Paciente(self.txtDni.get(), self.txtNombre.get(), self.txtApellido.get(), self.txtTelefono.get(), id=self.paciente_seleccionado_id)
        if p.modificar():
            messagebox.showinfo("Éxito", "Ficha modificada con éxito.")
            self.mostrarPacientes()
            self._limpiar_formulario_paciente()
        else:
            messagebox.showerror("Error", "Error al intentar actualizar la información.")

    def eliminarPaciente(self):
        p = Paciente(self.txtDni.get(), "", "", "")
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta ficha de paciente?"):
            if p.eliminar():
                messagebox.showinfo("Éxito", "Eliminado correctamente.")
                self._limpiar_formulario_paciente()
                self.mostrarPacientes()
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
    
    def mostrarPacientes(self):
        for elemento in self.tabla_pacientes.get_children():
            self.tabla_pacientes.delete(elemento)

        pacientes = Paciente.obtenerTodos()
        if not pacientes:
            messagebox.showinfo("Pacientes", "No hay pacientes registrados.")
            return

        for fila in pacientes:
            self.tabla_pacientes.insert("", "end", values=fila)

        # --- TURNOS ---
    def _inicializar_modulo_turnos(self):
        frame = self.pestana_turnos
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Fecha:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.calendario = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.calendario.bind("<<CalendarSelected>>", lambda event: self.consultarAgendaDiaria())
        
        ttk.Label(frame, text="Hora (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txtHora = ttk.Entry(frame, justify="center")
        self.txtHora.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="DNI Paciente:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txtTurnoDni = ttk.Entry(frame, justify="center")
        self.txtTurnoDni.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Tratamiento:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.cboTratamientos = ttk.Combobox(frame, state="readonly", justify="center")
        self.cboTratamientos.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # --- Botones CRUD ---
        f_botones = ttk.Frame(frame)
        f_botones.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(f_botones, text="Agendar", command=self.agendarTurno).pack(side="left", padx=5)
        ttk.Button(f_botones, text="Modificar", command=self.modificarTurno).pack(side="left", padx=5)
        ttk.Button(f_botones, text="Eliminar", command=self.eliminarTurno).pack(side="left", padx=5)

        # --- Tabla de turnos ---
        self.tabla_turnos = ttk.Treeview(
            frame,
            columns=("ID", "FechaOculta", "Hora", "DNI", "Paciente", "Tratamiento"),
            show="headings",
            height=7
        )
        self.tabla_turnos.heading("ID", text="ID")
        self.tabla_turnos.heading("FechaOculta", text="Fecha")
        self.tabla_turnos.heading("Hora", text="Hora")
        self.tabla_turnos.heading("DNI", text="DNI")
        self.tabla_turnos.heading("Paciente", text="Paciente")
        self.tabla_turnos.heading("Tratamiento", text="Tratamiento")

        self.tabla_turnos.column("ID", width=30, anchor="center")
        self.tabla_turnos.column("FechaOculta", width=0, anchor="center", stretch=False)  # oculta la fecha
        self.tabla_turnos.column("Hora", width=60, anchor="center")
        self.tabla_turnos.column("DNI", width=80, anchor="center")
        self.tabla_turnos.column("Paciente", width=170, anchor="w")
        self.tabla_turnos.column("Tratamiento", width=150, anchor="w")
        self.tabla_turnos.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Evento de selección
        self.tabla_turnos.bind("<<TreeviewSelect>>", self.seleccionarTurno)

        # Refrescar tratamientos al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._cargar_desplegable_tratamientos())

        self._cargar_desplegable_tratamientos()

    def seleccionarTurno(self, event):
        seleccion = self.tabla_turnos.selection()
        if not seleccion:
            return
        valores = self.tabla_turnos.item(seleccion[0], "values")

        if len(valores) < 6:
            messagebox.showerror("Error", "Los datos del turno están incompletos.")
            return

        # Hora
        self.txtHora.delete(0, tk.END)
        self.txtHora.insert(0, valores[2])

        # DNI
        self.txtTurnoDni.delete(0, tk.END)
        self.txtTurnoDni.insert(0, valores[3])

        # Tratamiento
        nombre_tratamiento = valores[5]
        if nombre_tratamiento in self.cboTratamientos['values']:
            self.cboTratamientos.set(nombre_tratamiento)
            indice = list(self.cboTratamientos['values']).index(nombre_tratamiento)
            self.cboTratamientos.current(indice)

        # Guardar ID y fecha oculta
        self.turno_seleccionado_id = valores[0]
        self.turno_seleccionado_fecha = valores[1]

    def agendarTurno(self):
        paciente = Paciente.buscarPorDni(self.txtTurnoDni.get())
        seleccion = self.cboTratamientos.current()

        if not paciente:
            messagebox.showerror("Error", "Primero debe dar de alta al paciente con ese DNI.")
            return
        if seleccion == -1:
            messagebox.showerror("Error", "Debe seleccionar un tratamiento de la lista.")
            return

        tratamiento_seleccionado = self.lista_cache_tratamientos[seleccion]
        fecha_turno = self.calendario.get_date()
        hora_turno = self.txtHora.get()

        t = Turno(fecha_turno, hora_turno, paciente.id, tratamiento_seleccionado.id)

        if t.agendar():
            messagebox.showinfo("Éxito", "Turno cargado correctamente.")
            self.consultarAgendaDiaria()
        else:
            messagebox.showerror("Error", "No se pudo agendar el turno en la base de datos.")

    def modificarTurno(self):
        if not hasattr(self, "turno_seleccionado_id"):
            messagebox.showwarning("Atención", "Seleccione un turno primero.")
            return
        paciente = Paciente.buscarPorDni(self.txtTurnoDni.get())
        seleccion = self.cboTratamientos.current()
        if not paciente or seleccion == -1:
            messagebox.showerror("Error", "Debe seleccionar paciente y tratamiento válidos.")
            return
        tratamiento_seleccionado = self.lista_cache_tratamientos[seleccion]

        fecha_turno = self.turno_seleccionado_fecha

        t = Turno(fecha_turno, self.txtHora.get(), paciente.id, tratamiento_seleccionado.id, id=self.turno_seleccionado_id)

        if t.actualizar():
            messagebox.showinfo("Éxito", "Turno actualizado.")
            self.consultarAgendaDiaria()
            self.marcarDiasConTurnos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el turno.")

    def eliminarTurno(self):
        if not hasattr(self, "turno_seleccionado_id"):
            messagebox.showwarning("Atención", "Seleccione un turno primero.")
            return
        t = Turno("", "", 0, 0, id=self.turno_seleccionado_id)
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este turno?"):
            if t.cancelar():
                messagebox.showinfo("Éxito", "Turno eliminado.")
                self.consultarAgendaDiaria()
                self.marcarDiasConTurnos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el turno.")

    def consultarAgendaDiaria(self):
        for elemento in self.tabla_turnos.get_children():
            self.tabla_turnos.delete(elemento)

        fecha = self.calendario.get_date()
        turnos = Turno.obtenerAgendaDiaria(fecha)
        if not turnos:
            messagebox.showinfo("Agenda", f"No hay turnos reservados para {fecha}")
        else:
            for fila in turnos:
                self.tabla_turnos.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]))
        
        self.marcarDiasConTurnos()
        self._cargar_desplegable_tratamientos()

    def _cargar_desplegable_tratamientos(self):
        registros = Tratamiento.obtenerTodos()  # devuelve tuplas (id, nombre, precio)
        self.lista_cache_tratamientos = [Tratamiento(nombre, precio, id) for (id, nombre, precio) in registros]
        self.cboTratamientos['values'] = [t.nombre for t in self.lista_cache_tratamientos]

    def marcarDiasConTurnos(self):
        """Colorea en verde los días que tienen turnos."""
        self.calendario.calevent_remove('all')
        sql = "SELECT DISTINCT fecha FROM turnos"
        fechas = db.ejecutarConsulta(sql)

        for fila in fechas:
            fecha_str = fila[0]
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            self.calendario.calevent_create(fecha_dt, "Turnos", "turno")
        self.calendario.tag_config("turno", background="lightgreen", foreground="black")

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

        f_botones = ttk.Frame(frame)
        f_botones.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(f_botones, text="Agregar", command=self.gestionarTratamientos).pack(side="left", padx=5)
        ttk.Button(f_botones, text="Modificar", command=self.modificarTratamiento).pack(side="left", padx=5)
        ttk.Button(f_botones, text="Eliminar", command=self.eliminarTratamiento).pack(side="left", padx=5)

        self.tabla_tratamientos = ttk.Treeview(frame, columns=("ID", "Nombre", "Precio"), show="headings", height=7)
        self.tabla_tratamientos.heading("ID", text="ID")
        self.tabla_tratamientos.column("ID", anchor="center", width=50)
        self.tabla_tratamientos.heading("Nombre", text="Nombre")
        self.tabla_tratamientos.column("Nombre", anchor="center", width=150)
        self.tabla_tratamientos.heading("Precio", text="Precio")
        self.tabla_tratamientos.column("Precio", anchor="center", width=100)
        self.tabla_tratamientos.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tabla_tratamientos.bind("<<TreeviewSelect>>", self.seleccionarTratamiento)

        ttk.Button(frame, text="Ver todos los tratamientos", command=self.mostrarTratamientos).grid(row=4, column=0, columnspan=2, pady=5)

    def gestionarTratamientos(self):
        try:
            nombre = self.txtTratNombre.get()
            precio = float(self.txtTratPrecio.get())
            t = Tratamiento(nombre, precio)
            if t.insertar():
                messagebox.showinfo("Éxito", "Tratamiento registrado.")
                self.txtTratNombre.delete(0, tk.END)
                self.txtTratPrecio.delete(0, tk.END)
                self._cargar_desplegable_tratamientos()
                self.mostrarTratamientos()
            else:
                messagebox.showerror("Error", "El tratamiento ya existe o no se pudo guardar.")
        except ValueError:
            messagebox.showerror("Error", "El precio ingresado debe ser un número válido.")

    def mostrarTratamientos(self):
        for elemento in self.tabla_tratamientos.get_children():
            self.tabla_tratamientos.delete(elemento)

        tratamientos = Tratamiento.obtenerTodos()
        if not tratamientos:
            messagebox.showinfo("Tratamientos", "No hay tratamientos registrados.")
            return

        for fila in tratamientos:
            self.tabla_tratamientos.insert("", "end", values=fila)

    def seleccionarTratamiento(self, event):
        seleccion = self.tabla_tratamientos.selection()
        if not seleccion:
            return
        valores = self.tabla_tratamientos.item(seleccion[0], "values")
        self.txtTratNombre.delete(0, tk.END)
        self.txtTratNombre.insert(0, valores[1])
        self.txtTratPrecio.delete(0, tk.END)
        self.txtTratPrecio.insert(0, valores[2])
        self.tratamiento_seleccionado_id = valores[0]

    def modificarTratamiento(self):
        if not hasattr(self, "tratamiento_seleccionado_id"):
            messagebox.showwarning("Atención", "Seleccione un tratamiento primero.")
            return
        try:
            t = Tratamiento(self.txtTratNombre.get(), float(self.txtTratPrecio.get()), id=self.tratamiento_seleccionado_id)
            if t.actualizar():
                messagebox.showinfo("Éxito", "Tratamiento actualizado.")
                self.mostrarTratamientos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el tratamiento.")
        except ValueError:
            messagebox.showerror("Error", "El precio ingresado debe ser un número válido.")

    def eliminarTratamiento(self):
        if not hasattr(self, "tratamiento_seleccionado_id"):
            messagebox.showwarning("Atención", "Seleccione un tratamiento primero.")
            return
        t = Tratamiento("", 0, id=self.tratamiento_seleccionado_id)
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este tratamiento?"):
            if t.eliminar():
                messagebox.showinfo("Éxito", "Tratamiento eliminado.")
                self.mostrarTratamientos()
                self.txtTratNombre.delete(0, tk.END)
                self.txtTratPrecio.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el tratamiento.")
