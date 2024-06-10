import streamlit as st
import pandas as pd

# Título de la aplicación
st.title('Resumen de Materiales por Producto')

# Cargar datos
@st.cache_data
def cargar_datos():
    productos = pd.read_csv('Productos.csv')
    materiales = pd.read_csv('Materiales.csv')
    producto_material = pd.read_csv('ProductoMaterial.csv')
    
    # Merge de las tablas para obtener una vista completa
    producto_material_completo = producto_material.merge(productos, on='ProductoID').merge(materiales, on='MaterialID')
    
    return productos, materiales, producto_material_completo

# Llamar la función para cargar los datos
productos, materiales, producto_material_completo = cargar_datos()

# Selección del producto
producto_seleccionado = st.selectbox('Selecciona un Producto', productos['ProductoNombre'])

# Filtrar los materiales según el producto seleccionado
materiales_necesarios = producto_material_completo[producto_material_completo['ProductoNombre'] == producto_seleccionado]

# Mostrar el resumen de materiales necesarios
st.write(f'Materiales necesarios para construir: {producto_seleccionado}')
st.table(materiales_necesarios[['MaterialNombre']])

# Sección de validación y copia de selección
if st.button('Guardar Selección'):
    # Crear un resumen de la selección
    resumen_seleccion = materiales_necesarios[['MaterialNombre']]
    
    # Guardar el resumen en una nueva hoja
    resumen_seleccion.to_csv('ResumenSeleccion.csv', index=False)
    st.success('Selección guardada exitosamente en ResumenSeleccion.csv')

# Visualización adicional opcional
st.subheader('Vista Completa de Productos y Materiales')
st.dataframe(producto_material_completo)
