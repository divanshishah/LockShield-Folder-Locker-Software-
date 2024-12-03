import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, font

class FolderLockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Locker Application")
        self.root.geometry("800x400")  # Set window size
        self.folder_path = ''
        self.padding = {'padx': 10, 'pady': 10}
        self.create_widgets()

    def create_widgets(self):
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        label_font = font.Font(family="Helvetica", size=14)
        button_font = font.Font(family="Helvetica", size=10, weight="bold")

        # Title label
        tk.Label(self.root, text="Folder Locker Application", font=title_font).grid(row=0, column=0, columnspan=3, **self.padding)

        # Separator line
        tk.Label(self.root, text="="*50).grid(row=1, column=0, columnspan=3, **self.padding)

        # Folder path entry and label
        tk.Label(self.root, text="Folder Path:", font=label_font).grid(row=2, column=0, sticky=tk.E, **self.padding)
        self.folder_entry = tk.Entry(self.root, width=50, font=label_font)
        self.folder_entry.grid(row=2, column=1, **self.padding)

        # Browse button
        browse_button = tk.Button(self.root, text="Browse", command=self.browse_folder, font=button_font)
        browse_button.grid(row=2, column=2, **self.padding)

        # Lock Button
        lock_button = tk.Button(self.root, text="Lock Folder", command=self.lock_folder_action, font=button_font, bg='lightcoral')
        lock_button.grid(row=3, column=0, **self.padding)

        #unlock button
        unlock_button = tk.Button(self.root, text="Unlock Folder", command=self.unlock_folder_action, font=button_font, bg='lightgreen')
        unlock_button.grid(row=3, column=1, **self.padding)

        # Message label
        self.message_label = tk.Label(self.root, text="", font=label_font)
        self.message_label.grid(row=4, column=0, columnspan=3, **self.padding)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, self.folder_path)

    def lock_folder_action(self):
        self.folder_path = self.folder_entry.get()
        password = simpledialog.askstring("Password", "Enter a password to lock the folder:", show='*')
        if self.folder_path and password:
            if self.lock_folder(self.folder_path, password):
                self.message_label.config(text="Folder locked successfully!", fg='green')
            else:
                self.message_label.config(text="Failed to lock the folder. Please try again.", fg='red')
        else:
            self.message_label.config(text="Invalid folder path or password.", fg='red')

    def unlock_folder_action(self):
        self.folder_path = self.folder_entry.get()
        password = simpledialog.askstring("Password", "Enter the password to unlock the folder:", show='*')
        if self.folder_path and password:
            if self.unlock_folder(self.folder_path, password):
                self.message_label.config(text="Folder unlocked successfully!", fg='green')
            else:
                self.message_label.config(text="Failed to unlock the folder. Please try again.", fg='red')
        else:
            self.message_label.config(text="Invalid folder path or password.", fg='red')

    def lock_folder(self, folder_path, password):
        try:
            temp_folder = folder_path + "_temp"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                    encrypted_content = self.encrypt(file_content, password)
                    new_file_path = os.path.join(temp_folder, os.path.relpath(file_path, folder_path))
                    new_file_dir = os.path.dirname(new_file_path)
                    if not os.path.exists(new_file_dir):
                        os.makedirs(new_file_dir)
                    with open(new_file_path, 'wb') as f:
                        f.write(encrypted_content)
            shutil.rmtree(folder_path)
            os.rename(temp_folder, folder_path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def unlock_folder(self, folder_path, password):
        try:
            temp_folder = folder_path + "_temp"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                    decrypted_content = self.decrypt(file_content, password)
                    new_file_path = os.path.join(temp_folder, os.path.relpath(file_path, folder_path))
                    new_file_dir = os.path.dirname(new_file_path)
                    if not os.path.exists(new_file_dir):
                        os.makedirs(new_file_dir)
                    with open(new_file_path, 'wb') as f:
                        f.write(decrypted_content)
            shutil.rmtree(folder_path)
            os.rename(temp_folder, folder_path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def encrypt(self, data, password):
        password_int = sum([ord(char) for char in password]) % 256
        return bytes([(byte + password_int) % 256 for byte in data])

    def decrypt(self, data, password):
        password_int = sum([ord(char) for char in password]) % 256
        return bytes([(byte - password_int) % 256 for byte in data])

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderLockerApp(root)
    root.mainloop()
