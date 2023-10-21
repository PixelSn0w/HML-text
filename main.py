import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile

class HackmeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("HML Text")
        self.root.geometry("600x400")  # Set the initial size of the main window

        self.app_list = []

        self.create_ui()

    def create_ui(self):
        # Application Listbox
        self.app_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.app_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Import Button
        import_button = tk.Button(self.root, text="Import HML", command=self.import_hml)
        import_button.pack(pady=5)

        # View Button
        view_button = tk.Button(self.root, text="View", command=self.view_content)
        view_button.pack(pady=5)

    def import_hml(self):
        hml_file = filedialog.askopenfilename(filetypes=[("HML files", "*.hml")])

        if hml_file:
            # Extract title and content from the HML file
            try:
                with zipfile.ZipFile(hml_file, 'r') as zip_ref:
                    title = zip_ref.read('title.txt').decode('utf-8')
                    content = zip_ref.read('content.txt').decode('utf-8') if 'content.txt' in zip_ref.namelist() else None

                # Add the app to the list
                self.app_list.append({"name": title, "content": content})
                self.refresh_listbox()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to import HML file: {e}")

    def view_content(self):
        selected_index = self.app_listbox.curselection()

        if not selected_index:
            messagebox.showinfo("HML Text", "Please select an application to view.")
            return

        selected_app = self.app_list[selected_index[0]]

        try:
            # Display content in a new window
            content_window = tk.Toplevel(self.root)
            content_window.title(selected_app['name'])
            content_window.geometry("500x500")

            content_label = tk.Label(content_window, text=selected_app['content'])
            content_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to view application: {e}")

    def refresh_listbox(self):
        self.app_listbox.delete(0, tk.END)
        for app in self.app_list:
            self.app_listbox.insert(tk.END, app["name"])

if __name__ == "__main__":
    root = tk.Tk()
    app = HackmeLauncher(root)
    root.mainloop()
