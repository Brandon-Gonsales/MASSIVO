import tkinter as tk
from tkinter import messagebox,filedialog
from backend.clases import BootMassivo,Agenda

import tkinter as tk

# Función para mostrar la ventana de configuración
def show_config():
    global entry1,entry2,entry3,config_window
    config_window = tk.Toplevel(root)
    config_window.title("Configuración Boot")
    
    # Mismo ancho y posición X que la ventana principal
    ancho_v = 300  # Mismo ancho que la ventana principal
    alto_v = 200   # Altura fija para la ventana de configuración (ajusta según necesites)
    x = root.winfo_x()  # Misma posición X que la ventana principal
    y = 100             # Posición Y fija desde el borde superior
    
    config_window.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
    config_window.transient(root) 
    config_window.grab_set()

    config_frame = tk.Frame(config_window, padx=20, pady=20)
    config_frame.pack(fill="both", expand=True)
    config_frame.grid_columnconfigure(1, weight=1)

    # Campos de configuración
    tk.Label(config_frame, text="Nivel Random [1,2,3]:").grid(row=0, column=0, sticky="w", pady=5)
    entry1 = tk.Entry(config_frame, width=30)
    entry1.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    tk.Label(config_frame, text="Delay Mínimo:").grid(row=1, column=0, sticky="w", pady=5)
    entry2 = tk.Entry(config_frame, width=30)
    entry2.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

    tk.Label(config_frame, text="Delay Máximo:").grid(row=2, column=0, sticky="w", pady=5)
    entry3 = tk.Entry(config_frame, width=30)
    entry3.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

    btn_send_config = tk.Button(
        config_frame,
        text="Guardar Configuración",
        bg="#000000", fg="#ffffff",font=("Arial", 16, "bold"),
        command=init_boot)
    btn_send_config.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

def leer_text_contacts():
    contenido = contacts_text.get("1.0", "end-1c")
    lineas = contenido.split('\n') 
    vec = []
    for linea in lineas:
        linea = linea.strip() 
        if linea:  
            datos = linea.split(',', 1)  
            datos = [dato.strip() for dato in datos]
            if len(datos) == 2:
                vec.append(datos)
    return vec

def anadir():
    global agenda
    vec=leer_text_contacts()
    for ele in vec:
        agenda.add(nombre=ele[0],telefono=ele[1])

def exportar():
    global agenda
    agenda.export_contacts("contactos")

def importar():
    global ruta_csv
    
    ruta_csv = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    if ruta_csv:
        agenda.import_contacts(ruta_csv)
        actualizar_text()

def importar_img():
    global ruta_img
    
    ruta_img = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),  # Formatos de imagen comunes
            ("Todos los archivos", "*.*")
        ]
    )
    
    if ruta_img:
        rutita=ruta_img.split(r'/')
        img_titulo.config(text=rutita[-1])


def actualizar_text():
    diccionario=agenda.contacts
    contacts_text.delete("1.0", tk.END)
    for nombre, telefono in diccionario.items():
        linea = f"{nombre}, {telefono}\n"
        contacts_text.insert(tk.END, linea)
def clean():
    global agenda
    agenda.contacts={}
    actualizar_text()

def clean_msj():
    global msj
    msj_text.delete("1.0", tk.END)
    msj=[]
    print(msj)

def guardar_msj():
    global msj
    contenido = msj_text.get("1.0", "end-1c")
    lineas = contenido.split('\n') 
    msj=lineas
    print(msj)

agenda=Agenda(1000000) #Un milón
ruta_img=""
def init_boot():
    global boot,agenda

    try: 
        level_random=int(entry1.get())
        min_delay=int(entry2.get())
        max_delay=int(entry3.get())
        boot=BootMassivo(level_random=level_random,min_delay=min_delay,max_delay=max_delay)
        print("Boot iniciado exitosamente con los valores introducidos")
    except:
        boot=BootMassivo()
        print("Boot iniciado fozosamente con valores predeterminados")
    config_window.destroy()
def go():
    boot.open_whatsapp()
    if ruta_img and msj and agenda.contacts and boot: 
        for key, valor in agenda.contacts.items():
            boot.open_chat(cell_phone=valor,contact_name=key)
            boot.send_picture(route=ruta_img,legend=msj)
    elif msj and agenda.contacts and boot:
        for key, valor in agenda.contacts.items():
            boot.open_chat(cell_phone=valor,contact_name=key)
            boot.send_text(msj)

# raiz
root = tk.Tk()
root.title("Massivo")
ancho_v = 300
alto_v = root.winfo_screenheight()
ancho_p = root.winfo_screenwidth()
x = ancho_p - ancho_v
y = 0
root.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Frame para el título
frame_title = tk.Frame(root)
frame_title.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=10)
frame_title.grid_columnconfigure(0, weight=1)
frame_title.grid_rowconfigure(0, weight=1)
frame_title.grid_rowconfigure(1, weight=1)
l1 = tk.Label(frame_title, text="MASSIVO", font=("Arial", 30, "bold"))
l1.grid(row=0, column=0, pady=(5,0))
l2 = tk.Label(frame_title, text="____by: Datahub Group____", font=("Arial", 12,"italic"))
l2.grid(row=1, column=0, pady=(0,5))


