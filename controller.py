import math

class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self  # обратная связь

        # Загружаем историю при старте
        self.view.update_history_display(self.model.history)

    def calculate(self):
        expr = self.view.get_expression()
        if not expr.strip():
            self.view.show_error("Введите выражение")
            return

        try:
            result = self.model.evaluate(expr)
            self.view.set_result(result)
            self.model.add_to_history(expr, result)
            self.view.update_history_display(self.model.history)
        except ValueError as e:
            self.view.show_error(str(e))

    def on_button_click(self, button):
        current = self.view.get_expression()
        if button == 'C':
            self.view.set_expression("")
        elif button == 'CE':
            self.view.set_expression("")
            self.view.set_result("")
        elif button == '←':
            self.view.set_expression(current[:-1])
        else:
            self.view.set_expression(current + button)

    def show_history(self):
        if not self.model.history:
            self.view.show_info("История пуста")
        else:
            history_str = "\n".join([h["formatted"] for h in self.model.history])
            self.view.show_info(f"История:\n{history_str}")

    def clear_history(self):
        self.model.clear_history()
        self.view.update_history_display(self.model.history)
        self.view.show_info("История очищена")