
# SGMI - Sistema de gestión y monitoreo de invernaderos en Python
Por: Valentina Lopez Orozco

Este proyecto es una aplicación desarrollada en Python para la gestión y monitoreo de invernaderos, utilizando diversas librerías para facilitar la interfaz gráfica, la manipulación de datos y el envío de notificaciones vía WhatsApp.

## Descripción

SGMI está diseñado para ayudar a gestionar la información y el monitoreo de cultivos dentro de un invernadero. A través de una interfaz gráfica amigable, el sistema permite al usuario administrar datos de los cultivos como lo es la humedad y temperatura y recibir notificaciones mediante WhatsApp cuando es necesario.

### Características principales:
- Gestión de datos de usuarios y cultivos.
- Interfaz gráfica desarrollada con `tkinter` para facilidad de uso.
- Envío de mensajes automáticos a través de WhatsApp utilizando `pywhatkit`.
- Almacenamiento de datos en formato JSON.
- Utilización de `pandas` para manipulación de datos.
- Control y gestión de eventos con fechas mediante la librería `datetime`.

## Instalación

### Requisitos:
- Tener instalado Python 3.7+
- Librerías necesarias:
  - `pandas`
  - `tkinter`
  - `pywhatkit`
  - `json` (incluida en Python)
  - `datetime` (incluida en Python)

### Pasos:
1. Clona este repositorio:
   ```bash
   git clone https://github.com/valen-agro/SGMI.git
   ```
2. Instala las dependencias:
   ```bash
   pip install pandas
   pip install pywhatkit
   ```

## Uso

1. Ejecuta el script principal para iniciar la interfaz gráfica del sistema:
   ```bash
   python verduras(5).py
   ```

2. Desde la interfaz gráfica, puedes realizar las siguientes acciones:
   - Agregar y modificar datos de cultivos.
   - Configurar notificaciones automáticas para enviar recordatorios por WhatsApp sobre el estado de los cultivos.

3. Los datos se almacenarán en archivos JSON para su persistencia y consulta posterior.

## Estructura del proyecto

- `verduras(5).py`: Archivo principal que contiene la lógica del sistema y la interfaz gráfica.
- `usuarios.json`: Archivo donde se almacenan los datos de los usuarios del sistema.
- `PyWhatKit_DB.txt`: Archivo temporal que contiene el historial de mensajes enviados a través de WhatsApp.

## Librerías utilizadas

- `pandas`: Para la manipulación y análisis de datos de los cultivos.
- `tkinter`: Para el diseño y control de la interfaz gráfica de usuario.
- `pywhatkit`: Para el envío automatizado de mensajes de WhatsApp.
- `json`: Para el almacenamiento estructurado de datos.
- `datetime`: Para el manejo de fechas y horas.
