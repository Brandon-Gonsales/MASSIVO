# 🤖 Massivo
Este proyecto es un bot de automatización desarrollado en Python con Selenium, diseñado para enviar mensajes masivos de texto e imágenes a través de WhatsApp Web. Incluye técnicas para simular el comportamiento humano y evitar la detección, así como un sistema de gestión de contactos a partir de archivos CSV.
## Características Principales
* Gestión de contactos (agregar, editar, eliminar)
* Importación desde archivos CSV (formato compatible con Google Contacts)
* Sistema automático de backups
* Validación de datos (números de teléfono, duplicados, etc.)
* Simulación de comportamiento humano (tiempo de escritura, errores aleatorios)
* Simulaciòn de diferentes agentes de usuario (Windows, Mac, Android, iOS)
* Envío de mensajes de texto con formato, emoticones y saltos de linea
* Delays aleatorios entre acciones para parecer humano
## Requisitos del sistema
* Python 3.7+
* Google Chrome instalado
* Conexión a internet
## Instalación
1. Clonar el repositorio o descargar los archivos
2. Instalar las dependencias:

<code>pip install pandas selenium webdriver-manager</code>

3. Para usar WhatsApp Web, necesitarás escanear el código QR la primera vez


## Clase Agenda
Una herramienta para gestionar contactos con capacidad de importar/exportar desde archivos CSV y realizar backups.
### Constructor __init__
**max (int, opcional=100):** Número máximo de contactos permitidos  
**backup_route (str, opcional="backup"):** Ruta para guardar backups  
### Métodos:
### add(nombre: str, telefono: str) -> int
Añade un nuevo contacto 

**Retornos:**  
- 1: Éxito  
- 100: Agenda llena  
- 200: Teléfono no válido  
- 300: Contacto ya existe  

### delete(nombre: str) -> int
Elimina un contacto existente  

**Retornos:**  
- 1: Éxito
- 400: Contacto no encontrado

### edit(nombre: str, nuevo_telefono: str) -> int
Modifica el teléfono de un contacto  
Si el contacto no existe, lo añade  
Retorna los mismos códigos que add()  

### import_contacts(route: str) -> None
Importa contactos desde archivo CSV (formato Google Contacts)  
Maneja nombres compuestos y limpia formatos de teléfono  

### export_contacts(csv_name: str) -> None
Exporta contactos a CSV compatible con Google Contacts    
Guarda en la ruta de backup especificada  

### backup_contacts() -> None
Crea backup automático con marca de tiempo    
Usa internamente export_contacts()  

### show(n: int = 5) -> None
Muestra los primeros N contactos en formato tabular   
Por defecto muestra 5 contactos  

## Clase BootMassivo
Un sistema automatizado para enviar mensajes y multimedia a través de WhatsApp Web con comportamiento humano simulado.  
### Constructor __init__
**agent_code (int, opcional=0):** Código del user-agent a usar:  
  - 0: Windows
  - 1: Mac
  - 2: Android
  - 3: iOS  

**level_random (int, opcional=5):** Nivel de aleatoriedad al tipear (0-5)  
**min_delay (int, opcional=2):** Delay mínimo entre acciones (segundos)  
**max_delay (int, opcional=6):** Delay máximo entre acciones (segundos)  

### Métodos:
### tipear_renglon(element, text)
Simula escritura humana con posibles errores aleatorios   
**element:** Objeto Selenium del campo de texto  
**text (str):** Texto a escribir  

### tipear_renglones(element, vector)
Escribe múltiples líneas con saltos  
**element:** Objeto Selenium del campo de texto  
**vector (list[str]):** Lista de líneas a escribir  

### open_whatsapp() -> None
Abre WhatsApp Web y espera login manual (QR)   

### open_chat(cell_phone: str, contact_name: str) -> bool
Abre chat con un contacto específico  
**cell_phone:** Número en formato internacional sin espacios  
**contact_name:** Nombre para propósitos de logging  

*Retorna True si tuvo éxito*  

### send_text(text) -> bool
Envía mensaje de texto      
**Text (list[str]):** Mensaje a enviar  

*Retorna True si tuvo éxito*    

### send_picture(route: str, legend: list = []) -> bool
Envía imagen con leyenda opcional   
**route:** Ruta local de la imagen  
**legend:** Texto opcional para la imagen  

*Retorna True si tuvo éxito*  

### quit() -> None
Cierra el navegador y finaliza la sesión  