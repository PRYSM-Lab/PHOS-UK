import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import runpy

# ----------------- Run Functions -----------------
def run_hybrid_approach(file_name):
    print(f"Running {file_name}...")
    runpy.run_path(file_name)

def select_hybrid_approach(option, root):
    root.after(0, root.quit)
    if option == "Base Case":
        run_hybrid_approach('hybridtkinder.py')
    elif option == "H2Gas":
        run_hybrid_approach('hybridtkinder.py')
    elif option == "H2Electricity":
        run_hybrid_approach('hybridtkinder.py')
    elif option == "H2Blend":
        run_hybrid_approach('hybridtkinder.py')

# ----------------- External Link -----------------
def open_link(event=None):
    # Replace this link with the related Hybrid Approach paper if available
    webbrowser.open("https://www.example.com/hybrid-hydrogen-paper")

# ----------------- Hybrid Window -----------------
def create_hybrid_window():
    rootH = tk.Tk()
    rootH.title("Hybrid Approach – Select Case")
    rootH.configure(bg="#EAEDED")
    rootH.geometry("1300x1050")
    
    frame = tk.Frame(rootH, bg="#EAEDED")
    frame.pack(pady=20)

    # ---- Logos ----
    logo_frame = tk.Frame(frame, bg="#EAEDED")
    logo_frame.pack(pady=10)

    try:
        ucl_logo = Image.open("ucl_logo.png").resize((180, 60))
        ucl_logo = ImageTk.PhotoImage(ucl_logo)
        tk.Label(logo_frame, image=ucl_logo, bg="#EAEDED").pack(side="left", padx=10)
    except:
        pass

    try:
        prysm_logo = Image.open("Picture1.png").resize((180, 60))
        prysm_logo = ImageTk.PhotoImage(prysm_logo)
        tk.Label(logo_frame, image=prysm_logo, bg="#EAEDED").pack(side="left", padx=10)
    except:
        pass

    # ---- Title ----
    label_title = tk.Label(frame, 
                           text="Hybrid Approach – Hydrogen Infrastructure Optimization", 
                           font=("Arial", 20, "bold"), fg="#2C3E50", bg="#EAEDED")
    label_title.pack(pady=10)

    # ---- Description ----
    text_widget = tk.Text(frame, font=("Georgia", 13), wrap="word", width=80, height=15, bg="white", fg="#333")
    text_widget.pack(pady=10)
    text_widget.insert("1.0",
        "The Hybrid Approach integrates features of deterministic, robust, and flexible modeling to better "
        "capture the role of hydrogen in decarbonization pathways. Four cases are available for evaluation:\n\n"
        "🔹 Base Case – Inflexible:\n"
        "   Benchmark case without fuel substitution flexibility.\n\n"
        "🔹 Hydrogen–Gas Flexible:\n"
        "   Allows substitution between hydrogen and natural gas in end-use demand.\n\n"
        "🔹 Hydrogen–Electricity Flexible:\n"
        "   Considers power–hydrogen sector coupling via electrolysis and power generation.\n\n"
        "🔹 Hydrogen Blend to Gas Grid:\n"
        "   Evaluates feasibility of hydrogen injection into the existing gas distribution grid."
    )
    text_widget.config(state="disabled")

    # ---- Reference Link ----
    #link_label = tk.Label(frame, text="For more details, refer to Hybrid Approach Paper", 
                         # font=("Arial", 14, "bold"), fg="blue", bg="#EAEDED", cursor="hand2")
    #link_label.pack(pady=5)
    #link_label.bind("<Button-1>", open_link)

    # ---- Instruction ----
    label = tk.Label(frame, text="Please Select the Hybrid Case", 
                     font=("Arial", 14, "bold"), fg="#2C3E50", bg="#EAEDED")
    label.pack(pady=10)

    # ---- Buttons ----
    button_style = {"width": 30, "height": 2, "font": ("Arial", 12, "bold"), "fg": "white"}

    tk.Button(frame, text="Base Case – Inflexible", 
              command=lambda: select_hybrid_approach("Base Case", rootH), 
              bg="#1E88E5", **button_style).pack(pady=5)

    tk.Button(frame, text="Hydrogen–Gas Flexible", 
              command=lambda: select_hybrid_approach("H2Gas", rootH), 
              bg="#43A047", **button_style).pack(pady=5)

    tk.Button(frame, text="Hydrogen–Electricity Flexible", 
              command=lambda: select_hybrid_approach("H2Electricity", rootH), 
              bg="#FB8C00", **button_style).pack(pady=5)

    tk.Button(frame, text="Hydrogen Blend to Gas Grid", 
              command=lambda: select_hybrid_approach("H2Blend", rootH), 
              bg="#8E24AA", **button_style).pack(pady=5)

    rootH.mainloop()


# ----------------- Run This to Test -----------------
if __name__ == "__main__":
    create_hybrid_window()
