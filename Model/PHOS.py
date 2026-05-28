import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import runpy
# Keep references to images to avoid garbage collection
images = []

# ---------------- Functions ----------------

def center_window(win, width, height):
    """Center the window on the screen"""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_newgui():
    pre_win.destroy()
    runpy.run_path("NewGUI.py")

def open_other_panel():
    pre_win.destroy()
    runpy.run_path("Hybrid.py", run_name="__main__")   
# ---------------- Pre-window ----------------

pre_win = tk.Tk()
#pre_win.title("Select Initial Option")
pre_win.configure(bg="#EAEDED")

# Set size and center
center_window(pre_win, 1300, 600)

# ----- Frame for logos and layout -----
frame = tk.Frame(pre_win, bg="#EAEDED")
frame.pack(pady=20)

logo_frame = tk.Frame(frame, bg="#EAEDED")
logo_frame.pack(pady=10)

# ----- Logos -----
try:
    ucl_logo_img = Image.open("ucl_logo.png").resize((180, 60))
    ucl_logo = ImageTk.PhotoImage(ucl_logo_img)
    lbl = tk.Label(logo_frame, image=ucl_logo, bg="#EAEDED")
    lbl.pack(side="left", padx=10)
    images.append(ucl_logo)  # keep reference
except Exception as e:
    print("UCL logo not loaded:", e)

try:
    prysm_logo_img = Image.open("Picture1.png").resize((180, 60))
    prysm_logo = ImageTk.PhotoImage(prysm_logo_img)
    lbl2 = tk.Label(logo_frame, image=prysm_logo, bg="#EAEDED")
    lbl2.pack(side="left", padx=10)
    images.append(prysm_logo)  # keep reference
except Exception as e:
    print("Prysm logo not loaded:", e)

# ----- Text / instruction -----
tk.Label(frame, text="Choose Decarbonisation Pathway:", font=("Arial", 16, "bold"), bg="#EAEDED").pack(pady=20)

description = (
    "This tool is a spatial optimization decision tool for the UK energy system.\n\n"
    "Option 1: Decarbonisation of the Heat Sector via Hydrogen.\n"
    "Option 2: Decarbonisation of Heat Sector via Hybrid Hydrogen & Electrification.\n\n"
    "This tool provides whole-system optimization to find the least-cost, optimal energy infrastructure "
    "from generation, storage, transfer, and consumption for electricity, hydrogen, and carbon to meet Heat Demand under the UK Net Zero 2050 targets."
)

text_widget = tk.Text(frame, font=("Georgia", 12), wrap="word", width=100, height=8, bg="white", fg="#333")
text_widget.pack(pady=10)
text_widget.insert("1.0", description)
text_widget.config(state="disabled")  # make read-only
# ----- Buttons -----
tk.Button(frame, text="Decarbonisation of Heat Sector via Hydrogen", bg="#1E88E5", fg="white",
          width=50, height=2, font=("Arial", 12, "bold"),
          command=open_newgui).pack(pady=10)

tk.Button(frame, text="Decarbonisation of Heat Sector via Hydrogen & Electrification", bg="#228B22", fg="white",
          width=50, height=2, font=("Arial", 12, "bold"),
          command=open_other_panel).pack(pady=10)

pre_win.mainloop()
