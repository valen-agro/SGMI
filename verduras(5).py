import pandas as pd
import tkinter as tk
from tkinter import messagebox
import pywhatkit
import json
from datetime import datetime

PLANTAS = {
    "tomate": {"temperatura_minima": 15, "temperatura_maxima": 25, "humedad_minima": 40, "humedad_maxima": 60},
    "lechuga": {"temperatura_minima": 10, "temperatura_maxima": 20, "humedad_minima": 30, "humedad_maxima": 50},
    "pepino": {"temperatura_minima": 18, "temperatura_maxima": 28, "humedad_minima": 50, "humedad_maxima": 70},
    "fresa": {"temperatura_minima": 12, "temperatura_maxima": 22, "humedad_minima": 60, "humedad_maxima": 80},
    "pimiento": {"temperatura_minima": 18, "temperatura_maxima": 30, "humedad_minima": 50, "humedad_maxima": 70},
    "albahaca": {"temperatura_minima": 15, "temperatura_maxima": 25, "humedad_minima": 40, "humedad_maxima": 60},
    "espinaca": {"temperatura_minima": 10, "temperatura_maxima": 20, "humedad_minima": 50, "humedad_maxima": 70},
    "berenjena": {"temperatura_minima": 20, "temperatura_maxima": 30, "humedad_minima": 50, "humedad_maxima": 70},
    "rábano": {"temperatura_minima": 12, "temperatura_maxima": 22, "humedad_minima": 30, "humedad_maxima": 60},
    "cilantro": {"temperatura_minima": 15, "temperatura_maxima": 25, "humedad_minima": 40, "humedad_maxima": 60},
    "zanahoria": {"temperatura_minima": 10, "temperatura_maxima": 20, "humedad_minima": 50, "humedad_maxima": 70},
    "menta": {"temperatura_minima": 15, "temperatura_maxima": 25, "humedad_minima": 60, "humedad_maxima": 80},
    "brócoli": {"temperatura_minima": 15, "temperatura_maxima": 20, "humedad_minima": 50, "humedad_maxima": 70},
    "coliflor": {"temperatura_minima": 15, "temperatura_maxima": 20, "humedad_minima": 50, "humedad_maxima": 80},
    "fresón": {"temperatura_minima": 12, "temperatura_maxima": 22, "humedad_minima": 60, "humedad_maxima": 80},
}

df = pd.DataFrame(PLANTAS)
print (df)

