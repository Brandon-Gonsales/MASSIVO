import tkinter as tk

class MiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Massivo")
        ancho_v = 300
        alto_v = self.winfo_screenheight()
        ancho_p = self.winfo_screenwidth()

        x = ancho_p - ancho_v
        y = 0

        self.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.show_title()
        self.show_first()

    def show_title(self):
        self.frame_title = tk.Frame(self)
        self.frame_title.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=10)

        self.frame_title.grid_columnconfigure(0, weight=1)
        self.frame_title.grid_rowconfigure(0, weight=1)
        self.frame_title.grid_rowconfigure(1, weight=1)

        self.l1 = tk.Label(self.frame_title, text="MASSIVO", font=("Arial", 14, "bold"))
        self.l1.grid(row=0, column=0, pady=(0,5))
        
        self.l2 = tk.Label(self.frame_title, text="by: Datahub Group", font=("Arial", 10))
        self.l2.grid(row=1, column=0)

    def show_first(self):
        self.frame_body = tk.Frame(self)
        self.frame_body.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10, padx=10)
        
        self.frame_body.grid_columnconfigure(0, weight=1)
        self.frame_body.grid_columnconfigure(1, weight=0)
        
        self.lbl_titulo = tk.Label(self.frame_body, text="Destinatarios:", font=("Arial", 12))
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=0, sticky="w")
        
        text_frame = tk.Frame(self.frame_body,bd=1,relief="solid",highlightbackground="gray",highlightthickness=1)
        text_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        self.txt_entrada = tk.Text(text_frame,height=10,bd=0,highlightthickness=0)
        self.txt_entrada.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        self.frame_botones = tk.Frame(self.frame_body)
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.btn_guardar = tk.Button(self.frame_botones, text="Editar", width=10)
        self.btn_guardar.grid(row=0, column=0, padx=5)
        
        self.btn_limpiar = tk.Button(self.frame_botones, text="Borrar", width=10)
        self.btn_limpiar.grid(row=0, column=1, padx=5)


if __name__ == "__main__":
    app = MiApp()
    app.mainloop()