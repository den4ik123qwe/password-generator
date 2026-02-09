import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей v2.0")
        self.root.geometry("500x500")
        
        # Настройки
        self.settings_file = "passgen_settings.json"
        self.settings = self.load_settings()
        
        # Переменные
        self.password_var = tk.StringVar()
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="ГЕНЕРАТОР ПАРОЛЕЙ", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Фрейм режимов
        mode_frame = ttk.LabelFrame(main_frame, text="Режим генерации", padding="10")
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.mode_var = tk.StringVar(value="auto")
        ttk.Radiobutton(mode_frame, text="Автоматический", variable=self.mode_var, 
                       value="auto", command=self.toggle_mode).pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Ручной", variable=self.mode_var, 
                       value="manual", command=self.toggle_mode).pack(anchor=tk.W)
        
        # Фрейм параметров (автоматический режим)
        self.auto_frame = ttk.LabelFrame(main_frame, text="Параметры", padding="10")
        
        # Длина пароля
        length_frame = ttk.Frame(self.auto_frame)
        length_frame.pack(fill=tk.X, pady=5)
        ttk.Label(length_frame, text="Длина пароля:").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=12)
        ttk.Spinbox(length_frame, from_=4, to=32, textvariable=self.length_var, 
                   width=10).pack(side=tk.LEFT, padx=10)
        
        # Настройки символов
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.auto_frame, text="Заглавные буквы (A-Z)", 
                       variable=self.use_upper).pack(anchor=tk.W)
        ttk.Checkbutton(self.auto_frame, text="Строчные буквы (a-z)", 
                       variable=self.use_lower).pack(anchor=tk.W)
        ttk.Checkbutton(self.auto_frame, text="Цифры (0-9)", 
                       variable=self.use_digits).pack(anchor=tk.W)
        ttk.Checkbutton(self.auto_frame, text="Спецсимволы (!@#$%)", 
                       variable=self.use_special).pack(anchor=tk.W)
        
        # Фрейм ручного ввода
        self.manual_frame = ttk.LabelFrame(main_frame, text="Ручной ввод", padding="10")
        
        ttk.Label(self.manual_frame, text="Основа пароля:").pack(anchor=tk.W)
        self.base_word_var = tk.StringVar()
        ttk.Entry(self.manual_frame, textvariable=self.base_word_var, 
                 width=30).pack(fill=tk.X, pady=5)
        
        # Кнопка генерации
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Сгенерировать пароль", 
                  command=self.generate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Копировать", 
                  command=self.copy_password).pack(side=tk.LEFT, padx=5)
        
        # Результат
        result_frame = ttk.LabelFrame(main_frame, text="Результат", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(result_frame, height=6, width=50, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Инициализация
        self.toggle_mode()
        
    def toggle_mode(self):
        if self.mode_var.get() == "auto":
            self.auto_frame.pack(fill=tk.X, pady=5)
            self.manual_frame.pack_forget()
        else:
            self.auto_frame.pack_forget()
            self.manual_frame.pack(fill=tk.X, pady=5)
    
    def generate_password(self):
        if self.mode_var.get() == "auto":
            password = self.generate_auto_password()
        else:
            password = self.generate_manual_password()
        
        self.display_result(password)
    
    def generate_auto_password(self):
        # Собираем набор символов
        chars = ''
        if self.use_lower.get():
            chars += string.ascii_lowercase
        if self.use_upper.get():
            chars += string.ascii_uppercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_special.get():
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return ""
        
        # Генерируем пароль
        length = self.length_var.get()
        password = ''.join(random.choice(chars) for _ in range(length))
        
        return password
    
    def generate_manual_password(self):
        base = self.base_word_var.get()
        if not base:
            messagebox.showwarning("Ошибка", "Введите основу пароля!")
            return ""
        
        # Простые преобразования
        variations = []
        variations.append(base.title() + str(random.randint(10, 99)) + "!")
        variations.append(base.upper() + "#" + str(random.randint(100, 999)))
        variations.append(str(random.randint(1, 9)) + base + "@" + str(random.randint(1, 9)))
        variations.append(base + "^" + base[::-1])
        
        return "\n".join(variations)
    
    def display_result(self, password):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, password)
        
        # Простая оценка сложности
        self.evaluate_password(password.split('\n')[0] if '\n' in password else password)
    
    def evaluate_password(self, password):
        # Простой анализ
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        score = 0
        if length >= 8: score += 1
        if length >= 12: score += 1
        if has_upper: score += 1
        if has_lower: score += 1
        if has_digit: score += 1
        if has_special: score += 1
        
        if score <= 2:
            strength = "Очень слабый"
            color = "red"
        elif score <= 4:
            strength = "Средний"
            color = "orange"
        else:
            strength = "Сильный"
            color = "green"
        
        # Добавляем оценку
        self.result_text.insert(tk.END, f"\n\nОценка: {strength}")
        self.result_text.tag_add("strength", "end-2l", "end-1l")
        self.result_text.tag_config("strength", foreground=color, font=('Arial', 10, 'bold'))
    
    def copy_password(self):
        password = self.result_text.get(1.0, "end-1c").split('\n\n')[0]
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
            except:
                messagebox.showerror("Ошибка", "Не удалось скопировать в буфер обмена")
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_settings(self):
        settings = {
            "mode": self.mode_var.get(),
            "length": self.length_var.get(),
            "use_upper": self.use_upper.get(),
            "use_lower": self.use_lower.get(),
            "use_digits": self.use_digits.get(),
            "use_special": self.use_special.get()
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except:
            pass

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    
    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()