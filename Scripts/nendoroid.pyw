from pathlib import Path as P
import tkinter as tk
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from ruamel.yaml import YAML
from PIL import Image, ImageTk
import subprocess
import sys

OUTPUT_PATH = P().parent
ASSETS_PATH = OUTPUT_PATH / P(r"Assets/nendo_frame")
ACCOUNTS_DIR = P('./Accounts')
ACCOUNTS_DIR.mkdir(exist_ok=True)
USERS_FILE = ACCOUNTS_DIR / 'users.yaml'
ICON = P('./Assets/logour.png')
yaml = YAML()
type = "Nendoroid Figures"
textheader = "Nendoroids"

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - 30
    window.geometry(f'{width}x{height}+{x}+{y}')

def relative_to_assets(path: str) -> P:
    return ASSETS_PATH / P(path)

def icon(window):
    img = PhotoImage(file=ICON)
    window.tk.call('wm', 'iconphoto', window._w, img)

def load_and_resize_image(path, scale_factor):
    # Load the image using Pillow
    image = Image.open(path)
    # Calculate new dimensions
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)
scale_factor = 0.97

def get_username_from_yaml():
    try:
        yaml = YAML()
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            account_data = yaml.load(file) or {}
        for username, details in account_data.items():
            if details.get('logged', False):
                return username
        return None
    except FileNotFoundError:
        messagebox.showinfo("Notice", "Accounts file not found.")
        return None
    except Exception as e:
        messagebox.showinfo("Error", f"Error loading account details: {e}")
        return None

def load_user_data(username):
    try:
        yaml = YAML()
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            user_data = yaml.load(file) or {}
        return user_data.get(username, {})
    except FileNotFoundError:
        print(f"User '{username}' file not found in account details.")
        return {}
    except Exception as e:
        print(f"Error loading user data for '{username}': {e}")
        return {}

def count_items_in_cart():    # use this function sa cart text     (count_items_in_cart())
    # Path to the cart YAML file
    CART_FILE = P('./Accounts/cart.yaml')
    try:
        yaml = YAML()
        with open(CART_FILE, 'r', encoding='utf-8') as file:
            cart_data = yaml.load(file)

        user_name = get_username_from_yaml()
        user_data = load_user_data(user_name)
        if user_data.get('logged', False):
            cname = user_name

        # Initialize the total quantity counter
        total_quantity = 0
        
        # Loop through items in the cart and count the total quantity
        if 'cart' in cart_data and cname in cart_data['cart'] and 'items' in cart_data['cart'][cname]:
            for item in cart_data['cart'][cname]['items']:
                quantity = item.get('Item Instance', 0)
                total_quantity += int(quantity)

        # Update the cart label text with the current total items and quantity
        canvas.itemconfig(cart_label, text=f"Items on cart:  {total_quantity}")
        # Schedule the function to run again after 1 seconds
        window.after(1000, count_items_in_cart)
    except FileNotFoundError:
        # If cart file is not found or empty, schedule the function to run again after 1 seconds
        window.after(1000, count_items_in_cart)

# Products
def miku():
    script_path = "Scripts/product_frames/nendo_miku.pyw"
    subprocess.Popen([sys.executable, script_path])
def kageyama():
    script_path = "Scripts/product_frames/nendo_kageyama.pyw"
    subprocess.Popen([sys.executable, script_path])
def lucy():
    script_path = "Scripts/product_frames/nendo_lucy.pyw"
    subprocess.Popen([sys.executable, script_path])
def levi():
    script_path = "Scripts/product_frames/nendo_levi.pyw"
    subprocess.Popen([sys.executable, script_path])

window = Tk()
window.geometry("1143x619")
window.configure(bg = "#FFFFFF")
window.title(type)

# Checkout and Remove Items keyboard shortcut
def checkout_script(event):
    script_path = "Scripts/checkout.pyw"
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = subprocess.SW_HIDE
    try:
        subprocess.Popen(['python', script_path], startupinfo=startup_info)
    except Exception as e:
        print("Error executing checkout script:", e)
def remove_script(event):
    script_path = "Scripts/remove_items.pyw"
    subprocess.Popen([sys.executable, script_path])
window.bind("<Return>", checkout_script)
window.bind("<BackSpace>", remove_script)

canvas = Canvas(window, bg = "#FFFFFF", height = 619, width = 1143, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1143.0, 619.3824462890625, fill="#FFFFFF", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image( 570.0, 60.0, image=image_image_1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(571.0, 365.0, image=image_image_2)
image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(571.0, 396.0, image=image_image_3)
image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(145.9810791015625, 60.89190673828125, image=image_image_4)

# Product 1 (Miku)
miku_img = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=miku_img, borderwidth=0, highlightthickness=0, command=miku, relief="flat")
button_1.place(x=43.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_1 = load_and_resize_image("Assets/nendo_frame/button_1.png", scale_factor)
def button_1_hover(e):
    button_1.config(
        image=button_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=miku_img
    )
button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

# Product 2 (kageyama)
kageyana_img = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=kageyana_img, borderwidth=0, highlightthickness=0, command=kageyama, relief="flat")
button_2.place(x=314.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_2 = load_and_resize_image("Assets/nendo_frame/button_2.png", scale_factor)
def button_2_hover(e):
    button_2.config(
        image=button_hover_2
    )
def button_2_leave(e):
    button_2.config(
        image=kageyana_img
    )
button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

# Product 3 (lucy)
lucy_img = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=lucy_img, borderwidth=0, highlightthickness=0, command=lucy, relief="flat")
button_3.place(x=585.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_3 = load_and_resize_image("Assets/nendo_frame/button_3.png", scale_factor)
def button_3_hover(e):
    button_3.config(
        image=button_hover_3
    )
def button_3_leave(e):
    button_3.config(
        image=lucy_img
    )
button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

# Product 4 (levi)
levi_imgg = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=levi_imgg, borderwidth=0, highlightthickness=0, command=levi, relief="flat")
button_4.place(x=856.0, y=220.0, width=245.59054565429688, height=352.1675720214844)
button_hover_4 = load_and_resize_image("Assets/nendo_frame/button_4.png", scale_factor)
def button_4_hover(e):
    button_4.config(
        image=button_hover_4
    )
def button_4_leave(e):
    button_4.config(
        image=levi_imgg
    )
button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

# Cart
image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(990.0, 60.0,image=image_image_5)
cart_label = canvas.create_text(937.0, 47.0, anchor="nw",
                   text="Items on cart:", fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
canvas.create_text(1059.0, 47.0, anchor="nw",
                   text=count_items_in_cart(), fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(914.0, 60.0, image=image_image_6)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(572.0, 64.0, image=image_image_7)

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(571.0, 61.0, image=image_image_8)

canvas.create_text(478.0, 36.0, anchor="nw",
                   text=textheader, fill="#FFFFFF", font=("Montserrat SemiBold", 32 * -1))

window.bind("<Escape>", quit)
icon(window)
center_window(window)
window.resizable(False, False)
window.mainloop()