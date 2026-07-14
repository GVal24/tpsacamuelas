# Sistema de Gestión para Consultorio Odontológico "Saca Muela" 🦷

Este proyecto es una aplicación de escritorio desarrollada en **Python** diseñada específicamente para la administración de la agenda profesional, el seguimiento de tratamientos odontológicos y la gestión de la cartilla de pacientes del consultorio "Saca Muela".

El sistema cumple con los lineamientos del **Hito 2 (Implementación)** para la materia *Algoritmos y Estructuras de Datos II* de la carrera *Análisis de Sistemas* (ISFT 151).

---

## 📌 Características Principales

* **Agenda Diaria Automatizada:** Consulta interactiva de turnos diarios vinculada directamente a la selección de fechas en un calendario interactivo.
* **Gestión Integral (CRUD):**
  * **Pacientes:** Registro, modificación, consulta y eliminación de fichas personales.
  * **Turnos:** Agendamiento, reprogramación y cancelación de citas en tiempo real.
  * **Tratamientos:** Catálogo de prestaciones ofrecidas en el consultorio.
* **Persistencia Local Segura:** Almacenamiento y persistencia local de datos utilizando **SQLite**, eliminando dependencias de conexión a Internet.
* **Validación Robusta:** Cumple de manera estricta con las restricciones del dominio del negocio (DNI único para pacientes, validación de formatos, control estricto de superposiciones horarias y campos obligatorios).

---

## 🛠️ Arquitectura y Tecnologías Utilizadas

El sistema sigue un enfoque de **separación estricta de capas** (interfaz, lógica de negocio y acceso a datos):

* **Lenguaje:** Python 3
* **Interfaz Gráfica (GUI):** `tkinter` y `ttk.notebook` para la organización de la aplicación en pestañas intuitivas.
* **Calendario Dinámico:** `tkcalendar` (integración con bindings de eventos en tiempo real).
* **Base de Datos:** SQLite (`sqlite3`).

### Estructura de Capas
* **`consultorio.py`:** Administra la conexión, creación de tablas y ejecución directa de sentencias SQL en la base de datos local.
* **`paciente.py` / `turno.py` / `tratamiento.py`:** Capa de lógica de negocio y modelado de objetos. Llevan a cabo las validaciones lógicas antes de la persistencia.
* **`formulario_odontologico.py`:** Capa de presentación (interfaz gráfica) encargada de la captura de datos y renderizado de la UI.

---

## 📋 Requisitos del Sistema

* **Sistema Operativo:** Windows 10 u 11, macOS o Linux.
* **Procesador:** Cualquier procesador moderno.
* **Memoria RAM:** 2 GB de RAM libres.
* **Python:** v3.8 o superior instalado.

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para clonar el repositorio e iniciar la aplicación en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/GVal24/tpsacamuelas.git](https://github.com/GVal24/tpsacamuelas.git)
   cd tpsacamuelas
2. **Instalar dependencia necesaria**
    ```bash
    pip install tkcalendar
3. **Ejecutar la aplicación**
    ```bash
    python main.py

---

## ⚙️ Reglas de Dominio del Negocio Implementadas

* **DNI Único:** No se permite la duplicación de fichas personales bajo un mismo número de DNI.
* **Integridad de Tratamientos:** Cada tratamiento asignado está vinculado estrictamente a un paciente preexistente.
* **Contacto Obligatorio:** Se exige un número de teléfono de contacto para agendar o modificar un turno.
* **Sin superposiciones:** El sistema bloquea de forma inteligente cualquier intento de agendar un turno que colisione en fecha y hora con uno ya existente.

---

## 🧑‍💻 Autor
* **Institución:** ISFT N°151- Mar del Plata
* **Carrera:** Tecnicatura Superior en Análisis de Sistemas
* **Estudiante:** Guillermina Valdez 
