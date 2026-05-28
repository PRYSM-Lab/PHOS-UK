import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import runpy



def run_final_approach(file_name):
    print(f"Running {file_name}...")
    runpy.run_path(file_name)

def select_final_approach(option, root):
    root.after(0, root.quit)
    if option == "Monolithic":
        run_final_approach('Monolithic.py')  
    elif option == "Hierarchical 2":
        run_final_approach('HA2 approach.py')
    elif option == "Hierarchical 1":
        run_final_approach('HA1 approach.py')  

def open_link(event=None):
    webbrowser.open("https://www.sciencedirect.com/science/article/pii/S0263876224001102")

def open_final_window():
    root.destroy()
    create_final_window()

def create_final_window():
    root2 = tk.Tk()
    root2.title("Select Final Approach")
    root2.configure(bg="#EAEDED")
    root2.geometry("1300x900")
    
    frame = tk.Frame(root2, bg="#EAEDED")
    frame.pack(pady=20)

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

    label_title = tk.Label(frame, text="Hydrogen Infrastructure Optimization Under Deterministic Approach", 
                           font=("Arial", 20, "bold"), fg="#2C3E50", bg="#EAEDED")  
    label_title.pack(pady=10)

    text_widget = tk.Text(frame, font=("Georgia", 13), wrap="word", width=110, height=18, bg="white", fg="#333")
    text_widget.pack(pady=10)
    text_widget.insert("1.0",  
            "Optimize hydrogen infrastructure planning for heat decarbonization in Great Britain. The optimization framework considers a long-term planning horizon in 5-year steps from 2035 to 2050, while "
            "also incorporating typical days with an hourly resolution under deterministic approach.\n\n"
            "To alleviate the computational effort of such a multiscale model, three approaches are available for selection:\n\n"

            "🔹 Monolithic Approach\n"
            "   A single, comprehensive model that solves all computations in one step, ensuring an integrated solution with "
            "1-hour time resolution.\n\n"

            "🔹 Hierarchical 1 Approach\n"
            "   1. The model is solved by dividing the day into six 4-hour intervals, reducing model complexity.\n"
            "   2. A refined model with 1-hour daily resolution is solved to determine all remaining decision variables.\n\n"

            "🔹 Hierarchical 2 Approach\n"
            "   1. The model is solved without considering pipeline infrastructure design, focusing on production and storage.\n"
            "   2. The second step includes fixing the production and storage investment decisions from the first step, then solving a reduced model where pipeline infrastructure and other decision variables are determined.\n"
        )
    text_widget.config(state="disabled")  

    link_label = tk.Label(frame, text="For more details, refer to Paper 1", font=("Arial", 14, "bold"), 
                          fg="blue", bg="#EAEDED", cursor="hand2")
    link_label.pack(pady=5)
    link_label.bind("<Button-1>", open_link)

    label = tk.Label(frame, text="Please Select the Solving Method", font=("Arial", 14, "bold"), fg="#2C3E50", bg="#EAEDED")
    label.pack(pady=10)

    button_style = {"width": 30, "height": 2, "font": ("Arial", 12, "bold"), "fg": "white"}

    tk.Button(frame, text="Monolithic", command=lambda: select_final_approach("Monolithic", root2), bg="#66BB6A", **button_style).pack(pady=5)
    tk.Button(frame, text="Hierarchical 1", command=lambda: select_final_approach("Hierarchical 1", root2), bg="#17A2B8", **button_style).pack(pady=5)
    tk.Button(frame, text="Hierarchical 2", command=lambda: select_final_approach("Hierarchical 2", root2), bg="#DC3545", **button_style).pack(pady=5)

    root2.mainloop()



def run_robust_approach(file_name):
    print(f"Running {file_name}...")
    runpy.run_path(file_name)

def select_robust_approach(option2, root):
    root.after(0, root.quit)
    if option2 == "Static Robust":
        run_robust_approach('SROH2.py')  
    elif option2 == "Adaptive Robust":
        run_robust_approach('ARO.py')
     

def open_link2(event=None):
    webbrowser.open("https://www.sciencedirect.com/science/article/pii/S0306261924016052")
def open_robust_window():
    root.destroy()
    create_robust_window()

