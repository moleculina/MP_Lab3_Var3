import tkinter as tk
from tkinter import messagebox, simpledialog

class CalculatorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller  # может быть None
        self.root.title("Расширенный калькулятор")
        self.root.geometry("500x600")
        self.root.resizable(True, True)

        # Переменная для отображения ввода
        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar()

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Показать историю", command=self.show_history_wrapper)
        file_menu.add_command(label="Очистить историю", command=self.clear_history_wrapper)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def show_history_wrapper(self):
        """Обёртка для вызова show_history у контроллера"""
        if self.controller:
            self.controller.show_history()
        else:
            self.show_info("Контроллер ещё не инициализирован")

    def clear_history_wrapper(self):
        """Обёртка для вызова clear_history у контроллера"""
        if self.controller:
            self.controller.clear_history()
        else:
            self.show_info("Контроллер ещё не инициализирован")

    def create_widgets(self):
        # Поле ввода выражения
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Выражение:").pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(entry_frame, textvariable=self.expression_var, width=40, font=("Arial", 12))
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind('<Return>', lambda event: self.calculate_wrapper())
        entry.focus()

        # Поле результата
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=5)
        tk.Label(result_frame, text="Результат:").pack(side=tk.LEFT, padx=5)
        tk.Label(result_frame, textvariable=self.result_var, relief=tk.SUNKEN,
                 width=30, anchor=tk.W, bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

        # Кнопка "Вычислить"
        tk.Button(self.root, text="Вычислить", command=self.calculate_wrapper,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # Кнопки калькулятора
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        buttons = [
            '7', '8', '9', '/', 'sin(', 'cos(',
            '4', '5', '6', '*', 'tan(', 'sqrt(',
            '1', '2', '3', '-', 'log(', 'ln(',
            '0', '.', '(', ')', '^', 'pi',
            'C', 'CE', '←'
        ]

        row, col = 0, 0
        for btn in buttons:
            cmd = lambda x=btn: self.button_click_wrapper(x)
            tk.Button(buttons_frame, text=btn, width=5, height=2,
                      command=cmd).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 5:
                col = 0
                row += 1

        # История (текстовое поле)
        tk.Label(self.root, text="История вычислений:").pack(pady=(10,0))
        self.history_text = tk.Text(self.root, height=8, state=tk.DISABLED, wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def calculate_wrapper(self):
        """Обёртка для вызова calculate у контроллера"""
        if self.controller:
            self.controller.calculate()
        else:
            self.show_error("Контроллер не инициализирован")

    def button_click_wrapper(self, button):
        """Обёртка для вызова on_button_click у контроллера"""
        if self.controller:
            self.controller.on_button_click(button)
        else:
            # Временно:直接在界面中添加字符
            current = self.get_expression()
            if button == 'C':
                self.set_expression("")
            elif button == 'CE':
                self.set_expression("")
                self.set_result("")
            elif button == '←':
                self.set_expression(current[:-1])
            else:
                self.set_expression(current + button)

    def update_history_display(self, history):
        """Обновляет отображение истории"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for entry in history:
            self.history_text.insert(tk.END, entry.get("formatted", f"{entry['expression']} = {entry['result']}") + "\n")
        self.history_text.config(state=tk.DISABLED)

    def get_expression(self):
        return self.expression_var.get()

    def set_result(self, result):
        self.result_var.set(str(result))

    def set_expression(self, expr):
        self.expression_var.set(expr)

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)

    def show_info(self, message):
        messagebox.showinfo("Информация", message)

    def show_about(self):
        self.show_info("Расширенный калькулятор\nВариант №3\nПоддерживает: + - * / ^ sin cos tan sqrt log ln ( ) pi e")