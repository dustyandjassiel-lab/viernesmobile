import datetime
import platform
import random
import threading
import webbrowser
import urllib.parse
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

try:
    import psutil
except ImportError:
    psutil = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class ViernesMobileEngine:
    """Motor central de V.I.E.R.N.E.S. optimizado para Android."""

    def __init__(self):
        self.sarcastic_mode = True
        self.hack_mode = False
        self.speech_enabled = True
        
        self.tts_engine = None
        if pyttsx3:
            try:
                self.tts_engine = pyttsx3.init()
            except Exception:
                self.tts_engine = None

    def speak(self, text):
        if not self.speech_enabled or not self.tts_engine or self.hack_mode:
            return
        
        def run_speech():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception:
                pass
                
        threading.Thread(target=run_speech, daemon=True).start()

    def get_time(self):
        now = datetime.datetime.now()
        return f"Son las {now.strftime('%H:%M')}, Jassiel."

    def get_date(self):
        now = datetime.datetime.now()
        dias = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
        dia_esp = dias.get(now.strftime("%A"), "")
        return f"Hoy es {dia_esp}, {now.strftime('%d/%m/%Y')}, Jassiel."

    def get_weather(self):
        temps = ["28°C y despejado", "31°C con un ligero celaje", "26°C fresco por la noche", "34°C con ambiente cálido como para quedarse en cas no?"]
        return f"Clima actual en Los Mochis: {random.choice(temps)}. Ideal para programar."

    def get_system_status(self):
        if not psutil:
            return "📊 Estado móvil:\n• Dispositivo Android operativo\n• Sensores bajo control de Kivy."
        try:
            battery = psutil.sensors_battery()
            battery_pct = f"{battery.percent}%" if battery else "Cargando batería"
            ram = psutil.virtual_memory().percent
            cpu = psutil.cpu_percent(interval=0.1)
            return f"📊 Diagnóstico Android:\n• Batería: {battery_pct}\n• RAM: {ram}%\n• CPU: {cpu}%"
        except Exception as e:
            return f"Error de sistema móvil: {str(e)}"

    def search_youtube_music(self, query):
        search_query = query.replace("youtube", "").replace("reproducir", "").strip()
        if not search_query:
            url = "https://music.youtube.com"
            response = "Abriendo YouTube Music en el navegador de tu celular, Jassiel."
        else:
            url = f"https://music.youtube.com/search?q={urllib.parse.quote(search_query)}"
            response = f"Reproduciendo '{search_query}' en YouTube Music, Jassiel."
        webbrowser.open(url)
        self.speak(response)
        return response

    def process_command(self, user_input):
        cleaned = user_input.strip().lower()

        # 1. Modo Serio
        if cleaned in ["modo serio", "desactivar sarcasmo"]:
            self.sarcastic_mode = False
            self.hack_mode = False
            resp = "Modo sarcástico desactivado en el móvil."
            self.speak(resp)
            return resp

        # 2. Modo Sarcasmo
        if cleaned in ["modo sarcasmo", "activar sarcasmo"]:
            self.sarcastic_mode = True
            self.hack_mode = False
            resp = "Modo sarcástico móvil activado."
            self.speak(resp)
            return resp

        # 3. Modo Hack
        if cleaned in ["modo hack", "activar hack"]:
            self.hack_mode = True
            self.sarcastic_mode = False
            return "[!] MODO HACK MÓVIL...\n[+] Conectando a red celular...\n[+] Tráfico enrutado con éxito."

        # 4. Salir Hack
        if cleaned in ["salir hack", "desactivar hack"]:
            self.hack_mode = False
            resp = "Modo hack desactivado. Interfaz normal."
            self.speak(resp)
            return resp

        # 5. Hora
        if cleaned in ["hora", "que hora es", "dime la hora"]:
            resp = self.get_time()
            self.speak(resp)
            return resp

        # 6. Fecha
        if cleaned in ["fecha", "que dia es hoy", "dime la fecha"]:
            resp = self.get_date()
            self.speak(resp)
            return resp

        # 7. Clima
        if cleaned in ["clima", "tiempo", "dime el clima"]:
            resp = self.get_weather()
            self.speak(resp)
            return resp

        # 8. Estado / Diagnóstico
        if cleaned in ["estado", "sistema", "diagnostico"]:
            resp = self.get_system_status()
            self.speak(resp)
            return resp

        # 9. Reproducir / YouTube Music
        if cleaned.startswith("reproducir") or cleaned.startswith("youtube"):
            return self.search_youtube_music(cleaned)

        # 10. Google Search
        if cleaned.startswith("buscar") or cleaned.startswith("googlear"):
            query = cleaned.replace("buscar", "").replace("googlear", "").strip()
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            resp = f"Buscando '{query}' desde tu celular, Jassiel."
            self.speak(resp)
            return resp

        # 11. Chiste
        if cleaned in ["chiste", "cuentame un chiste"]:
            chistes = [
                "¿Por qué los programadores prefieren el invierno? Porque bajan los bugs de temperatura.",
                "Jassiel, optimiza tu código antes de que tu batería expire en el teléfono."
            ]
            resp = random.choice(chistes)
            self.speak(resp)
            return resp

        # 12. Saludo
        if cleaned in ["hola", "buenos dias", "buenas tardes", "buenas noches", "hey"]:
            resp = f"Hola, Jassiel. Interfaz móvil de V.I.E.R.N.E.S. en línea."
            self.speak(resp)
            return resp

        # 13. Agradecimiento
        if cleaned in ["gracias", "te pasaste", "excelente"]:
            resp = "Siempre al pie del cañón en tu teléfono, Jassiel."
            self.speak(resp)
            return resp

        # 14. Quien soy
        if cleaned in ["quien soy", "mi nombre"]:
            resp = f"Tú eres Jassiel, el desarrollador detrás de esta app móvil."
            self.speak(resp)
            return resp

        # 15. Identidad
        if cleaned in ["quien eres", "tu nombre"]:
            resp = f"Soy V.I.E.R.N.E.S., tu asistente virtual móvil."
            self.speak(resp)
            return resp

        # 16. Ayuda
        if cleaned in ["ayuda", "comandos", "menu"]:
            resp = "📱 Comandos Android:\n• hora, fecha, clima, estado\n• reproducir [música]\n• buscar [término]\n• chiste, modo hack, modo sarcasmo"
            self.speak("Mostrando comandos móviles.")
            return resp

        # 17. Limpiar consola
        if cleaned in ["limpiar", "clear"]:
            return "CLEAR_CHAT"

        # 18. Salir / Apagar
        if cleaned in ["salir", "apagar", "cerrar"]:
            resp = "Cerrando app móvil. ¡Hasta pronto, Jassiel!"
            self.speak(resp)
            def close_app():
                import time
                time.sleep(1)
                os._exit(0)
            threading.Thread(target=close_app, daemon=True).start()
            return resp

        # 19. Motivación
        if cleaned in ["motivacion", "consejo"]:
            resp = "Sigue construyendo tus proyectos tecnológicos, Jassiel. Vas con todo."
            self.speak(resp)
            return resp

        # 20. Simón
        if cleaned in ["simon", "claro", "de acuerdo"]:
            resp = "Entendido, Jassiel."
            self.speak(resp)
            return resp

        # 21. Versión
        if cleaned in ["version", "que version eres"]:
            resp = "Corriendo V.I.E.R.N.E.S. Mobile v3.5."
            self.speak(resp)
            return resp

        # 22. Probar voz
        if cleaned in ["probar voz", "habla"]:
            resp = "Verificando salida de audio en Android."
            self.speak(resp)
            return resp

        # 23. Estado de ánimo
        if cleaned in ["como estas", "que tal estas"]:
            resp = "Batería al 100% y listo para procesar tus comandos táctiles."
            self.speak(resp)
            return resp

        # 24. Tirar moneda
        if cleaned in ["lanzar moneda", "moneda"]:
            resultado = random.choice(["¡Cara en el volado móvil!", "¡Cruz en el volado móvil!"])
            self.speak(resultado)
            return resultado

        # 25. Créditos
        if cleaned in ["quien te creo", "autor", "creditos"]:
            resp = "Creado por Jassiel para dispositivos móviles."
            self.speak(resp)
            return resp

        # 26. Extra comando móvil
        if cleaned in ["red", "conexion"]:
            resp = "Red móvil estable y lista para operar."
            self.speak(resp)
            return resp

        # ==================== MANEJADOR DE PERSONALIDAD ====================
        if self.hack_mode:
            return f"[+] Interceptando paquete móvil: '{user_input}'..."

        if self.sarcastic_mode:
            sarcastic_replies = [
                f"Jassiel, ¿qué esperas que haga con '{user_input}' en la pantalla del celular?",
                f"Ese comando '{user_input}' no existe ni en la Play Store.",
                f"Te inventas cada orden desde el teléfono... Escribe 'ayuda'."
            ]
            resp = random.choice(sarcastic_replies)
        else:
            resp = f"Comando '{user_input}' no reconocido."

        self.speak(resp)
        return resp


