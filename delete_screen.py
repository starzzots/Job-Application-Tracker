import tkinter as tk
from tkinter import messagebox
from add_screen import JobApplication

class DeleteScreen:
    def __init__(self, window, filename, menu_frame):
        self.window = window
        self.filename = filename
        self.menu_frame = menu_frame  # Store a reference to the menu_frame
        self.delete_frame = tk.Frame(window)
        self.create_delete_screen()

    def create_delete_screen(self):
        # Create the delete UI components (listbox, buttons, etc.)
        self.listbox = tk.Listbox(self.delete_frame, height=10, width=50)
        self.listbox.grid(row=0, column=0, padx=10, pady=10)

        # Delete button to delete the selected application
        self.delete_button = tk.Button(self.delete_frame, text="Delete", command=self.delete_application)
        self.delete_button.grid(row=1, column=0, pady=10)

        # Back button for Delete page
        self.back_button = tk.Button(self.delete_frame, text="Back", command=self.back_to_menu)
        self.back_button.grid(row=2, column=0, pady=10)

        # Populate the listbox with existing job applications
        self.populate_company_list()

    def populate_company_list(self):
        self.listbox.delete(0, tk.END)  # Clear the current list
        applications = JobApplication.load_from_json(self.filename)
        for app in applications:
            self.listbox.insert(tk.END, app.company_name)

    def delete_application(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            company_name = self.listbox.get(selected_index)
            applications = JobApplication.load_from_json(self.filename)

            # Find and delete the selected application
            for app in applications:
                if app.company_name.lower() == company_name.lower():
                    applications.remove(app)
                    JobApplication.save_to_json(applications, self.filename)
                    messagebox.showinfo("Success", f"Application for {company_name} deleted.")
                    self.populate_company_list()  # Refresh the listbox
                    break
        else:
            messagebox.showwarning("Selection Error", "Please select a company to delete.")

    def back_to_menu(self):
        self.delete_frame.pack_forget()  # Hide the delete screen
        self.menu_frame.pack(padx=10, pady=10)  # Show the menu again

    def show(self):
        self.delete_frame.pack(padx=10, pady=10)
