# %% Reading Data from Excel==============================


import pandas as pd
import pandas as pd
import numpy as np
from numpy import unravel_index
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import concurrent.futures
from tkinter import simpledialog
import threading
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()  

file_path = filedialog.askopenfilename(
    title="Select Excel File",
    filetypes=[("Excel Files", "*.xlsx *.xls")] 
)

if file_path:
    excel_data = pd.ExcelFile(file_path, engine='openpyxl')

Regions_data = excel_data.parse('Regions')
Sets_data = excel_data.parse('Sets')
Distances_data = excel_data.parse('Distances')
General_data = excel_data.parse('General')
Storage_data = excel_data.parse('Storage')
Production_data = excel_data.parse('Production')
Renewables_data = excel_data.parse('Renewables')
Emissions_data = excel_data.parse('Emissions')
H2Pipline_data = excel_data.parse('H2Pipeline')
CO2Pipline_data = excel_data.parse('CO2Pipeline')
CO2Reservior_data = excel_data.parse('CO2Reservoir')
Biomass_data = excel_data.parse('Biomass')
#Demand_data = excel_data.parse('Demand4cave')

df_Biomass = excel_data.parse('Biomass', header=None, usecols="B:C", skiprows=3, nrows=13)
df_bio = excel_data.parse('General', header=None, usecols="E:F", skiprows=48, nrows=4)
df_cgas = excel_data.parse('General', header=None, usecols="A:B", skiprows=48, nrows=4)
df_dc = excel_data.parse('General', header=None, usecols="A:B", skiprows=58, nrows=4)
df_cccH = excel_data.parse('H2Pipeline', header=None, usecols="A:B", skiprows=32, nrows=3)
df_cccC_Onshore = excel_data.parse('CO2Pipeline', header=None, usecols="A:B", skiprows=59, nrows=2)
df_cccC_offshore = excel_data.parse('CO2Pipeline', header=None, usecols="D:E", skiprows=59, nrows=2)
df_ct = excel_data.parse('CO2Pipeline', header=None, usecols="C:F", skiprows=2, nrows=2)
df_Cstart = excel_data.parse('Production', header=None, usecols="A:B", skiprows=61, nrows=4)
df_Cshut = excel_data.parse('Production', header=None, usecols="C:D", skiprows=61, nrows=4)
df_DT = excel_data.parse('Production', header=None, usecols="C:D", skiprows=51, nrows=4)
df_ec = excel_data.parse('Renewables', header=None, usecols="D:G", skiprows=17, nrows=2)
df_emtarget = excel_data.parse('Emissions', header=None, usecols="D:G", skiprows=39, nrows=2)
df_DistRes = excel_data.parse('Distances', header=None, usecols="B:D", skiprows=23, nrows=3)
df_DistSt = excel_data.parse('Distances', header=None, usecols="B:D", skiprows=31, nrows=4)
df_Dist = excel_data.parse('Distances', header=None, usecols="B:N", skiprows=4, nrows=13)
df_DistPipe = excel_data.parse('Distances', header=None, usecols="R:AD", skiprows=38, nrows=13)
#df_Sheet1 = excel_data.parse('Sheet1', header=None, usecols="A:AO", skiprows=2, nrows=144)

import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import threading
import pandas as pd


# Global variables
global df_GasDemave, df_Demand_data, df_Availability, df_GasDemave, df_BigQ_neg, df_BigQ_pos, n_clusters

df_GasDem = None
df_Demand_data = None
df_Availability = None
n_clusters = None  
df_BigQ_neg = None
df_BigQ_pos= None

def run_robust(n_clusters_input):
    print("Running Robust3.py with clusters:", n_clusters_input)
    result = subprocess.run(
        ['python', 'Robust3.py'],
        input=n_clusters_input,  
        capture_output=True,
        text=True
    )
    if result.stderr:
        print(f"Error: {result.stderr}")
    else:
        print(f"Output: {result.stdout}")


def select_process(root):
    global df_GasDemave, df_Demand_data, df_Availability, df_BigQ_neg, df_BigQ_pos, n_clusters

    n_clusters = simpledialog.askinteger("Input", 
                                         "Enter number of representative days:\n(Default value: 5)", 
                                         minvalue=1, maxvalue=12)

    if n_clusters is None:
        return  

    n_clusters_input = str(n_clusters) + '\n'
    root.after(0, root.quit)

    thread = threading.Thread(target=run_robust, args=(n_clusters_input,), daemon=False)
    thread.start()
    thread.join()  

    process_data(n_clusters)
    root.withdraw()


def process_data(n_clusters):
    global df_GasDemave, df_Demand_data, df_Availability, df_BigQ_neg, df_BigQ_pos
    #file_path1 = r'C:\Users\Mohammed\Merged_final_average_data.csv'
    #file_path2 = r'C:\Users\Mohammed\merged_BigQneg.csv'
    #file_path3 = r'C:\Users\Mohammed\merged_BigQpos.csv'
    #file_path4 = r'C:\Users\Mohammed\Final_cluster_Robust.xlsx'
    file_path1 = os.path.join(os.getcwd(), 'Merged_final_average_data.csv')
    file_path2 = os.path.join(os.getcwd(), 'merged_BigQneg.csv')
    file_path3 = os.path.join(os.getcwd(), 'merged_BigQpos.csv')
    file_path4 = os.path.join(os.getcwd(), 'Final_cluster_Robust.xlsx')
    
    excel_data = pd.ExcelFile(file_path4, engine='openpyxl')
    
    df_GasDemave = pd.read_csv(file_path1, header=None, usecols=range(0, 54), skiprows=2, nrows=24 * (n_clusters+1))
    df_BigQ_neg = pd.read_csv(file_path2, header=None, usecols=range(0, 55), skiprows=2, nrows=24 *24 *(n_clusters))
    df_BigQ_pos = pd.read_csv(file_path3, header=None, usecols=range(0, 55), skiprows=2, nrows=24 * 24*(n_clusters))
    df_Demand_data = excel_data.parse('Cluster and weights', usecols="A:B", skiprows=0, nrows=n_clusters+1)
    df_Availability = excel_data.parse('Availability', header=None, usecols="A:AN", skiprows=1, nrows=24*(n_clusters+1))
    
    print("Clustering processing complete.")


def center_window(win, width=500, height=300):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


