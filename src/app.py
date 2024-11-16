import streamlit as st
import pandas as pd
from db import crear_tablas, agregar_reserva, ver_reservas, eliminar_reserva

# Inicializa las tablas al iniciar la aplicación
crear_tablas()

def main():
    st.title("Simulación de Gestión de Aulas")

    # Formulario para realizar reservas
    st.header("Reserva de Aulas")
    aula_opciones = {
        "Aula 1: Laboratorio": ["Informatica", "Laboratorio", "Ciencias"],
        "Aula 2: Educación Física": ["Fútbol", "Handball", "Actividades Físicas Varias", "Torneos y Eventos Escolares"],
        "Aula 3: Proyector": ["Proyección", "Conferencias", "Charlas", "Actividades Varias"]
    }

    # Selección del aula
    aula_seleccionada = st.selectbox("Selecciona el aula", list(aula_opciones.keys()))

    # Ingreso del nombre del profesor
    profesor = st.text_input("Nombre del Profesor")

    # Selección de la materia
    materia = st.selectbox("Selecciona la materia", aula_opciones[aula_seleccionada])

    # Selección de grado
    grado = st.selectbox("Selecciona el grado", ["Séptimo", "Octavo", "Noveno"])

    # Selección de fecha y horario
    fecha = st.date_input("Selecciona la fecha")
    hora_inicio = st.time_input("Hora de inicio")
    hora_fin = st.time_input("Hora de fin")

    if st.button("Reservar Aula"):
        # Agregar la reserva a la base de datos
        agregar_reserva(aula_seleccionada, profesor, materia, grado, fecha, hora_inicio, hora_fin)
        st.success("Reserva realizada con éxito!")

    # Mostrar reservas actuales
    reservas_df = ver_reservas()
    
    if not reservas_df.empty:
        st.header("Reservas Actuales")
        st.write(reservas_df)

    # Opción para eliminar una reserva
        reserva_id = st.selectbox("Selecciona la reserva a eliminar", reservas_df['id'].tolist(), key='eliminar_reserva')
        if st.button("Eliminar Reserva"):
            eliminar_reserva(reserva_id)
            st.success(f"Reserva con ID {reserva_id} eliminada con éxito!")

            # Volver a cargar las reservas después de la eliminación
            reservas_df = ver_reservas()
        
        # Mostrar reservas actualizadas
        st.write(reservas_df)
    else:
        st.write("No hay reservas actuales.")

if __name__ == "__main__":
    main()
