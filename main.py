import tkinter as tk
from Forms.Interfaz import InterfazConsultaRut, EstiloTkinter

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # Crear una instancia de EstiloTkinter
        estilo = EstiloTkinter()
        
        # Pasar la instancia de EstiloTkinter al constructor de InterfazConsultaRut
        self.app = InterfazConsultaRut(self.root, estilo)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()