def create_main_window():
    root = tk.Tk()
    root.title("Robust Clustering Method")
    
    root.geometry("500x300")
    center_window(root, 500, 300)  
    root.configure(bg="#2c3e50")  

    label = tk.Label(root, text="Clustering Method: Robust", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
    label.pack(pady=20)

    tk.Button(root, text="Run Robust Clustering", font=("Arial", 12, "bold"), fg="white", bg="#e67e22",
              width=25, height=2, command=lambda: select_process(root)).pack(pady=10)
    
    root.mainloop()


create_main_window()
#df_GasDem = excel_data.parse('Demand6cNEW2017', header=None, usecols="A:O", skiprows=1, nrows=144)
# %% Building the Model===================================
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

model = ConcreteModel()

# ---------------------------------Define Main and Additional Sets and Subsets ------------------------------

l_data = Sets_data.iloc[1, 2:4].values
g_data = Sets_data.iloc[2, 2:15].values 
p_data = Sets_data.iloc[3, 2:6].values
r_data = Sets_data.iloc[4, 2:6].values
s_data = Sets_data.iloc[5, 2:8].values
t_data = Sets_data.iloc[6, 2:8].values
d_data = Sets_data.iloc[7, 2:5].values
c_data = Sets_data.iloc[8, 2:4].values
h_data = Sets_data.iloc[9, 2:26].values
sc_data = Sets_data.iloc[10, 2:6].values
sv_data = Sets_data.iloc[11, 2:4].values
e_data = Sets_data.iloc[12, 2:5].values
I_data = Sets_data.iloc[1, 2:4].values
region1_data = Regions_data.iloc[2:48, 2].values
region2_data = Regions_data.iloc[2:48, 3].values
Neighbourhood_Regions = list(zip(region1_data,region2_data))

model.l = Set(initialize=['Trailer', 'Pipe'])
model.g = Set(initialize=g_data)
model.g1 = Set(initialize=g_data)
model.p = Set(initialize=p_data)
model.r = Set(initialize=r_data)
model.s = Set(initialize=s_data)
model.t = Set(initialize=[3,4,5,6])#t_data)
model.d1 = Set(initialize=d_data)
model.d2 = Set(initialize=[1, 2])
model.c = Set(initialize=c_data)
model.h = Set(initialize=h_data)
model.sc= Set(initialize=sc_data)
model.sv= Set(initialize=sv_data)
model.e = Set(initialize=e_data)
model.j = RangeSet(1,24)

Region3_data = Regions_data.iloc[6:32, 17].values
storage_data = Regions_data.iloc[6:32, 18].values


Region4_data = Regions_data.iloc[2:32, 17].values
storage1_data = Regions_data.iloc[2:32, 18].values

GS_data = list(zip(Region4_data, storage1_data))
GS_data1 = list(zip(Region3_data, storage_data))
GS_data2 = [('NO', 'OnTeeside'), ('NW', 'OnChesire'), ('NE', 'OnYorkshire'), ('NW', 'OffIrishSea')]

model.GS = Set(dimen=2, initialize=[(g,s) for g in model.g for s in model.s if (g,s) in GS_data])

model.GS1 = Set(dimen=2, initialize=[(g,sv) for g in model.g for sv in model.sv if (g,sv) in GS_data1])
model.GS2 = Set(dimen=2, initialize=[(g,sc) for g in model.g for sc in model.sc if (g,sc) in GS_data2])
Gimp_data = [(g_data[9]), (g_data[11]), (g_data[2]), (g_data[0])]
model.Gimp = Set(within=model.g, initialize= ['WS', 'SO', 'NO', 'NE', 'SC'])
#model.Gimp = Set(initialize=[(g) for g in model.g if (g) in Gimp_data])
GR_data=[(g_data[0], r_data[2]), (g_data[5], r_data[3]), (g_data[6], r_data[0])]
model.GR = Set(dimen=2, initialize=[(g,r) for g in model.g for r in model.r if (g,r) in GR_data])
model.N = Set(dimen=2, initialize=[(g,g1) for g in model.g for g1 in model.g if (g,g1) in Neighbourhood_Regions])


# Aliases
model.gg = Set(dimen=2, initialize=lambda model: [(g,g1) for g in model.g for g1 in model.g])
model.hh = Set(dimen=2, initialize=lambda model: [(h,h1) for h in model.h for h1 in model.h])


# ------ RangeSets -----

model.TT = RangeSet(3, 6)  #  TT(t) /3*6/
model.CC = RangeSet(1,n_clusters+1)  #  CC(c) /1*6/
model.HH = RangeSet(1, 24) #  HH(h) /1*24/

# %% #---------------------------------------Assign spacific data for parameters--------------------------
DistSt_data = {(g, s): df_DistSt.iloc[i,2] 
          for i, g in enumerate(df_DistSt.iloc[:, 0])
          for j, s in enumerate(df_DistSt.iloc[:, 1])
          if i==j}

Data1 = Emissions_data.iloc[30:34, 3:7]
y_c_data = {(p,t): Data1.iloc[i,j]
            for i, p in enumerate(model.p)
            for j, t in enumerate(model.TT)}

Data2 = Emissions_data.iloc[21:25, 3:7]
y_e_data = {(p,t): Data2.iloc[i,j]
            for i, p in enumerate(model.p)
            for j, t in enumerate(model.t)}

diaH_data1 = H2Pipline_data.iloc[9:12, 1]
diaH_data = {(d1): diaH_data1.iloc[i]
             for i, d1 in enumerate(model.d1)}

AV_data = {
    (int(c), int(h), g, e): df_Availability.iloc[i,  1+idx]  # مقدار برداشته شده از دیتا فریم
    for i, pair in enumerate(df_Availability.iloc[:, 0])  # جفت‌های (c, h) از ستون اول
    for idx, (g, e) in enumerate([(g, e) for g in model.g for e in model.e])  # ترکیب‌های مختلف g و e
    for c, h in [map(int, pair.strip("()").split(","))]  # تبدیل جفت (c, h) به مقادیر عددی
}

'''
AV_data = {(c, h, g, e): df_Sheet1.iloc[i, 2 + 3 * g_idx + e_idx]
    for i, (c, h) in enumerate(zip(df_Sheet1.iloc[:, 0], df_Sheet1.iloc[:, 1]))  
    for g_idx, g in enumerate(model.g)  
    for e_idx, e in enumerate(model.e)}
'''
df_Biomass.iloc[:, 0] = df_Biomass.iloc[:, 0].str.strip().str.upper()
br_data = dict(zip(df_Biomass.iloc[:, 0], df_Biomass.iloc[:, 1]))

cbio_data = dict(zip(df_bio.iloc[:, 0], df_bio.iloc[:, 1]))

cccH_data = dict(zip(df_cccH.iloc[:, 0], df_cccH.iloc[:, 1]))
cccC_onshore_data = dict(zip(df_cccC_Onshore.iloc[:, 0], df_cccC_Onshore.iloc[:, 1]))
cccC_offshore_data = dict(zip(df_cccC_offshore.iloc[:, 0], df_cccC_offshore.iloc[:, 1]))

cgas_data = dict(zip(df_cgas.iloc[:,0], df_cgas.iloc[:,1]))

df_Cstart.iloc[:, 0] = df_Cstart.iloc[:, 0].str.strip().str.upper()
Cstart_data = dict(zip(df_Cstart.iloc[:, 0], df_Cstart.iloc[:, 1]))

df_Cshut.iloc[:, 0] = df_Cshut.iloc[:, 0].str.strip().str.upper()
Cshut_data = dict(zip(df_Cshut.iloc[:, 0], df_Cshut.iloc[:, 1]))

df_transposed= df_ct.T
df_transposed.columns = ['key', 'value']
ct_data = dict(zip(df_transposed['key'], df_transposed['value']))

dc_data = dict(zip(df_dc.iloc[:,0], df_dc.iloc[:,1]))
'''
DistPipe_data = {
    (g_row, g_col): df_DistPipe.iloc[i, j]
    for i, g_row in enumerate(model.g)
    for j, g_col in enumerate(model.g)}
'''
DistPipe_data = {
    (g_row, g_col): df_DistPipe.iloc[i, j]
    for i, g_row in enumerate(model.g)
    for j, g_col in enumerate(model.g)
    if df_DistPipe.iloc[i, j] > 0  
}


DistRes_data = {(g, r): df_DistRes.iloc[i,2] 
          for i, g in enumerate(df_DistRes.iloc[:, 0])
          for j, r in enumerate(df_DistRes.iloc[:, 1])
          if i==j}


Dist_data = {
    (g_row, g_col): df_Dist.iloc[i, j]
    for i, g_row in enumerate(model.g)
    for j, g_col in enumerate(model.g) 
    if df_Dist.iloc[i, j] > 0}
    

DT_data = dict(zip(df_DT.iloc[:, 0], df_DT.iloc[:, 1]))
df_ec_transposed= df_ec.T
df_ec_transposed.columns = ['key', 'value']
ec_data = dict(zip(df_ec_transposed['key'], df_ec_transposed['value']))

Data4 = Production_data.iloc[69:73, 3:7]
eta_data = {(p,t): Data4.iloc[i,j]
            for i, p in enumerate(model.p)
            for j, t in enumerate(model.t)}

df_emtarget_transposed= df_emtarget.T
df_emtarget_transposed.columns = ['key', 'value']
emtarget_data = dict(zip(df_emtarget_transposed['key'], df_emtarget_transposed['value']))




GasDemave_data = {(c, h,t, g): df_GasDemave.iloc[i, 2 + 13 * t_idx + g_idx]
    for i, (c, h) in enumerate(zip(df_GasDemave.iloc[:, 0], df_GasDemave.iloc[:, 1]))  
    for t_idx, t in enumerate(model.TT)  
    for g_idx, g in enumerate(model.g)}

BigQneg_data = {(c, h,j,t, g): df_BigQ_neg.iloc[i, 3 + 13 * t_idx + g_idx]
    for i, (c, h,j) in enumerate(zip(df_BigQ_neg.iloc[:, 0], df_BigQ_neg.iloc[:, 1], df_BigQ_neg.iloc[:, 2]))  
    for t_idx, t in enumerate(model.TT)  
    for g_idx, g in enumerate(model.g)}

BigQpos_data = {(c, h,j,t, g): df_BigQ_pos.iloc[i, 3 + 13 * t_idx + g_idx]
    for i, (c, h,j) in enumerate(zip(df_BigQ_pos.iloc[:, 0], df_BigQ_pos.iloc[:, 1], df_BigQ_pos.iloc[:, 2]))  
    for t_idx, t in enumerate(model.TT)  
    for g_idx, g in enumerate(model.g)}



Data5 = Renewables_data.iloc[28:31, 1:14]
landAV_data = {(e,g): Data5.iloc[i,j]
            for i, e in enumerate(model.e)
            for j, g in enumerate(model.g)}

Data6 = Production_data.iloc[34:38, 5]
Capmax_data = {(p): Data6.iloc[i]
            for i, p in enumerate(model.p)}

Data7 = Production_data.iloc[34:38, 1]
Capmin_data = {(p): Data7.iloc[i]
            for i, p in enumerate(model.p)}

Data8 = Production_data.iloc[4:8, 3:7]
pccost_data = {(p,t): Data8.iloc[i,j]
            for i, p in enumerate(model.p)
            for j, t in enumerate(model.t)}

Data9 = Production_data.iloc[14:18, 3:7]
pocostF_data = {(p,t): Data9.iloc[i,j]
            for i, p in enumerate(model.p)
            for j, t in enumerate(model.t)}


Data10 = Production_data.iloc[14:18, 12:16]
pocostV_data = {(p,t): Data10.iloc[i,j]
            for i, p in enumerate(model.p)
            for j, t in enumerate(model.t)}

Data11 = H2Pipline_data.iloc[20:23, 1]
qHmax_data = {(d1): Data11.iloc[i]
            for i, d1 in enumerate(model.d1)}

Data12 = CO2Pipline_data.iloc[49:51, 1]
qCmax_data = {(d2): Data12.iloc[i]
            for i, d2 in enumerate(model.d2)}

Data13 = Storage_data.iloc[59:65, 1]
QImax_data = {(s): Data13.iloc[i]
              for i, s in enumerate(model.s)}

Data14 = Storage_data.iloc[59:65, 4]
QRmax_data = {(s): Data14.iloc[i]
              for i, s in enumerate(model.s)}

Data15 = CO2Reservior_data.iloc[3:7, 4]
rcap_data = {(r):Data15.iloc[i]
             for i, r in enumerate(model.r)}

Data16 = CO2Reservior_data.iloc[12:16, 1]
ri0_data = {(r):Data16.iloc[i]
             for i, r in enumerate(model.r)}

Data17 = Production_data.iloc[50:54, 8]
RD_data = {(p): Data17.iloc[i]
           for i, p in enumerate(model.p)}

Data18 = Storage_data.iloc[36:42, 5]
scap_max_data = {(s): Data18.iloc[i]
                 for i, s in enumerate(model.s)}



rccost = Renewables_data.iloc[3:6, 3:7]
rccost_data = {(e,t): rccost.iloc[i,j]
               for i, e in enumerate(model.e)
               for j, t in enumerate(model.t)}

rocost = Renewables_data.iloc[10:13, 3:7]
rocost_data = {(e,t): rocost.iloc[i,j]
               for i, e in enumerate(model.e)
               for j, t in enumerate(model.t)}

Data19 = Storage_data.iloc[2:8, 1] 
sccost_data = {(s): Data19.iloc[i]
               for i, s in enumerate(model.s)}

Data20 = Storage_data.iloc[14:20, 1]
socostF_data = {(s): Data20.iloc[i]
                for i, s in enumerate(model.s)}

Data21 = Storage_data.iloc[14:20, 7]
socostV_data = {(s): Data21.iloc[i]
                for i, s in enumerate(model.s)}

Data22 = Production_data.iloc[23:27, 1]
Pcap_data = {(p): Data22.iloc[i]
             for i, p in enumerate(model.p)}

Data23 = Storage_data.iloc[25:31, 1]
SCap_data = {(s): Data23.iloc[i]
             for i, s in enumerate(model.s)}

Data24 = Production_data.iloc[50:54, 1]
UT_data = {(p): Data24.iloc[i]
           for i, p in enumerate(model.p)}


Data25 = Biomass_data.iloc[24:29, 2]
Vbio_data = {(t): Data25.iloc[i]
             for i, t in enumerate(model.t)}


df_Demand_data.iloc[:, 1] = df_Demand_data.iloc[:, 1].astype(str).str.strip().astype(int)
WF_data = dict(zip(df_Demand_data.iloc[:, 0], df_Demand_data.iloc[:, 1]))


# -----------------Define Order in Pyomo for some variable ---------------
# %% Making order of set for some equations---------------

region_order = {region: i + 1 for i, region in enumerate(model.g)}
diameter_order1 = {diameter: i + 1 for i, diameter in enumerate(model.d1)}   
diameter_order2 = {diameter: i + 1 for i, diameter in enumerate(model.d2)}          
       
Trans_order = {transLine: i + 1 for i, transLine in enumerate(model.l)}  
Production_order = {production: i+1 for i, production in enumerate(model.p)}
Storage_order = {storage: i+1 for i, storage in enumerate(model.s)}
Cluster_order = {cluster: i+1 for i, cluster in enumerate(model.CC)}

model.ord_g = Param(model.g, initialize=region_order)
model.ord_d1 = Param(model.d1, initialize=diameter_order1)
model.ord_d2 = Param(model.d2, initialize=diameter_order2)

model.ord_l = Param(model.l, initialize=Trans_order)
model.ord_p = Param(model.p, initialize=Production_order)
model.ord_s= Param(model.s, initialize=Storage_order )
model.ord_c = Param(model.CC, initialize=Cluster_order)
# %% Parameters===========================================
model.beta = Param(initialize=0.15, doc='Ratio of stored amount (%)')

# Distance between region and underground storage
model.DistSt = Param(model.g, model.sc, initialize=DistSt_data, doc='distance between region g and underground storage type s')

# CO2 capture and emission coefficients
model.y_c = Param(model.p, model.t, initialize=y_c_data, doc='CO2 capture coefficient for plant type p in time period t (tn CO2 / MWh H2)')
model.y_e = Param(model.p, model.t, initialize=y_e_data,   doc='CO2 emission coefficient for plant type p and size j in time period t (tn CO2 / MWh H2)')


# Pipeline operating cost ratios
model.deltaH = Param(initialize=0.05, doc='Ratio of hydrogen regional pipeline operating costs to capital costs (%)')
model.deltaC_onshore = Param(initialize=0.05, doc='Ratio of onshore CO2 pipeline operating costs to capital costs')
model.deltaC_offshore = Param(initialize=0.05, doc='Ratio of offshore CO2 pipeline operating costs to capital costs')


# Pipeline diameters
model.diaH = Param(model.d1, initialize=diaH_data)
model.diaC_onshore = Param(model.d2, initialize={1: 0.6, 2: 1.2}, doc='Diameter of an onshore CO2 pipeline of diameter size d (m)')
model.diaC_offshore = Param(model.d2, initialize={1: 0.6, 2: 1.2}, doc='Diameter of an offshore CO2 pipeline of diameter size d (m)')

# Hydrogen import ratio
model.iota = Param(initialize=0.1, doc='Maximum percentage of international hydrogen imports over the total demand (%)')

# Time-related parameters
model.dur = Param(initialize=5, doc='Duration of time periods (y)')
model.LTonshore = Param(initialize=50, doc='Useful life of onshore CO2 pipelines (y)')
model.LToffshore = Param(initialize=50, doc='Useful life of offshore CO2 pipelines (y)')
model.LTpipe = Param(initialize=50, doc='Useful life of hydrogen pipelines (y)')
model.a = Param(initialize=365, doc='Days in a year (days)')

model.LTp = Param(model.p, initialize={'SMRCCS':40, 'ATRCCS':40, 'BECCS':30, 'WE':30},doc='Useful life of hydrogen production plants (y)')
model.LTs = Param(model.s, initialize={'OnTeeside':40, 'OnChesire':40, 'OnYorkshire':40, 'OffIrishSea':40, 'MPSV':40, 'HPSV':40}, doc='Useful life of hydrogen storage facilities (y)')
model.LTt = Param(model.l, initialize={'Trailer': 15}, doc='Useful life of hydrogen road transportation modes (y)')



# Biomass parameters
model.br = Param(model.g, initialize=br_data,doc='Parameter for region-specific values')
model.bp = Param( initialize=0.5)
model.cbio = Param(model.TT, initialize=cbio_data, doc='Biomass cost in time period t (€/MWh)')


# Pipeline costs and renewable energy parameters
model.cccH = Param(model.d1, initialize=cccH_data, doc='Capital costs of a regional hydrogen pipeline of diameter size q d (€/k km-1)')
model.cccC_onshore = Param(model.d2, initialize=cccC_onshore_data, doc='Capital costs of an onshore CO2 pipeline of diameter size d (€/k km-1)')
model.cccC_offshore = Param(model.d2, initialize=cccC_offshore_data, doc='Capital costs of an offshore CO2 pipeline of diameter size d (€/k km-1)')
model.cgas = Param(model.t, initialize=cgas_data, doc='Natural gas cost in time period t (€/MWh)')
model.crf = Param(initialize=0.07, doc='Capital recovery factor')

# Start-up and shut-down costs for technologies
model.Cstart = Param(model.p, initialize=Cstart_data, doc='Cost for starting up for each technology type (€/MW)')
model.Cshut = Param(model.p,initialize=Cshut_data, doc='Cost for shutting down for each technology type (€/MW)')

# Carbon tax and demand parameters
model.ct = Param(model.t, initialize=ct_data,doc='carbon tax i time period t (€/kg CO2)')
model.dc = Param(model.t, initialize=dc_data, doc='Demand coefficient at time period t')
#model.dem = Param(model.g, model.t, model.c, model.h, doc='Total hydrogen demand in region g in time period t (MW)')


# Transportation and pipeline parameters
model.dw = Param(model.l, initialize={'Trailer':16.62 }, doc='Driver wage of road transportation mode l (€/h)')
model.DistPipe = Param(model.g, model.g, initialize=DistPipe_data, within=NonNegativeReals, doc='Delivery distance of an onshore CO2 pipeline between regions g and g1 (km)')
model.DistRes = Param(model.g, model.r, initialize=DistRes_data, doc='Distance from CO2 collection point in region g to reservoir r (km)')
model.Dist = Param(model.g, model.g, initialize=Dist_data, doc='Regional delivery distance of hydrogen transportation mode l in region g (km)')


# Technical parameters for plants and pipelines
model.DT = Param(model.p, initialize=DT_data, doc='Min down time (h)')
model.ec = Param(model.t, initialize=ec_data, doc='Cost of electricity back to grid (€/MWe)')
model.eta = Param(model.p, model.t, initialize=eta_data, doc='Efficiency of WE in time period t (%)')
model.emtarget = Param(model.t, initialize=emtarget_data, doc='Emissions target in time period t (kgCO2)')

# Road transportation costs and fuel economy
model.feR = Param(model.l, initialize={'Trailer': 2.3}, doc='Fuel economy of road transportation mode l transporting product type i within a region (km/l)')
model.fp = Param(model.l, initialize={'Trailer': 1.63 }, doc='Fuel price of road transportation mode l (€/l)')
#model.GasDem = Param(model.CC, model.h, model.g,  initialize=GasDem_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')
model.GasDemave = Param(model.CC, model.h, model.t,model.g,  initialize=GasDemave_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')
model.ge = Param(model.l, initialize={'Trailer': 0.25 }, doc='General expenses of road transportation mode l transporting product type i (€/d)')

# Economic parameters
model.ir = Param(initialize=0.06, doc='Discount rate (%)')
model.landAV = Param(model.e, model.g, initialize=landAV_data, doc='Land availability of renewable e in region g (MW)')
model.lut = Param(model.l, initialize={'Trailer':2}, doc='Load and unload time of road transportation mode l (h)')
model.me = Param(model.l, initialize={'Trailer':0.07}, doc='Maintenance expenses of road transportation mode l (€/km)')
model.nel = Param(initialize=30, doc='Economic life cycle of capital investments (y)')

# Initial number of plants and storage units
model.np0 = Param(model.p, model.g, initialize=0, doc='Initial number of hydrogen production plants of technology p and size j in region g')
model.ns0 = Param(model.s, model.g, initialize=0, doc='Initial number of hydrogen storage facilities of type s and size j in region g')

# Production and storage capacity parameters
model.pcap_max = Param(model.p, initialize=Capmax_data, doc='Maximum capacity of a hydrogen production plant of type p and size j (MW)')
model.pcap_min = Param(model.p, initialize=Capmin_data, doc='Minimum capacity of a hydrogen production plant of type p and size j (MW)')
model.pccost = Param(model.p, model.t, initialize=pccost_data, doc='Capital cost of a production plant of type p (€/kW)')
model.pimp = Param(initialize=127.6, doc='Price of hydrogen import (€/MWh)')
model.pocostF = Param(model.p, model.t, initialize=pocostF_data, doc='Operating production cost in a production plant of type p (€/MWh/y)')
model.pocostV = Param(model.p, model.t, initialize=pocostV_data, doc='Operating production cost in a production plant of type p (€/MWh)')

# Flow rate and capacity limits
model.qHmax = Param(model.d1, initialize=qHmax_data, doc='Maximum flow rate in a hydrogen pipeline of diameter size d (kg H2/day)')
model.qCmax = Param(model.d2, initialize=qCmax_data, within=NonNegativeReals, doc='Maximum flow rate in a CO2 pipeline of diameter size d (kg H2/day)')
model.QImax = Param(model.s, initialize=QImax_data, doc='Maximum injection rate for each storage type s')
model.QRmax = Param(model.s, initialize=QRmax_data, doc='Maximum retrieval rate for each storage type s')

# Reservoir-related parameters
model.rcap = Param(model.r, initialize=rcap_data, doc='Total capacity of reservoir r (kg CO2-eq)')
model.ri0 = Param(model.r, initialize=ri0_data, doc='Initial CO2 inventory in reservoir r (kg CO2)')

# Ramp-up and ramp-down parameters
model.RD = Param(model.p, initialize=RD_data, doc='Commit Ramp down')
model.rccost = Param(model.e, model.t, initialize=rccost_data, doc='Renewable e capital cost in time period t (€/MW)')
model.rocost = Param(model.e, model.t, initialize=rocost_data, doc='Renewable e operating cost in time period t (€/MW)')

# Storage parameters
model.RU = Param(model.p, initialize=RD_data, doc='Commit Ramp up', )
model.scap_max = Param(model.s, initialize=scap_max_data, doc='Maximum capacity of a storage facility of type s (MWh H2)')
model.scap_min = Param(model.s, initialize=0, doc='Minimum capacity of a storage facility of type s (MWh H2)')
model.sccost = Param(model.s, initialize=sccost_data, doc='Fixed operating storage cost in a production plant of type p (€/MW/y)')
model.socostF = Param(model.s, initialize=socostF_data, doc='Fixed operating storage cost in a production plant of type p (€/MW/y)')
model.socostV = Param(model.s, initialize=socostV_data, doc='Variable operating storage cost in a production plant of type p (€/kWh stored)')

# Road transportation speed and capacity
model.spR = Param(model.l, initialize={'Trailer': 55}, doc='Regional average speed of road transportation mode l (km/h)')
model.st0 = Param(model.s, model.g, initialize=0, doc='Storage at time 0')
model.tcap = Param(model.l, initialize={'Trailer': 21.66 }, doc='Capacity of road transportation mode l transporting product type i (MWh unit-1)')
model.tmc = Param(model.l, initialize={'Trailer': 253000 }, doc='Capital cost of establishing a road transportation unit of transportation mode l (€/unit)')
model.tmaR = Param(model.l, initialize={'Trailer': 18 }, doc='Regional availability of road transportation mode l (h/day)')

# Unit capacity for production and storage
model.PCap = Param(model.p, initialize=Pcap_data, doc='Unit capacity for production type p (MW)')
model.SCap = Param(model.s, initialize=SCap_data, doc='Unit capacity for storage type s (MW)')

# Initial operating units
model.uInit = Param(model.p, model.g, model.t, initialize=0, doc='Initial operating units type p in region g at time period t')

# Technical parameters for up and down time
model.UT = Param(model.p, initialize=UT_data, doc='Min up time (h)')

# Biomass consumption and cluster weights
model.Vbio_max = Param(model.t, initialize=Vbio_data, doc='Maximum biomass consumption in year t')
#model.WF = Param(model.CC, initialize=WF_data, doc='Weight of clusters')
WF_data_modified = {k: ( round(v * 0.2526) if i >= 1 else v) for i, (k, v) in enumerate(WF_data.items())}
model.WF = Param(model.CC, initialize=WF_data_modified, doc='Weight of clusters')


# ---- Scalar ----
model.y1 = Param(initialize=3, doc="Scalar y1")
model.y2 = Param(initialize=6, doc="Scalar y2")

model.theta = Param(initialize=1, doc="Scalar theta")

# Define a function for initializing the values of dfc
def dfc_init(model, t):
    return round(1 / (1 + model.ir) ** (model.dur * t - model.dur), 2)

model.dfc = Param(model.TT, initialize=dfc_init,  doc='Discount factor for capital costs in time period t')

#model.dfc = Expression(model.t, rule=lambda model, t: round(1 / (1 + model.ir) ** (model.dur * t - model.dur), 2), doc='Discount factor for capital costs in time period t')

def dfo_init(model,t):
    return round(
        1 / (1 + model.ir) ** (model.dur * t - 5) +
        1 / (1 + model.ir) ** (5 * t - 4) +
        1 / (1 + model.ir) ** (5 * t - 3) +
        1 / (1 + model.ir) ** (5 * t - 2) +
        1 / (1 + model.ir) ** (5 * t - 1),
        2
    )
model.dfo= Param(model.TT, initialize=dfo_init)

def biomass_availability_init(model, g, t):
    return model.bp * model.br[g] * model.Vbio_max[t] * 1000000

model.BA = Param(model.g, model.TT, initialize=biomass_availability_init,  doc="Biomass availability in region g and time period t")


#def dem_init(model, g, t, CC, h):
    #return model.dc[t] * model.GasDem[CC, h, g] 
#model.dem = Param(model.g, model.TT, model.CC, model.h, initialize=dem_init)
def dem_init(model, g, t, c, h):
    return model.GasDemave[c, h, t, g]

model.dem = Param(model.g, model.t, model.CC, model.h, initialize=dem_init)


model.Npipe = Set(dimen=2,initialize=model.DistPipe.keys(), doc='Set of region pairs with nonzero pipeline distances')



# %% New sets
# Defining the iteration sets
model.it = Set(initialize=[f'it{i}' for i in range(1, 2)])  # Equivalent to /it1*it8/

# Defining Stage2_it set
#model.phi = Param(initialize=3) 
model.BigQ_neg=Param(model.CC,model.h, model.j, model.TT,model.g, initialize=BigQneg_data)
model.BigQ_pos=Param(model.CC,model.h, model.j, model.TT,model.g, initialize=BigQpos_data)

def dem_stage1(model,it,g,t,c,h):
    return model.dem[g,t,c,h]
model.Stage1_dem=Param(model.it,model.g,model.t,model.CC,model.h, initialize=dem_stage1)
model.iter1 = Set(within=model.it, initialize=[f'it1'])  
#model.iter1 = Set(within=model.it, initialize=[f'it{i}' for i in range(1,2)])  # Empty subset
model.iter_fesi = Set(within=model.it, initialize=[f'it1']) 

# Availability and initial availability parameters
model.AV = Param(model.CC, model.h, model.g, model.e, initialize=AV_data, doc='Availability of renewable e in region g, cluster c and hour h (%)')
model.ayHR0 = Param(model.d1, model.Npipe,initialize=0, doc='Initial availability of a regional hydrogen pipeline of diameter size d between regions g and g1 (0-1)')
model.ayC0 = Param(model.d2, model.N, initialize=0, doc='Initial availability of an onshore CO2 pipeline of diameter size d between regions g and g1 (0-1)')
model.aeC0 = Param(model.r, initialize=0, doc='Initial availability of an offshore CO2 pipeline between collection point in regions g and reservoir r (0-1)')


InvP_bounds = {
    'SMRCCS': 10,
    'ATRCCS': 10,
    'BECCS': 10,
    'WE': 50
}

def InvP_bounds_rule(model, p, g, t):
    if p in InvP_bounds and t in model.TT:
        return (0, InvP_bounds[p]) 
    

InvS_bounds = {
    'MPSV': 80,
    'HPSV': 80}
def InvS_bounds_rule(model, s, g, t):
    if s in InvS_bounds and t in model.TT:
        return (0, InvS_bounds[s])
    elif s in ['OnTeeside', 'OnChesire', 'OnYorkshire', 'OffIrishSea']:
        return (0, 1) 
    return (0, None)  

def NS_bounds_rule(model, s, g, t):
    if s in model.sc and (g, s) in model.GS2 and t in model.TT:
        return (0, 1)  
    else:
        return (0, None)
    
def RI_bounds_rule(model, r, t):
    return (0, model.rcap[r] / 1000)


def Qup_bounds_rule(model, it,l, g, g1,t, c, h):
    if l in ['Pipe']:
        return (0,15343)
    return (0, None)
# %% Variables============================================


model.InvP = Var(model.p, model.g, model.TT, within=NonNegativeIntegers, bounds=InvP_bounds_rule,
                 doc="Investment of new plants of type p producing in region g in time period t")
#.InvP_up = Var(model.p, model.g, model.TT, within=NonNegativeIntegers)
model.InvS = Var(model.s, model.g, model.TT, within=NonNegativeIntegers, bounds=InvS_bounds_rule,
                 doc="Investment of new storage facilities of type in region g in time period t")
#model.InvS_up = Var(model.s, model.g, model.TT,  within=NonNegativeIntegers)
model.Yh = Var(model.d1, model.Npipe, model.TT, within=NonNegativeIntegers,  doc="Establishment of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
model.Yon = Var(model.d2, model.N, model.TT, within=NonNegativeIntegers, 
                doc="Establishment of onshore CO2 pipelines of diameter size d in region g in time period t")
model.Yoff = Var(model.d2, model.GR, model.TT, within=NonNegativeIntegers, 
                 doc="Establishment of offshore CO2 pipelines of diameter size d in region g in time period t")
model.Yst = Var(model.d1, model.GS2, model.TT, within=NonNegativeIntegers, 
                doc="Establishment of hydrogen pipelines of diameter size d in region g in time period d to storage type s")


model.lemma_neg = Var(model.TT, model.g, model.CC, model.h, model.j, within=NonNegativeReals)  # Dual for z ≤ 1
model.lemma_pos = Var(model.TT, model.g, model.CC, model.h, model.j, within=NonNegativeReals)  # Another dual for z ≤ 1
model.gamma = Var(model.TT, model.g, model.CC, model.h, model.j, within=NonNegativeReals)  # Dual for A^Tz ≤ 1
model.xi = Var(model.TT, model.g, model.CC, model.h, within=NonNegativeReals)


# Positive variables
model.NP = Var(model.p, model.g, model.TT, within=NonNegativeReals, doc="Number of plants of type j and size p in region g in time period t")
model.NS = Var(model.s, model.g, model.TT, within=NonNegativeReals, bounds=NS_bounds_rule, doc="Number of storage facilities of type s and size p in region g in time period t")
#model.NS_up = Var(model.s, model.g, model.TT, within=NonNegativeIntegers)
#model.ITU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals, bounds=(0,25), doc="Number of new transportation units of type l for regional transportation byroad in region g to region g acquired in time period t")
#model.NTU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals,   doc="Number of transportation units of type l for regional transportation by road in region g in time period t")
model.AY = Var(model.d1, model.Npipe, model.TT, within=NonNegativeReals,  doc="availability of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
model.AYon=Var(model.d2, model.N, model.TT, within=NonNegativeReals,  doc="availability of onshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
model.AYoff = Var(model.d2, model.GR, model.TT, within=NonNegativeReals,  doc="availability of offshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
model.AYst = Var(model.d1, model.GS2, model.TT, within=NonNegativeReals,  doc="availability of hydrogen pipelines of diameter size d for distribution in region g in time period t")
model.CL = Var(model.it, model.g, model.TT, model.CC, model.HH, within=NonNegativeReals, doc='Curtailment (MW)')
model.InvR = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000), doc='Invested capacity of renewable (MW)')
#model.InvR_up = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000))
model.IMP = Var(model.it,model.g, model.TT, model.CC, model.h, within=NonNegativeReals,
                doc='Flow rate of international import (MW)')
model.NR = Var(model.e, model.g, model.TT, within=NonNegativeReals,  doc='Capacity of renewable (MW)')
model.Pr = Var(model.it,model.p, model.g, model.TT, model.CC,model.HH,within=NonNegativeReals,      doc='Production rate (MW)')
model.Pre = Var(model.it, model.e, model.g, model.TT, model.CC, model.HH, within=NonNegativeReals,    doc='Electricity production from renewable (MW)')
model.Q = Var(model.it,model.l, model.Npipe, model.TT, model.CC, model.HH, within=NonNegativeReals, bounds=Qup_bounds_rule, doc='Regional flowrate of H2 (MWh)')
model.Qi = Var(model.it,model.g,model.s, model.TT, model.CC,model.HH, within=NonNegativeReals,  doc='H2 via pipeline to storage (MWh)')
model.Qr = Var(model.it,model.s, model.g, model.TT, model.CC, model.HH, within=NonNegativeReals,  doc= 'flowrate of H2 via pipeline from region g to storage type s in time period t(MWh)')
model.Qon = Var(model.it,model.N, model.TT, model.CC, model.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via onshore pipelines (kg CO2/d)')
model.Qoff = Var(model.it,model.GR, model.TT, model.CC, model.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via offshore pipelines (kg CO2/d)')
#odel.Rdown = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals,initialize=0, doc='Upward reserve contribution (MWh)')
#odel.Rup = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Downward reserve contribution (MWh)')
model.St = Var(model.it,model.s,model.g, model.TT, model.CC, model.HH, within=NonNegativeReals, doc='Average inventory of product stored (kW)')
model.Vbio = Var(model.TT, within=NonNegativeReals,  doc='Biomass consumption (kg)' )
model.Vgas = Var(model.TT, within=NonNegativeReals, doc='Gas consumption (kg)')
#model.slak1 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 1')
#model.slak2 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 2')
model.PCC = Var()
model.SCC = Var()
model.TCC=Var()
model.POC1 = Var()
model.POC2 = Var(model.it)
model.SOC1 = Var()
model.SOC2 = Var(model.it)

model.RI = Var(model.r, model.TT,  within=NonNegativeReals, bounds=RI_bounds_rule)
#model.RI_up = Var(model.r, model.TT, within=NonNegativeReals)
#model.TC = Var()
#model.RCC = Var()
model.FCR = Var()
model.GCR = Var()
model.LCR = Var()
model.MCR = Var()
model.PipeOC = Var()
model.PipeCC = Var()
model.CEC = Var(model.it)
model.IIC = Var(model.it)
model.ReC = Var()
model.GC = Var(model.it)
model.BC = Var(model.it)
model.ROC = Var(model.it)
model.TOC=Var()
model.em = Var(model.TT, within=Reals)
model.Stage1_eta=Var()
model.Stage2_TC=Var()
# %% The initial objective function with all continous variables
# Constraint for PCC
def pcc_rule(model):
    return 0.001*model.PCC == 0.001*sum(
        model.dfc[t] * model.pccost[p, t] * model.PCap[p] * model.InvP[p, g, t]
        for p in model.p for g in model.g for t in model.TT
    )
model.PCCConstraint = Constraint(rule=pcc_rule)

# Constraint for SCC
def scc_rule(model):
    return 0.001*model.SCC ==  0.001*sum(
        model.dfc[t] * model.sccost[s] * model.SCap[s] * model.InvS[s, g, t]
       for s in model.s  for g in model.g if  (g, s) in model.GS for t in model.TT
    )
model.SCCConstraint = Constraint(rule=scc_rule)

# Constraint for PipeCC (Pipeline Capital Cost)
def pipecc_rule(model):
    return model.PipeCC == (sum(
        # First summation: Hydrogen pipeline cost
        model.dfc[t] * model.cccH[d1] * model.DistPipe[g, g1] * model.Yh[d1, (g, g1), t]
        for d1 in model.d1 if model.ord_d1[d1]==3
        for g in model.g
        for g1 in model.g
        if (g, g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1] 
        for t in model.TT
    ) + sum(
        # Second summation: Onshore CO2 cost
        model.dfc[t] * model.cccC_onshore[d2] * model.Dist[g, g1] * model.Yon[d2, (g, g1), t]
        for d2 in model.d2 if model.ord_d2[d2]==2
        for g in model.g
        for g1 in model.g
        if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]
        for t in model.TT
    ) + sum(
        # Third summation: Offshore CO2 cost
        model.dfc[t] * model.cccC_offshore[d2] * model.DistRes[g, r] * model.Yoff[d2, (g, r), t]
        for d2 in model.d2 if model.ord_d2[d2]==2
        for g in model.g
        for r in model.r
        if (g, r) in model.GR
        for t in model.TT
    ) + sum(
        # Fourth summation: Storage cost
        model.dfc[t] * model.cccH[d1] * model.DistSt[g, sc] * model.Yst[d1, (g, sc), t]
        for d1 in model.d1 if model.ord_d1[d1]==3
        for g in model.g
        for sc in model.sc
        if (g, sc) in model.GS2
        for t in model.TT
    ))
model.PipeCCConstraint = Constraint(rule=pipecc_rule)

# Constraint for PipeOC
def pipeoc_rule(model):
    return model.PipeOC == (sum(
        model.dfo[t] * model.deltaH * model.crf * model.cccH[d1] * model.DistPipe[g, g1] * model.AY[d1, (g, g1), t]
        for d1 in model.d1 if model.ord_d1[d1]==3
        for g in model.g 
        for g1 in model.g 
        if (g, g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1]
        for t in model.TT
    ) + sum(
        model.dfo[t] * model.deltaC_onshore * model.crf * model.cccC_onshore[d2] * model.Dist[g, g1] * model.AYon[d2, (g, g1), t]
        for d2 in model.d2 if model.ord_d2[d2]==2
        for g in model.g 
        for g1 in model.g 
        if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]
        for t in model.TT
    ) + sum(
        model.dfo[t] * model.deltaC_offshore * model.crf * model.cccC_offshore[d2] * model.DistRes[g, r] * model.AYoff[d2, (g, r), t]
        for d2 in model.d2 if model.ord_d2[d2]==2
        for g in model.g 
        for r in model.r if (g, r) in model.GR 
        for t in model.TT
    ) + sum(
        model.dfo[t] * model.deltaH * model.crf * model.cccH[d1] * model.DistSt[g, sc] * model.AYst[d1, (g, sc), t]
        for d1 in model.d1 if model.ord_d1[d1]==3
        for g in model.g 
        for sc in model.sc if (g, sc) in model.GS2 
        for t in model.TT
    ))
model.PipeOCConstraint = Constraint(rule=pipeoc_rule)


# Constraint for POC
def poc_rule(model):
    return 0.001*model.POC1 == 0.001*sum(
        model.dfo[t] * (
            model.pocostF[p, t] * model.PCap[p] * model.NP[p, g, t] 
            
        )
        for p in model.p for g in model.g for t in model.TT
    )
model.POCConstraint = Constraint(rule=poc_rule)

# Constraint for SOC
def soc_rule(model):
    return 0.001*model.SOC1 == 0.001* sum(
        model.dfo[t] * (
            model.socostF[s] * model.SCap[s] * model.NS[s, g, t] 
            
        )
        for s in model.s for g in model.g if (g, s) in model.GS for t in model.TT
    )
model.SOCConstraint = Constraint(rule=soc_rule)

# Constraint for ReC
def rec_rule(model):
    return model.ReC == sum(
        model.dfc[t] * model.rccost[e, t]* model.InvR[e, g, t] +
        model.dfo[t] * model.rocost[e, t] * model.NR[e, g, t]
        for t in model.TT for e in model.e for g in model.g
    )
model.ReCConstraint = Constraint(rule=rec_rule)




def POCeq2_rule(model, iter_fesi):
    return 0.001*model.POC2[iter_fesi] == 0.001*sum(
        model.dfo[t] * model.WF[c] * model.pocostV[p, t] * model.theta * model.Pr[iter_fesi, p, g, t, c, h]
        for p in model.p for g in model.g for t in model.TT for c in model.CC for h in model.HH
    )
model.POC2Constraint=Constraint(model.iter_fesi,rule=POCeq2_rule)        


def SOCeq2_rule(model, iter_fesi):
    return 0.001*model.SOC2[iter_fesi] == 0.001*sum(
        model.dfo[t] * model.WF[c] * model.socostV[s] * model.theta * model.Qi[iter_fesi, g, s, t, c, h]
        for s in model.s for g in model.g if (g, s) in model.GS for t in model.TT for c in model.CC for h in model.HH
        
    )
model.SOC2Constraint=Constraint(model.iter_fesi,rule=SOCeq2_rule)        


def CECeq_rule(model, iter_fesi):
    return model.CEC[iter_fesi] == sum(
        model.WF[c] * model.dfo[t] * model.ct[t] * model.y_e[p, t] * model.theta * model.Pr[iter_fesi, p, g, t, c, h]
        for p in model.p for g in model.g for t in model.TT for c in model.CC for h in model.HH
        
    )

model.CECConstraint=Constraint(model.iter_fesi,rule=CECeq_rule)        

def IICeq_rule(model, iter_fesi):
    return model.IIC[iter_fesi] == sum(
        model.WF[c] * model.dfo[t] * model.pimp * model.theta * model.IMP[iter_fesi, g, t, c, h]
        for g in model.Gimp for t in model.TT for c in model.CC for h in model.HH
    )
model.IICConstraint=Constraint(model.iter_fesi,rule=IICeq_rule)        

def GasCost_rule(model, iter_fesi):
    return model.GC[iter_fesi] == sum(
        model.dfo[t] * model.cgas[t] * model.WF[c] * model.theta * model.Pr[iter_fesi, p, g, t, c, h] / model.eta[p, t]
        for g in model.g for p in model.p for c in model.CC for h in model.HH for t in model.TT if model.ord_p[p] <= 2 
    )
model.GasCosConstraint=Constraint(model.iter_fesi,rule=GasCost_rule)        

def BioCost_rule(model, iter_fesi):
    return model.BC[iter_fesi] == sum(
        model.dfo[t] * model.cbio[t] * model.WF[c] * model.theta * model.Pr[iter_fesi, 'BECCS', g, t, c, h] / model.eta['BECCS', t]
        for g in model.g for c in model.CC for h in model.HH for t in model.TT
    )
model.BioCosConstraint=Constraint(model.iter_fesi,rule=BioCost_rule)        

def stage1_eta_rule(model,iter_fesi):
    return model.Stage1_eta >= model.POC2[iter_fesi]+model.SOC2[iter_fesi]+model.CEC[iter_fesi]+model.IIC[iter_fesi]+model.GC[iter_fesi]+model.BC[iter_fesi]
model.etaconstraint = Constraint(model.iter_fesi,rule=stage1_eta_rule) 


def objective1_rule(model):
    return (
        1000*model.PCC+ 
        model.SCC+ 
        1000*model.PipeCC+ 
        model.POC1+ 
        model.SOC1+ 
        1000*model.PipeOC+ 
        model.ReC+
        model.Stage1_eta 
    )   
                  
model.Stage1_TC = Objective(rule=objective1_rule, sense=minimize)



# %%
# HA2 Monolithic Version


def flow_balance_rule(model, iter1,g, t, c, h):
    return (
        sum(model.Pr[iter1, p, g, t, c, h] for p in model.p) +
        sum(model.Q[iter1,'Pipe', g1, g, t, c, h] for g1 in model.g if (g1, g) in model.Npipe) +
        (model.IMP[iter1,g, t, c, h] if g in model.Gimp else 0) +
        sum(model.Qr[iter1,s, g, t, c, h] for s in model.s if (g, s) in model.GS)
        ==
        sum(model.Q[iter1,'Pipe', g, g1, t, c, h] for g1 in model.g if (g, g1) in model.Npipe) +
        sum(model.Qi[iter1,g, s, t, c, h] for s in model.s if (g, s) in model.GS) +
        model.Stage1_dem[iter1,g, t, c, h]
    )

model.FlowBalance = Constraint(model.iter1, model.g, model.TT, model.CC, model.HH, rule=flow_balance_rule)



# Co2 Balanace
def co2_mass_balance_rule(model, iter1,g, t, c, h):
    if t in model.TT and c in model.CC and h in model.HH:
        return (
            sum(model.Qon[iter1,g1, g, t, c, h] for g1 in model.g if (g1, g) in model.N) +
            sum(model.y_c[p, t] * model.Pr[iter1,p, g, t, c, h] for p in model.p)
         == 
            sum(model.Qon[iter1,g, g1, t, c, h] for g1 in model.g if (g, g1) in model.N) +
            sum(model.Qoff[iter1,g, r, t, c, h] for r in model.r if (g, r) in model.GR)
        )
    return Constraint.Skip

model.CO2MassBalanceConstraint = Constraint(model.iter1,model.g, model.TT, model.CC, model.HH, rule=co2_mass_balance_rule)

def biomass_availability_rule(model, iter1,g, t):
    if t in model.TT:  # Apply the constraint only for TT(t)
        return sum(
            model.WF[c] * model.theta * model.Pr[iter1,'BECCS', g, t, c, h] / model.eta['BECCS', t]
            for c in model.CC for h in model.HH
        ) <=  model.BA[g,t]
    return Constraint.Skip

model.BiomassAvailabilityConstraint = Constraint(model.iter1,model.g, model.TT, rule=biomass_availability_rule)

#%% 
# Ramp Up
def ramp_up_rule(model, iter1,p, g, c, h, t):
    if t in model.TT and c in model.CC and h in model.HH and h > 1:
        return model.Pr[iter1,p, g, t, c, h] - model.Pr[iter1,p, g, t, c, h - 1] <=model.theta * model.RU[p] * model.PCap[p] * model.NP[p, g, t]
    return Constraint.Skip

model.RampUpConstraint = Constraint(model.iter1,model.p, model.g, model.CC, model.HH, model.TT, rule=ramp_up_rule)


# Ramp Down
def ramp_down_rule(model, iter1,p, g, c, h, t):
    if t in model.TT and c in model.CC and h in model.HH and h > 1:
        return model.Pr[iter1,p, g, t, c, h - 1] - model.Pr[iter1,p, g, t, c, h] <= model.theta * model.RD[p] * model.PCap[p] * model.NP[p, g, t]
    return Constraint.Skip

model.RampDownConstraint = Constraint(model.iter1,model.p, model.g, model.CC, model.HH, model.TT, rule=ramp_down_rule)

# %%  Peoduction Limit ---------------------------
# Production Limit

def p_capacity2_rule(model, iter1,p, g, t, c, h):
    if t in model.TT and c in model.CC and h in model.HH:
        return model.Pr[iter1,p, g, t, c, h] <= model.PCap[p] * model.pcap_max[p] * model.NP[p, g, t]
    return Constraint.Skip

model.PCapacity2Constraint = Constraint(model.iter1, model.p, model.g, model.TT, model.CC, model.HH, rule=p_capacity2_rule)

def p_availability_rule(model, p, g, t):
     if t in model.TT:
      return model.NP[p, g, t] == (
            model.NP[p, g, t-1] if t>model.y1 else 0 
        )+( 
        model.np0[p, g] if t==model.y1 else 0
        )+ model.InvP[p, g, t] 
     return Constraint.Skip

model.PAvailability = Constraint(model.p, model.g, model.TT, rule=p_availability_rule)
#%% Storage
def sinventory2_rule(model, iter1,s, g, t, c, h):
    if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
        return model.St[iter1,s, g, t, c, h] == (
            (model.St[iter1,s, g, t, c, h - 1] if h > 1 else model.st0[s, g]) 
            + model.theta * (model.Qi[iter1,g, s, t, c, h] - model.Qr[iter1,s, g, t, c, h])
        )
    return Constraint.Skip
model.SInventory2 = Constraint(model.iter1,model.s, model.g, model.TT, model.CC, model.HH, rule=sinventory2_rule)


# Maximum injection rate
def max_inj_rule(model, iter1,s,g,t, c, h):
    if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
        return model.Qi[iter1,(g, s), t, c, h] <= model.QImax[s] * model.NS[s, g, t]
    return Constraint.Skip

model.MaxInjConstraint = Constraint( model.iter1,model.GS, model.TT, model.CC, model.HH, rule=max_inj_rule)


# Maximum retrieval rate
def max_retr_rule(model, iter1,s, g, t, c, h):
    if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
        return model.Qr[iter1,s, g, t, c, h] <= model.QRmax[s] * model.NS[s, g, t]
    return Constraint.Skip
model.MaxRetrConstraint = Constraint(model.iter1,model.s,model.g, model.TT, model.CC, model.HH, rule=max_retr_rule)

# Underground storage capacity
def s_capacity_u_rule(model,sc, g, t, c, h):
    if (g,sc) in model.GS2 and t in model.TT and c in model.CC and h in model.HH:
        return model.InvS[sc, g, t] <= sum(model.Yst[d1, g, sc, t] for d1 in model.d1)
    return Constraint.Skip

model.SCapacityUConstraint = Constraint(model.GS2, model.TT, model.CC, model.HH, rule=s_capacity_u_rule)


# Storage capacity constraints
def s_capacity1_rule(model, iter1,s, g, t, c, h):
    if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
        return model.St[iter1,s, g, t, c, h] >= model.SCap[s] * model.scap_min[s] * model.NS[s, g, t]
    return Constraint.Skip

model.SCapacity1Constraint = Constraint(model.iter1,model.s,model.g, model.TT, model.CC, model.HH, rule=s_capacity1_rule)

def s_capacity2_rule(model, iter1, s, g, t, c, h):
    if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
        return model.St[iter1,s, g, t, c, h] <= model.SCap[s] * model.scap_max[s] * model.NS[s, g, t]
    return Constraint.Skip

model.SCapacity2Constraint = Constraint(model.iter1,model.s,model.g, model.TT, model.CC, model.HH, rule=s_capacity2_rule)



# Storage facility availability

def savailability_rule(model, s, g, t):
    if (g, s) in model.GS and t in model.TT:
        return model.NS[s, g, t] == (
            (model.NS[s, g, t - 1] if t > model.y1 else model.ns0[s, g])
            + model.InvS[s, g, t]
        )
    return Constraint.Skip

model.SAvailability = Constraint(model.s, model.g, model.TT, rule=savailability_rule)


# Final storage
def s_final_rule(model, iter1,s, g, t, c):
    if (s, g) in model.GS and t in model.TT and c in model.CC:
        return model.St[iter1,(s, g), t, c, '24'] == 0
    return Constraint.Skip

model.SFinalConstraint = Constraint(model.iter1,model.s,model.g, model.TT, model.CC, rule=s_final_rule)


# %%  RENEWABLES CONSTRAINTS ---------------------
# Electricity production for electrolysis
def elec_prod_rule(model, iter1,g, t, c, h):
        return model.Pr[iter1,'WE', g, t, c, h] == model.eta['WE', t] * (
            sum(model.Pre[iter1,e, g, t, c, h] for e in model.e) - model.CL[iter1,g, t, c, h]
        )

model.ElecProdConstraint = Constraint(model.iter1,model.g, model.TT, model.CC, model.HH, rule=elec_prod_rule)


# Renewables availability
def renew_av_rule(model, iter1,e, g, t, c, h):
    if t in model.TT and c in model.CC and h in model.HH:
        return model.Pre[iter1,e, g, t, c, h] ==  0.7*model.AV[c, h, g, e] * model.NR[e, g, t]

model.RenewAvConstraint = Constraint(model.iter1,model.e, model.g, model.TT, model.CC, model.HH, rule=renew_av_rule)



def renew_cap_rule(model, e, g, t):
    if t in model.TT:
            return model.NR[e, g, t] == (model.NR[e, g, t - 1] if t >model.y1 else 0)+ model.InvR[e, g, t]
    return Constraint.Skip

model.RenewCapConstraint = Constraint(model.e, model.g, model.TT, rule=renew_cap_rule)


def land_availability_rule(model, e, g, t):
    if t in model.TT:
        return model.NR[e, g, t] <= model.landAV[e, g]
    return Constraint.Skip

model.LandAvailabilityConstraint = Constraint(model.e, model.g, model.TT, rule=land_availability_rule)

'''
def curtailment_limit_rule(model, iter1,c, h):
    if c in model.CC and h in model.HH:
        return sum(model.CL[iter1,g, t, c, h] for g in model.g for t in model.TT) <= 0.1 * sum(model.Pre[iter1,e, g, t, c, h] for e in model.e for g in model.g for t in model.TT)
    return Constraint.Skip

model.CurtailmentLimitConstraint = Constraint(model.iter1,model.CC, model.HH, rule=curtailment_limit_rule)
'''
# %%  RESERVIORS Constraints ---------------------
# Inventory
def res_inventory_rule(model, iter1,r, t):
    if t in model.TT: 
      return model.RI[r, t] == (model.RI[r, t - 1] if t>model.y1 else  model.ri0[r] / 1000)+ model.dur * sum(
        model.WF[c] * model.theta * model.Qoff[iter1,(g, r), t, c, h] for g in model.g if 
        (g, r) in model.GR  for c in model.CC for h in model.HH
         ) / 1000
   

model.ResInventoryConstraint = Constraint(model.iter1,model.r, model.TT, rule=res_inventory_rule)

# %%  Hydrogen Import Limit ----------------------
# Import limit
def imp_limit_rule(model, iter1,t, c, h):
    if t in model.TT and c in model.CC and h in model.HH:
        return sum(model.IMP[iter1, g, t, c, h] for g in model.Gimp) <= 0.1*sum(model.GasDemave[c,h, t, g] for g in model.g)
    return Constraint.Skip
model.ImpLimitConstraint = Constraint(model.iter1,model.TT, model.CC, model.HH, rule=imp_limit_rule)

# %%  Emission Target Limit ----------------------
# Emissions target
def em_target_rule(model, iter1,t):
    if t in model.TT:
        return  0.001*sum(
            model.WF[c] * model.y_e[p, t] * model.theta * model.Pr[iter1,p, g, t, c, h]
            for p in model.p
            for g in model.g
            for c in model.CC
            for h in model.HH
        ) <=0.001*model.emtarget[t]
    return Constraint.Skip
model.EmissionConstraint = Constraint(model.iter1,model.TT, rule=em_target_rule)

# %%  PIPELINE CONSTRAINTS------------------------
#------Hydrogen Pipeline Limit ------

# Maximum flowrate for pipelines
'''
def h2pipe_max_rule(model, iter1,g, g1, t, c, h):
    if (g, g1) in model.Npipe:
        return model.Q[iter1,'Pipe', (g, g1), t, c, h] <= sum(model.qHmax[d1] * (
            (model.AY[d1, (g, g1), t] if model.ord_g[g] < model.ord_g[g1] else 0)+
            (model.AY[d1, (g1, g), t] if model.ord_g[g1] < model.ord_g[g] else 0) 
            )
            for d1 in model.d1 if model.ord_d1[d1]==3 )
    return Constraint.Skip

model.H2PipeMax = Constraint(model.iter1,model.Npipe, model.TT, model.CC, model.HH, rule=h2pipe_max_rule)



def onshorepipe_max_rule(model, iter1,g, g1, t, c, h):
    if (g, g1) in model.N:
        return model.Qon[iter1,g, g1, t, c, h] <= sum(model.qCmax[d2] * (
                (model.AYon[d2, g, g1, t] if model.ord_g[g] < model.ord_g[g1] else 0) +
                (model.AYon[d2, g1, g, t] if model.ord_g[g1] < model.ord_g[g] else 0)
            )
            for d2 in model.d2 if model.ord_d2[d2]==2
        )
    return Constraint.Skip

model.OnshorePipeMax = Constraint(model.iter1,model.N, model.TT, model.CC, model.HH, rule=onshorepipe_max_rule)




def offshorepipe_max_rule(model, iter1,g, r, t, c, h):
    if (g, r) in model.GR:
        return model.Qoff[iter1,(g, r), t, c, h]  <= sum(model.qCmax[d2] * model.AYoff[d2, (g, r), t] for d2 in model.d2 if model.ord_d2[d2]==2)
    return Constraint.Skip
model.OffshorePipeMax = Constraint(model.iter1,model.GR, model.TT, model.CC, model.HH, rule=offshorepipe_max_rule)

'''
# Availability of pipelines
def H2PAvailability_rule(model, d1, g, g1, t):
    if (g,g1) in model.Npipe and t in model.TT and model.ord_g[g] < model.ord_g[g1] and model.ord_d1[d1]==3:
        return model.AY[d1, g, g1, t] == (
            model.AY[d1, g, g1, t - 1] if t > model.y1 else 0
        ) + (model.ayHR0[d1, g, g1] if t == model.y1 else 0) + model.Yh[d1, g, g1, t]
    return Constraint.Skip

model.H2PAvailability = Constraint(model.d1, model.Npipe, model.TT, rule=H2PAvailability_rule)


def onp_availability_rule_simple(model, d2, g, g1, t):
       if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1] and model.ord_d2[d2]==2:
            return model.AYon[d2, (g, g1), t] == (
                model.AYon[d2, (g, g1), t - 1] if t>model.y1 else 0
                )+ (model.ayC0[d2, (g, g1)] if t ==model.y1 else 0 ) + model.Yon[d2, (g, g1), t]
       return Constraint.Skip
model.OnPAvailability = Constraint(model.d2, model.N, model.TT, rule=onp_availability_rule_simple)


def offp_availability_rule(model, d2, g, r, t):
     if (g, r) in model.GR and t in model.TT and model.ord_d2[d2]==2: 
         return model.AYoff[d2, (g, r), t] == (
             model.AYoff[d2, (g, r), t-1] if t> model.y1 else 0
             )+ (model.aeC0[r] if t==model.y1 else 0) + model.Yoff[d2, (g, r), t]
     return Constraint.Skip

model.OffPAvailability = Constraint(model.d2, model.GR, model.TT, rule=offp_availability_rule)

def pipest_availability_rule(model, d1, g, sc, t):
      if (g, sc) in model.GS2 and t in model.TT and model.ord_d1[d1]==3: 
           return model.AYst[d1, (g, sc), t] == (
               model.AYst[d1, g, sc, t-1]  if t>model.y1 else 0)+ model.Yst[d1, (g, sc), t]
      return Constraint.Skip
model.PipeStAvailability = Constraint(model.d1, model.GS2, model.TT, rule=pipest_availability_rule)





# %% Maxmic Problem
from pyomo.environ import *
from pyomo.opt import SolverFactory
model2 = ConcreteModel()

# ---------------------------------Define Main and Additional Sets and Subsets ------------------------------

l_data = Sets_data.iloc[1, 2:4].values
g_data = Sets_data.iloc[2, 2:15].values 
p_data = Sets_data.iloc[3, 2:6].values
r_data = Sets_data.iloc[4, 2:6].values
s_data = Sets_data.iloc[5, 2:8].values
t_data = Sets_data.iloc[6, 2:8].values
d_data = Sets_data.iloc[7, 2:5].values
c_data = Sets_data.iloc[8, 2:4].values
h_data = Sets_data.iloc[9, 2:26].values
sc_data = Sets_data.iloc[10, 2:6].values
sv_data = Sets_data.iloc[11, 2:4].values
e_data = Sets_data.iloc[12, 2:5].values
I_data = Sets_data.iloc[1, 2:4].values
region1_data = Regions_data.iloc[2:48, 2].values
region2_data = Regions_data.iloc[2:48, 3].values
Neighbourhood_Regions = list(zip(region1_data,region2_data))

model2.l = Set(initialize=['Trailer', 'Pipe'])
model2.g = Set(initialize=g_data)
model2.g1 = Set(initialize=g_data)
model2.p = Set(initialize=p_data)
model2.r = Set(initialize=r_data)
model2.s = Set(initialize=s_data)
model2.t = Set(initialize=[3,4,5,6])#t_data)
model2.d1 = Set(initialize=d_data)
model2.d2 = Set(initialize=[1, 2])
model2.c = Set(initialize=c_data)
model2.h = Set(initialize=h_data)
model2.sc= Set(initialize=sc_data)
model2.sv= Set(initialize=sv_data)
model2.e = Set(initialize=e_data)
model2.j = RangeSet(1,24)

Region3_data = Regions_data.iloc[6:32, 17].values
storage_data = Regions_data.iloc[6:32, 18].values


Region4_data = Regions_data.iloc[2:32, 17].values
storage1_data = Regions_data.iloc[2:32, 18].values

GS_data = list(zip(Region4_data, storage1_data))
GS_data1 = list(zip(Region3_data, storage_data))
GS_data2 = [('NO', 'OnTeeside'), ('NW', 'OnChesire'), ('NE', 'OnYorkshire'), ('NW', 'OffIrishSea')]

model2.GS = Set(dimen=2, initialize=[(g,s) for g in model2.g for s in model2.s if (g,s) in GS_data])

model2.GS1 = Set(dimen=2, initialize=[(g,sv) for g in model2.g for sv in model2.sv if (g,sv) in GS_data1])
model2.GS2 = Set(dimen=2, initialize=[(g,sc) for g in model2.g for sc in model2.sc if (g,sc) in GS_data2])
Gimp_data = [(g_data[9]), (g_data[11]), (g_data[2]), (g_data[0])]
model2.Gimp = Set(within=model2.g, initialize= ['WS', 'SO', 'NO', 'NE', 'SC'])
#model.Gimp = Set(initialize=[(g) for g in model.g if (g) in Gimp_data])
GR_data=[(g_data[0], r_data[2]), (g_data[5], r_data[3]), (g_data[6], r_data[0])]
model2.GR = Set(dimen=2, initialize=[(g,r) for g in model2.g for r in model2.r if (g,r) in GR_data])
model2.N = Set(dimen=2, initialize=[(g,g1) for g in model2.g for g1 in model2.g if (g,g1) in Neighbourhood_Regions])


# Aliases
model2.gg = Set(dimen=2, initialize=lambda model: [(g,g1) for g in model2.g for g1 in model2.g])
model2.hh = Set(dimen=2, initialize=lambda model: [(h,h1) for h in model2.h for h1 in model2.h])


# ------ RangeSets -----

model2.TT = RangeSet(3, 6)  #  TT(t) /3*6/
model2.CC = RangeSet(1,n_clusters+1)  #  CC(c) /1*6/
model2.HH = RangeSet(1, 24) #  HH(h) /1*24/

# %% #---------------------------------------Assign spacific data for parameters--------------------------
DistSt_data = {(g, s): df_DistSt.iloc[i,2] 
          for i, g in enumerate(df_DistSt.iloc[:, 0])
          for j, s in enumerate(df_DistSt.iloc[:, 1])
          if i==j}

Data1 = Emissions_data.iloc[30:34, 3:7]
y_c_data = {(p,t): Data1.iloc[i,j]
            for i, p in enumerate(model2.p)
            for j, t in enumerate(model2.TT)}

Data2 = Emissions_data.iloc[21:25, 3:7]
y_e_data = {(p,t): Data2.iloc[i,j]
            for i, p in enumerate(model2.p)
            for j, t in enumerate(model2.t)}

diaH_data1 = H2Pipline_data.iloc[9:12, 1]
diaH_data = {(d1): diaH_data1.iloc[i]
             for i, d1 in enumerate(model2.d1)}

AV_data = {
        (int(c), int(h), g, e): df_Availability.iloc[i,  1+idx]  # مقدار برداشته شده از دیتا فریم
        for i, pair in enumerate(df_Availability.iloc[:, 0])  # جفت‌های (c, h) از ستون اول
        for idx, (g, e) in enumerate([(g, e) for g in model.g for e in model.e])  # ترکیب‌های مختلف g و e
        for c, h in [map(int, pair.strip("()").split(","))]  # تبدیل جفت (c, h) به مقادیر عددی
    }
'''
AV_data = {(c, h, g, e): df_Sheet1.iloc[i, 2 + 3 * g_idx + e_idx]
    for i, (c, h) in enumerate(zip(df_Sheet1.iloc[:, 0], df_Sheet1.iloc[:, 1]))  
    for g_idx, g in enumerate(model.g)  
    for e_idx, e in enumerate(model.e)}
'''
df_Biomass.iloc[:, 0] = df_Biomass.iloc[:, 0].str.strip().str.upper()
br_data = dict(zip(df_Biomass.iloc[:, 0], df_Biomass.iloc[:, 1]))

cbio_data = dict(zip(df_bio.iloc[:, 0], df_bio.iloc[:, 1]))

cccH_data = dict(zip(df_cccH.iloc[:, 0], df_cccH.iloc[:, 1]))
cccC_onshore_data = dict(zip(df_cccC_Onshore.iloc[:, 0], df_cccC_Onshore.iloc[:, 1]))
cccC_offshore_data = dict(zip(df_cccC_offshore.iloc[:, 0], df_cccC_offshore.iloc[:, 1]))

cgas_data = dict(zip(df_cgas.iloc[:,0], df_cgas.iloc[:,1]))

df_Cstart.iloc[:, 0] = df_Cstart.iloc[:, 0].str.strip().str.upper()
Cstart_data = dict(zip(df_Cstart.iloc[:, 0], df_Cstart.iloc[:, 1]))

df_Cshut.iloc[:, 0] = df_Cshut.iloc[:, 0].str.strip().str.upper()
Cshut_data = dict(zip(df_Cshut.iloc[:, 0], df_Cshut.iloc[:, 1]))

df_transposed= df_ct.T
df_transposed.columns = ['key', 'value']
ct_data = dict(zip(df_transposed['key'], df_transposed['value']))

dc_data = dict(zip(df_dc.iloc[:,0], df_dc.iloc[:,1]))
'''
DistPipe_data = {
    (g_row, g_col): df_DistPipe.iloc[i, j]
    for i, g_row in enumerate(model.g)
    for j, g_col in enumerate(model.g)}
'''
DistPipe_data = {
    (g_row, g_col): df_DistPipe.iloc[i, j]
    for i, g_row in enumerate(model2.g)
    for j, g_col in enumerate(model2.g)
    if df_DistPipe.iloc[i, j] > 0  
}


DistRes_data = {(g, r): df_DistRes.iloc[i,2] 
          for i, g in enumerate(df_DistRes.iloc[:, 0])
          for j, r in enumerate(df_DistRes.iloc[:, 1])
          if i==j}


Dist_data = {
    (g_row, g_col): df_Dist.iloc[i, j]
    for i, g_row in enumerate(model2.g)
    for j, g_col in enumerate(model2.g) 
    if df_Dist.iloc[i, j] > 0}
    

DT_data = dict(zip(df_DT.iloc[:, 0], df_DT.iloc[:, 1]))
df_ec_transposed= df_ec.T
df_ec_transposed.columns = ['key', 'value']
ec_data = dict(zip(df_ec_transposed['key'], df_ec_transposed['value']))

Data4 = Production_data.iloc[69:73, 3:7]
eta_data = {(p,t): Data4.iloc[i,j]
            for i, p in enumerate(model2.p)
            for j, t in enumerate(model2.t)}

df_emtarget_transposed= df_emtarget.T
df_emtarget_transposed.columns = ['key', 'value']
emtarget_data = dict(zip(df_emtarget_transposed['key'], df_emtarget_transposed['value']))



GasDemave_data = {(c, h,t, g): df_GasDemave.iloc[i, 2 + 13 * t_idx + g_idx]
    for i, (c, h) in enumerate(zip(df_GasDemave.iloc[:, 0], df_GasDemave.iloc[:, 1]))  
    for t_idx, t in enumerate(model2.TT)  
    for g_idx, g in enumerate(model2.g)}

BigQneg_data = {(c, h,j,t, g): df_BigQ_neg.iloc[i, 3 + 13 * t_idx + g_idx]
    for i, (c, h,j) in enumerate(zip(df_BigQ_neg.iloc[:, 0], df_BigQ_neg.iloc[:, 1], df_BigQ_neg.iloc[:, 2]))  
    for t_idx, t in enumerate(model2.TT)  
    for g_idx, g in enumerate(model2.g)}

BigQpos_data = {(c, h,j,t, g): df_BigQ_pos.iloc[i, 3 + 13 * t_idx + g_idx]
    for i, (c, h,j) in enumerate(zip(df_BigQ_pos.iloc[:, 0], df_BigQ_pos.iloc[:, 1], df_BigQ_pos.iloc[:, 2]))  
    for t_idx, t in enumerate(model2.TT)  
    for g_idx, g in enumerate(model2.g)}

Data5 = Renewables_data.iloc[28:31, 1:14]
landAV_data = {(e,g): Data5.iloc[i,j]
            for i, e in enumerate(model2.e)
            for j, g in enumerate(model2.g)}

Data6 = Production_data.iloc[34:38, 5]
Capmax_data = {(p): Data6.iloc[i]
            for i, p in enumerate(model2.p)}

Data7 = Production_data.iloc[34:38, 1]
Capmin_data = {(p): Data7.iloc[i]
            for i, p in enumerate(model2.p)}

Data8 = Production_data.iloc[4:8, 3:7]
pccost_data = {(p,t): Data8.iloc[i,j]
            for i, p in enumerate(model2.p)
            for j, t in enumerate(model2.t)}

Data9 = Production_data.iloc[14:18, 3:7]
pocostF_data = {(p,t): Data9.iloc[i,j]
            for i, p in enumerate(model2.p)
            for j, t in enumerate(model2.t)}


Data10 = Production_data.iloc[14:18, 12:16]
pocostV_data = {(p,t): Data10.iloc[i,j]
            for i, p in enumerate(model2.p)
            for j, t in enumerate(model2.t)}

Data11 = H2Pipline_data.iloc[20:23, 1]
qHmax_data = {(d1): Data11.iloc[i]
            for i, d1 in enumerate(model2.d1)}

Data12 = CO2Pipline_data.iloc[49:51, 1]
qCmax_data = {(d2): Data12.iloc[i]
            for i, d2 in enumerate(model2.d2)}

Data13 = Storage_data.iloc[59:65, 1]
QImax_data = {(s): Data13.iloc[i]
              for i, s in enumerate(model2.s)}

Data14 = Storage_data.iloc[59:65, 4]
QRmax_data = {(s): Data14.iloc[i]
              for i, s in enumerate(model2.s)}

Data15 = CO2Reservior_data.iloc[3:7, 4]
rcap_data = {(r):Data15.iloc[i]
             for i, r in enumerate(model2.r)}

Data16 = CO2Reservior_data.iloc[12:16, 1]
ri0_data = {(r):Data16.iloc[i]
             for i, r in enumerate(model2.r)}

Data17 = Production_data.iloc[50:54, 8]
RD_data = {(p): Data17.iloc[i]
           for i, p in enumerate(model2.p)}

Data18 = Storage_data.iloc[36:42, 5]
scap_max_data = {(s): Data18.iloc[i]
                 for i, s in enumerate(model2.s)}



rccost = Renewables_data.iloc[3:6, 3:7]
rccost_data = {(e,t): rccost.iloc[i,j]
               for i, e in enumerate(model2.e)
               for j, t in enumerate(model2.t)}

rocost = Renewables_data.iloc[10:13, 3:7]
rocost_data = {(e,t): rocost.iloc[i,j]
               for i, e in enumerate(model2.e)
               for j, t in enumerate(model2.t)}

Data19 = Storage_data.iloc[2:8, 1] 
sccost_data = {(s): Data19.iloc[i]
               for i, s in enumerate(model2.s)}

Data20 = Storage_data.iloc[14:20, 1]
socostF_data = {(s): Data20.iloc[i]
                for i, s in enumerate(model2.s)}

Data21 = Storage_data.iloc[14:20, 7]
socostV_data = {(s): Data21.iloc[i]
                for i, s in enumerate(model2.s)}

Data22 = Production_data.iloc[23:27, 1]
Pcap_data = {(p): Data22.iloc[i]
             for i, p in enumerate(model2.p)}

Data23 = Storage_data.iloc[25:31, 1]
SCap_data = {(s): Data23.iloc[i]
             for i, s in enumerate(model2.s)}

Data24 = Production_data.iloc[50:54, 1]
UT_data = {(p): Data24.iloc[i]
           for i, p in enumerate(model2.p)}


Data25 = Biomass_data.iloc[24:29, 2]
Vbio_data = {(t): Data25.iloc[i]
             for i, t in enumerate(model2.t)}


df_Demand_data.iloc[:, 1] = df_Demand_data.iloc[:, 1].astype(str).str.strip().astype(int)
WF_data = dict(zip(df_Demand_data.iloc[:, 0], df_Demand_data.iloc[:, 1]))

# -----------------Define Order in Pyomo for some variable ---------------
# %% Making order of set for some equations---------------

region_order = {region: i + 1 for i, region in enumerate(model2.g)}
diameter_order1 = {diameter: i + 1 for i, diameter in enumerate(model2.d1)}   
diameter_order2 = {diameter: i + 1 for i, diameter in enumerate(model2.d2)}          
       
Trans_order = {transLine: i + 1 for i, transLine in enumerate(model2.l)}  
Production_order = {production: i+1 for i, production in enumerate(model2.p)}
Storage_order = {storage: i+1 for i, storage in enumerate(model2.s)}
Cluster_order = {cluster: i+1 for i, cluster in enumerate(model2.CC)}

model2.ord_g = Param(model2.g, initialize=region_order)
model2.ord_d1 = Param(model2.d1, initialize=diameter_order1)
model2.ord_d2 = Param(model2.d2, initialize=diameter_order2)

model2.ord_l = Param(model2.l, initialize=Trans_order)
model2.ord_p = Param(model2.p, initialize=Production_order)
model2.ord_s= Param(model2.s, initialize=Storage_order )
model2.ord_c = Param(model2.CC, initialize=Cluster_order)
# %% Parameters===========================================
model2.beta = Param(initialize=0.15, doc='Ratio of stored amount (%)')

# Distance between region and underground storage
model2.DistSt = Param(model2.g, model2.sc, initialize=DistSt_data, doc='distance between region g and underground storage type s')

# CO2 capture and emission coefficients
model2.y_c = Param(model2.p, model2.t, initialize=y_c_data, doc='CO2 capture coefficient for plant type p in time period t (tn CO2 / MWh H2)')
model2.y_e = Param(model2.p, model2.t, initialize=y_e_data,   doc='CO2 emission coefficient for plant type p and size j in time period t (tn CO2 / MWh H2)')


# Pipeline operating cost ratios
model2.deltaH = Param(initialize=0.05, doc='Ratio of hydrogen regional pipeline operating costs to capital costs (%)')
model2.deltaC_onshore = Param(initialize=0.05, doc='Ratio of onshore CO2 pipeline operating costs to capital costs')
model2.deltaC_offshore = Param(initialize=0.05, doc='Ratio of offshore CO2 pipeline operating costs to capital costs')


# Pipeline diameters
model2.diaH = Param(model2.d1, initialize=diaH_data)
model2.diaC_onshore = Param(model2.d2, initialize={1: 0.6, 2: 1.2}, doc='Diameter of an onshore CO2 pipeline of diameter size d (m)')
model2.diaC_offshore = Param(model2.d2, initialize={1: 0.6, 2: 1.2}, doc='Diameter of an offshore CO2 pipeline of diameter size d (m)')

# Hydrogen import ratio
model2.iota = Param(initialize=0.1, doc='Maximum percentage of international hydrogen imports over the total demand (%)')

# Time-related parameters
model2.dur = Param(initialize=5, doc='Duration of time periods (y)')
model2.LTonshore = Param(initialize=50, doc='Useful life of onshore CO2 pipelines (y)')
model2.LToffshore = Param(initialize=50, doc='Useful life of offshore CO2 pipelines (y)')
model2.LTpipe = Param(initialize=50, doc='Useful life of hydrogen pipelines (y)')
model2.a = Param(initialize=365, doc='Days in a year (days)')

model2.LTp = Param(model2.p, initialize={'SMRCCS':40, 'ATRCCS':40, 'BECCS':30, 'WE':30},doc='Useful life of hydrogen production plants (y)')
model2.LTs = Param(model2.s, initialize={'OnTeeside':40, 'OnChesire':40, 'OnYorkshire':40, 'OffIrishSea':40, 'MPSV':40, 'HPSV':40}, doc='Useful life of hydrogen storage facilities (y)')
model2.LTt = Param(model2.l, initialize={'Trailer': 15}, doc='Useful life of hydrogen road transportation modes (y)')



# Biomass parameters
model2.br = Param(model2.g, initialize=br_data,doc='Parameter for region-specific values')
model2.bp = Param( initialize=0.5)
model2.cbio = Param(model2.TT, initialize=cbio_data, doc='Biomass cost in time period t (€/MWh)')


# Pipeline costs and renewable energy parameters
model2.cccH = Param(model2.d1, initialize=cccH_data, doc='Capital costs of a regional hydrogen pipeline of diameter size q d (€/k km-1)')
model2.cccC_onshore = Param(model2.d2, initialize=cccC_onshore_data, doc='Capital costs of an onshore CO2 pipeline of diameter size d (€/k km-1)')
model2.cccC_offshore = Param(model2.d2, initialize=cccC_offshore_data, doc='Capital costs of an offshore CO2 pipeline of diameter size d (€/k km-1)')
model2.cgas = Param(model2.t, initialize=cgas_data, doc='Natural gas cost in time period t (€/MWh)')
model2.crf = Param(initialize=0.07, doc='Capital recovery factor')

# Start-up and shut-down costs for technologies
model2.Cstart = Param(model2.p, initialize=Cstart_data, doc='Cost for starting up for each technology type (€/MW)')
model2.Cshut = Param(model2.p,initialize=Cshut_data, doc='Cost for shutting down for each technology type (€/MW)')

# Carbon tax and demand parameters
model2.ct = Param(model2.t, initialize=ct_data,doc='carbon tax i time period t (€/kg CO2)')
model2.dc = Param(model2.t, initialize=dc_data, doc='Demand coefficient at time period t')
#model.dem = Param(model.g, model.t, model.c, model.h, doc='Total hydrogen demand in region g in time period t (MW)')


# Transportation and pipeline parameters
model2.dw = Param(model2.l, initialize={'Trailer':16.62 }, doc='Driver wage of road transportation mode l (€/h)')
model2.DistPipe = Param(model2.g, model2.g, initialize=DistPipe_data, within=NonNegativeReals, doc='Delivery distance of an onshore CO2 pipeline between regions g and g1 (km)')
model2.DistRes = Param(model2.g, model2.r, initialize=DistRes_data, doc='Distance from CO2 collection point in region g to reservoir r (km)')
model2.Dist = Param(model2.g, model2.g, initialize=Dist_data, doc='Regional delivery distance of hydrogen transportation mode l in region g (km)')


# Technical parameters for plants and pipelines
model2.DT = Param(model2.p, initialize=DT_data, doc='Min down time (h)')
model2.ec = Param(model2.t, initialize=ec_data, doc='Cost of electricity back to grid (€/MWe)')
model2.eta = Param(model2.p, model2.t, initialize=eta_data, doc='Efficiency of WE in time period t (%)')
model2.emtarget = Param(model2.t, initialize=emtarget_data, doc='Emissions target in time period t (kgCO2)')

# Road transportation costs and fuel economy
model2.feR = Param(model2.l, initialize={'Trailer': 2.3}, doc='Fuel economy of road transportation mode l transporting product type i within a region (km/l)')
model2.fp = Param(model2.l, initialize={'Trailer': 1.63 }, doc='Fuel price of road transportation mode l (€/l)')
#model.GasDem = Param(model.CC, model.h, model.g,  initialize=GasDem_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')
model2.GasDemave = Param(model2.CC, model2.h, model2.t,model2.g,  initialize=GasDemave_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')
model2.ge = Param(model2.l, initialize={'Trailer': 0.25 }, doc='General expenses of road transportation mode l transporting product type i (€/d)')

# Economic parameters
model2.ir = Param(initialize=0.06, doc='Discount rate (%)')
model2.landAV = Param(model2.e, model2.g, initialize=landAV_data, doc='Land availability of renewable e in region g (MW)')
model2.lut = Param(model2.l, initialize={'Trailer':2}, doc='Load and unload time of road transportation mode l (h)')
model2.me = Param(model2.l, initialize={'Trailer':0.07}, doc='Maintenance expenses of road transportation mode l (€/km)')
model2.nel = Param(initialize=30, doc='Economic life cycle of capital investments (y)')

# Initial number of plants and storage units
model2.np0 = Param(model2.p, model2.g, initialize=0, doc='Initial number of hydrogen production plants of technology p and size j in region g')
model2.ns0 = Param(model2.s, model2.g, initialize=0, doc='Initial number of hydrogen storage facilities of type s and size j in region g')

# Production and storage capacity parameters
model2.pcap_max = Param(model2.p, initialize=Capmax_data, doc='Maximum capacity of a hydrogen production plant of type p and size j (MW)')
model2.pcap_min = Param(model2.p, initialize=Capmin_data, doc='Minimum capacity of a hydrogen production plant of type p and size j (MW)')
model2.pccost = Param(model2.p, model2.t, initialize=pccost_data, doc='Capital cost of a production plant of type p (€/kW)')
model2.pimp = Param(initialize=127.6, doc='Price of hydrogen import (€/MWh)')
model2.pocostF = Param(model2.p, model2.t, initialize=pocostF_data, doc='Operating production cost in a production plant of type p (€/MWh/y)')
model2.pocostV = Param(model2.p, model2.t, initialize=pocostV_data, doc='Operating production cost in a production plant of type p (€/MWh)')

# Flow rate and capacity limits
model2.qHmax = Param(model2.d1, initialize=qHmax_data, doc='Maximum flow rate in a hydrogen pipeline of diameter size d (kg H2/day)')
model2.qCmax = Param(model2.d2, initialize=qCmax_data, within=NonNegativeReals, doc='Maximum flow rate in a CO2 pipeline of diameter size d (kg H2/day)')
model2.QImax = Param(model2.s, initialize=QImax_data, doc='Maximum injection rate for each storage type s')
model2.QRmax = Param(model2.s, initialize=QRmax_data, doc='Maximum retrieval rate for each storage type s')

# Reservoir-related parameters
model2.rcap = Param(model2.r, initialize=rcap_data, doc='Total capacity of reservoir r (kg CO2-eq)')
model2.ri0 = Param(model2.r, initialize=ri0_data, doc='Initial CO2 inventory in reservoir r (kg CO2)')

# Ramp-up and ramp-down parameters
model2.RD = Param(model2.p, initialize=RD_data, doc='Commit Ramp down')
model2.rccost = Param(model2.e, model2.t, initialize=rccost_data, doc='Renewable e capital cost in time period t (€/MW)')
model2.rocost = Param(model2.e, model2.t, initialize=rocost_data, doc='Renewable e operating cost in time period t (€/MW)')

# Storage parameters
model2.RU = Param(model2.p, initialize=RD_data, doc='Commit Ramp up', )
model2.scap_max = Param(model2.s, initialize=scap_max_data, doc='Maximum capacity of a storage facility of type s (MWh H2)')
model2.scap_min = Param(model2.s, initialize=0, doc='Minimum capacity of a storage facility of type s (MWh H2)')
model2.sccost = Param(model2.s, initialize=sccost_data, doc='Fixed operating storage cost in a production plant of type p (€/MW/y)')
model2.socostF = Param(model2.s, initialize=socostF_data, doc='Fixed operating storage cost in a production plant of type p (€/MW/y)')
model2.socostV = Param(model2.s, initialize=socostV_data, doc='Variable operating storage cost in a production plant of type p (€/kWh stored)')

# Road transportation speed and capacity
model2.spR = Param(model2.l, initialize={'Trailer': 55}, doc='Regional average speed of road transportation mode l (km/h)')
model2.st0 = Param(model2.s, model2.g, initialize=0, doc='Storage at time 0')
model2.tcap = Param(model2.l, initialize={'Trailer': 21.66 }, doc='Capacity of road transportation mode l transporting product type i (MWh unit-1)')
model2.tmc = Param(model2.l, initialize={'Trailer': 253000 }, doc='Capital cost of establishing a road transportation unit of transportation mode l (€/unit)')
model2.tmaR = Param(model2.l, initialize={'Trailer': 18 }, doc='Regional availability of road transportation mode l (h/day)')

# Unit capacity for production and storage
model2.PCap = Param(model2.p, initialize=Pcap_data, doc='Unit capacity for production type p (MW)')
model2.SCap = Param(model2.s, initialize=SCap_data, doc='Unit capacity for storage type s (MW)')

# Initial operating units
model2.uInit = Param(model2.p, model2.g, model2.t, initialize=0, doc='Initial operating units type p in region g at time period t')

# Technical parameters for up and down time
model2.UT = Param(model2.p, initialize=UT_data, doc='Min up time (h)')

# Biomass consumption and cluster weights
model2.Vbio_max = Param(model2.t, initialize=Vbio_data, doc='Maximum biomass consumption in year t')
#model2.WF = Param(model2.CC, initialize=WF_data, doc='Weight of clusters')
WF_data_modified = {k: ( round(v * 0.2526) if i >= 1 else v) for i, (k, v) in enumerate(WF_data.items())}
model2.WF = Param(model.CC, initialize=WF_data_modified, doc='Weight of clusters')

# ---- Scalar ----
model2.y1 = Param(initialize=3, doc="Scalar y1")
model2.y2 = Param(initialize=6, doc="Scalar y2")

model2.theta = Param(initialize=1, doc="Scalar theta")

# Define a function for initializing the values of dfc
def dfc_init(model2, t):
    return round(1 / (1 + model2.ir) ** (model2.dur * t - model2.dur), 2)

model2.dfc = Param(model2.TT, initialize=dfc_init,  doc='Discount factor for capital costs in time period t')

#model.dfc = Expression(model.t, rule=lambda model, t: round(1 / (1 + model.ir) ** (model.dur * t - model.dur), 2), doc='Discount factor for capital costs in time period t')

def dfo_init(model2,t):
    return round(
        1 / (1 + model2.ir) ** (model2.dur * t - 5) +
        1 / (1 + model2.ir) ** (5 * t - 4) +
        1 / (1 + model2.ir) ** (5 * t - 3) +
        1 / (1 + model2.ir) ** (5 * t - 2) +
        1 / (1 + model2.ir) ** (5 * t - 1),
        2
    )
model2.dfo= Param(model2.TT, initialize=dfo_init)

def biomass_availability_init(model2, g, t):
    return model2.bp * model2.br[g] * model2.Vbio_max[t] * 1000000

model2.BA = Param(model2.g, model2.TT, initialize=biomass_availability_init,  doc="Biomass availability in region g and time period t")


#def dem_init(model, g, t, CC, h):
    #return model.dc[t] * model.GasDem[CC, h, g] 
#model.dem = Param(model.g, model.TT, model.CC, model.h, initialize=dem_init)
def dem_init(model2, g, t, c, h):
    return model2.GasDemave[c, h, t, g]

model2.dem = Param(model2.g, model2.t, model2.CC, model2.h, initialize=dem_init)


model2.Npipe = Set(dimen=2,initialize=model2.DistPipe.keys(), doc='Set of region pairs with nonzero pipeline distances')



# %% New sets
# Defining the iteration sets

# Defining Stage2_it set
model2.Stage2_it = Set(initialize=[f'Stage2_it'])  # Equivalent to /Stage2_it1*Stage2_it30/
#model.phi = Param(initialize=3) 


model.iter1 = Set(within=model.it, initialize=[f'it1'])  
#model.iter1 = Set(within=model.it, initialize=[f'it{i}' for i in range(1,2)])  # Empty subset
model.iter_fesi = Set(within=model.it, initialize=[f'it1']) 

# Availability and initial availability parameters
model2.AV = Param(model2.CC, model2.h, model2.g, model2.e, initialize=AV_data, doc='Availability of renewable e in region g, cluster c and hour h (%)')
model2.ayHR0 = Param(model2.d1, model2.Npipe,initialize=0, doc='Initial availability of a regional hydrogen pipeline of diameter size d between regions g and g1 (0-1)')
model2.ayC0 = Param(model2.d2, model2.N, initialize=0, doc='Initial availability of an onshore CO2 pipeline of diameter size d between regions g and g1 (0-1)')
model2.aeC0 = Param(model2.r, initialize=0, doc='Initial availability of an offshore CO2 pipeline between collection point in regions g and reservoir r (0-1)')


InvP_bounds = {
    'SMRCCS': 10,
    'ATRCCS': 10,
    'BECCS': 10,
    'WE': 50
}

def InvP_bounds_rule(model2, p, g, t):
    if p in InvP_bounds and t in model2.TT:
        return (0, InvP_bounds[p]) 
    

InvS_bounds = {
    'MPSV': 80,
    'HPSV': 80}
def InvS_bounds_rule(model2, s, g, t):
    if s in InvS_bounds and t in model2.TT:
        return (0, InvS_bounds[s])
    elif s in ['OnTeeside', 'OnChesire', 'OnYorkshire', 'OffIrishSea']:
        return (0, 1) 
    return (0, None)  

def NS_bounds_rule(model2, s, g, t):
    if s in model2.sc and (g, s) in model2.GS2 and t in model2.TT:
        return (0, 1)  
    else:
        return (0, None)
    
def RI_bounds_rule(model2, r, t):
    return (0, model2.rcap[r] / 1000)


def Qup_bounds_rule(model2, l, g, g1,t, c, h):
    if l in ['Pipe']:
        return (0,15343)
    return (0, None)
# %% Variables============================================


model2.InvP = Var(model2.p, model2.g, model2.TT, within=NonNegativeIntegers, bounds=InvP_bounds_rule,
                 doc="Investment of new plants of type p producing in region g in time period t")
#.InvP_up = Var(model.p, model.g, model.TT, within=NonNegativeIntegers)
model2.InvS = Var(model2.s, model2.g, model2.TT, within=NonNegativeIntegers, bounds=InvS_bounds_rule,
                 doc="Investment of new storage facilities of type in region g in time period t")
#model.InvS_up = Var(model.s, model.g, model.TT,  within=NonNegativeIntegers)
model2.Yh = Var(model2.d1, model2.Npipe, model2.TT, within=NonNegativeIntegers,  doc="Establishment of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
model2.Yon = Var(model2.d2, model2.N, model2.TT, within=NonNegativeIntegers, 
                doc="Establishment of onshore CO2 pipelines of diameter size d in region g in time period t")
model2.Yoff = Var(model2.d2, model2.GR, model2.TT, within=NonNegativeIntegers, 
                 doc="Establishment of offshore CO2 pipelines of diameter size d in region g in time period t")
model2.Yst = Var(model2.d1, model2.GS2, model2.TT, within=NonNegativeIntegers, 
                doc="Establishment of hydrogen pipelines of diameter size d in region g in time period d to storage type s")


model2.lemma_neg = Var(model2.TT, model2.g, model2.CC, model2.h, model2.j, within=NonNegativeReals)  # Dual for z ≤ 1
model2.lemma_pos = Var(model2.TT, model2.g, model2.CC, model2.h, model2.j, within=NonNegativeReals)  # Another dual for z ≤ 1
model2.gamma = Var(model2.TT, model2.g, model2.CC, model2.h, model2.j, within=NonNegativeReals)  # Dual for A^Tz ≤ 1
model2.xi = Var(model2.TT, model2.g, model2.CC, model2.h, within=NonNegativeReals)


# Positive variables
model2.NP = Var(model2.p, model2.g, model2.TT, within=NonNegativeReals, doc="Number of plants of type j and size p in region g in time period t")
model2.NS = Var(model2.s, model2.g, model2.TT, within=NonNegativeReals, bounds=NS_bounds_rule, doc="Number of storage facilities of type s and size p in region g in time period t")
#model.NS_up = Var(model.s, model.g, model.TT, within=NonNegativeIntegers)
#model.ITU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals, bounds=(0,25), doc="Number of new transportation units of type l for regional transportation byroad in region g to region g acquired in time period t")
#model.NTU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals,   doc="Number of transportation units of type l for regional transportation by road in region g in time period t")
model2.AY = Var(model2.d1, model2.Npipe, model2.TT, within=NonNegativeReals,  doc="availability of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
model2.AYon=Var(model2.d2, model2.N, model2.TT, within=NonNegativeReals,  doc="availability of onshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
model2.AYoff = Var(model2.d2, model2.GR, model2.TT, within=NonNegativeReals,  doc="availability of offshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
model2.AYst = Var(model2.d1, model2.GS2, model2.TT, within=NonNegativeReals,  doc="availability of hydrogen pipelines of diameter size d for distribution in region g in time period t")
#model2.CL = Var(model2.it, model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, doc='Curtailment (MW)')
model2.CL_Stage2 = Var( model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, doc='Curtailment (MW)')

model2.InvR = Var(model2.e, model2.g, model2.TT, within=NonNegativeReals, bounds=(0, 10000), doc='Invested capacity of renewable (MW)')
#model.InvR_up = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000))
#model2.IMP = Var(model2.it,model2.g, model2.TT, model2.CC, model2.h, within=NonNegativeReals,doc='Flow rate of international import (MW)')
model2.IMP_Stage2 = Var(model2.g, model2.TT, model2.CC, model2.h, within=NonNegativeReals,doc='Flow rate of international import (MW)')

model2.NR = Var(model2.e, model2.g, model2.TT, within=NonNegativeReals,  doc='Capacity of renewable (MW)')
#model2.Pr = Var(model2.it,model2.p, model2.g, model2.TT, model2.CC,model2.HH,within=NonNegativeReals,      doc='Production rate (MW)')
model2.Pr_Stage2 = Var(model2.p, model2.g, model2.TT, model2.CC,model2.HH,within=NonNegativeReals,      doc='Production rate (MW)')

#model2.Pre = Var(model2.it, model2.e, model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals,    doc='Electricity production from renewable (MW)')
model2.Pre_Stage2 = Var( model2.e, model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals,    doc='Electricity production from renewable (MW)')

#model2.Q = Var(model2.it,model2.l, model2.Npipe, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, bounds=Qup_bounds_rule, doc='Regional flowrate of H2 (MWh)')
model2.Q_Stage2 = Var(model2.l, model2.Npipe, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, bounds=Qup_bounds_rule, doc='Regional flowrate of H2 (MWh)')

#model2.Qi = Var(model2.it,model2.g,model2.s, model2.TT, model2.CC,model2.HH, within=NonNegativeReals,  doc='H2 via pipeline to storage (MWh)')
model2.Qi_Stage2 = Var(model2.g,model2.s, model2.TT, model2.CC,model2.HH, within=NonNegativeReals,  doc='H2 via pipeline to storage (MWh)')

#model2.Qr = Var(model2.it,model2.s, model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals,  doc= 'flowrate of H2 via pipeline from region g to storage type s in time period t(MWh)')
model2.Qr_Stage2 = Var(model2.s, model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals,  doc= 'flowrate of H2 via pipeline from region g to storage type s in time period t(MWh)')

#model2.Qon = Var(model2.it,model2.N, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via onshore pipelines (kg CO2/d)')
model2.Qon_Stage2 = Var(model2.N, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via onshore pipelines (kg CO2/d)')

#model2.Qoff = Var(model2.it,model2.GR, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via offshore pipelines (kg CO2/d)')
model2.Qoff_Stage2 = Var(model2.GR, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via offshore pipelines (kg CO2/d)')

#odel.Rdown = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals,initialize=0, doc='Upward reserve contribution (MWh)')
#odel.Rup = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Downward reserve contribution (MWh)')
#model2.St = Var(model2.it,model2.s,model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, doc='Average inventory of product stored (kW)')
model2.St_Stage2 = Var(model2.s,model2.g, model2.TT, model2.CC, model2.HH, within=NonNegativeReals, doc='Average inventory of product stored (kW)')

model2.Vbio = Var(model2.TT, within=NonNegativeReals,  doc='Biomass consumption (kg)' )
model2.Vgas = Var(model2.TT, within=NonNegativeReals, doc='Gas consumption (kg)')
#model.slak1 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 1')
#model.slak2 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 2')
model2.PCC = Var(within=NonNegativeReals)
model2.SCC = Var(within=NonNegativeReals)
model2.TCC=Var(within=NonNegativeReals)
model2.POC1 = Var(within=NonNegativeReals)

#model2.POC2 = Var(model2.it,within=NonNegativeReals)
model2.POC2_Stage2 = Var(within=NonNegativeReals)

model2.SOC1 = Var(within=NonNegativeReals)
#model2.SOC2 = Var(model2.it,within=NonNegativeReals)
model2.SOC2_Stage2 = Var(within=NonNegativeReals)

model2.RI = Var(model2.r, model2.TT,  within=NonNegativeReals, bounds=RI_bounds_rule)
#model.RI_up = Var(model.r, model.TT, within=NonNegativeReals)
#model.TC = Var()
#model.RCC = Var()
model2.FCR = Var()
model2.GCR = Var()
model2.LCR = Var()
model2.MCR = Var()
model2.PipeOC = Var(within=NonNegativeReals)
model2.PipeCC = Var(within=NonNegativeReals)
#model2.CEC = Var(model2.it,within=Reals)
model2.CEC_Stage2 = Var(within=Reals)

#model2.IIC = Var(model2.it,within=NonNegativeReals)
model2.IIC_Stage2 = Var(within=NonNegativeReals)

model2.ReC = Var(within=NonNegativeReals)
#model2.GC = Var(model2.it,within=NonNegativeReals)
model2.GC_Stage2 = Var(within=NonNegativeReals)

#model2.BC = Var(model2.it,within=NonNegativeReals)
model2.BC_Stage2 = Var(within=NonNegativeIntegers)

#model2.ROC = Var(model2.it)
model2.TOC=Var(within=NonNegativeReals)
model2.em = Var(model2.TT, within=Reals)
model2.Stage1_eta=Var()
#model2.Stage2_TC=Var()
model2.Stage2_dem=Var(model2.g, model2.TT, model2.CC, model2.HH, within=Reals)
model2.Stage2_middle_dem=Var(model2.g, model2.TT, model2.CC, model2.HH, within=Reals)
model2.Stage2_Lower_TC=Var()
model2.Stage2_middle_TC=Var()

def dem_stage2(model2,g,t,c,h):
    return model2.GasDemave[c, h, t, g]
model2.Stage2_fixed_dem=Param(model2.g,model2.TT,model2.CC,model2.HH, initialize=dem_stage2)
model2.Lem_Stage2=Param(model2.g, model2.TT, model2.CC, model2.HH)

# %% The initial objective function with all continous variables

# Constraint for POC
def poc2_rule(model2):
    return model2.POC2_Stage2 ==  sum(model2.dfo[t] *
        model2.WF[c] * model2.pocostV[p, t] * model2.theta * model2.Pr_Stage2[p, g, t, c, h]
        for p in model2.p for g in model2.g for t in model2.TT for c in model2.CC for h in model2.HH
    )
model2.POCConstraint2 = Constraint(rule=poc2_rule)

# Constraint for SOC
def soc2_rule(model2):
    return model2.SOC2_Stage2 ==  sum( model2.dfo[t] *
       
            model2.WF[c] * model2.socostV[s] * model2.theta * model2.Qi_Stage2[g, s, t, c, h] 
            
        for s in model2.s for g in model2.g if (g, s) in model2.GS for t in model2.TT for c in model2.CC for h in model2.HH
    )
model2.SOCConstraint2 = Constraint(rule=soc2_rule)




def CECeq2_rule(model2):
    return model2.CEC_Stage2 == sum(
        model2.WF[c] * model2.dfo[t] * model2.ct[t] * model2.y_e[p, t] * model2.theta * model2.Pr_Stage2[ p, g, t, c, h]
        for p in model2.p for g in model2.g for t in model2.TT for c in model2.CC for h in model2.HH
        
    )

model2.CECConstraint2=Constraint(rule=CECeq2_rule)        

def IICeq2_rule(model2):
    return model2.IIC_Stage2 == sum(
        model2.WF[c] * model2.dfo[t] * model2.pimp * model2.theta * model2.IMP_Stage2[g, t, c, h]
        for g in model2.Gimp for t in model2.TT for c in model2.CC for h in model2.HH
    )
model2.IICConstraint=Constraint(rule=IICeq2_rule)        

def GasCost2_rule(model2):
    return model2.GC_Stage2 == sum(
        model2.dfo[t] * model2.cgas[t] * model2.WF[c] * model2.theta * model2.Pr_Stage2[ p, g, t, c, h] / model2.eta[p, t]
        for g in model2.g for p in model2.p for c in model2.CC for h in model2.HH for t in model2.TT if model2.ord_p[p] <= 2 
    )
model2.GasCosConstraint2=Constraint(rule=GasCost2_rule)        

def BioCost2_rule(model2):
    return model2.BC_Stage2 == sum(
        model2.dfo[t] * model2.cbio[t] * model2.WF[c] * model2.theta * model2.Pr_Stage2[ 'BECCS', g, t, c, h] / model2.eta['BECCS', t]
        for g in model2.g for c in model2.CC for h in model2.HH for t in model2.TT
    )
model2.BioCosConstraint2=Constraint(rule=BioCost2_rule)        


def objectiveStage2_lower_rule(model2):
    return (
        model2.POC2_Stage2+ 
        model2.SOC2_Stage2+ 
        model2.CEC_Stage2+
        model2.IIC_Stage2+
        model2.GC_Stage2+
        model2.BC_Stage2
    )   
                  
model2.Stage2_Lower_TC = Objective(rule=objectiveStage2_lower_rule, sense=minimize)



# %%
# HA2 Monolithic Version

def Demand_Stage2_rule(model2, g,t,c,h):
    if  t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.Stage2_dem[g,t,c,h]==model2.Stage2_fixed_dem[g,t,c,h]
    else:
        return Constraint.Skip
model2.Demand_Stage2Cons= Constraint(model2.g, model2.TT, model2.CC, model2.HH, rule=Demand_Stage2_rule)

def flow_balance2_rule(model2,g, t, c, h):
    return (
        sum(model2.Pr_Stage2[p, g, t, c, h] for p in model2.p) +
        sum(model2.Q_Stage2['Pipe', g1, g, t, c, h] for g1 in model2.g if (g1, g) in model2.Npipe) +
        (model2.IMP_Stage2[g, t, c, h] if g in model2.Gimp else 0) +
        sum(model2.Qr_Stage2[s, g, t, c, h] for s in model2.s if (g, s) in model2.GS)
        ==
        sum(model2.Q_Stage2['Pipe', g, g1, t, c, h] for g1 in model2.g if (g, g1) in model2.Npipe) +
        sum(model2.Qi_Stage2[g, s, t, c, h] for s in model2.s if (g, s) in model2.GS) +
        model2.Stage2_dem[g, t, c, h]
    )

model2.FlowBalance2 = Constraint( model2.g, model2.TT, model2.CC, model2.HH, rule=flow_balance2_rule)



# Co2 Balanace
def co2_mass_balance2_rule(model2, g, t, c, h):
    if t in model2.TT and c in model2.CC and h in model2.HH:
        return (
            sum(model2.Qon_Stage2[g1, g, t, c, h] for g1 in model2.g if (g1, g) in model2.N) +
            sum(model2.y_c[p, t] * model2.Pr_Stage2[p, g, t, c, h] for p in model2.p)
         == 
            sum(model2.Qon_Stage2[g, g1, t, c, h] for g1 in model2.g if (g, g1) in model2.N) +
            sum(model2.Qoff_Stage2[g, r, t, c, h] for r in model2.r if (g, r) in model2.GR)
        )
    return Constraint.Skip

model2.CO2MassBalanceConstraint2 = Constraint(model2.g, model2.TT, model2.CC, model2.HH, rule=co2_mass_balance2_rule)

def biomass_availability2_rule(model2, g, t):
    if t in model2.TT:  # Apply the constraint only for TT(t)
        return sum(
            model2.WF[c] * model2.theta * model2.Pr_Stage2['BECCS', g, t, c, h] / model2.eta['BECCS', t]
            for c in model2.CC for h in model2.HH
        ) <=  model2.BA[g,t]
    return Constraint.Skip

model2.BiomassAvailabilityConstraint2 = Constraint(model2.g, model2.TT, rule=biomass_availability2_rule)

#%% 
# Ramp Up
def ramp_up2_rule(model2, p, g, c, h, t):
    if t in model2.TT and c in model2.CC and h in model2.HH and h > 1:
        return model2.Pr_Stage2[p, g, t, c, h] - model2.Pr_Stage2[p, g, t, c, h - 1] <=model2.theta * model2.RU[p] * model2.PCap[p] * model2.NP[p, g, t]
    return Constraint.Skip

model2.RampUpConstraint2 = Constraint(model2.p, model2.g, model2.CC, model2.HH, model2.TT, rule=ramp_up2_rule)


# Ramp Down
def ramp_down2_rule(model2, p, g, c, h, t):
    if t in model2.TT and c in model2.CC and h in model2.HH and h > 1:
        return model2.Pr_Stage2[p, g, t, c, h - 1] - model2.Pr_Stage2[p, g, t, c, h] <= model2.theta * model2.RD[p] * model2.PCap[p] * model2.NP[p, g, t]
    return Constraint.Skip

model2.RampDownConstraint2 = Constraint(model2.p, model2.g, model2.CC, model2.HH, model2.TT, rule=ramp_down2_rule)

# %%  Peoduction Limit ---------------------------
# Production Limit

def p_capacity2_rule(model2, p, g, t, c, h):
    if t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.Pr_Stage2[p, g, t, c, h] <= model2.PCap[p] * model2.pcap_max[p] * model2.NP[p, g, t]
    return Constraint.Skip

model2.PCapacity2Constraint = Constraint( model2.p, model2.g, model2.TT, model2.CC, model2.HH, rule=p_capacity2_rule)

#%% Storage
def sinventory2_rule(model2, s, g, t, c, h):
    if (g, s) in model2.GS and t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.St_Stage2[s, g, t, c, h] == (
            (model2.St_Stage2[s, g, t, c, h - 1] if h > 1 else model2.st0[s, g]) 
            + model2.theta * (model2.Qi_Stage2[g, s, t, c, h] - model2.Qr_Stage2[s, g, t, c, h])
        )
    return Constraint.Skip
model2.SInventory2 = Constraint(model2.s, model2.g, model2.TT, model2.CC, model2.HH, rule=sinventory2_rule)


# Maximum injection rate
def max_inj_rule(model2, s,g,t, c, h):
    if (g, s) in model2.GS and t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.Qi_Stage2[(g, s), t, c, h] <= model2.QImax[s] * model2.NS[s, g, t]
    return Constraint.Skip

model2.MaxInjConstraint = Constraint(model2.GS, model2.TT, model2.CC, model2.HH, rule=max_inj_rule)


# Maximum retrieval rate
def max_retr_rule(model2, s, g, t, c, h):
    if (g, s) in model2.GS and t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.Qr_Stage2[s, g, t, c, h] <= model2.QRmax[s] * model2.NS[s, g, t]
    return Constraint.Skip
model2.MaxRetrConstraint = Constraint(model2.s,model2.g, model2.TT, model2.CC, model2.HH, rule=max_retr_rule)



# Storage capacity constraints
def s_capacity1_rule(model2, s, g, t, c, h):
    if (g, s) in model2.GS and t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.St_Stage2[s, g, t, c, h] >= model2.SCap[s] * model2.scap_min[s] * model2.NS[s, g, t]
    return Constraint.Skip

model2.SCapacity1Constraint = Constraint(model2.s,model2.g, model2.TT, model2.CC, model2.HH, rule=s_capacity1_rule)

def s_capacity2_rule(model2,  s, g, t, c, h):
    if (g, s) in model2.GS and t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.St_Stage2[s, g, t, c, h] <= model2.SCap[s] * model2.scap_max[s] * model2.NS[s, g, t]
    return Constraint.Skip

model2.SCapacity2Constraint = Constraint(model2.s,model2.g, model2.TT, model2.CC, model2.HH, rule=s_capacity2_rule)





# Final storage
def s_final_rule(model2, s, g, t, c):
    if (s, g) in model2.GS and t in model2.TT and c in model2.CC:
        return model2.St_Stage2[(s, g), t, c, '24'] == 0
    return Constraint.Skip

model2.SFinalConstraint = Constraint(model2.s,model2.g, model2.TT, model2.CC, rule=s_final_rule)


# %%  RENEWABLES CONSTRAINTS ---------------------
# Electricity production for electrolysis
def elec_prod_rule(model2, g, t, c, h):
        return model2.Pr_Stage2['WE', g, t, c, h] == model2.eta['WE', t] * (
            sum(model2.Pre_Stage2[e, g, t, c, h] for e in model2.e) - model2.CL_Stage2[g, t, c, h]
        )

model2.ElecProdConstraint = Constraint(model2.g, model2.TT, model2.CC, model2.HH, rule=elec_prod_rule)


# Renewables availability
def renew_av_rule(model2, e, g, t, c, h):
    if t in model2.TT and c in model2.CC and h in model2.HH:
        return model2.Pre_Stage2[e, g, t, c, h] ==  0.7*model2.AV[c, h, g, e] * model2.NR[e, g, t]

model2.RenewAvConstraint = Constraint(model2.e, model2.g, model2.TT, model2.CC, model2.HH, rule=renew_av_rule)





# %%  RESERVIORS Constraints ---------------------
# Inventory
def res_inventory_rule(model2, r, t):
    if t in model2.TT: 
      return model2.RI[r, t] == (model2.RI[r, t - 1] if t>model2.y1 else  model2.ri0[r] / 1000)+ model2.dur * sum(
        model2.WF[c] * model2.theta * model2.Qoff_Stage2[(g, r), t, c, h] for g in model2.g if 
        (g, r) in model2.GR  for c in model2.CC for h in model2.HH
         ) / 1000
   

model2.ResInventoryConstraint = Constraint(model2.r, model2.TT, rule=res_inventory_rule)

# %%  Hydrogen Import Limit ----------------------
# Import limit
def imp_limit_rule(model2,t, c, h):
    if t in model2.TT and c in model2.CC and h in model2.HH:
        return sum(model2.IMP_Stage2[ g, t, c, h] for g in model2.Gimp) <= 0.1*sum(model2.GasDemave[c,h, t, g] for g in model2.g)
    return Constraint.Skip
model2.ImpLimitConstraint = Constraint(model2.TT, model2.CC, model2.HH, rule=imp_limit_rule)

# %%  Emission Target Limit ----------------------
# Emissions target
def em_target_rule(model2, t):
    if t in model2.TT:
        return  0.001*sum(
            model2.WF[c] * model2.y_e[p, t] * model2.theta * model2.Pr_Stage2[p, g, t, c, h]
            for p in model2.p
            for g in model2.g
            for c in model2.CC
            for h in model2.HH
        ) <=0.001*model2.emtarget[t]
    return Constraint.Skip
model2.EmissionConstraint = Constraint(model2.TT, rule=em_target_rule)

# %%  PIPELINE CONSTRAINTS------------------------
#------Hydrogen Pipeline Limit ------

# Maximum flowrate for pipelines

def h2pipe_max_rule(model2,g, g1, t, c, h):
    if (g, g1) in model2.Npipe:
        return model2.Q_Stage2['Pipe', (g, g1), t, c, h] <= sum(model2.qHmax[d1] * (
            (model2.AY[d1, (g, g1), t] if model2.ord_g[g] < model2.ord_g[g1] else 0)+
            (model2.AY[d1, (g1, g), t] if model2.ord_g[g1] < model2.ord_g[g] else 0) 
            )
            for d1 in model2.d1 if model2.ord_d1[d1]==3 )
    return Constraint.Skip

model2.H2PipeMax = Constraint(model2.Npipe, model2.TT, model2.CC, model2.HH, rule=h2pipe_max_rule)



def onshorepipe_max_rule(model2, g, g1, t, c, h):
    if (g, g1) in model2.N:
        return model2.Qon_Stage2[g, g1, t, c, h] <= sum(model2.qCmax[d2] * (
                (model2.AYon[d2, g, g1, t] if model2.ord_g[g] < model2.ord_g[g1] else 0) +
                (model2.AYon[d2, g1, g, t] if model2.ord_g[g1] < model2.ord_g[g] else 0)
            )
            for d2 in model2.d2 if model2.ord_d2[d2]==2
        )
    return Constraint.Skip

model2.OnshorePipeMax = Constraint(model2.N, model2.TT, model2.CC, model2.HH, rule=onshorepipe_max_rule)




def offshorepipe_max_rule(model2, g, r, t, c, h):
    if (g, r) in model2.GR:
        return model2.Qoff_Stage2[(g, r), t, c, h]  <= sum(model2.qCmax[d2] * model2.AYoff[d2, (g, r), t] for d2 in model2.d2 if model2.ord_d2[d2]==2)
    return Constraint.Skip
model2.OffshorePipeMax = Constraint(model2.GR, model2.TT, model2.CC, model2.HH, rule=offshorepipe_max_rule)


'''
def qon_up_rule(model, g, g1, t, c, h):
    if (g,g1) in model.N and t in model.TT and c in model.CC and h in model.HH:
        return model.Qon[(g, g1), t, c, h] <= 1.17E+04
    return Constraint.Skip
model.Qon_up_constraint = Constraint(model.N, model.TT, model.CC, model.h, rule=qon_up_rule)

def qoff_up_rule(model, g, r, t, c, h):
    if (g,r) in model.GR and t in model.TT and c in model.CC and h in model.HH:
        return model.Qoff[(g, r), t, c, h] <= 1.17E+04*model.AYoff[2, (g, r), t]
    return Constraint.Skip
model.Qoff_up_constraint = Constraint(model.GR, model.TT, model.CC, model.h, rule=qoff_up_rule)
'''


# %% Stage 2 middle problem



from pyomo.environ import *
from pyomo.opt import SolverFactory

model1=ConcreteModel()


l_data = Sets_data.iloc[1, 2:4].values
g_data = Sets_data.iloc[2, 2:15].values 
p_data = Sets_data.iloc[3, 2:6].values
r_data = Sets_data.iloc[4, 2:6].values
s_data = Sets_data.iloc[5, 2:8].values
t_data = Sets_data.iloc[6, 2:8].values
d_data = Sets_data.iloc[7, 2:5].values
c_data = Sets_data.iloc[8, 2:4].values
h_data = Sets_data.iloc[9, 2:26].values
sc_data = Sets_data.iloc[10, 2:6].values
sv_data = Sets_data.iloc[11, 2:4].values
e_data = Sets_data.iloc[12, 2:5].values
I_data = Sets_data.iloc[1, 2:4].values
region1_data = Regions_data.iloc[2:48, 2].values
region2_data = Regions_data.iloc[2:48, 3].values
Neighbourhood_Regions = list(zip(region1_data,region2_data))

model1.l = Set(initialize=['Trailer', 'Pipe'])
model1.g = Set(initialize=g_data)
model1.g1 = Set(initialize=g_data)
model1.p = Set(initialize=p_data)
model1.r = Set(initialize=r_data)
model1.s = Set(initialize=s_data)
model1.t = Set(initialize=[3,4,5,6])#t_data)
model1.d1 = Set(initialize=d_data)
model1.d2 = Set(initialize=[1, 2])
model1.c = Set(initialize=c_data)
model1.h = Set(initialize=h_data)
model1.sc= Set(initialize=sc_data)
model1.sv= Set(initialize=sv_data)
model1.e = Set(initialize=e_data)
model1.j = RangeSet(1,24)

Region3_data = Regions_data.iloc[6:32, 17].values
storage_data = Regions_data.iloc[6:32, 18].values


Region4_data = Regions_data.iloc[2:32, 17].values
storage1_data = Regions_data.iloc[2:32, 18].values

GS_data = list(zip(Region4_data, storage1_data))
GS_data1 = list(zip(Region3_data, storage_data))
GS_data2 = [('NO', 'OnTeeside'), ('NW', 'OnChesire'), ('NE', 'OnYorkshire'), ('NW', 'OffIrishSea')]

model1.GS = Set(dimen=2, initialize=[(g,s) for g in model1.g for s in model1.s if (g,s) in GS_data])

model1.GS1 = Set(dimen=2, initialize=[(g,sv) for g in model1.g for sv in model1.sv if (g,sv) in GS_data1])
model1.GS2 = Set(dimen=2, initialize=[(g,sc) for g in model1.g for sc in model1.sc if (g,sc) in GS_data2])
Gimp_data = [(g_data[9]), (g_data[11]), (g_data[2]), (g_data[0])]
model1.Gimp = Set(within=model1.g, initialize= ['WS', 'SO', 'NO', 'NE', 'SC'])
#model.Gimp = Set(initialize=[(g) for g in model.g if (g) in Gimp_data])
GR_data=[(g_data[0], r_data[2]), (g_data[5], r_data[3]), (g_data[6], r_data[0])]
model1.GR = Set(dimen=2, initialize=[(g,r) for g in model1.g for r in model1.r if (g,r) in GR_data])
model1.N = Set(dimen=2, initialize=[(g,g1) for g in model1.g for g1 in model1.g if (g,g1) in Neighbourhood_Regions])



# ------ RangeSets -----

model1.TT = RangeSet(3, 6)  #  TT(t) /3*6/
model1.CC = RangeSet(1,n_clusters+1)  #  CC(c) /1*6/
model1.HH = RangeSet(1, 24) #  HH(h) /1*24/

Cluster_order = {cluster: i+1 for i, cluster in enumerate(model1.CC)}
model1.ord_c = Param(model1.CC, initialize=Cluster_order)

GasDemave_data = {(c, h,t, g): df_GasDemave.iloc[i, 2 + 13 * t_idx + g_idx]
    for i, (c, h) in enumerate(zip(df_GasDemave.iloc[:, 0], df_GasDemave.iloc[:, 1]))  
    for t_idx, t in enumerate(model1.TT)  
    for g_idx, g in enumerate(model1.g)}


BigQneg_data = {(c, h,j,t, g): df_BigQ_neg.iloc[i, 3 + 13 * t_idx + g_idx]
    for i, (c, h,j) in enumerate(zip(df_BigQ_neg.iloc[:, 0], df_BigQ_neg.iloc[:, 1], df_BigQ_neg.iloc[:, 2]))  
    for t_idx, t in enumerate(model1.TT)  
    for g_idx, g in enumerate(model1.g)}

BigQpos_data = {(c, h,j,t, g): df_BigQ_pos.iloc[i, 3 + 13 * t_idx + g_idx]
    for i, (c, h,j) in enumerate(zip(df_BigQ_pos.iloc[:, 0], df_BigQ_pos.iloc[:, 1], df_BigQ_pos.iloc[:, 2]))  
    for t_idx, t in enumerate(model1.TT)  
    for g_idx, g in enumerate(model1.g)}


model1.GasDemave = Param(model1.CC, model1.h, model1.t,model1.g,  initialize=GasDemave_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')

def dem_init2(model1, g, t, c, h):
    return model1.GasDemave[c, h, t, g]

model1.dem = Param(model1.g, model1.t, model1.CC, model1.h, initialize=dem_init2)


model1.BigQ_neg=Param(model1.CC,model1.h, model1.j, model1.TT,model1.g, initialize=BigQneg_data)
model1.BigQ_pos=Param(model1.CC,model1.h, model1.j, model1.TT,model1.g, initialize=BigQpos_data)



model1.Lem_Stage2=Param(model1.g, model1.TT, model1.CC, model1.HH)

model1.Stage2_phi=Param(initialize=2)
model1.Z_neg=Var(model1.TT,model1.g, model1.CC, model1.j, within=NonNegativeReals)
model1.Z_pos=Var(model1.TT,model1.g, model1.CC, model1.j, within=NonNegativeReals)
model1.Stage2_middle_dem=Var(model1.g, model1.TT, model1.CC, model1.HH, within=Reals)
model1.Stage2_middle_TC=Var()






def middle_demand_const1_rule(model1, g, t, c, h):
    if t in model1.TT and model1.ord_c[c]==1 and h in model1.HH:  # Equivalent to $(TT(t) and ord(c)=1 and HH(h))
        return model1.Stage2_middle_dem[g, t, c, h] == model1.dem[g, t, c, h]
    return Constraint.Skip

model1.Stage2_Middle_demand_const1 = Constraint(model1.g, model1.TT, model1.CC, model1.HH, rule=middle_demand_const1_rule)

def middle_demand_const2_rule(model1, g, t, c, h):
    if t in model1.TT and model1.ord_c[c]>1 and h in model1.HH:  # Equivalent to $(TT(t) and CC(c) and ord(c)>1 and HH(h))
        return model1.Stage2_middle_dem[g, t, c, h] == model1.GasDemave[c, h, t, g] + sum(
            model1.BigQ_neg[c, h, j, t, g] * model1.Z_neg[t, g, c, j] + 
            model1.BigQ_pos[c, h, j, t, g] * model1.Z_pos[t, g, c, j]
            for j in model1.j
        )
    return Constraint.Skip

model1.Stage2_Middle_demand_const2 = Constraint(model1.g, model1.TT, model1.CC, model1.HH, rule=middle_demand_const2_rule)


def constr_Z1_rule(model1, t, g, c, j):
    if model1.ord_c[c]>1:  # Equivalent to $(CC(c) and ord(c)>1)
        return model1.Z_neg[t, g, c, j] + model1.Z_pos[t, g, c, j] <= 1
    return Constraint.Skip

model1.Constr_Z1 = Constraint(model1.TT, model1.g, model1.CC, model1.j, rule=constr_Z1_rule)

# Constraint 2: sum_j (Z_neg + Z_pos) ≤ Stage2_phi
def constr_Z2_rule(model1, t, g, c):
    if model1.ord_c[c]>1:
        return sum(model1.Z_neg[t, g, c, j] + model1.Z_pos[t, g, c, j] for j in model1.j) <= model1.Stage2_phi
    return Constraint.Skip

model1.Constr_Z2 = Constraint(model1.TT, model1.g, model1.CC, rule=constr_Z2_rule)

# Constraint 3: Z_neg ≤ 1
def constr_Z3_rule(model1, t, g, c, j):
    if model1.ord_c[c]>1:
        return model1.Z_neg[t, g, c, j] <= 1
    return Constraint.Skip

model1.Constr_Z3 = Constraint(model1.TT, model1.g, model1.CC, model1.j, rule=constr_Z3_rule)

# Constraint 4: Z_pos ≤ 1
def constr_Z4_rule(model1, t, g, c, j):
    if model1.ord_c[c]>1:
        return model1.Z_pos[t, g, c, j] <= 1
    return Constraint.Skip

model1.Constr_Z4 = Constraint(model1.TT, model1.g, model1.CC, model1.j, rule=constr_Z4_rule)



# %%
model.log = Param(model.it, mutable=True, initialize=0) 
model2.log_Stage2 = Param(model2.Stage2_it, mutable=True, initialize=0)
model2.log_Stage2_fesi = Param(model2.Stage2_it, mutable=True, initialize=0)

model.lastiteration = Param(initialize=0, mutable=True)

model.Stage2_fesi_bound = Param(initialize=0, mutable=True)
model2.iteration_Stage2 = Param(initialize=0, mutable=True)
model.fesi_iteration_Stage2 = Param(initialize=0, mutable=True)
model.aa_index = Param(initialize=0, mutable=True)
model.aa_e = Param(initialize=1)
import math
model.ub = Param(initialize=math.inf, mutable=True)  # بی‌نهایت مثبت
model.lb = Param(initialize=-math.inf, mutable=True)  # بی‌نهایت منفی

model.outer_upper = Param(initialize=math.inf, mutable=True)
# %% 

# %%  Solving the model
import tkinter as tk
from tkinter import messagebox
from pyomo.environ import SolverFactory, SolverManagerFactory
import os

# List of Local Solvers
solvers = [("Gurobi", "gurobi"), ("CPLEX", "cplex"), ("GLPK", "glpk"), ("HiGHS", "highs")]

# ------------------- Helper: Center Window -------------------
def center_window(win, width=400, height=200):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# ------------------- Local Solver Settings -------------------
def open_local_solver_settings(selected_solver, model):
    settings_dialog = tk.Toplevel(root)
    settings_dialog.title(f"{selected_solver} Settings")
    settings_dialog.configure(bg="#34495e")
    center_window(settings_dialog, 300, 250)
    
    tk.Label(settings_dialog, text="Enter Solver Settings", font=("Arial", 14, "bold"), fg="white", bg="#34495e").pack(pady=10)

    tk.Label(settings_dialog, text="Time Limit (seconds):", font=("Arial", 12), fg="white", bg="#34495e").pack()
    time_limit_entry = tk.Entry(settings_dialog, font=("Arial", 12))
    time_limit_entry.insert(0, "600")
    time_limit_entry.pack(pady=5)

    tk.Label(settings_dialog, text="MIP Gap (e.g. 0.05):", font=("Arial", 12), fg="white", bg="#34495e").pack()
    mip_gap_entry = tk.Entry(settings_dialog, font=("Arial", 12))
    mip_gap_entry.insert(0, "0.05")
    mip_gap_entry.pack(pady=5)

    def solve_local():
       
        time_limit = (time_limit_entry.get())
        mip_gap = (mip_gap_entry.get())
        settings_dialog.destroy()
        root.destroy()
        opt = SolverFactory(selected_solver.lower())
        opt.options['Threads'] = 36
        opt.options['Presolve'] = 2
        opt.options['MIPGap'] = mip_gap
        opt.options['TimeLimit'] = time_limit
        opt.options['Heuristics'] = 0.1
        root.update()
        results = opt.solve(model, tee=True)
        messagebox.showinfo("Solver Finished", f"{selected_solver} finished solving!")
        settings_dialog.destroy()

    tk.Button(settings_dialog, text="Solve", command=solve_local, font=("Arial", 12), bg="#2ecc71", fg="white").pack(pady=15)

# ------------------- NEOS Solver -------------------
def open_neos_settings(model):
    neos_dialog = tk.Toplevel(root)
    neos_dialog.title("NEOS Settings")
    neos_dialog.configure(bg="#34495e")
    center_window(neos_dialog, 300, 180)

    tk.Label(neos_dialog, text="NEOS Solver Settings", font=("Arial", 14, "bold"), fg="white", bg="#34495e").pack(pady=10)
    tk.Label(neos_dialog, text="Enter your NEOS Email:", font=("Arial", 12), fg="white", bg="#34495e").pack()
    email_entry = tk.Entry(neos_dialog, font=("Arial", 12))
    email_entry.pack(pady=5)
    email_entry.insert(0, "m.hemmati@ucl.ac.uk")

    def solve_neos():
        
        email = email_entry.get()
        neos_dialog.destroy()
        root.destroy()
        os.environ['NEOS_EMAIL'] = email
        solver_manager = SolverManagerFactory('neos')
        root.update()
        results = solver_manager.solve(
            model,
            opt='cplex',
            tee=True,
            keepfiles=False,
            load_solutions=True,
            timelimit=600
        )
        messagebox.showinfo("NEOS Finished", "Model solved on NEOS!")
        neos_dialog.destroy()

    tk.Button(neos_dialog, text="Solve on NEOS", command=solve_neos, font=("Arial", 12), bg="#2980b9", fg="white").pack(pady=15)

# ------------------- Local Solver Selection -------------------
def open_local_solver_selection(model):
    local_dialog = tk.Toplevel(root)
    local_dialog.title("Select Local Solver")
    local_dialog.configure(bg="#34495e")
    center_window(local_dialog, 300, 250)

    tk.Label(local_dialog, text="Select a Local Solver", font=("Arial", 14, "bold"), fg="white", bg="#34495e").pack(pady=10)
    
    for solver_name, solver_id in solvers:
        tk.Button(local_dialog, text=solver_name, font=("Arial", 12), bg="#16a085", fg="white",
                  command=lambda s=solver_id, w=local_dialog: select_solver(s, model, w)).pack(pady=5)

def select_solver(solver_id, model, parent_window):
    parent_window.destroy()  
    
    open_local_solver_settings(solver_id, model)

# ------------------- Main Window -------------------
root = tk.Tk()
root.title("Optimization Solver Selector")
root.configure(bg="#2c3e50")
center_window(root, 400, 200)

tk.Label(root, text="Select Solver Mode", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=20)


try:
    model
except NameError:
    messagebox.showerror("Error", "The variable 'model' is not defined!")
    root.destroy()

tk.Button(root, text="Local Solver", font=("Arial", 14), bg="#27ae60", fg="white", width=15,
          command=lambda: open_local_solver_selection(model)).pack(pady=5)

tk.Button(root, text="NEOS Solver", font=("Arial", 14), bg="#2980b9", fg="white", width=15,
          command=lambda: open_neos_settings(model)).pack(pady=5)

root.mainloop()
#%%

current_Stage2_fixed_dem = {
    ('it1', g, t, c, h): value  # Assigning a default iteration value ('it1')
    for (g, t, c, h), value in model2.Stage2_fixed_dem.extract_values().items()
}

for i in range(2, 10):  # مقدار `it2` تا `it9`
    if hasattr(model, "iter1"):
        model.del_component("iter1")  # حذف قبلی

    valid_values = [f'it{i}' for i in range(2, 10) if f'it{i}' in model.it]
    model.add_component("iter1", Set(within=model.it, initialize=valid_values))

    if hasattr(model, "iter_fesi"):
        model.del_component("iter_fesi")  # حذف قبلی

    valid_values2 = [f'it{i}' for i in range(2, 10) if f'it{i}' in model.it]
    model.add_component("iter_fesi", Set(within=model.it, initialize=valid_values2))

    if hasattr(model, "Stage1_dem"):
        model.del_component("Stage1_dem")

    model.Stage1_dem = Param(model.it, model.g, model.t, model.CC, model.h, initialize=current_Stage2_fixed_dem)

    results = opt.solve(model, tee=True)

    fixed_values_InvP = {(p, g, t): round(model.InvP[p, g, t]()) for p in model.p for g in model.g for t in model.TT}
    fixed_values_InvS = {(s, g, t): round(model.InvS[s, g, t]()) for s in model.s for g in model.g for t in model.TT if (s, g) in model.GS}

    model2.Stage2_converged = Param(initialize=0, mutable=True)
    model2.Stage2_bound = Param(initialize=math.inf, mutable=True)

    if not hasattr(model2, "log_Stage2"):
        model2.log_Stage2 = Param(mutable=True, initialize={})

    for i in range(2, 31):
        if hasattr(model, "Stage2_it"):
            model.del_component("Stage2_it")

        valid_values = [f'Stage2_it{i}' for i in range(2, 10) if f'Stage2_it{i}' in model.it]
        model.add_component("Stage2_it", Set(within=model.it, initialize=valid_values))

        results = opt.solve(model2, tee=True)

        current_Stage2_Lower_TC = model2.Stage2_Lower_TC()

        if current_Stage2_Lower_TC is not None:
           current_Stage2_Lower_TC = 0 
            

        status = results.solver.termination_condition
        

        if status in {TerminationCondition.optimal, TerminationCondition.feasible}:
            model2.log_Stage2.store_values({(i, 'Sta2_error'): abs(
                (model2.Stage2_bound.value - current_Stage2_Lower_TC) / model2.Stage2_bound.value
            )})

            if not hasattr(model2, "iteration_Stage2"):
                model2.iteration_Stage2 = Param(initialize=i, mutable=True)
            else:
                model2.iteration_Stage2.value = i

            if abs((model2.Stage2_bound.value - current_Stage2_Lower_TC) / model2.Stage2_bound.value) < 1E-8:
                model2.stage2_converged.value = 1

            model2.Stage2_bound.value = current_Stage2_Lower_TC

            for g in model2.g:
                for t in model2.TT:
                    for c in model2.CC:
                        for h in model2.HH:
                            model2.Lem_stage2[g, t, c, h] = model2.Demand_Stage2Cons[g, t, c, h].dual  

            print("Stage2_lower_TC:", current_Stage2_Lower_TC)
            print("Stage2_bound:", model2.Stage2_bound.value)

        elif status not in {TerminationCondition.optimal, TerminationCondition.feasible}:
            model2.aa_index.value = 0
            raise StopIteration


        def middle_obj_rule(model1):
            return model1.Stage2_middle_TC == current_Stage2_Lower_TC + sum(
                model1.Lem_stage2[g, t, c, h] * 
                (model1.Stage2_middle_dem[g, t, c, h] - model1.Stage2_fixed_dem[g, t, c, h])
                for g in model1.g for t in model1.TT for c in model1.CC for h in model1.HH
            )

        model1.Stage2_middle_Obj = Constraint(rule=middle_obj_rule)
        results = opt.solve(model1, tee=True)

        current_Stage2_middle_dem = {
            (g, t, c, h): model1.Stage2_middle_dem[g, t, c, h]()
            for g in model1.g for t in model1.TT for c in model1.CC for h in model1.HH
        }

        model2.Stage2_fixed_dem = Param(model2.g, model2.TT, model2.CC, model2.HH, initialize=current_Stage2_middle_dem)

        model.outer_lower = Param(initialize=model.Stage1_TC)
        model.outer_upper = Var(initialize=0)  # مقداردهی اولیه متغیر 

        model.outer_upper.set_value(
            model.Stage2_middle_TC.value +
            1000 * model.PCC.value + model.SCC.value +
            1000 * model.PipeCC.value + 1000 * model.PipeOC.value +
            model.ReC.value + model.POC1.value + model.SOC1.value
        )

        if abs((model.outer_upper.value - model.outer_lower.value) / model.outer_upper.value) < 1E-3 and model.it.value > 1:
            model.converged.value = 1

        model.log[model.it, 'lb'] = model.outer_lower.value
        model.log[model.it, 'ub'] = model.outer_upper.value

        model.lastiteration.value = model.it.value




    


    
    

    
    
    
    
   
                



# %% Saving Results