def create_robust_window():
    root3 = tk.Tk()
    root3.title("Select Robust Approach")
    root3.configure(bg="#EAEDED")
    root3.geometry("1200x600")
    
    frame2 = tk.Frame(root3, bg="#EAEDED")
    frame2.pack(pady=20)
    
    logo_frame2 = tk.Frame(frame2, bg="#EAEDED")
    logo_frame2.pack(pady=10)

    try:
        ucl_logo = Image.open("ucl_logo.png").resize((180, 60))
        ucl_logo = ImageTk.PhotoImage(ucl_logo)
        tk.Label(logo_frame, image=ucl_logo, bg="#EAEDED").pack(side="left", padx=10)
    except:
        pass

    try:
        prysm_logo2 = Image.open("Picture1.png").resize((180, 60))
        prysm_logo2 = ImageTk.PhotoImage(prysm_logo2)
        tk.Label(logo_frame, image=prysm_logo2, bg="#EAEDED").pack(side="left", padx=10)
    except:
        pass

    label_title = tk.Label(frame2, text="Hydrogen Infrastructure Optimization Under Robust Approach", 
                           font=("Arial", 20, "bold"), fg="#2C3E50", bg="#EAEDED")  
    label_title.pack(pady=10)

    text_widget = tk.Text(frame2, font=("Georgia", 13), wrap="word", width=100, height=8, bg="white", fg="#333")
    text_widget.pack(pady=10)
    text_widget.insert("1.0", 
        "Spatially-explicit multi-period hydrogen infrastructure planning is studied under demand uncertainty \n\n"
        "The proposed framework is applied on a multi-period mixed-integer linear model with dual temporal "
        "resolution which aims to determine the optimal yearly investment decisions and hourly operational"
        "decisions for the hydrogen infrastructure planning under demand uncertainty. To efficiently solve"
        "the large-scale two-stage adaptive robust optimisation problem, a hybrid decomposition algorithm "
        "is developed based on a two-step hierarchical procedure and the column-and-constraint generation method,"
        "which can significantly reduce the computational complexity.")
    text_widget.config(state="disabled")  

    link_label = tk.Label(frame2, text="For more details, refer to Paper 2", font=("Arial", 14, "bold"), 
                          fg="blue", bg="#EAEDED", cursor="hand2")
    link_label.pack(pady=5)
    link_label.bind("<Button-1>", open_link2)


    label = tk.Label(frame2, text="Please Select the Robust Approach", font=("Arial", 14, "bold"), fg="#2C3E50", bg="#EAEDED")
    label.pack(pady=10)

    button_style = {"width": 30, "height": 2, "font": ("Arial", 12, "bold"), "fg": "white"}

    tk.Button(frame2, text="Static Robust", command=lambda: select_robust_approach("Static Robust", root3), bg="#F06292", **button_style).pack(pady=5)
    tk.Button(frame2, text="Adaptive Robust", command=lambda: select_robust_approach("Adaptive Robust", root3), bg="#17A2B8", **button_style).pack(pady=5)

    root3.mainloop()



def run_stochastic_approach(file_name):
    print(f"Running {file_name}...")
    runpy.run_path(file_name)

def select_number_scenario(option3, root):
    root.after(0, root.quit)
    if option3 == "Stochastic Approach":
        run_stochastic_approach('Stochastic1.py')  
    elif option3 == "20":
        run_stochastic_approach('Stochastic1.py')
    elif option3 == "25":
        run_stochastic_approach('Stochastic1.py')
def open_link3(event=None):
    webbrowser.open("https://pubs.acs.org/doi/full/10.1021/acs.iecr.4c04211")

def open_stochastic_window():
    root.destroy()
    create_stochastic_window()