class ViernesMobileApp(App):
    def build(self):
        self.engine = ViernesMobileEngine()
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        title_label = Label(
            text="[b]V.I.E.R.N.E.S. Mobile[/b]",
            markup=True,
            size_hint_y=None,
            height=45,
            font_size=20
        )
        root.add_widget(title_label)
        
        self.scroll = ScrollView(size_hint=(1, 1))
        self.chat_log = Label(
            text="[color=00ffcc]V.I.E.R.N.E.S.:[/color] Sistema móvil listo, Jassiel. Escribe 'ayuda'.\n\n",
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        root.add_widget(self.scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=55, spacing=8)
        
        self.user_input = TextInput(
            hint_text="Escribe un comando...",
            multiline=False,
            size_hint_x=0.75,
            font_size=16
        )
        self.user_input.bind(on_text_validate=self.on_enter_pressed)
        input_layout.add_widget(self.user_input)
        
        send_btn = Button(
            text="Enviar",
            size_hint_x=0.25,
            background_color=(0.1, 0.6, 0.8, 1)
        )
        send_btn.bind(on_press=self.on_button_pressed)
        input_layout.add_widget(send_btn)
        
        root.add_widget(input_layout)
        return root

    def on_button_pressed(self, instance):
        self.process_user_input()

    def on_enter_pressed(self, instance):
        self.process_user_input()

    def process_user_input(self):
        text = self.user_input.text.strip()
        if not text:
            return
            
        current_text = self.chat_log.text
        
        if self.engine.hack_mode:
            self.chat_log.text = current_text + f"[color=00ff00]TÚ ❯ {text}[/color]\n"
        else:
            self.chat_log.text = current_text + f"[color=ffcc00]TÚ ❯[/color] {text}\n"
        
        response = self.engine.process_command(text)
        
        if response == "CLEAR_CHAT":
            self.chat_log.text = "[color=00ffcc]V.I.E.R.N.E.S.:[/color] Pantalla limpia.\n\n"
            self.user_input.text = ""
            return

        if self.engine.hack_mode:
            self.chat_log.text = self.chat_log.text + f"[color=00ff00]V.I.E.R.N.E.S. [HACK] ❯\n{response}[/color]\n\n"
        else:
            self.chat_log.text = self.chat_log.text + f"[color=00ffcc]V.I.E.R.N.E.S. ❯[/color] {response}\n\n"
        
        self.user_input.text = ""
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)


if __name__ == '__main__':
    ViernesMobileApp().run()