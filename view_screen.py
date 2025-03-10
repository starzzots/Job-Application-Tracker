import tkinter as tk
from tkinter import messagebox
import json
import re
from add_screen import JobApplication

class ViewScreen:
    def __init__(self, window, filename, menu_frame):
        self.window = window
        self.filename = filename
        self.menu_frame = menu_frame  # Store a reference to the menu_frame
        self.selected_app = None

        self.view_frame = tk.Frame(window)
        self.create_view_screen()

    def create_view_screen(self):
        # Listbox for displaying the company names
        self.listbox = tk.Listbox(self.view_frame, height=10, width=50)
        self.listbox.grid(row=0, column=0, padx=10, pady=10)
        self.listbox.bind("<Double-1>", self.display_details)

        # Back button for View page
        self.back_button = tk.Button(self.view_frame, text="Back", command=self.back_to_menu)
        self.back_button.grid(row=1, column=0, pady=10)

        # Create labels for the fields and position them closer
        self.create_label("Company Name", 2)
        self.create_label("Company Address", 3)
        self.create_label("Company Website", 4)
        self.create_label("Job Description", 5)
        self.create_label("Date Applied (yyyy-dd-mm)", 6)
        self.create_label("Application Status", 7)

        # Create entry fields for each job attribute
        self.company_name_entry = self.create_entry(2)
        self.company_address_entry = self.create_entry(3)
        self.company_website_entry = self.create_entry(4)
        self.job_description_text = self.create_text(5)
        self.date_applied_entry = self.create_entry(6)
        self.application_status_entry = self.create_entry(7)

        # Save button to save the changes made
        self.save_button = tk.Button(self.view_frame, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=8, column=1, pady=10)

    def create_label(self, text, row):
        label = tk.Label(self.view_frame, text=text)
        label.grid(row=row, column=0, padx=5, pady=3, sticky="e")

    def create_entry(self, row):
        entry = tk.Entry(self.view_frame, width=40)
        entry.grid(row=row, column=1, padx=5, pady=3)
        return entry

    def create_text(self, row):
        text_widget = tk.Text(self.view_frame, width=40, height=3)
        text_widget.grid(row=row, column=1, padx=5, pady=3)
        return text_widget

    def populate_company_list(self):
        self.listbox.delete(0, tk.END)  # Clear the current list
        applications = JobApplication.load_from_json(self.filename)
        for app in applications:
            self.listbox.insert(tk.END, app.company_name)

    def display_details(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            company_name = self.listbox.get(selected_index)
            applications = JobApplication.load_from_json(self.filename)

            # Find the application that matches the selected company
            for app in applications:
                if app.company_name.lower() == company_name.lower():
                    self.selected_app = app  # Store the selected application

                    # Populate the entry fields with the application's details
                    self.company_name_entry.delete(0, tk.END)
                    self.company_name_entry.insert(0, app.company_name)

                    self.company_address_entry.delete(0, tk.END)
                    self.company_address_entry.insert(0, app.company_address)

                    self.company_website_entry.delete(0, tk.END)
                    self.company_website_entry.insert(0, app.company_website)

                    self.job_description_text.delete(1.0, tk.END)
                    self.job_description_text.insert(tk.END, app.job_description)

                    self.date_applied_entry.delete(0, tk.END)
                    self.date_applied_entry.insert(0, app.date_applied)

                    self.application_status_entry.delete(0, tk.END)
                    self.application_status_entry.insert(0, app.application_status)

    def save_changes(self):
        if not self.selected_app:
            messagebox.showerror("Error", "No application selected to save.")
            return
        
        # Get the updated values from the entry fields
        updated_company_name = self.company_name_entry.get()
        updated_company_address = self.company_address_entry.get()
        updated_company_website = self.company_website_entry.get()
        updated_job_description = self.job_description_text.get(1.0, tk.END).strip()
        updated_date_applied = self.date_applied_entry.get()
        updated_application_status = self.application_status_entry.get()

        # Validate the date format (yyyy-dd-mm)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", updated_date_applied):
            messagebox.showerror("Invalid Date", "Date must be in yyyy-dd-mm format.")
            return

        # Update the selected application's details
        self.selected_app.company_name = updated_company_name
        self.selected_app.company_address = updated_company_address
        self.selected_app.company_website = updated_company_website
        self.selected_app.job_description = updated_job_description
        self.selected_app.date_applied = updated_date_applied
        self.selected_app.application_status = updated_application_status

        # Save the updated applications list back to the JSON file
        applications = JobApplication.load_from_json(self.filename)
        for idx, app in enumerate(applications):
            if app.company_name.lower() == self.selected_app.company_name.lower():
                applications[idx] = self.selected_app
                break
        JobApplication.save_to_json(applications, self.filename)

        messagebox.showinfo("Success", "Application details updated successfully.")

    def back_to_menu(self):
        self.view_frame.pack_forget()  # Hide the view screen
        self.menu_frame.pack(padx=10, pady=10)  # Show the menu again

    def show(self):
        self.view_frame.pack(padx=10, pady=10)
        self.populate_company_list()
