import pandas as pd
from datetime import datetime
from pathlib import Path
import re
import random
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Se importa webdriver-manager para gestionar chromedriver automáticamente
from webdriver_manager.chrome import ChromeDriverManager

class Agenda:
    def __init__(self,max: int=100,backup_route: str="backup"):
        self.contacts={}
        self.max=max
        self.date_create=datetime.now()
        self.date_change = None
        self.backup_route = backup_route
        Path(self.backup_route).mkdir(parents=True, exist_ok=True)

    def add(self,nombre:str,telefono:str):
        if len(self.contacts)>=self.max:
            return 100
        elif not telefono.isdigit():
            return 200
        elif nombre in self.contacts:
            return 300
        else:
            self.contacts[nombre] = telefono
            self.date_change= datetime.now()
            return 1

    def delete(self, nombre: str):
        if nombre in self.contacts:
            del self.contacts[nombre]
            # (BUG FIX): Corregido el nombre del atributo de 'fecha_modificacion' a 'date_change'
            self.date_change = datetime.now()
            return 1
        else:
            return 400

    def edit(self, nombre: str, nuevo_telefono: str):
        # (EFICIENCIA): Se actualiza directamente el diccionario en lugar de borrar y añadir.
        if nombre in self.contacts:
            self.contacts[nombre] = nuevo_telefono
            self.date_change = datetime.now()
            return 1
        else:
            return self.add(nombre, nuevo_telefono)
    
    def import_contacts(self, route: str):
        try:
            cols = ["First Name", "Middle Name", "Last Name", "Phone 1 - Value"]
            datos = pd.read_csv(route, usecols=cols)
            datos["Full Name"] = datos["First Name"].fillna("") + " " + datos["Middle Name"].fillna("") + " " + datos["Last Name"].fillna("")
            datos["Full Name"] = datos["Full Name"].str.strip()
            for row in datos.itertuples():
                name = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', f"{row._5}")
                telf = str(row._4).strip().replace(" ", "").replace("+", "")[-8:] # Limpieza más robusta
                if name and telf:
                    self.add(name, telf)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {route}")
        except Exception as e:
            print(f"Ocurrió un error al importar los contactos: {e}")

    def export_contacts(self,csv_name: str):
        columnas = ["First Name", "Middle Name", "Last Name", "Phonetic First Name", "Phonetic Middle Name",
        "Phonetic Last Name", "Name Prefix", "Name Suffix", "Nickname", "File As",
        "Organization Name", "Organization Title", "Organization Department", "Birthday",
        "Notes", "Photo", "Labels", "E-mail 1 - Label", "E-mail 1 - Value",
        "Phone 1 - Label", "Phone 1 - Value", "Phone 2 - Label", "Phone 2 - Value"]
        df = pd.DataFrame(columns=columnas)
        df["First Name"] = list(self.contacts.keys())
        df["Phone 1 - Value"] = list(self.contacts.values())
        ruta_completa = os.path.join(self.backup_route, f"{csv_name}.csv")
        df.to_csv(ruta_completa, index=False, encoding='utf-8')
        print(f"Contactos exportados a {ruta_completa}")
   
    def backup_contacts(self):
        time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"Backup_{time_str}"
        self.export_contacts(backup_name)
        
    def show(self, n: int = 5):
        if not self.contacts:
            print("La agenda está vacía.")
            return
        df = pd.DataFrame(self.contacts.items(), columns=['Nombre', 'Telefono'])
        print(df.head(n))


"""route_test="C:\\Users\\usuario\\Downloads\\contacts.csv"
Agenda1=Agenda()
Agenda1.import_contacts(route_test)
Agenda1.show(20)
Agenda1.export_contacts("Prueba1")
Agenda1.backup_contacts()
print(Agenda1.contacts)"""

WINDOWS_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
MAC_UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/116.0"
ANDROID_UA="Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
IOS_UA="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
UA=[{"agent":WINDOWS_UA,"x_size":1380,"y_size":780},
    {"agent":MAC_UA,"x_size":1440,"y_size":900},
    {"agent":ANDROID_UA,"x_size":412,"y_size":915},
    {"agent":IOS_UA,"x_size":390,"y_size":844}]

