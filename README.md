# Simulación de Rover en Django

## Descripción del Proyecto

Este proyecto es una simulación de un rover que puede recorrer parcelas o acudir a ciertos puntos de referencia para realizar funciones específicas. Ha sido desarrollado en Django, utilizando las siguientes tecnologías:

- **Leaflet**: Para la representación de mapas interactivos.  
- **PostgreSQL**: Como sistema de gestión de bases de datos.  
- **PostGIS**: Para el manejo de datos geoespaciales.  

## Estructura de la Base de Datos

El sistema incluye una base de datos con tres entidades principales:

1. **Parcelas**: Almacena el nombre de la parcela y los puntos que definen su polígono.  
2. **Puntos de Referencia**: Guarda la localización de los puntos definidos, junto con un atributo que se relaciona con la actividad correspondiente.  
3. **Actividades**: Incluye el nombre de la actividad, la duración y un indicador de si es necesaria una revisión.  

## Funcionalidades

La simulación permite al usuario:

- Visualizar el mapa con las parcelas y los puntos de actividad.  
- Enviar al rover a recorrer una parcela o acudir a ciertos puntos de referencia mediante botones de la interfaz.  
- Monitorear el recorrido del rover en el mapa y mostrar información en pantalla al llegar a un punto de referencia.  