def create_stochastic_window():
    root4 = tk.Tk()
    root4.title("Select Number of Scenario")
    root4.configure(bg="#EAEDED")
    root4.geometry("1200x600")
    
    frame3 = tk.Frame(root4, bg="#EAEDED")
    frame3.pack(pady=20)
    
    logo_frame3 = tk.Frame(frame3, bg="#EAEDED")
    logo_frame3.pack(pady=10)

    try:
        ucl_logo = Image.open("ucl_logo.png").resize((180, 60))
        ucl_logo = ImageTk.PhotoImage(ucl_logo)
        tk.Label(logo_frame, image=ucl_logo, bg="#EAEDED").pack(side="left", padx=10)
    except:
        pass

    try:
        prysm_logo2 = Image.open("Picture1.png").resize((180, 60))
        prysm_logo2 = ImageTk.PhotoImage(prysm_logo2)
        tk.Label(logo_frame, image=prysm_logo2, bg="#EAEDED").pack(side="left", padx=10)
    except:
        pass

    label_title = tk.Label(frame3, text="Hydrogen Infrastructure Optimization Under Stochastic Approach", 
                           font=("Arial", 20, "bold"), fg="#2C3E50", bg="#EAEDED")  
    label_title.pack(pady=10)

    text_widget = tk.Text(frame3, font=("Georgia", 13), wrap="word", width=100, height=8, bg="white", fg="#333")
    text_widget.pack(pady=10)
    text_widget.insert("1.0", 
        "The model considers a two-stage stochastic optimisation framework to provide insights or infrastructure  \n\n"
        "investments in hydrogen production, storage, transmission, and CO2 capture and storage. The mixed-integer linear programming "
        "(MILP) model aims to minimise total system cost with detailed spatio-temporal resolution to meet"
        "hydrogen demand in Great Britain. Uncertainty is considered in hydrogen demand, gas"
        "and technology costs, as well as renewables and biomass availability. ")
    text_widget.config(state="disabled") 
    
    link_label = tk.Label(frame3, text="For more details, refer to Paper 3", font=("Arial", 14, "bold"), 
                          fg="blue", bg="#EAEDED", cursor="hand2")
    link_label.pack(pady=5)

    link_label.bind("<Button-1>", open_link3)


    label = tk.Label(frame3, text="Please Run the Stochastic Model", font=("Arial", 14, "bold"), fg="#2C3E50", bg="#EAEDED")
    label.pack(pady=10)

    button_style = {"width": 30, "height": 2, "font": ("Arial", 12, "bold"), "fg": "white"}

    tk.Button(frame3, text="Stochastic Approach", command=lambda: select_number_scenario("Stochastic Approach", root4), bg="#F06292", **button_style).pack(pady=5)
   
    root4.mainloop()


root = tk.Tk()
root.title("Optimization Approach Selection")
root.configure(bg="#EAEDED")
root.geometry("1100x700")

frame = tk.Frame(root, bg="#EAEDED")
frame.pack(pady=20)

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

label_title = tk.Label(frame, text="GUI Decision Making Tool for Hydrogen Infrastructure Optimization", 
                       font=("Arial", 20, "bold"), fg="#2C3E50", bg="#EAEDED")  
label_title.pack(pady=10)

text_widget = tk.Text(frame, font=("Georgia", 12), wrap="word", width=95, height=13, bg="white", fg="#333")
text_widget.pack(pady=10)
text_widget.insert("1.0", 
    "This tool provides three user interface to solve the hydrogen infrastructure optimization model under different approaches:\n\n"
    "🔹 Deterministic: Solves the problem with fixed inputs.\n"
    "🔹 Stochastic: Solves the model under the two-stage stochastic optimization.\n"
    "🔹 Robust: Solves the model under demand uncertainty with hybrid decomposition method.\n\n\n"
    "Note 1: Before exceuting the tool, ensure tht all required libraries are installed by running 'pip install -r requirements.txt' in the terminal. \n\n"
    "Note 2: The general input data are provided in the file 'newhydro_clusters.xlsx'. Whenever the interface prompts for an input file, please select this"
    "file from the specified path. This input can be updated, as long as the original format is preserved.")
text_widget.config(state="disabled")  



button_style = {"width": 30, "height": 2, "font": ("Arial", 12, "bold"), "fg": "white"}

tk.Button(frame, text="Deterministic", command=open_final_window, bg="#1E88E5", **button_style).pack(pady=5)
tk.Button(frame, text="Stochastic", command=open_stochastic_window, bg="#228B22", **button_style).pack(pady=5)
tk.Button(frame, text="Robust", command=open_robust_window, bg="#8E24AA", **button_style).pack(pady=5)

root.mainloop()

