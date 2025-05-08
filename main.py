import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from PIL.Image import Resampling
from io import BytesIO
import webbrowser

from philosopher import Philosopher, ImageLinks

# Constants
API_URL = "https://philosophersapi.com/api/philosophers/"

root = tk.Tk()
root.title("Philosopher Finder")
root.geometry("800x600")
root.configure(bg="#f0f0f0")
root.resizable(True, True)

# Function to fetch philosopher data from the API
def fetch_philosopher_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return None

# Function to display philosopher information
def display_philosopher_info(philosopher: Philosopher):
    info_window = tk.Toplevel(root)
    info_window.title(philosopher.name)
    info_window.geometry("800x600")
    info_window.configure(bg="#f0f0f0")
    info_window.resizable(True, True)

    # Display the philosopher's image
    if philosopher.images.face500x500:
        try:
            image_url = philosopher.images.full420x560 or philosopher.images.face500x500
            response = requests.get(f"https://philosophersapi.com{image_url}")
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content))
            image_data = image_data.resize((400, 400), Resampling.LANCZOS)
            img = ImageTk.PhotoImage(image_data)

            image_label = tk.Label(info_window, image=img, bg="#f0f0f0")
            image_label.image = img
            image_label.pack(pady=10)
        except Exception as e:
            tk.Label(info_window, text=f"Failed to load image: {e}", bg="#f0f0f0").pack(pady=10)
    else:
        tk.Label(info_window, text="No image available for this philosopher.", bg="#f0f0f0").pack(pady=10)

    # Display philosopher details in a scrollable Text widget
    details_frame = tk.Frame(info_window, bg="#f0f0f0")
    details_frame.pack(fill="both", expand=True, padx=20, pady=10)

    details_text = tk.Text(details_frame, wrap="word", bg="#f0f0f0", font=("Arial", 12), relief="flat")
    details_text.pack(fill="both", expand=True, side="left")

    scrollbar = tk.Scrollbar(details_frame, orient="vertical", command=details_text.yview)
    scrollbar.pack(side="right", fill="y")
    details_text.config(yscrollcommand=scrollbar.set)

    details = [
        f"Name: {philosopher.name}",
        f"Life: {philosopher.life}",
        f"Interests: {philosopher.interests}",
        f"Birth Year: {philosopher.birth_year}",
        f"Death Year: {philosopher.death_year}",
        f"Description: {philosopher.topical_description}",
    ]

    for detail in details:
        details_text.insert("end", detail + "\n\n")
    details_text.config(state="disabled")  # Make the text read-only

    # Add a button to open the philosopher's Wikipedia page
    wiki_button = tk.Button(info_window, text="Open Wikipedia", command=lambda: open_wikipedia(philosopher.name), bg="#4CAF50", fg="white", font=("Arial", 12))
    wiki_button.pack(pady=10)

    # Add a button to close the info window
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy, bg="#f44336", fg="white", font=("Arial", 12))
    close_button.pack(pady=10)

# Function to open the philosopher's Wikipedia page
def open_wikipedia(philosopher_name: str):
    search_url = f"https://en.wikipedia.org/wiki/{philosopher_name.replace(' ', '_')}"
    webbrowser.open(search_url)

# Function to handle the selection of a philosopher
def on_philosopher_select(event):
    selected_index = philosopher_listbox.curselection()
    if selected_index:
        selected_philosopher = philosophers[selected_index[0]]
        images = ImageLinks.from_dict(selected_philosopher.get('images', {}))
        philosopher_obj = Philosopher(
            images=images,
            life=selected_philosopher.get('life', ''),
            name=selected_philosopher.get('name', ''),
            interests=selected_philosopher.get('interests', ''),
            birth_year=selected_philosopher.get('birthYear', None),
            death_year=selected_philosopher.get('deathYear', None),
            topical_description=selected_philosopher.get('topicalDescription', None)
        )
        display_philosopher_info(philosopher_obj)

# Fetch philosopher data and populate the listbox
philosophers = fetch_philosopher_data()
if philosophers:
    list_frame = tk.Frame(root, bg="#f0f0f0")
    list_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(list_frame, text="Select a Philosopher:", bg="#f0f0f0", font=("Arial", 14)).pack(anchor="w", pady=5)

    philosopher_listbox = tk.Listbox(list_frame, font=("Arial", 12), height=20, width=50)
    philosopher_listbox.pack(side="left", fill="y", padx=10)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=philosopher_listbox.yview)
    scrollbar.pack(side="right", fill="y")

    philosopher_listbox.config(yscrollcommand=scrollbar.set)

    for philosopher in philosophers:
        philosopher_listbox.insert("end", philosopher.get('name', 'Unknown'))

    philosopher_listbox.bind("<<ListboxSelect>>", on_philosopher_select)
else:
    messagebox.showerror("Error", "No philosopher data available.")

# Start the main loop
root.mainloop()