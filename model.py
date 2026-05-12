import json
import math
import os

class CalculatorModel:
    def __init__(self, history_file="history.json"):
        self.history_file = history_file
        self.history = self.load_history()

    def evaluate(self, expression):
        """Вычисляет математическое выражение"""
        try:
            # Заменяем ^ на ** для степени
            expression = expression.replace('^', '**')
            # Добавляем поддержку математических функций
            result = eval(expression, {"__builtins__": None}, {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "pi": math.pi,
                "e": math.e
            })
            return result
        except Exception as e:
            raise ValueError("Ошибка в выражении")

    def add_to_history(self, expression, result):
        """Добавляет запись в историю"""
        self.history.append({
            "expression": expression,
            "result": str(result),
            "formatted": f"{expression} = {result}"
        })
        self.save_history()

    def load_history(self):
        """Загружает историю из JSON"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self):
        """Сохраняет историю в JSON"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def clear_history(self):
        """Очищает историю"""
        self.history = []
        self.save_history()