import tkinter as tk
from tkinter import ttk, messagebox

# Importamos las clases de negocio individuales
from models.paciente import Paciente
from models.tratamiento import Tratamiento
from models.turno import Turno

class FormularioOdontologico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultorio Odontológico - Panel de Control")
        self.geometry("750x520")

        # Estructura del panel mediante pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.pestana_pacientes = ttk.Frame(self.notebook)
        self.pestana_turnos = ttk.Frame(self.notebook)
        self.pestana_tratamientos = ttk.Frame(self.notebook)

        self.notebook.add(self.pestana_pacientes, text="Pacientes")
        self.notebook.add(self.pestana_turnos, text="Turnos")
        self.notebook.add(self.pestana_tratamientos, text="Tratamientos")

        # Construcción de las interfaces individuales
        self._inicializar_modulo_pacientes()
        self._inicializar_modulo_turnos()
        self._inicializar_modulo_tratamientos()

    # --- MÓDULO PACIENTES ---
    def _inicializar_modulo_pacientes(self):
        frame = self.pestana_pacientes
        
        ttk.Label(frame, text="DNI:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.txtDni = ttk.Entry(frame)
        self.txtDni.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(frame, text="Buscar", command=self.buscarPaciente).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.txtNombre = ttk.Entry(frame)
        self.txtNombre.grid(row=1, column=1, padx=10, pady=10)

        # Modificado para coincidir con tu diagrama de clases (txtApellido y txtTelefono)
        ttk.Label(frame, text="Apellido:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txtApellido = ttk.Entry(frame)
        self.txtApellido.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.txtTelefono = ttk.Entry(frame)
        self.txtTelefono.grid(row=3, column=1, padx=10, pady=10)

        # Contenedor para acciones organizadas
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
            self.txtNombre.delete(0, tk.END)
            self.txtNombre.insert(0, p.nombre)
            self.txtApellido.delete(0, tk.END)
            self.txtApellido.insert(0, p.apellido)
            self.txtTelefono.delete(0, tk.END)
            self.txtTelefono.insert(0, p.telefono)
        else:
            messagebox.showwarning("Atención", "No se encontró ningún paciente asociado a ese DNI.")

    def _limpiar_formulario_paciente(self):
        self.txtDni.delete(0, tk.END)
        self.txtNombre.delete(0, tk.END)
        self.txtApellido.delete(0, tk.END)
        self.txtTelefono.delete(0, tk.END)

    # --- MÓDULO TURNOS ---
    def _inicializar_modulo_turnos(self):
        frame = self.pestana_turnos

        ttk.Label(frame, text="Fecha (AAAA-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.txtFecha = ttk.Entry(frame)
        self.txtFecha.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Hora (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtHora = ttk.Entry(frame)
        self.txtHora.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame, text="DNI Paciente:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txtTurnoDni = ttk.Entry(frame)
        self.txtTurnoDni.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Tratamiento:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.cboTratamientos = ttk.Combobox(frame, state="readonly")
        self.cboTratamientos.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Agendar Turno", command=self.agendarTurno).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Consultar Agenda", command=self.consultarAgendaDiaria).grid(row=0, column=2, padx=10)

        # Lista visual estructurada (Treeview)
        self.tabla_turnos = ttk.Treeview(frame, columns=("ID", "Hora", "Paciente", "Tratamiento"), show="headings", height=7)
        self.tabla_turnos.heading("ID", text="ID")
        self.tabla_turnos.heading("Hora", text="Hora")
        self.tabla_turnos.heading("Paciente", text="Paciente")
        self.tabla_turnos.heading("Tratamiento", text="Tratamiento")
        self.tabla_turnos.column("ID", width=50)
        self.tabla_turnos.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ttk.Button(frame, text="Cancelar Turno Seleccionado", command=self.cancelarTurno).grid(row=6, column=0, columnspan=3, pady=5)

        # Enlace para recargar los tratamientos disponibles en el menú desplegable al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._cargar_desplegable_tratamientos())

    def _cargar_desplegable_tratamientos(self):
        self.lista_cache_tratamientos = Tratamiento.obtenerTodos()
        self.cboTratamientos['values'] = [t.nombre for t in self.lista_cache_tratamientos]

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
        t = Turno(self.txtFecha.get(), self.txtHora.get(), paciente.id, tratamiento_seleccionado.id)
        
        if t.agendar():
            messagebox.showinfo("Éxito", "Turno cargado correctamente.")
            self.consultarAgendaDiaria()
        else:
            messagebox.showerror("Error", "No se pudo agendar el turno.")

    def consultarAgendaDiaria(self):
        for elemento in self.tabla_turnos.get_children():
            self.tabla_turnos.delete(elemento)

        turnos = Turno.obtainAgendaDiaria(self.txtFecha.get()) if hasattr(Turno, 'obtainAgendaDiaria') else Turno.obtenerAgendaDiaria(self.txtFecha.get())
        for fila in turnos:
            # Estructura del SELECT: (id, fecha, hora, nombre_paciente, nombre_tratamiento)
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

    # --- MÓDULO TRATAMIENTOS (gestionarTratamientos) ---
    def _inicializar_modulo_tratamientos(self):
        frame = self.pestana_tratamientos

        ttk.Label(frame, text="Nombre del Tratamiento:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.txtTratNombre = ttk.Entry(frame)
        self.txtTratNombre.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Precio ($):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.txtTratPrecio = ttk.Entry(frame)
        self.txtTratPrecio.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(frame, text="Agregar Tratamiento", command=self.gestionarTratamientos).grid(row=2, column=0, columnspan=2, pady=10)

    def gestionarTratamientos(self):
        """Maneja el alta de nuevos tratamientos validando el tipo de dato."""
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