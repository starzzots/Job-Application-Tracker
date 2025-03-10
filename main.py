import tkinter as tk
from add_screen import AddScreen
from view_screen import ViewScreen
from delete_screen import DeleteScreen  # Import DeleteScreen class

def show_add_screen():
    add_screen = AddScreen(window, filename, menu_frame)  # Pass menu_frame to AddScreen
    add_screen.show()

def show_view_screen():
    # Hide the menu and show the View screen
    menu_frame.pack_forget()
    view_screen = ViewScreen(window, filename, menu_frame)  # Pass menu_frame to ViewScreen
    view_screen.show()

def show_delete_screen():
    # Hide the menu and show the Delete screen
    menu_frame.pack_forget()
    delete_screen = DeleteScreen(window, filename, menu_frame)  # Pass menu_frame to DeleteScreen
    delete_screen.show()

def back_to_menu():
    # Show the menu again and hide the current screen
    menu_frame.pack(padx=10, pady=10)

def main():
    global filename
    filename = "Jobs_Applied_to_2025.json" # change the to json you want to work with

    global window
    window = tk.Tk()
    window.title("Job Application Manager")

    # Set up window geometry
    window.geometry("720x640")

    # Create a frame for the menu buttons
    global menu_frame
    menu_frame = tk.Frame(window)

    # Menu buttons to choose Add, View, or Delete
    tk.Button(menu_frame, text="Add Data", command=show_add_screen).pack(pady=5)
    tk.Button(menu_frame, text="View Data", command=show_view_screen).pack(pady=5)
    tk.Button(menu_frame, text="Delete Data", command=show_delete_screen).pack(pady=5)

    # Initially show the menu
    menu_frame.pack(padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