class BootMassivo:
#NOTA: Quedò pendiente conseguir iniciar secion desde algun usuario previuamente creado (Quitar cosas innecesarias del __init__)
    
    def __init__(self,agent_code:int=0,level_random:int=5,min_delay:int=2,max_delay:int=6):
        self.is_active=True
        self.level_random=level_random
        self.min_delay=min_delay
        self.max_delay=max_delay
        self.agent=UA[agent_code]["agent"]
        self.x_size=UA[agent_code]["x_size"]
        self.y_size=UA[agent_code]["y_size"]      
        
        options = Options()
        options.add_argument(f"user-agent={self.agent}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
       
        # La ruta del perfil ya no está hardcodeada. Se crea en la carpeta del proyecto.
        profile_path = os.path.join(os.getcwd(), "AutomationProfile")
        options.add_argument(f"--user-data-dir={profile_path}")

        # Se usa ChromeDriverManager para no depender de una ruta local.
        service = Service(ChromeDriverManager().install())


        self.driver=webdriver.Chrome(options=options,service=service) 
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.set_window_size(self.x_size,self.y_size)
        
        # Se añade un "wait" explícito para hacer las búsquedas de elementos más fiables.
        self.wait = WebDriverWait(self.driver, 20)

    def tipear(self,element,string):
        for char in string:
            element.send_keys(char)
            time.sleep(random.uniform(0.1,0.25))
            if random.random() < min((self.level_random/10),0.3):
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.4))
                element.send_keys(char)


    def open_whatsapp(self):
        try:
            print("Abriendo WhatsApp Web... Por favor, escanea el código QR si es la primera vez.")
            self.driver.get("https://web.whatsapp.com")
            # Esperar a que la barra de búsqueda de chats aparezca
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Cuadro de texto para ingresar la búsqueda"]')))
            print("WhatsApp Web cargado exitosamente.")
        except TimeoutException:
            print("Error: WhatsApp Web tardó demasiado en cargar o no se pudo encontrar un elemento clave.")
            print("Asegúrate de tener una buena conexión y de que la sesión esté iniciada.")
        except Exception as e:
            print(f"Se presentó un problema inesperado al abrir WhatsApp: {e}")

    
    def open_chat(self, cell_phone, contact_name):
        try:
            url_chat = f"https://web.whatsapp.com/send?phone={cell_phone}"
            self.driver.get(url_chat)
            # Se espera a que la caja de texto del chat esté disponible para confirmar que se abrió el chat.
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Escribe un mensaje"]')))
            print(f"Chat abierto con {contact_name} ({cell_phone})")
            return True
        except TimeoutException:
            print(f"No se pudo abrir el chat con {contact_name} ({cell_phone}). Es posible que el número sea incorrecto o no tenga WhatsApp.")
            return False
        except Exception as e:
            print(f"Error inesperado al abrir el chat: {e}")
            return False

    def send_text(self,text):
        try:
            # Selector más firme y uso de WebDriverWait.
            caja_mensaje = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Escribe un mensaje"]')))
            caja_mensaje.click()
            self.tipear(caja_mensaje, text)
            caja_mensaje.send_keys(Keys.ENTER)
            print(f"Mensaje enviado: '{text[:30]}...'")
            time.sleep(random.uniform(self.min_delay, self.max_delay))
            return True
        except Exception as e:
            print(f"Error al cargar el mensaje de texto: {e}")
            return False
        
    def send_picture(self,route,legend=""):
        try:
            if not os.path.exists(route):
                print(f"Error: La imagen no existe en la ruta: {route}")
                return False
            print(1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Adjuntar"]'))).click()
            print(2)
            input_archivo = self.driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            print(3)
            ruta_absoluta = os.path.abspath(route)
            print(4)
            input_archivo.send_keys(ruta_absoluta)
            print(5)
            boton_enviar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Enviar"]')))
            print(6)
            if legend:
                caja_caption = self.driver.find_element(By.XPATH, '//div[@aria-label="Añade un comentario"]')
                self.tipear(caja_caption, legend)
            boton_enviar.click()
            print(f"Imagen '{route}' enviada con éxito.")
            time.sleep(random.uniform(self.min_delay, self.max_delay))
            return True

        except Exception as e:
            print(f"Error al enviar la imagen: {e}")
            return False

    def quit(self):
        print("Cerrando el navegador.")
        self.driver.quit()


Armando=BootMassivo()
Armando.open_whatsapp()
Armando.open_chat(cell_phone="59170483000",contact_name="")

#Armando.send_picture("C:\\Users\\usuario\\Downloads\\photo1.jpg","Mensaje de prueba nmro 312")
Armando.send_text("""Perfil Requerido:
* Estudiantes de últimos semestres o egresados recientes de las carreras de:
 Ingeniería Mecánica, Electromecánica, Ingeniería Industrial.
•  Conocimientos básicos en mantenimiento preventivo y correctivo de maquinaria industrial.
•  Capacidad de trabajo en equipo y disposición para aprender.
•  Responsabilidad, puntualidad y proactividad.
📍 Lugar de trabajo
Unidades Productivas de AGRIPAC.
📅 Duración de la pasantía: 6 meses.
🎯 Ofrecemos 
* Oportunidad de aprendizaje en un entorno industrial real.
•  Acompañamiento y tutoría por parte de profesionales del área.
•  Certificado de pasantía al finalizar el período.
📩 Postulación
Interesados/as deben enviar su postulación al siguiente QR 
Pasantía Mantenimiento Industrial.""")

time.sleep(3600)