# Boton config sin frame
btn_config = tk.Button(root, text="Configuración Inicial", width=10, bg="#000000",fg="#ffffff", font=("Arial", 16, "bold"), command=show_config)
btn_config.grid(row=1, column=0, columnspan=2, pady=0, sticky="ew",padx=10)



# seccion de destinatarios contactos
contacts_frame = tk.Frame(root, padx=20, pady=20)
contacts_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
contacts_frame.grid_columnconfigure(0, weight=1)
contacts_frame.grid_rowconfigure(1, weight=1) 

contact_titulo = tk.Label(contacts_frame, text="Destinatarios:", font=("Arial", 12))
contact_titulo.grid(row=0, column=0, columnspan=2, pady=0, sticky="w")

text_frame = tk.Frame(contacts_frame, bd=2, relief="sunken")
text_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 10))
text_frame.grid_columnconfigure(0, weight=1)
text_frame.grid_rowconfigure(0, weight=1)

text_scroll = tk.Scrollbar(text_frame)
text_scroll.grid(row=0, column=1, sticky="ns")

contacts_text = tk.Text(
    text_frame, 
    height=10, 
    wrap="word", 
    yscrollcommand=text_scroll.set,
    padx=5,
    pady=5
)
contacts_text.grid(row=0, column=0, sticky="nsew")
text_scroll.config(command=contacts_text.yview)

btn_add = tk.Button(
    contacts_frame,
    text="Añadir Contacto",
    bg="#000000",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    comman=anadir
)
btn_add.grid(row=2, column=0, pady=(0, 10), sticky="ew")

buttons_frame = tk.Frame(contacts_frame)
buttons_frame.grid(row=3, column=0, sticky="ew")
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)

btn_import = tk.Button(
    buttons_frame,
    text="Importar CSV",
    bg="#000000",  
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    command=importar
)
btn_import.grid(row=0, column=0, padx=(0, 5), sticky="ew")

btn_export = tk.Button(
    buttons_frame,
    text="Exportar CSV",
    bg="#000000",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    command=exportar
)
btn_export.grid(row=0, column=1, padx=(5, 0), sticky="ew")


btn_clean = tk.Button(
    contacts_frame,
    text="Reset",
    bg="#01a863",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    comman=clean
)
btn_clean.grid(row=4, column=0, pady=(5, 0), sticky="ew")

#seccion de mensaje
msj_frame = tk.Frame(root, padx=20, pady=5)
msj_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
msj_frame.grid_columnconfigure(0, weight=1)
msj_frame.grid_rowconfigure(1, weight=1) 

msj_frame_titulo = tk.Label(msj_frame, text="Campaña:", font=("Arial", 12))
msj_frame_titulo.grid(row=0, column=0, columnspan=2, pady=0, sticky="w")

text_frame2 = tk.Frame(msj_frame, bd=2, relief="sunken")
text_frame2.grid(row=1, column=0, sticky="nsew", pady=(5, 10))
text_frame2.grid_columnconfigure(0, weight=1)
text_frame2.grid_rowconfigure(0, weight=1)

text_scroll2 = tk.Scrollbar(text_frame2)
text_scroll2.grid(row=0, column=1, sticky="ns")

msj_text = tk.Text(
    text_frame2, 
    height=10, 
    wrap="word", 
    yscrollcommand=text_scroll2.set,
    padx=5,
    pady=5
)
msj_text.grid(row=0, column=0, sticky="nsew")
text_scroll2.config(command=msj_text.yview)

buttons_frame2 = tk.Frame(msj_frame)
buttons_frame2.grid(row=2, column=0, sticky="ew")
buttons_frame2.grid_columnconfigure(0, weight=1)
buttons_frame2.grid_columnconfigure(1, weight=1)

btn_set = tk.Button(
    buttons_frame2,
    text="Guardar",
    bg="#000000",  
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    command=guardar_msj
)
btn_set.grid(row=0, column=0, padx=(0, 5), sticky="ew")

btn_clean2 = tk.Button(
    buttons_frame2,
    text="Reset",
    bg="#01a863",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    command=clean_msj
)
btn_clean2.grid(row=0, column=1, padx=(5, 0), sticky="ew")

# Boton config sin frame
btn_config = tk.Button(root, text="INICIAR CAMPAÑA", width=10, bg="#81edbe",fg="#ffffff", font=("Arial", 15, "bold"), command=go ,height=2)
btn_config.grid(row=4, column=0, columnspan=2, pady=0, sticky="ew",padx=20)

#seccion de otras
otro_frame = tk.Frame(root, padx=20, pady=50)
otro_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
otro_frame.grid_columnconfigure(0, weight=1)
otro_frame.grid_rowconfigure(1, weight=1) 

otro_frame_titulo = tk.Label(otro_frame, text="Otras funciones:", font=("Arial", 12))
otro_frame_titulo.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

buttons_frame3 = tk.Frame(otro_frame)
buttons_frame3.grid(row=1, column=0, sticky="ew")
buttons_frame3.grid_columnconfigure(0, weight=1)
buttons_frame3.grid_columnconfigure(1, weight=1)

img_import = tk.Button(
    buttons_frame3,
    text="Imagen",
    bg="#000000",  
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
    command=importar_img
)
img_import.grid(row=0, column=0, padx=(0, 5), sticky="ew")

img_titulo = tk.Label(buttons_frame3, text="", font=("Arial", 12))
img_titulo.grid(row=0, column=1, pady=5, sticky="w")

# Ejecutar la aplicación
root.mainloop()

