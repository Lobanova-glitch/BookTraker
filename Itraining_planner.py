import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

FAVORITES_FILE = 'favorites.json'


class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")

        # Поиск
        self.search_label = tk.Label(root, text="Введите имя пользователя GitHub:")
        self.search_label.pack()

        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Поиск", command=self.search_user)
        self.search_button.pack()

        # Результаты поиска
        self.results_list = tk.Listbox(root, width=80, height=10)
        self.results_list.pack()

        # Кнопка добавить в избранное
        self.add_fav_button = tk.Button(root, text="Добавить в избранное", command=self.add_to_favorites)
        self.add_fav_button.pack()

        # Загрузка избранных
        self.favorites = self.load_favorites()

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_favorites(self):
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(self.favorites, f, indent=4)

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
            return
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            self.results_list.delete(0, tk.END)
            display_text = f"{user_data['login']} - {user_data.get('name', 'Нет имени')}"
            self.results_list.insert(tk.END, display_text)
            # Можно сохранять полный словарь пользователя для добавления
            self.current_user = user_data
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def add_to_favorites(self):
        if hasattr(self, 'current_user'):
            if self.current_user not in self.favorites:
                self.favorites.append(self.current_user)
                self.save_favorites()
                messagebox.showinfo("Успех", "Пользователь добавлен в избранное")
            else:
                messagebox.showinfo("Информация", "Пользователь уже в избранных")
        else:
            messagebox.showwarning("Предупреждение", "Нет выбранного пользователя для добавления")


if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()