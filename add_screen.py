import json
import tkinter as tk
from tkinter import messagebox

class JobApplication:
    def __init__(self, company_name, company_address, company_website, job_description, date_applied, application_status):
        self.company_name = company_name
        self.company_address = company_address
        self.company_website = company_website
        self.job_description = job_description
        self.date_applied = date_applied
        self.application_status = application_status

    @staticmethod
    def load_from_json(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return [JobApplication(**{key.replace(" ", "_").lower(): value for key, value in job.items()}) for job in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return []

    @staticmethod
    def save_to_json(applications, filename):
        try:
            with open(filename, "w") as file:
                json.dump([{
                    key.replace("_", " ").title(): value for key, value in app.__dict__.items()
                } for app in applications], file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

class AddScreen:
    def __init__(self, window, filename, menu_frame):
        self.window = window
        self.filename = filename
        self.menu_frame = menu_frame  # Store reference to the menu frame

        self.form_frame = tk.Frame(window)
        self.create_form()

    def create_form(self):
        tk.Label(self.form_frame, text="Company Name").grid(row=0, column=0)
        self.company_name_entry = tk.Entry(self.form_frame)
        self.company_name_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Company Address").grid(row=1, column=0)
        self.company_address_entry = tk.Entry(self.form_frame)
        self.company_address_entry.grid(row=1, column=1)

        tk.Label(self.form_frame, text="Company Website").grid(row=2, column=0)
        self.company_website_entry = tk.Entry(self.form_frame)
        self.company_website_entry.grid(row=2, column=1)

        tk.Label(self.form_frame, text="Job Description").grid(row=3, column=0)
        self.job_description_entry = tk.Entry(self.form_frame)
        self.job_description_entry.grid(row=3, column=1)

        tk.Label(self.form_frame, text="Date Applied").grid(row=4, column=0)
        self.date_applied_entry = tk.Entry(self.form_frame)
        self.date_applied_entry.grid(row=4, column=1)

        tk.Label(self.form_frame, text="Application Status").grid(row=5, column=0)
        self.application_status_entry = tk.Entry(self.form_frame)
        self.application_status_entry.grid(row=5, column=1)

        tk.Button(self.form_frame, text="Clear", command=self.clear_form).grid(row=6, column=0)
        tk.Button(self.form_frame, text="Save", command=self.save_data).grid(row=6, column=1)

        # Back button
        self.back_button = tk.Button(self.form_frame, text="Back", command=self.back_to_menu)
        self.back_button.grid(row=7, column=0, columnspan=2, pady=10)

    def clear_form(self):
        self.company_name_entry.delete(0, tk.END)
        self.company_address_entry.delete(0, tk.END)
        self.company_website_entry.delete(0, tk.END)
        self.job_description_entry.delete(0, tk.END)
        self.date_applied_entry.delete(0, tk.END)
        self.application_status_entry.delete(0, tk.END)

    def save_data(self):
        company_name = self.company_name_entry.get()
        company_address = self.company_address_entry.get()
        company_website = self.company_website_entry.get()
        job_description = self.job_description_entry.get()
        date_applied = self.date_applied_entry.get()
        application_status = self.application_status_entry.get()

        job = JobApplication(company_name, company_address, company_website, job_description, date_applied, application_status)
        applications = JobApplication.load_from_json(self.filename)
        applications.append(job)
        JobApplication.save_to_json(applications, self.filename)

        messagebox.showinfo("Success", f"Application for {company_name} added.")
        self.clear_form()

    def back_to_menu(self):
        self.form_frame.pack_forget()
        self.menu_frame.pack(padx=10, pady=10)  # Show menu frame again

    def show(self):
        # Hide the main menu before showing the form
        self.menu_frame.pack_forget()
        
        # Show the add form
        self.form_frame.pack(padx=10, pady=10)
