import tkinter as tk
from model import CalculatorModel
from view import CalculatorView
from controller import CalculatorController

def main():
    root = tk.Tk()
    model = CalculatorModel()
    view = CalculatorView(root, None)  # временно None
    controller = CalculatorController(model, view)
    view.controller = controller  # связываем

    root.mainloop()

if __name__ == "__main__":
    main()