class AplicacionMonitoreoDePlantas:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Monitoreo de Plantas")
        self.ventana_principal.geometry("400x300")

        self.usuarios = self.cargar_usuarios()
        self.usuario_actual = None

        self.mostrar_inicio_sesion()

    def cargar_usuarios(self):
        try:
            with open("usuarios.json", "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def guardar_usuarios(self):
        with open("usuarios.json", "w") as f:
            json.dump(self.usuarios, f, indent=4)

    def mostrar_inicio_sesion(self):
        self.clear_frame()
        tk.Label(self.ventana_principal, text="telefono con el que se registró:").pack(pady=10)
        self.numero_telefono = tk.Entry(self.ventana_principal)
        self.numero_telefono.pack(pady=5)

        tk.Button(self.ventana_principal, text="Iniciar Sesión", command=self.iniciar_sesion).pack(pady=5)
        tk.Button(self.ventana_principal, text="Registrarse", command=self.mostrar_registro).pack(pady=5)

    def iniciar_sesion(self):
        telefono = self.numero_telefono.get()
        if telefono in self.usuarios:
            self.usuario_actual = telefono
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario no encontrado. Por favor, regístrese.")

    def mostrar_registro(self):
        self.clear_frame()
        tk.Label(self.ventana_principal, text="Ingrese un numero de telefono con el codigo del pais:").pack(pady=10)
        self.numero_telefono = tk.Entry(self.ventana_principal)
        self.numero_telefono.pack(pady=5)

        tk.Label(self.ventana_principal, text="Tipo de planta:").pack(pady=10)
        self.seleccionar_planta_var = tk.StringVar(self.ventana_principal)
        self.seleccionar_planta_var.set(list(PLANTAS.keys())[0])
        tk.OptionMenu(self.ventana_principal, self.seleccionar_planta_var, *PLANTAS.keys()).pack(pady=5)

        tk.Button(self.ventana_principal, text="Registrar", command=self.registrar_usuario).pack(pady=5)
        tk.Button(self.ventana_principal, text="Volver", command=self.mostrar_inicio_sesion).pack(pady=5)

    def mostrar_menu_principal(self):
        self.clear_frame()
        tk.Label(self.ventana_principal, text=f"Planta actual: {self.usuarios[self.usuario_actual]['tipo_planta']}").pack(pady=10)

        tk.Label(self.ventana_principal, text="Temperatura (°C):").pack(pady=5)
        self.ingresar_temperatura = tk.Entry(self.ventana_principal)
        self.ingresar_temperatura.pack(pady=5)

        tk.Label(self.ventana_principal, text="Humedad (%):").pack(pady=5)
        self.ingresar_humedad = tk.Entry(self.ventana_principal)
        self.ingresar_humedad.pack(pady=5)

        tk.Button(self.ventana_principal, text="Ver Informe", command=self.ver_informe).pack(pady=5)
        tk.Button(self.ventana_principal, text="Ver Historial", command=self.ver_historial).pack(pady=5)
        tk.Button(self.ventana_principal, text="Actualizar Datos", command=self.actualizar_datos).pack(pady=5)
        tk.Button(self.ventana_principal, text="Cambiar Tipo de Planta", command=self.cambiar_tipo_planta).pack(pady=5)
        tk.Button(self.ventana_principal, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def clear_frame(self):
        for widget in self.ventana_principal.winfo_children():
            widget.destroy()

    def registrar_usuario(self):
        telefono = self.numero_telefono.get()
        tipo_planta = self.seleccionar_planta_var.get()

        if not telefono:
            messagebox.showerror("Error", "Por favor, ingrese un número de telefono valido.")
            return

        if telefono in self.usuarios:
            messagebox.showinfo("Info", "El usuario ya está registrado.")
            return

        self.usuarios[telefono] = {
            "tipo_planta": tipo_planta,
            "historial": []
        }
        self.guardar_usuarios()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        self.usuario_actual = telefono
        self.mostrar_menu_principal()

    def ver_informe(self):
        try:
            temp = float(self.ingresar_temperatura.get())
            humidity = float(self.ingresar_humedad.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            return
        
        informe = self.generar_informe(temp, humidity)

        informe_window = tk.Toplevel(self.ventana_principal)
        informe_window.title("Informe")
        informe_window.geometry("500x400")  

            
        text_widget = tk.Text(informe_window, wrap=tk.WORD)
        text_widget.insert(tk.END, informe)
        text_widget.config(state=tk.DISABLED)  
        text_widget.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)  

        tk.Button(informe_window, text="Enviar por WhatsApp", command=lambda: self.enviar_informe(informe)).pack(pady=5)

    def ver_historial(self):
        if not self.usuarios[self.usuario_actual]['historial']:
            messagebox.showinfo("Historial", "No hay registros en el historial.")
            return

        history_window = tk.Toplevel(self.ventana_principal)
        history_window.title("Historial de Registros")

        historial_str = "\n".join([f"{registro['fecha']}: Temp: {registro['temperatura']}°C, Hum: {registro['humedad']}%"
                                   for registro in self.usuarios[self.usuario_actual]['historial'][-10:]])

        tk.Label(history_window, text=historial_str).pack(pady=10)
        tk.Button(history_window, text="Enviar Últimos 5 Registros por WhatsApp", command=self.enviar_historial).pack(pady=5)

    def enviar_informe(self, informe):
        try:
            pywhatkit.sendwhatmsg_instantly(f"+{self.usuario_actual}", informe, 50, True, 5)
            messagebox.showinfo("Completo", "Informe enviado por WhatsApp.")
            self.actualizar_historial(float(self.ingresar_temperatura.get()), float(self.ingresar_humedad.get()))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el mensaje: {str(e)}")

    def enviar_historial(self):
        if not self.usuarios[self.usuario_actual]['historial']:
            messagebox.showinfo("Historial", "No hay registros en el historial.")
            return

        ultimos_cinco = self.usuarios[self.usuario_actual]['historial'][-5:]
        resumen = self.generar_resumen_historial(ultimos_cinco)

        try:
            pywhatkit.sendwhatmsg_instantly(f"+{self.usuario_actual}", resumen, 50, True, 5)
            messagebox.showinfo("Completo", "Historial enviado por WhatsApp.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el historial: {str(e)}")

    def generar_resumen_historial(self, registros):
        cambios_temperatura = [registro['temperatura'] for registro in registros]
        cambios_humedad = [registro['humedad'] for registro in registros]

        comportamiento = "Resumen de los últimos 5 registros:\n"
        comportamiento += "Temperatura:\n"
        comportamiento += f"Máxima: {max(cambios_temperatura)}°C, Mínima: {min(cambios_temperatura)}°C\n"
        comportamiento += "Humedad:\n"
        comportamiento += f"Máxima: {max(cambios_humedad)}%, Mínima: {min(cambios_humedad)}%\n"

        tendencia_temperatura = "ha aumentado" if cambios_temperatura[-1] > cambios_temperatura[0] else \
                                "ha disminimauido" if cambios_temperatura[-1] < cambios_temperatura[0] else \
                                "se ha mantenido constante"

        tendencia_humedad = "ha aumentado" if cambios_humedad[-1] > cambios_humedad[0] else \
                            "ha disminimauido" if cambios_humedad[-1] < cambios_humedad[0] else \
                            "se ha mantenido constante"

        comportamiento += f"La temperatura {tendencia_temperatura} en los últimos 5 registros.\n"
        comportamiento += f"La humedad {tendencia_humedad} en los últimos 5 registros.\n"

        return comportamiento

    def actualizar_datos(self):
        try:
            temp = float(self.ingresar_temperatura.get())
            humidity = float(self.ingresar_humedad.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            return

        self.actualizar_historial(temp, humidity)
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")

    def actualizar_historial(self, temp, humidity):
        self.usuarios[self.usuario_actual]['historial'].append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura": temp,
            "humedad": humidity
        })
        self.guardar_usuarios()

    def generar_informe(self, temp, humidity):
        plant_config = PLANTAS[self.usuarios[self.usuario_actual]['tipo_planta']]
        informe = f"Informe para {self.usuarios[self.usuario_actual]['tipo_planta']}:\n"
        informe += f"Temperatura: {temp}°C (Óptimo: {plant_config['temperatura_minima']}°C - {plant_config['temperatura_maxima']}°C)\n"
        informe += f"Humedad: {humidity}% (Óptimo: {plant_config['humedad_minima']}% - {plant_config['humedad_maxima']}%)\n"
        informe += "Estado: "

        if (plant_config['temperatura_minima'] <= temp <= plant_config['temperatura_maxima'] and
                plant_config['humedad_minima'] <= humidity <= plant_config['humedad_maxima']):
            informe += "Óptimo"
        else:
            informe += "No óptimo"
        informe += "\nRecomendaciones:\n"
        if temp < plant_config['temperatura_minima']:
            informe += ("Aumentar la temperatura:\n"
                   "La temperatura es uno de los factores más cruciales en el desarrollo de las plantas. Cuando la "
                   "temperatura cae por debajo del umbral mínimo establecido, la planta puede entrar en un estado de "
                   "estrés que ralentiza su metabolismo, inhibiendo su crecimiento y fotosíntesis. Si la temperatura "
                   "está por debajo de los 15°C, muchas plantas tropicales pueden sufrir daños en su estructura celular. "
                   "Para solucionar esto, se recomienda usar un calefactor o mover la planta a una zona más cálida. "
                   "Es fundamental monitorear la temperatura para evitar fluctuaciones bruscas que puedan causar un shock "
                   "térmico.\n\n")

        if humidity < plant_config['humedad_minima']:
            informe += ("Aumentar la humedad:\n"
                   "La humedad baja afecta significativamente el crecimiento de la planta, especialmente en especies "
                   "que provienen de climas tropicales. Cuando la humedad cae por debajo de lo requerido, la planta pierde "
                   "agua rápidamente, provocando que las hojas se marchiten y que las raíces no puedan compensar la pérdida. "
                   "Usar un humidificador o colocar un plato con agua cerca puede aumentar la humedad ambiental de manera "
                   "natural. También se puede rociar agua sobre las hojas, pero debe hacerse sin exposición directa al sol "
                   "para evitar quemaduras.\n\n")

        if temp > plant_config['temperatura_maxima']:
            informe += ("Reducir la temperatura:\n"
                   "Las altas temperaturas estresan a la planta y ralentizan su fotosíntesis. Si la temperatura supera "
                   "los 30°C, algunas plantas pueden sufrir quemaduras en las hojas, y las raíces podrían dañarse debido "
                   "a la evaporación acelerada del agua en el suelo. Para reducir la temperatura, mueve la planta a un lugar "
                   "más fresco o utiliza ventiladores para mejorar la circulación de aire. Controlar la ubicación es clave "
                   "para evitar daños permanentes.\n\n")
            
        if humidity > plant_config['humedad_maxima']:
            informe += ("Reducir la humedad:\n"
                   "Un exceso de humedad crea el ambiente ideal para enfermedades fúngicas como el mildiu y el oídio. Estas "
                   "enfermedades se propagan rápidamente en condiciones de alta humedad y baja circulación de aire. Para reducir "
                   "la humedad, asegúrate de una buena ventilación alrededor de la planta, disminimauye la frecuencia de riego y, "
                   "si es necesario, usa un deshumidificador. Prevenir las enfermedades fúngicas es crucial, ya que son difíciles "
                   "de erradicar sin dañar la planta.\n\n")
            
        if (temp >= plant_config['temperatura_minima'] and temp <= plant_config['temperatura_maxima'] and
        humidity >= plant_config['humedad_minima'] and humidity <= plant_config['humedad_maxima']):
            informe += ("Mantener las condiciones óptimas:\n"
                   "Cuando la temperatura y la humedad están dentro de los rangos óptimos, la planta puede crecer "
                   "de manera saludable. Continúa monitoreando las condiciones regularmente para asegurarte de que no "
                   "haya cambios bruscos. Documentar este periodo de estabilidad puede ser útil para futuras referencias y para "
                   "optimizar el cuidado de la planta. También es recomendable ajustar el riego y la exposición al sol según la "
                   "estación del año.\n\n")

        return informe

    def cambiar_tipo_planta(self):
        self.clear_frame()
        tk.Label(self.ventana_principal, text="Seleccione nuevo tipo de planta:").pack(pady=10)
        self.nueva_seleccionar_planta = tk.StringVar(self.ventana_principal)
        self.nueva_seleccionar_planta.set(self.usuarios[self.usuario_actual]['tipo_planta'])
        tk.OptionMenu(self.ventana_principal, self.nueva_seleccionar_planta, *PLANTAS.keys()).pack(pady=5)

        tk.Button(self.ventana_principal, text="Actualizar Tipo de Planta", command=self.actualizar_tipo_planta).pack(pady=5)
        tk.Button(self.ventana_principal, text="Volver", command=self.mostrar_menu_principal).pack(pady=5)

    def actualizar_tipo_planta(self):
        nueva_planta = self.nueva_seleccionar_planta.get()
        self.usuarios[self.usuario_actual]['tipo_planta'] = nueva_planta
        self.guardar_usuarios()
        messagebox.showinfo("Éxito", "Tipo de planta actualizado correctamente.")
        self.mostrar_menu_principal()

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.mostrar_inicio_sesion()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionMonitoreoDePlantas(root)
    root.mainloop()