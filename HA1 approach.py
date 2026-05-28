#======================================Input Data========================================================*
# %% Reading Data from Excel-----------------------

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
Heating_data = excel_data.parse('Heating')
Storage_data = excel_data.parse('Storage')
Production_data = excel_data.parse('Production')
Renewables_data = excel_data.parse('Renewables')
Emissions_data = excel_data.parse('Emissions')
H2Pipline_data = excel_data.parse('H2Pipeline')
CO2Pipline_data = excel_data.parse('CO2Pipeline')
CO2Reservior_data = excel_data.parse('CO2Reservoir')
Biomass_data = excel_data.parse('Biomass')

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


import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import threading
import pandas as pd


# Global variables
global df_GasDem, df_Demand_data, df_Availability, n_clusters

df_GasDem = None
df_Demand_data = None
df_Availability = None
n_clusters = None  


def run_kmediods(n_clusters_input):
    print("Running Kmediods.py with clusters:", n_clusters_input)
    result = subprocess.run(
        ['python', 'Kmediods.py'],
        input=n_clusters_input,  
        capture_output=True,
        text=True
    )
    if result.stderr:
        print(f"Error: {result.stderr}")
    else:
        print(f"Output: {result.stdout}")


def select_process(root):
    global df_GasDem, df_Demand_data, df_Availability, n_clusters

    n_clusters = simpledialog.askinteger("Input", 
                                         "Enter number of representative days:\n(Default value: 5)"
                                        )

    if n_clusters is None:
        return  

    n_clusters_input = str(n_clusters) + '\n'
    root.after(0, root.quit)

    thread = threading.Thread(target=run_kmediods, args=(n_clusters_input,), daemon=False)
    thread.start()
    thread.join()  

    process_data(n_clusters)
    root.withdraw()


def process_data(n_clusters):
    global df_GasDem, df_Demand_data, df_Availability
    file_path3 = os.path.join(os.getcwd(), 'Final_cluster.xlsx')
    excel_data = pd.ExcelFile(file_path3, engine='openpyxl')
    
    df_GasDem = excel_data.parse('Demand', header=None, usecols="A:N", skiprows=1, nrows=24 * (n_clusters+1))
    df_Demand_data = excel_data.parse('Cluster and weights', usecols="A:B", skiprows=0, nrows=n_clusters+1)
    df_Availability = excel_data.parse('Availability', header=None, usecols="A:AN", skiprows=1, nrows=24*(n_clusters+1))

    print("Clustering processing complete.")


def center_window(win, width=500, height=400):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


def create_main_window():
    root = tk.Tk()
    root.title("Clustering Method Selection")
    
    root.geometry("500x300")
    center_window(root, 500, 300)  
    root.configure(bg="#2c3e50")  

    label = tk.Label(root, text="Select Clustering Method", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
    label.pack(pady=20)

    tk.Button(root, text="Kmediods", font=("Arial", 12, "bold"), fg="white", bg="#3498db",
              width=25, height=2, command=lambda: select_process(root)).pack(pady=10)
    
    root.mainloop()


create_main_window()


#======================================Building the Model========================================================*
# %% Concerete Model ------------------------------
from pyomo.environ import *
from pyomo.environ import SolverFactory

def First_step():
 model = ConcreteModel()
 # %% ---------------------------------Define Main and Additional Sets and Subsets ------------------------------
 l_data = Sets_data.iloc[1, 2:4].values
 g_data = Sets_data.iloc[2, 2:15].values 
 p_data = Sets_data.iloc[3, 2:6].values
 r_data = Sets_data.iloc[4, 2:6].values
 s_data = Sets_data.iloc[5, 2:8].values
 t_data = Sets_data.iloc[6, 2:8].values
 d_data = Sets_data.iloc[7, 2:5].values
 c_data = Sets_data.iloc[8, 2:8].values
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

 #model.g = Set(initialize=lambda model: {pair[0] for pair in model.N})
 #model.g1 = Set(initialize=lambda model: {pair[1] for pair in model.N})

 # Aliases
 model.gg = Set(dimen=2, initialize=lambda model: [(g,g1) for g in model.g for g1 in model.g])
 model.hh = Set(dimen=2, initialize=lambda model: [(h,h1) for h in model.h for h1 in model.h])

 # ------ RangeSets -----

 model.TT = RangeSet(3, 6)  #  TT(t) /3*6/
 model.CC = RangeSet(1,n_clusters+1)  #  CC(c) /1*6/
 model.HH = RangeSet(1, 6) #  HH(h) /1*24/
 # %% Assign spacific data for parameters-----------
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
 AV_data = {(c, h, g, e): df_Availability.iloc[i, 2 + 3 * g_idx + e_idx]
     for i, (c, h) in enumerate(zip(df_Availability.iloc[:, 0], df_Availability.iloc[:, 1]))  
     for g_idx, g in enumerate(model.g)  
     for e_idx, e in enumerate(model.e)}

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

 
 
 GasDem_data = {
         (int(c), int(h), g): df_GasDem.iloc[i, 1 + j] 
         for i, pair in enumerate(df_GasDem.iloc[:, 0])  
         for j, g in enumerate(model.g)  
         for c, h in [map(int, pair.strip("()").split(","))]  
     }
 #elif method == 'Robust':
     
     #GasDem_data = {(c, h, g): df_GasDem.iloc[i, 2+j] 
                   # for i, (c, h) in enumerate(zip(df_GasDem.iloc[:, 0], df_GasDem.iloc[:, 1]))  
                   # for j, g in enumerate(model.g)}




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
 diameter_order = {diameter: i + 1 for i, diameter in enumerate(model.d1)}          
 Trans_order = {transLine: i + 1 for i, transLine in enumerate(model.l)}  
 Production_order = {production: i+1 for i, production in enumerate(model.p)}
 Storage_order = {storage: i+1 for i, storage in enumerate(model.s)}
 Hour_order = {time: i+1 for i, time in enumerate (model.h)}

 model.ord_g = Param(model.g, initialize=region_order)
 #model.ord_d = Param(model.d, initialize=diameter_order)
 model.ord_l = Param(model.l, initialize=Trans_order)
 model.ord_p = Param(model.p, initialize=Production_order)
 model.ord_s= Param(model.s, initialize=Storage_order )
 model.ord_h = Param(model.h, initialize=Hour_order)
 # %%
 #======================================Parameters========================================================
 # %% Define Parameter------------------------------
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
 model.GasDem = Param(model.CC, model.h, model.g,  initialize=GasDem_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')
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
 model.WF = Param(model.CC, initialize=WF_data, doc='Weight of clusters')

 # ---- Scalar ----
 model.y1 = Param(initialize=3, doc="Scalar y1")
 model.theta = Param(initialize=4, doc="Scalar theta")

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
 '''
 model.dfo = Expression(
     model.t,
     rule=lambda model, t: round(
         1 / (1 + model.ir) ** (model.dur * t - 5) +
         1 / (1 + model.ir) ** (5 * t - 4) +
         1 / (1 + model.ir) ** (5 * t - 3) +
         1 / (1 + model.ir) ** (5 * t - 2) +
         1 / (1 + model.ir) ** (5 * t - 1),
         2
     )
 )
 '''
 def biomass_availability_init(model, g, t):
     return model.bp * model.br[g] * model.Vbio_max[t] * 1000000

 model.BA = Param(model.g, model.TT, initialize=biomass_availability_init,  doc="Biomass availability in region g and time period t")


 '''
 model.BA = Expression(model.g, model.t, rule=lambda model, g, t: model.bp * model.br[g] * model.Vbio_max[t] * 1000000,  doc='Biomass availability in region g and time period t')
 '''
 #model.dem = Expression(model.g, model.t, model.CC, model.h, rule=lambda model, g, t, c, h:model.dc[t]*model.GasDem[c,h,g])

 def dem_init(model, g, t, CC, h):
     return model.dc[t] * model.GasDem[CC, h, g] 
 model.dem = Param(model.g, model.TT, model.CC, model.h, initialize=dem_init)
 '''
 model.RI_up = Expression(model.r, model.TT, rule=lambda model, r,t :model.rcap[r]/1000 )
 '''
 '''
 model.Npipe = Set(dimen=2, initialize=[(g,g1) for g in model.g for g1 in model.g if model.DistPipe[g, g1] > 0 ])
 '''
 model.Npipe = Set(dimen=2,initialize=model.DistPipe.keys(), doc='Set of region pairs with nonzero pipeline distances')

 '''
 model.Npipe = Set(
     initialize=lambda model: [(g, g1) for g in model.g for g1 in model.g1 if model.DistPipe[g, g1] > 0],
     doc="Set of region pairs (g, g1) with a non-zero distance (DistPipe > 0)"
 )
 '''

 # Availability and initial availability parameters
 model.AV = Param(model.CC, model.h, model.g, model.e, initialize=AV_data, doc='Availability of renewable e in region g, cluster c and hour h (%)')
 model.ayHR0 = Param(model.d1, model.Npipe,initialize=0, doc='Initial availability of a regional hydrogen pipeline of diameter size d between regions g and g1 (0-1)')
 model.ayC0 = Param(model.d2, model.N, initialize=0, doc='Initial availability of an onshore CO2 pipeline of diameter size d between regions g and g1 (0-1)')
 model.aeC0 = Param(model.r, initialize=0, doc='Initial availability of an offshore CO2 pipeline between collection point in regions g and reservoir r (0-1)')

 '''
 InvP_data = {}
 for g in model.g:
     for t in model.TT:
         InvP_data[('SMRCCS', g, t)] = 10
         InvP_data[('ATRCCS', g, t)] = 10
         InvP_data[('BECCS', g, t)] = 10
         InvP_data[('WE', g, t)] = 50
 model.InvP_up = Param(model.p, model.g, model.TT, initialize=InvP_data)
 '''

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


 def Qup_bounds_rule(model, l, g, g1,t, c, h):
     if l in ['Pipe']:
         return (0,15343)
     return (0, None)


 # %% HA1 defination Parameter
  
 
 def demH_init(model, g, t, c, HH):
     start_h = (HH - 1) * 4 + 1  
     end_h = start_h + 3  
     
     return sum(model.dem[g, t, c, h]/4 for h in range(start_h, end_h + 1))

 model.demH = Param(model.g, model.TT, model.CC, model.HH, initialize=demH_init)
 
 def AVH_init(model, c,HH,g,e):
     start_h = (HH - 1) * 4 + 1
     end_h = start_h + 3
     return sum(model.AV[c, h, g, e]/4 for h in range(start_h, end_h + 1))

 model.AVH = Param(model.CC, model.HH, model.g, model.e, initialize=AVH_init)    
 


 # %%
 #======================================Variables========================================================
 # %% Define Variables------------------------------

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


 # Positive variables
 model.NP = Var(model.p, model.g, model.TT, within=NonNegativeReals, doc="Number of plants of type j and size p in region g in time period t")
 model.NS = Var(model.s, model.g, model.TT, within=NonNegativeReals, bounds=NS_bounds_rule, doc="Number of storage facilities of type s and size p in region g in time period t")
 #model.NS_up = Var(model.s, model.g, model.TT, within=NonNegativeIntegers)
 #model.ITU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals, bounds=(0,25), doc="Number of new transportation units of type l for regional transportation byroad in region g to region g acquired in time period t")
 #model.NTU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals,   doc="Number of transportation units of type l for regional transportation by road in region g in time period t")
 model.AY = Var(model.d1, model.Npipe, model.TT, within=NonNegativeReals,  doc="availability of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
 model.AYon=Var(model.d2, model.N, model.TT, within=NonNegativeReals,  doc="availability of onshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
 model.AYoff = Var(model.d2, model.GR, model.TT, within=NonNegativeReals,  doc="availability of offshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
 model.AYst = Var(model.d1, model.GS2, model.TT, within=NonNegativeReals, doc="availability of hydrogen pipelines of diameter size d for distribution in region g in time period t")
 model.CL = Var(model.g, model.TT, model.CC, model.HH, within=NonNegativeReals, doc='Curtailment (MW)')
 model.InvR = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000), doc='Invested capacity of renewable (MW)')
 #model.InvR_up = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000))
 model.IMP = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals,
                 doc='Flow rate of international import (MW)')
 model.NR = Var(model.e, model.g, model.TT, within=NonNegativeReals,  doc='Capacity of renewable (MW)')
 model.Pr = Var(model.p, model.g, model.TT, model.CC,model.HH,within=NonNegativeReals,      doc='Production rate (MW)')
 model.Pre = Var(model.e, model.g, model.TT, model.CC, model.HH, within=NonNegativeReals,    doc='Electricity production from renewable (MW)')
 model.Q = Var(model.l, model.Npipe, model.TT, model.CC, model.HH, within=NonNegativeReals, bounds=Qup_bounds_rule, doc='Regional flowrate of H2 (MWh)')
 model.Qi = Var(model.g,model.s, model.TT, model.CC,model.HH, within=NonNegativeReals,  doc='H2 via pipeline to storage (MWh)')
 model.Qr = Var(model.s, model.g, model.TT, model.CC, model.HH, within=NonNegativeReals,  doc= 'flowrate of H2 via pipeline from region g to storage type s in time period t(MWh)')
 model.Qon = Var(model.N, model.TT, model.CC, model.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via onshore pipelines (kg CO2/d)')
 model.Qoff = Var(model.GR, model.TT, model.CC, model.HH, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via offshore pipelines (kg CO2/d)')
 #odel.Rdown = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals,initialize=0, doc='Upward reserve contribution (MWh)')
 #odel.Rup = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Downward reserve contribution (MWh)')
 model.St = Var(model.s,model.g, model.TT, model.CC, model.HH, within=NonNegativeReals, doc='Average inventory of product stored (kW)')
 model.Vbio = Var(model.TT, within=NonNegativeReals,  doc='Biomass consumption (kg)' )
 model.Vgas = Var(model.TT, within=NonNegativeReals, doc='Gas consumption (kg)')
 #model.slak1 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 1')
 #model.slak2 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 2')
 model.PCC = Var()
 model.SCC = Var()
 model.TCC=Var()
 model.POC = Var()
 model.SOC = Var()
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
 model.CEC = Var(within=Reals)
 model.IIC = Var()
 model.ReC = Var()
 model.GC = Var( )
 model.BC = Var( )
 model.ROC = Var()
 model.TOC=Var()
 model.em = Var(model.TT, within=Reals)




 # %%
 #======================================Objective Function========================================================*
 # %% Objective Function and related components----

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
     return 0.001*model.PipeCC == 0.001*(sum(
         # First summation: Hydrogen pipeline cost
         model.dfc[t] * model.cccH[d1] * model.DistPipe[g, g1] * model.Yh[d1, (g, g1), t]
         for d1 in model.d1
         for g in model.g
         for g1 in model.g
         if (g, g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1]
         for t in model.TT
     ) + sum(
         # Second summation: Onshore CO2 cost
         model.dfc[t] * model.cccC_onshore[d2] * model.Dist[g, g1] * model.Yon[d2, (g, g1), t]
         for d2 in model.d2
         for g in model.g
         for g1 in model.g
         if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]
         for t in model.TT
     ) + sum(
         # Third summation: Offshore CO2 cost
         model.dfc[t] * model.cccC_offshore[d2] * model.DistRes[g, r] * model.Yoff[d2, (g, r), t]
         for d2 in model.d2
         for g in model.g
         for r in model.r
         if (g, r) in model.GR
         for t in model.TT
     ) + sum(
         # Fourth summation: Storage cost
         model.dfc[t] * model.cccH[d1] * model.DistSt[g, sc] * model.Yst[d1, (g, sc), t]
         for d1 in model.d1
         for g in model.g
         for sc in model.sc
         if (g, sc) in model.GS2
         for t in model.TT
     ))
 model.PipeCCConstraint = Constraint(rule=pipecc_rule)

 # Constraint for TCC (Total Capital Cost)
 def tcc_rule(model):
     return model.TCC == 1000*model.PipeCC
 model.TCCConstraint = Constraint(rule=tcc_rule)


 # Constraint for POC
 def poc_rule(model):
     return 0.001*model.POC == 0.001*sum(
         model.dfo[t] * (
             model.pocostF[p, t] * model.PCap[p] * model.NP[p, g, t] +
             sum(
                 model.WF[c] * model.pocostV[p, t] * model.theta * model.Pr[p, g, t, c, h]
                 for c in model.CC for h in model.HH
             )
         )
         for p in model.p for g in model.g for t in model.TT
     )
 model.POCConstraint = Constraint(rule=poc_rule)

 # Constraint for SOC
 def soc_rule(model):
     return 0.001*model.SOC == 0.001* sum(
         model.dfo[t] * (
             model.socostF[s] * model.SCap[s] * model.NS[s, g, t] +
             sum(
                 model.WF[c] * model.socostV[s] * model.theta * model.Qi[g, s, t, c, h]
                 for c in model.CC for h in model.HH
             )
         )
         for s in model.s for g in model.g if (g, s) in model.GS for t in model.TT
     )
 model.SOCConstraint = Constraint(rule=soc_rule)
 
 # Constraint for PipeOC
 def pipeoc_rule(model):
     return 0.001*model.PipeOC == 0.001*(sum(
         model.dfo[t] * model.deltaH * model.crf * model.cccH[d1] * model.DistPipe[g, g1] * model.AY[d1, (g, g1), t]
         for d1 in model.d1 
         for g in model.g 
         for g1 in model.g 
         if (g, g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1]
         for t in model.TT
     ) + sum(
         model.dfo[t] * model.deltaC_onshore * model.crf * model.cccC_onshore[d2] * model.Dist[g, g1] * model.AYon[d2, (g, g1), t]
         for d2 in model.d2 
         for g in model.g 
         for g1 in model.g 
         if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]
         for t in model.TT
     ) + sum(
         model.dfo[t] * model.deltaC_offshore * model.crf * model.cccC_offshore[d2] * model.DistRes[g, r] * model.AYoff[d2, (g, r), t]
         for d2 in model.d2 
         for g in model.g 
         for r in model.r if (g, r) in model.GR 
         for t in model.TT
     ) + sum(
         model.dfo[t] * model.deltaH * model.crf * model.cccH[d1] * model.DistSt[g, sc] * model.AYst[d1, (g, sc), t]
         for d1 in model.d1 
         for g in model.g 
         for sc in model.sc if (g, sc) in model.GS2 
         for t in model.TT
     ))
 model.PipeOCConstraint = Constraint(rule=pipeoc_rule)
 
 # Constraint for TOC
 def toc_rule(model):
     return model.TOC ==  1000 * model.PipeOC
 model.TOCConstraint = Constraint(rule=toc_rule) 


 # Constraint for CEC
 def cec_rule(model):
     return model.CEC == sum(
         model.WF[c] * model.dfo[t] * model.ct[t] * model.y_e[p, t] * model.theta * model.Pr[p, g, t, c, h]
         for p in model.p for g in model.g for t in model.TT for c in model.CC for h in model.HH
     )
 model.CECConstraint = Constraint(rule=cec_rule)

 # Constraint for IIC
 def iic_rule(model):
     return model.IIC == sum(
         model.WF[c] * model.dfo[t] * model.pimp * model.theta * model.IMP[g, t, c, h]
         for g in model.Gimp for t in model.TT for c in model.CC for h in model.HH
     )
 model.IICConstraint = Constraint(rule=iic_rule)

 # Constraint for ReC
 def rec_rule(model):
     return 0.001*model.ReC == 0.001*sum(
         model.dfc[t] * model.rccost[e, t]* model.InvR[e, g, t] +
         model.dfo[t] * model.rocost[e, t] * model.NR[e, g, t]
         for t in model.TT for e in model.e for g in model.g
     )
 model.ReCConstraint = Constraint(rule=rec_rule)

 # Constraint for GC
 def gc_rule(model):
     return model.GC == sum(
         model.dfo[t] * model.cgas[t] * model.Vgas[t]
         for t in model.TT
     )
 model.GCConstraint = Constraint(rule=gc_rule)

 # Constraint for BC
 def bc_rule(model):
     return model.BC == sum(
         model.dfo[t] * model.cbio[t] * model.Vbio[t]
         for t in model.TT
     )
 model.BCConstraint = Constraint(rule=bc_rule)


 def objective_rule(model):
     return (
         1000*model.PCC+ 
         model.SCC+ 
         model.TCC+ 
         model.POC+ 
         model.SOC+ 
         model.TOC+ 
         model.CEC+ 
         model.IIC+ 
         model.ReC+
         model.GC+ 
         model.BC 
     )   
                   
 model.TC = Objective(rule=objective_rule, sense=minimize)



 # %%
 #======================================Problem Constraints========================================================*



 #---------- FUELS CONSUMPTION --------------*
 # %%  Fuel Constraint ----------------------------
 def gas_cons_rule(model, t):
     if t in model.TT:
         return model.Vgas[t] == sum(
             model.WF[c] * model.theta * model.Pr[p, g, t, c, h] / model.eta[p, t]
             for p in model.p if model.ord_p[p] <= 2 for g in model.g for c in model.CC for h in model.HH
             
         )
     return Constraint.Skip

 model.GasConsConstraint = Constraint(model.TT, rule=gas_cons_rule)

 # Biomass consumption
 def bio_cons_rule(model, t):
     if t in model.TT:
         return model.Vbio[t] == sum(
             model.WF[c] * model.theta * model.Pr['BECCS', g, t, c, h] / model.eta['BECCS', t]
             for g in model.g for c in model.CC for h in model.HH
         )
     return Constraint.Skip

 model.BioConsConstraint = Constraint(model.TT, rule=bio_cons_rule)



 # Biomass Availability 
 
 def biomass_availability_rule(model, g, t):
     if t in model.TT:  # Apply the constraint only for TT(t)
         return sum(
             0.001* model.WF[c] * model.theta * model.Pr['BECCS', g, t, c, h] / model.eta['BECCS', t]
             for c in model.CC for h in model.HH
         ) <= 0.001* model.BA[g,t]
     return Constraint.Skip

 model.BiomassAvailabilityConstraint = Constraint(model.g, model.TT, rule=biomass_availability_rule)
 # %%  RAMP UP/DOWN -------------------------------

 # Ramp Up
 def ramp_up_rule(model, p, g, c, h, t):
     if t in model.TT and c in model.CC and h in model.HH and h > 1:
         return model.Pr[p, g, t, c, h] - model.Pr[p, g, t, c, h - 1] <=model.theta * model.RU[p] * model.PCap[p] * model.NP[p, g, t]
     return Constraint.Skip

 model.RampUpConstraint = Constraint(model.p, model.g, model.CC, model.HH, model.TT, rule=ramp_up_rule)


 # Ramp Down
 def ramp_down_rule(model, p, g, c, h, t):
     if t in model.TT and c in model.CC and h in model.HH and h > 1:
         return model.Pr[p, g, t, c, h - 1] - model.Pr[p, g, t, c, h] <= model.theta * model.RD[p] * model.PCap[p] * model.NP[p, g, t]
     return Constraint.Skip

 model.RampDownConstraint = Constraint(model.p, model.g, model.CC, model.HH, model.TT, rule=ramp_down_rule)
 # %%  Peoduction Limit ---------------------------
 # Production Limit
 
 def p_capacity2_rule(model, p, g, t, c, h):
     if t in model.TT and c in model.CC and h in model.HH:
         return model.Pr[p, g, t, c, h] <= model.PCap[p] * model.pcap_max[p] * model.NP[p, g, t]
     return Constraint.Skip

 model.PCapacity2Constraint = Constraint(model.p, model.g, model.TT, model.CC, model.HH, rule=p_capacity2_rule)

 
 def p_availability_rule(model, p, g, t):
      if t in model.TT:
       return model.NP[p, g, t] == (
             model.NP[p, g, t-1] if t>model.y1 else 0 
         )+( 
         model.np0[p, g] if t==model.y1 else 0
         )+ model.InvP[p, g, t] 
      return Constraint.Skip

 model.PAvailability = Constraint(model.p, model.g, model.TT, rule=p_availability_rule)
  
 #---------- STORAGE CONSTRAINTS --------------*
 # %%  Storage Limit ------------------------------
 # Storage 
 

 def sinventory2_rule(model, s, g, t, c, h):
     if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
         return model.St[s, g, t, c, h] == (
             (model.St[s, g, t, c, h - 1] if h > 1 else model.st0[s, g]) 
             + model.theta * (model.Qi[g, s, t, c, h] - model.Qr[s, g, t, c, h])
         )
     return Constraint.Skip
 model.SInventory2 = Constraint(model.s, model.g, model.TT, model.CC, model.HH, rule=sinventory2_rule)


 # Maximum injection rate
 def max_inj_rule(model, s,g,t, c, h):
     if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
         return model.Qi[(g, s), t, c, h] <= model.QImax[s] * model.NS[s, g, t]
     return Constraint.Skip

 model.MaxInjConstraint = Constraint( model.GS, model.TT, model.CC, model.HH, rule=max_inj_rule)


 # Maximum retrieval rate
 def max_retr_rule(model, s, g, t, c, h):
     if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
         return model.Qr[s, g, t, c, h] <= model.QRmax[s] * model.NS[s, g, t]
     return Constraint.Skip
 model.MaxRetrConstraint = Constraint(model.s,model.g, model.TT, model.CC, model.HH, rule=max_retr_rule)

 # Underground storage capacity
 def s_capacity_u_rule(model, sc, g, t, c, h):
     if (g,sc) in model.GS2 and t in model.TT and c in model.CC and h in model.HH:
         return model.InvS[sc, g, t] <= sum(model.Yst[d1, g, sc, t] for d1 in model.d1)
     return Constraint.Skip

 model.SCapacityUConstraint = Constraint(model.GS2, model.TT, model.CC, model.HH, rule=s_capacity_u_rule)

 # Storage capacity constraints
 def s_capacity1_rule(model, s, g, t, c, h):
     if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
         return model.St[s, g, t, c, h] >= model.SCap[s] * model.scap_min[s] * model.NS[s, g, t]
     return Constraint.Skip

 model.SCapacity1Constraint = Constraint(model.s,model.g, model.TT, model.CC, model.HH, rule=s_capacity1_rule)

 def s_capacity2_rule(model, s, g, t, c, h):
     if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
         return model.St[s, g, t, c, h] <= model.SCap[s] * model.scap_max[s] * model.NS[s, g, t]
     return Constraint.Skip

 model.SCapacity2Constraint = Constraint(model.s,model.g, model.TT, model.CC, model.HH, rule=s_capacity2_rule)



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
 def s_final_rule(model, s, g, t, c):
     if (s, g) in model.GS and t in model.TT and c in model.CC:
         return model.St[(s, g), t, c, '24'] == 0
     return Constraint.Skip

 model.SFinalConstraint = Constraint(model.s,model.g, model.TT, model.CC, rule=s_final_rule)



 #---------- RENEWABLES CONSTRAINTS --------------*
 # %%  RENEWABLES CONSTRAINTS ---------------------
 # Electricity production for electrolysis
 def elec_prod_rule(model, g, t, c, h):
         return model.Pr['WE', g, t, c, h] == model.eta['WE', t] * (
             sum(model.Pre[e, g, t, c, h] for e in model.e) - model.CL[g, t, c, h]
         )

 model.ElecProdConstraint = Constraint(model.g, model.TT, model.CC, model.HH, rule=elec_prod_rule)


 # Renewables availability
 def renew_av_rule(model, e, g, t, c, h):
     if t in model.TT and c in model.CC and h in model.HH:
         return model.Pre[e, g, t, c, h] ==  0.7*model.AVH[c, h, g, e] * model.NR[e, g, t]

 model.RenewAvConstraint = Constraint(model.e, model.g, model.TT, model.CC, model.HH, rule=renew_av_rule)



 def renew_cap_rule(model, e, g, t):
     if t in model.TT:
             return model.NR[e, g, t] == (model.NR[e, g, t - 1] if t >model.y1 else 0)+ model.InvR[e, g, t]
     return Constraint.Skip

 model.RenewCapConstraint = Constraint(model.e, model.g, model.TT, rule=renew_cap_rule)


 def land_availability_rule(model, e, g, t):
     if t in model.TT:
         return 0.001*model.NR[e, g, t] <= 0.001*model.landAV[e, g]
     return Constraint.Skip

 model.LandAvailabilityConstraint = Constraint(model.e, model.g, model.TT, rule=land_availability_rule)

 '''
 def curtailment_limit_rule(model, c, h):
     if c in model.CC and h in model.HH:
         return sum(model.CL[g, t, c, h] for g in model.g for t in model.TT) <= 0.1 * sum(model.Pre[e, g, t, c, h] for e in model.e for g in model.g for t in model.TT)
     return Constraint.Skip

 model.CurtailmentLimitConstraint = Constraint(model.CC, model.HH, rule=curtailment_limit_rule)
 '''


 # %%  Hydrogen and CO2 blance --------------------
 # HA1 Monolithic Version


 def flow_balance_rule(model, g, t, c, h):
     return (
         sum(model.Pr[p, g, t, c, h] for p in model.p) +
         sum(model.Q['Pipe', g1, g, t, c, h] for g1 in model.g if (g1, g) in model.Npipe) +
         (model.IMP[g, t, c, h] if g in model.Gimp else 0) +
         sum(model.Qr[s, g, t, c, h] for s in model.s if (g, s) in model.GS)
         ==
         sum(model.Q['Pipe', g, g1, t, c, h] for g1 in model.g if (g, g1) in model.Npipe) +
         sum(model.Qi[g, s, t, c, h] for s in model.s if (g, s) in model.GS) +
         model.demH[g, t, c, h]
     )

 model.FlowBalance = Constraint(model.g, model.TT, model.CC, model.HH, rule=flow_balance_rule)



 # Co2 Balanace
 def co2_mass_balance_rule(model, g, t, c, h):
     if t in model.TT and c in model.CC and h in model.HH:
         return (
             sum(model.Qon[g1, g, t, c, h] for g1 in model.g if (g1, g) in model.N) +
             sum(model.y_c[p, t] * model.Pr[p, g, t, c, h] for p in model.p)
          == 
             sum(model.Qon[g, g1, t, c, h] for g1 in model.g if (g, g1) in model.N) +
             sum(model.Qoff[g, r, t, c, h] for r in model.r if (g, r) in model.GR)
         )
     return Constraint.Skip

 model.CO2MassBalanceConstraint = Constraint(model.g, model.TT, model.CC, model.HH, rule=co2_mass_balance_rule)




 #---------- RESERVIORS Constraints --------------*
 # %%  RESERVIORS Constraints ---------------------
 # Inventory
 def res_inventory_rule(model, r, t):
     if t in model.TT: 
       return model.RI[r, t] == (model.RI[r, t - 1] if t>model.y1 else  model.ri0[r] / 1000)+ model.dur * sum(
         model.WF[c] * model.theta * model.Qoff[(g, r), t, c, h] for g in model.g if 
         (g, r) in model.GR  for c in model.CC for h in model.HH
          ) / 1000
    

 model.ResInventoryConstraint = Constraint(model.r, model.TT, rule=res_inventory_rule)

 
 # %%  Hydrogen Import Limit ----------------------
 # Import limit
 def imp_limit_rule(model, t, c, h):
     if t in model.TT and c in model.CC and h in model.HH:
         return sum(model.IMP[g, t, c, h] for g in model.Gimp) <= 0.1*sum(model.dem[g, t, c, h] for g in model.g)
     return Constraint.Skip
 model.ImpLimitConstraint = Constraint(model.TT, model.CC, model.HH, rule=imp_limit_rule)

 


 #---------- EMISSION --------------*
 # %%  Emission Target Limit ----------------------
 # Emissions target
 def emissions_rule(model, t):
     if t in model.TT:
         return model.em[t] == sum(
             model.WF[c] * model.y_e[p, t] * model.theta * model.Pr[p, g, t, c, h]
             for p in model.p
             for g in model.g
             for c in model.CC
             for h in model.HH
         )
     return Constraint.Skip
 model.EmissionConstraint = Constraint(model.TT, rule=emissions_rule)

 # Emissions target equation
 def em_target_rule(model, t):
    if t in model.TT:
         return 0.001*model.em[t] <= 0.001*model.emtarget[t]
    
 model.EmTargeteqConstraint = Constraint(model.TT, rule=em_target_rule)
 # %%  Tighting -----------------------------------
 # Tight Gas
 '''
 # TightGas Constraint
 def tight_gas_rule(model, t):
     if t in model.TT:
         return sum(
             model.InvP[p, g, t] for g in model.g for p in model.p if model.ord_p[p] <= 2
         ) <= 40
     return Constraint.Skip

 model.TightGasConstraint = Constraint(model.TT, rule=tight_gas_rule)


 # TightBio Constraint
 def tight_bio_rule(model, p, t):
     if model.ord_p[p] == 3 and t in model.TT:
         return sum(
             model.InvP[p, g, t] for g in model.g
         ) <= 30
     return Constraint.Skip

 model.TightBioConstraint = Constraint(model.p, model.TT, rule=tight_bio_rule)


 # TightInvWE Constraint
 def tight_inv_we_rule(model, p, t):
     if model.ord_p[p] == 4 and t in model.TT:
         return sum(
             model.InvP[p, g, t] for g in model.g
         ) <= 200
     return Constraint.Skip

 model.TightInvWEConstraint = Constraint(model.p, model.TT, rule=tight_inv_we_rule)


 # TightInvStorage Constraint
 def tight_inv_storage_rule(model, s, t):
     if model.ord_s[s] > 4 and t in model.TT:
         return sum(
             model.InvS[s, g, t] for g in model.g
         ) <= 250
     return Constraint.Skip

 model.TightInvStorageConstraint = Constraint(model.s, model.TT, rule=tight_inv_storage_rule)
 '''
 # %%  PIPELINE CONSTRAINTS------------------------
 #------Hydrogen Pipeline Limit ------

 #------Hydrogen Pipeline Limit ------

 # Maximum flowrate for pipelines

 def h2pipe_max_rule(model, g, g1, t, c, h):
     if (g, g1) in model.Npipe:
         return model.Q['Pipe', (g, g1), t, c, h] <= sum(model.qHmax[d1] * (
             (model.AY[d1, (g, g1), t] if model.ord_g[g] < model.ord_g[g1] else 0)+
             (model.AY[d1, (g1, g), t] if model.ord_g[g1] < model.ord_g[g] else 0) 
             )
             for d1 in model.d1)
     return Constraint.Skip

 model.H2PipeMax = Constraint(model.Npipe, model.TT, model.CC, model.HH, rule=h2pipe_max_rule)



 def onshorepipe_max_rule(model, g, g1, t, c, h):
     if (g, g1) in model.N:
         return 0.001*model.Qon[g, g1, t, c, h] <= 0.001*sum(model.qCmax[d2] * (
                 (model.AYon[d2, g, g1, t] if model.ord_g[g] < model.ord_g[g1] else 0) +
                 (model.AYon[d2, g1, g, t] if model.ord_g[g1] < model.ord_g[g] else 0)
             )
             for d2 in model.d2
         )
     return Constraint.Skip

 model.OnshorePipeMax = Constraint(model.N, model.TT, model.CC, model.HH, rule=onshorepipe_max_rule)




 def offshorepipe_max_rule(model, g, r, t, c, h):
     if (g, r) in model.GR:
         return 0.001*model.Qoff[(g, r), t, c, h]  <= 0.001*sum(model.qCmax[d2] * model.AYoff[d2, (g, r), t] for d2 in model.d2)
     return Constraint.Skip
 model.OffshorePipeMax = Constraint(model.GR, model.TT, model.CC, model.HH, rule=offshorepipe_max_rule)


 # Availability of pipelines
 def H2PAvailability_rule(model, d1, g, g1, t):
     if (g,g1) in model.Npipe and t in model.TT and model.ord_g[g] < model.ord_g[g1]:
         return model.AY[d1, g, g1, t] == (
             model.AY[d1, g, g1, t - 1] if t > model.y1 else 0
         ) + (model.ayHR0[d1, g, g1] if t == model.y1 else 0) + model.Yh[d1, g, g1, t]
     return Constraint.Skip

 model.H2PAvailability = Constraint(model.d1, model.Npipe, model.TT, rule=H2PAvailability_rule)


 def onp_availability_rule_simple(model, d2, g, g1, t):
        if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]:
             return model.AYon[d2, (g, g1), t] == (
                 model.AYon[d2, (g, g1), t - 1] if t>model.y1 else 0
                 )+ (model.ayC0[d2, (g, g1)] if t ==model.y1 else 0 ) + model.Yon[d2, (g, g1), t]
        return Constraint.Skip
 model.OnPAvailability = Constraint(model.d2, model.N, model.TT, rule=onp_availability_rule_simple)


 def offp_availability_rule(model, d2, g, r, t):
      if (g, r) in model.GR and t in model.TT: 
          return model.AYoff[d2, (g, r), t] == (
              model.AYoff[d2, (g, r), t-1] if t> model.y1 else 0
              )+ (model.aeC0[r] if t==model.y1 else 0) + model.Yoff[d2, (g, r), t]
      return Constraint.Skip

 model.OffPAvailability = Constraint(model.d2, model.GR, model.TT, rule=offp_availability_rule)

 def pipest_availability_rule(model, d1, g, sc, t):
       if (g, sc) in model.GS2 and t in model.TT: 
            return model.AYst[d1, (g, sc), t] == (
                model.AYst[d1, g, sc, t-1]  if t>model.y1 else 0)+ model.Yst[d1, (g, sc), t]
       return Constraint.Skip
 model.PipeStAvailability = Constraint(model.d1, model.GS2, model.TT, rule=pipest_availability_rule)


 # One diameter size
 def h2pipe_rule(model, g, g1, t):
      if (g,g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1] and t in model.TT:   
        return sum(model.AY[d1, (g, g1), t] for d1 in model.d1) <= 1
      return Constraint.Skip
 model.H2Pipe = Constraint(model.Npipe, model.TT, rule=h2pipe_rule)



 def onpipe_rule(model, g, g1, t):
     if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1] and t in model.TT:
         return sum(model.AYon[d2, g, g1, t] for d2 in model.d2) <= 1
     return Constraint.Skip

 model.OnPipeConstraint = Constraint(model.N, model.TT, rule=onpipe_rule)



 def offpipe_rule(model, g, r, t):
      if (g,r) in model.GR and t in model.TT:  
         return sum(model.AYoff[d2, (g, r), t] for d2 in model.d2) <= 1
         return Constraint.Skip
 model.OffPipe = Constraint(model.GR, model.TT, rule=offpipe_rule)

 def stpipe_rule(model, g, sc, t):
     if (g,sc) in model.GS2:
         return sum(model.AYst[d1, (g, sc), t] for d1 in model.d1) <= 1
     return Constraint.Skip
 model.StPipe = Constraint(model.GS2, model.TT, rule=stpipe_rule)


 


 # %%  Solving Step 1 and Fixing InvP and InvS Variables

 def get_solver():
     def submit():
         nonlocal selected_solver
         selected_solver = var.get()
         dialog.destroy() 
         root.quit() 

     root = tk.Tk()
     root.withdraw()  
     selected_solver = None

     dialog = tk.Toplevel(root)
     dialog.title("Select Solver")
     dialog.geometry("400x300")   
     dialog.configure(bg="#2c3e50")  
     center_window(dialog, 400, 300)  

     tk.Label(dialog, text="Choose a solver:", font=("Arial", 12, "bold"), fg="white", bg="#2c3e50").pack(pady=10)
     
     var = tk.StringVar(value="gurobi") 
     solvers = [("Gurobi", "gurobi"), ("CPLEX", "cplex"), ("GLPK", "glpk"), ("HIGHS", "highs")]

     for text, value in solvers:
         tk.Radiobutton(dialog, text=text, variable=var, value=value, font=("Arial", 11, "bold"), 
                        fg="black", bg="#ecf0f1", anchor="w").pack(fill="x", padx=20, pady=5)

     tk.Button(dialog, text="Confirm", font=("Arial", 11, "bold"), fg="white", bg="#2980b9", 
               width=15, height=2, command=submit).pack(pady=15)

     dialog.grab_set()  # جلوگیری از ادامه اجرا تا زمانی که این پنجره بسته شود
     root.mainloop()  
     return selected_solver

 def get_solver_settings():
  
     time_limit = 3600  
     mip_gap = 0.05 

     def submit_settings():
         nonlocal time_limit, mip_gap
         try:
             time_limit = int(time_limit_entry.get())
             mip_gap = float(mip_gap_entry.get())
         except ValueError:
             error_label.config(text="Invalid input! Enter numbers only.", fg="red")
             return

         settings_dialog.destroy()  

     settings_dialog = tk.Toplevel()
     settings_dialog.title("Solver Settings")
     settings_dialog.geometry("400x250")
     settings_dialog.configure(bg="#34495e")
     center_window(settings_dialog, 400, 250)

     tk.Label(settings_dialog, text="Enter Solver Settings", font=("Arial", 14, "bold"), fg="white", bg="#34495e").pack(pady=10)

     tk.Label(settings_dialog, text="Time Limit (seconds):", font=("Arial", 12), fg="white", bg="#34495e").pack()
     time_limit_entry = tk.Entry(settings_dialog, font=("Arial", 12))
     time_limit_entry.insert(0, str(time_limit)) 
     time_limit_entry.pack(pady=5)

     tk.Label(settings_dialog, text="MIP Gap (e.g. 0.05):", font=("Arial", 12), fg="white", bg="#34495e").pack()
     mip_gap_entry = tk.Entry(settings_dialog, font=("Arial", 12))
     mip_gap_entry.insert(0, str(mip_gap))  
     mip_gap_entry.pack(pady=5)

     error_label = tk.Label(settings_dialog, text="", font=("Arial", 10, "bold"), bg="#34495e")
     error_label.pack()

     tk.Button(settings_dialog, text="Apply", font=("Arial", 12, "bold"), fg="white", bg="#27ae60", 
               width=15, height=2, command=submit_settings).pack(pady=15)

     settings_dialog.grab_set()  
     settings_dialog.wait_window()  
     return time_limit, mip_gap

 def center_window(win, width=400, height=300):
     win.update_idletasks()
     screen_width = win.winfo_screenwidth()
     screen_height = win.winfo_screenheight()
     x = (screen_width - width) // 2
     y = (screen_height - height) // 2
     win.geometry(f"{width}x{height}+{x}+{y}")

 solver_name = get_solver()
 if solver_name:
     print(f"Selected solver: {solver_name}")
     time_limit, mip_gap = get_solver_settings()
 else:
     print("No solver selected. Exiting program.")
     exit()

 opt = SolverFactory(solver_name)
 opt.options['Threads'] = 36
 opt.options['Presolve'] = 2
 opt.options['MIPGap'] = mip_gap
 opt.options['TimeLimit'] = time_limit
 opt.options['Heuristics'] = 0.1 

 results = opt.solve(model, tee=True)
 
 
 
 
 from openpyxl import Workbook


 wb = Workbook()

 all_variables = []

 objective_value = model.TC()  
 all_variables.append({"Name": "Objective", "Index": "-", "Value": objective_value})

 for var in model.component_objects(Var, active=True):
     var_name = var.name
     for index in var:
         value = var[index]()
         all_variables.append({"Name": var_name, "Index": index, "Value": value})

 df = pd.DataFrame(all_variables)

 df.to_excel("resultsHA1_1.xlsx", index=False, sheet_name="All Data")

 print("All variables and objective saved in 'resultsHA1_1.xlsx'")
 
 fixed_values_InvP = {
 (p, g, t): round(model.InvP[p, g, t]() )
 for p in model.p for g in model.g for t in model.TT}

 fixed_values_InvS = {
 (s, g, t):  round(model.InvS[s, g, t]())
 for s in model.s for g in model.g for t in model.TT if (s,g) in model.GS}
 
 
 
 return fixed_values_InvP, fixed_values_InvS



# %%
def Second_step(fixed_values_InvP, fixed_values_InvS):
    
    model = ConcreteModel()
    # %% ---------------------------------Define Main and Additional Sets and Subsets ------------------------------
    l_data = Sets_data.iloc[1, 2:4].values
    g_data = Sets_data.iloc[2, 2:15].values 
    p_data = Sets_data.iloc[3, 2:6].values
    r_data = Sets_data.iloc[4, 2:6].values
    s_data = Sets_data.iloc[5, 2:8].values
    t_data = Sets_data.iloc[6, 2:8].values
    d_data = Sets_data.iloc[7, 2:5].values
    c_data = Sets_data.iloc[8, 2:8].values
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

    #model.g = Set(initialize=lambda model: {pair[0] for pair in model.N})
    #model.g1 = Set(initialize=lambda model: {pair[1] for pair in model.N})

    # Aliases
    model.gg = Set(dimen=2, initialize=lambda model: [(g,g1) for g in model.g for g1 in model.g])
    model.hh = Set(dimen=2, initialize=lambda model: [(h,h1) for h in model.h for h1 in model.h])

    # ------ RangeSets -----

    model.TT = RangeSet(3, 6)  #  TT(t) /3*6/
    model.CC = RangeSet(1,n_clusters+1)  #  CC(c) /1*6/
    model.HH = RangeSet(1, 24) #  HH(h) /1*24/
    # %% Assign spacific data for parameters-----------
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
        (int(c), int(h), g, e): df_Availability.iloc[i,  1+idx]  
        for i, pair in enumerate(df_Availability.iloc[:, 0])  
        for idx, (g, e) in enumerate([(g, e) for g in model.g for e in model.e])  
        for c, h in [map(int, pair.strip("()").split(","))]  
    }
    '''
    AV_data = {(c, h, g, e): df_Availability.iloc[i, 2 + 3 * g_idx + e_idx]
        for i, (c, h) in enumerate(zip(df_Availability.iloc[:, 0], df_Availability.iloc[:, 1]))  
        for g_idx, g in enumerate(model.g)  
        for e_idx, e in enumerate(model.e)}

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

    
    
    GasDem_data = {
            (int(c), int(h), g): df_GasDem.iloc[i, 1 + j] 
            for i, pair in enumerate(df_GasDem.iloc[:, 0])  
            for j, g in enumerate(model.g)  
            for c, h in [map(int, pair.strip("()").split(","))]  
        }
    


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
    diameter_order = {diameter: i + 1 for i, diameter in enumerate(model.d1)}          
    Trans_order = {transLine: i + 1 for i, transLine in enumerate(model.l)}  
    Production_order = {production: i+1 for i, production in enumerate(model.p)}
    Storage_order = {storage: i+1 for i, storage in enumerate(model.s)}
    Hour_order = {time: i+1 for i, time in enumerate (model.h)}

    model.ord_g = Param(model.g, initialize=region_order)
    #model.ord_d = Param(model.d, initialize=diameter_order)
    model.ord_l = Param(model.l, initialize=Trans_order)
    model.ord_p = Param(model.p, initialize=Production_order)
    model.ord_s= Param(model.s, initialize=Storage_order )
    model.ord_h = Param(model.h, initialize=Hour_order)
    # %%
    #======================================Parameters========================================================
    # %% Define Parameter------------------------------
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
    model.GasDem = Param(model.CC, model.h, model.g,  initialize=GasDem_data, doc='Hydrogen demand for each region g each cluster c and hour h (MWh)')
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
    model.WF = Param(model.CC, initialize=WF_data, doc='Weight of clusters')

    # ---- Scalar ----
    model.y1 = Param(initialize=3, doc="Scalar y1")
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
    '''
    model.dfo = Expression(
        model.t,
        rule=lambda model, t: round(
            1 / (1 + model.ir) ** (model.dur * t - 5) +
            1 / (1 + model.ir) ** (5 * t - 4) +
            1 / (1 + model.ir) ** (5 * t - 3) +
            1 / (1 + model.ir) ** (5 * t - 2) +
            1 / (1 + model.ir) ** (5 * t - 1),
            2
        )
    )
    '''
    def biomass_availability_init(model, g, t):
        return model.bp * model.br[g] * model.Vbio_max[t] * 1000000

    model.BA = Param(model.g, model.TT, initialize=biomass_availability_init,  doc="Biomass availability in region g and time period t")


    '''
    model.BA = Expression(model.g, model.t, rule=lambda model, g, t: model.bp * model.br[g] * model.Vbio_max[t] * 1000000,  doc='Biomass availability in region g and time period t')
    '''
    #model.dem = Expression(model.g, model.t, model.CC, model.h, rule=lambda model, g, t, c, h:model.dc[t]*model.GasDem[c,h,g])

    def dem_init(model, g, t, CC, h):
        return model.dc[t] * model.GasDem[CC, h, g] 
    model.dem = Param(model.g, model.TT, model.CC, model.h, initialize=dem_init)
    '''
    model.RI_up = Expression(model.r, model.TT, rule=lambda model, r,t :model.rcap[r]/1000 )
    '''
    '''
    model.Npipe = Set(dimen=2, initialize=[(g,g1) for g in model.g for g1 in model.g if model.DistPipe[g, g1] > 0 ])
    '''
    model.Npipe = Set(dimen=2,initialize=model.DistPipe.keys(), doc='Set of region pairs with nonzero pipeline distances')

    '''
    model.Npipe = Set(
        initialize=lambda model: [(g, g1) for g in model.g for g1 in model.g1 if model.DistPipe[g, g1] > 0],
        doc="Set of region pairs (g, g1) with a non-zero distance (DistPipe > 0)"
    )
    '''

    # Availability and initial availability parameters
    model.AV = Param(model.CC, model.h, model.g, model.e, initialize=AV_data, doc='Availability of renewable e in region g, cluster c and hour h (%)')
    model.ayHR0 = Param(model.d1, model.Npipe,initialize=0, doc='Initial availability of a regional hydrogen pipeline of diameter size d between regions g and g1 (0-1)')
    model.ayC0 = Param(model.d2, model.N, initialize=0, doc='Initial availability of an onshore CO2 pipeline of diameter size d between regions g and g1 (0-1)')
    model.aeC0 = Param(model.r, initialize=0, doc='Initial availability of an offshore CO2 pipeline between collection point in regions g and reservoir r (0-1)')

    '''
    InvP_data = {}
    for g in model.g:
        for t in model.TT:
            InvP_data[('SMRCCS', g, t)] = 10
            InvP_data[('ATRCCS', g, t)] = 10
            InvP_data[('BECCS', g, t)] = 10
            InvP_data[('WE', g, t)] = 50
    model.InvP_up = Param(model.p, model.g, model.TT, initialize=InvP_data)
    '''

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


    def Qup_bounds_rule(model, l, g, g1,t, c, h):
        if l in ['Pipe']:
            return (0,15343)
        return (0, None)

    
    
    
    
    #======================================Variables========================================================
# %% Define Variables------------------------------

    model.InvP = Var(model.p, model.g, model.TT, within=NonNegativeIntegers, bounds=InvP_bounds_rule,doc="Investment of new plants of type p producing in region g in time period t")
    model.InvS = Var(model.s, model.g, model.TT, within=NonNegativeIntegers, bounds=InvS_bounds_rule,doc="Investment of new storage facilities of type in region g in time period t")
    
    for (p, g, t), value in fixed_values_InvP.items():
            model.InvP[p, g, t].fix(value)

    for (s, g, t), value in fixed_values_InvS.items():
            model.InvS[s, g, t].fix(value)
    
    model.Yh = Var(model.d1, model.Npipe, model.TT, within=NonNegativeIntegers,  doc="Establishment of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
    model.Yon = Var(model.d2, model.N, model.TT, within=NonNegativeIntegers, doc="Establishment of onshore CO2 pipelines of diameter size d in region g in time period t")
    model.Yoff = Var(model.d2, model.GR, model.TT, within=NonNegativeIntegers, doc="Establishment of offshore CO2 pipelines of diameter size d in region g in time period t")
    model.Yst = Var(model.d1, model.GS2, model.TT, within=NonNegativeIntegers, doc="Establishment of hydrogen pipelines of diameter size d in region g in time period d to storage type s")
    # Positive variables
    model.NP = Var(model.p, model.g, model.TT, within=NonNegativeReals, doc="Number of plants of type j and size p in region g in time period t")
    model.NS = Var(model.s, model.g, model.TT, within=NonNegativeReals, bounds=NS_bounds_rule, doc="Number of storage facilities of type s and size p in region g in time period t")
    #model.NS_up = Var(model.s, model.g, model.TT, within=NonNegativeIntegers)
    #model.ITU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals, bounds=(0,25), doc="Number of new transportation units of type l for regional transportation byroad in region g to region g acquired in time period t")
    #model.NTU = Var(['Trailer'], model.Npipe, model.TT, within=NonNegativeReals,   doc="Number of transportation units of type l for regional transportation by road in region g in time period t")
    model.AY = Var(model.d1, model.Npipe, model.TT, within=NonNegativeReals,  doc="availability of hydrogen pipelines of diameter size d for regional distribution in region g in time period t")
    model.AYon=Var(model.d2, model.N, model.TT, within=NonNegativeReals,  doc="availability of onshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
    model.AYoff = Var(model.d2, model.GR, model.TT, within=NonNegativeReals,  doc="availability of offshore CO2 pipelines of diameter size d for local distribution in region g in time period t")
    model.AYst = Var(model.d1, model.GS2, model.TT, within=NonNegativeReals, doc="availability of hydrogen pipelines of diameter size d for distribution in region g in time period t")
    model.CL = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Curtailment (MW)')
    model.InvR = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000), doc='Invested capacity of renewable (MW)')
    #model.InvR_up = Var(model.e, model.g, model.TT, within=NonNegativeReals, bounds=(0, 10000))
    model.IMP = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals,
                    doc='Flow rate of international import (MW)')
    model.NR = Var(model.e, model.g, model.TT, within=NonNegativeReals,  doc='Capacity of renewable (MW)')
    model.Pr = Var(model.p, model.g, model.TT, model.CC,model.h,within=NonNegativeReals,      doc='Production rate (MW)')
    model.Pre = Var(model.e, model.g, model.TT, model.CC, model.h, within=NonNegativeReals,    doc='Electricity production from renewable (MW)')
    model.Q = Var(model.l, model.Npipe, model.TT, model.CC, model.h, within=NonNegativeReals, bounds=Qup_bounds_rule, doc='Regional flowrate of H2 (MWh)')
    model.Qi = Var(model.g,model.s, model.TT, model.CC,model.h, within=NonNegativeReals,  doc='H2 via pipeline to storage (MWh)')
    model.Qr = Var(model.s, model.g, model.TT, model.CC, model.h, within=NonNegativeReals,  doc= 'flowrate of H2 via pipeline from region g to storage type s in time period t(MWh)')
    model.Qon = Var(model.N, model.TT, model.CC, model.h, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via onshore pipelines (kg CO2/d)')
    model.Qoff = Var(model.GR, model.TT, model.CC, model.h, within=NonNegativeReals, bounds=(0,1.17E+04), doc='Flowrate of CO2 via offshore pipelines (kg CO2/d)')
    #odel.Rdown = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals,initialize=0, doc='Upward reserve contribution (MWh)')
    #odel.Rup = Var(model.p, model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Downward reserve contribution (MWh)')
    model.St = Var(model.s,model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Average inventory of product stored (kW)')
    model.Vbio = Var(model.TT, within=NonNegativeReals,  doc='Biomass consumption (kg)' )
    model.Vgas = Var(model.TT, within=NonNegativeReals, doc='Gas consumption (kg)')
    #model.slak1 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 1')
    #model.slak2 = Var(model.g, model.TT, model.CC, model.h, within=NonNegativeReals, doc='Slack variable 2')
    model.PCC = Var()
    model.SCC = Var()
    model.TCC=Var()
    model.POC = Var()
    model.SOC = Var()
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
    model.CEC = Var()
    model.IIC = Var()
    model.ReC = Var()
    model.GC = Var( )
    model.BC = Var( )
    model.ROC = Var()
    model.TOC=Var()
    model.em = Var(model.TT, within=Reals)




    # %%
    #======================================Objective Function========================================================*
    # %% Objective Function and related components----

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
        return 0.001*model.PipeCC == 0.001*(sum(
            # First summation: Hydrogen pipeline cost
            model.dfc[t] * model.cccH[d1] * model.DistPipe[g, g1] * model.Yh[d1, (g, g1), t]
            for d1 in model.d1
            for g in model.g
            for g1 in model.g
            if (g, g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1]
            for t in model.TT
        ) + sum(
            # Second summation: Onshore CO2 cost
            model.dfc[t] * model.cccC_onshore[d2] * model.Dist[g, g1] * model.Yon[d2, (g, g1), t]
            for d2 in model.d2
            for g in model.g
            for g1 in model.g
            if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]
            for t in model.TT
        ) + sum(
            # Third summation: Offshore CO2 cost
            model.dfc[t] * model.cccC_offshore[d2] * model.DistRes[g, r] * model.Yoff[d2, (g, r), t]
            for d2 in model.d2
            for g in model.g
            for r in model.r
            if (g, r) in model.GR
            for t in model.TT
        ) + sum(
            # Fourth summation: Storage cost
            model.dfc[t] * model.cccH[d1] * model.DistSt[g, sc] * model.Yst[d1, (g, sc), t]
            for d1 in model.d1
            for g in model.g
            for sc in model.sc
            if (g, sc) in model.GS2
            for t in model.TT
        ))
    model.PipeCCConstraint = Constraint(rule=pipecc_rule)

    # Constraint for TCC (Total Capital Cost)
    def tcc_rule(model):
        return model.TCC == 1000*model.PipeCC
    model.TCCConstraint = Constraint(rule=tcc_rule)


    # Constraint for POC
    def poc_rule(model):
        return 0.001*model.POC == 0.001*sum(
            model.dfo[t] * (
                model.pocostF[p, t] * model.PCap[p] * model.NP[p, g, t] +
                sum(
                    model.WF[c] * model.pocostV[p, t] * model.theta * model.Pr[p, g, t, c, h]
                    for c in model.CC for h in model.h
                )
            )
            for p in model.p for g in model.g for t in model.TT
        )
    model.POCConstraint = Constraint(rule=poc_rule)

    # Constraint for SOC
    def soc_rule(model):
        return 0.001*model.SOC == 0.001* sum(
            model.dfo[t] * (
                model.socostF[s] * model.SCap[s] * model.NS[s, g, t] +
                sum(
                    model.WF[c] * model.socostV[s] * model.theta * model.Qi[g, s, t, c, h]
                    for c in model.CC for h in model.h
                )
            )
            for s in model.s for g in model.g if (g, s) in model.GS for t in model.TT
        )
    model.SOCConstraint = Constraint(rule=soc_rule)
    
    # Constraint for PipeOC
    def pipeoc_rule(model):
        return 0.001*model.PipeOC == 0.001*(sum(
            model.dfo[t] * model.deltaH * model.crf * model.cccH[d1] * model.DistPipe[g, g1] * model.AY[d1, (g, g1), t]
            for d1 in model.d1 
            for g in model.g 
            for g1 in model.g 
            if (g, g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1]
            for t in model.TT
        ) + sum(
            model.dfo[t] * model.deltaC_onshore * model.crf * model.cccC_onshore[d2] * model.Dist[g, g1] * model.AYon[d2, (g, g1), t]
            for d2 in model.d2 
            for g in model.g 
            for g1 in model.g 
            if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]
            for t in model.TT
        ) + sum(
            model.dfo[t] * model.deltaC_offshore * model.crf * model.cccC_offshore[d2] * model.DistRes[g, r] * model.AYoff[d2, (g, r), t]
            for d2 in model.d2 
            for g in model.g 
            for r in model.r if (g, r) in model.GR 
            for t in model.TT
        ) + sum(
            model.dfo[t] * model.deltaH * model.crf * model.cccH[d1] * model.DistSt[g, sc] * model.AYst[d1, (g, sc), t]
            for d1 in model.d1 
            for g in model.g 
            for sc in model.sc if (g, sc) in model.GS2 
            for t in model.TT
        ))
    model.PipeOCConstraint = Constraint(rule=pipeoc_rule)
    
    # Constraint for TOC
    def toc_rule(model):
        return model.TOC ==  1000 * model.PipeOC
    model.TOCConstraint = Constraint(rule=toc_rule) 


    # Constraint for CEC
    def cec_rule(model):
        return model.CEC == sum(
            model.WF[c] * model.dfo[t] * model.ct[t] * model.y_e[p, t] * model.theta * model.Pr[p, g, t, c, h]
            for p in model.p for g in model.g for t in model.TT for c in model.CC for h in model.h
        )
    model.CECConstraint = Constraint(rule=cec_rule)

    # Constraint for IIC
    def iic_rule(model):
        return model.IIC == sum(
            model.WF[c] * model.dfo[t] * model.pimp * model.theta * model.IMP[g, t, c, h]
            for g in model.Gimp for t in model.TT for c in model.CC for h in model.h
        )
    model.IICConstraint = Constraint(rule=iic_rule)

    # Constraint for ReC
    def rec_rule(model):
        return 0.001*model.ReC == 0.001*sum(
            model.dfc[t] * model.rccost[e, t]* model.InvR[e, g, t] +
            model.dfo[t] * model.rocost[e, t] * model.NR[e, g, t]
            for t in model.TT for e in model.e for g in model.g
        )
    model.ReCConstraint = Constraint(rule=rec_rule)

    # Constraint for GC
    def gc_rule(model):
        return model.GC == sum(
            model.dfo[t] * model.cgas[t] * model.Vgas[t]
            for t in model.TT
        )
    model.GCConstraint = Constraint(rule=gc_rule)

    # Constraint for BC
    def bc_rule(model):
        return model.BC == sum(
            model.dfo[t] * model.cbio[t] * model.Vbio[t]
            for t in model.TT
        )
    model.BCConstraint = Constraint(rule=bc_rule)


    def objective_rule(model):
        return (
            1000*model.PCC+ 
            model.SCC+ 
            model.TCC+ 
            model.POC+ 
            model.SOC+ 
            model.TOC+ 
            model.CEC+ 
            model.IIC+ 
            model.ReC+
            model.GC+ 
            model.BC 
        )   
                      
    model.TC = Objective(rule=objective_rule, sense=minimize)



    # %%
    #======================================Problem Constraints========================================================*
    



    #---------- FUELS CONSUMPTION --------------*
    # %%  Fuel Constraint ----------------------------
    def gas_cons_rule(model, t):
        if t in model.TT:
            return model.Vgas[t] == sum(
                model.WF[c] * model.theta * model.Pr[p, g, t, c, h] / model.eta[p, t]
                for p in model.p if model.ord_p[p] <= 2 for g in model.g for c in model.CC for h in model.h
                
            )
        return Constraint.Skip

    model.GasConsConstraint = Constraint(model.TT, rule=gas_cons_rule)

    # Biomass consumption
    def bio_cons_rule(model, t):
        if t in model.TT:
            return model.Vbio[t] == sum(
                model.WF[c] * model.theta * model.Pr['BECCS', g, t, c, h] / model.eta['BECCS', t]
                for g in model.g for c in model.CC for h in model.h
            )
        return Constraint.Skip

    model.BioConsConstraint = Constraint(model.TT, rule=bio_cons_rule)



    # Biomass Availability 
   
    def biomass_availability_rule(model, g, t):
        if t in model.TT:  # Apply the constraint only for TT(t)
            return sum(
                0.001* model.WF[c] * model.theta * model.Pr['BECCS', g, t, c, h] / model.eta['BECCS', t]
                for c in model.CC for h in model.h
            ) <= 0.001* model.BA[g,t]
        return Constraint.Skip

    model.BiomassAvailabilityConstraint = Constraint(model.g, model.TT, rule=biomass_availability_rule)
    # %%  RAMP UP/DOWN -------------------------------

    # Ramp Up
    def ramp_up_rule(model, p, g, c, h, t):
        if t in model.TT and c in model.CC and h in model.h and h > 1:
            return model.Pr[p, g, t, c, h] - model.Pr[p, g, t, c, h - 1] <=model.theta * model.RU[p] * model.PCap[p] * model.NP[p, g, t]
        return Constraint.Skip

    model.RampUpConstraint = Constraint(model.p, model.g, model.CC, model.h, model.TT, rule=ramp_up_rule)


    # Ramp Down
    def ramp_down_rule(model, p, g, c, h, t):
        if t in model.TT and c in model.CC and h in model.h and h > 1:
            return model.Pr[p, g, t, c, h - 1] - model.Pr[p, g, t, c, h] <= model.theta * model.RD[p] * model.PCap[p] * model.NP[p, g, t]
        return Constraint.Skip

    model.RampDownConstraint = Constraint(model.p, model.g, model.CC, model.h, model.TT, rule=ramp_down_rule)
    # %%  Peoduction Limit ---------------------------
    # Production Limit
    
    def p_capacity2_rule(model, p, g, t, c, h):
        if t in model.TT and c in model.CC and h in model.h:
            return model.Pr[p, g, t, c, h] <= model.PCap[p] * model.pcap_max[p] * model.NP[p, g, t]
        return Constraint.Skip

    model.PCapacity2Constraint = Constraint(model.p, model.g, model.TT, model.CC, model.h, rule=p_capacity2_rule)

   
    def p_availability_rule(model, p, g, t):
         if t in model.TT:
          return model.NP[p, g, t] == (
                model.NP[p, g, t-1] if t>model.y1 else 0 
            )+( 
            model.np0[p, g] if t==model.y1 else 0
            )+ model.InvP[p, g, t] 
         return Constraint.Skip

    model.PAvailability = Constraint(model.p, model.g, model.TT, rule=p_availability_rule)
     
    #---------- STORAGE CONSTRAINTS --------------*
    # %%  Storage Limit ------------------------------
    # Storage 
   

    def sinventory2_rule(model, s, g, t, c, h):
        if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.h:
            return model.St[s, g, t, c, h] == (
                (model.St[s, g, t, c, h - 1] if h > 1 else model.st0[s, g]) 
                + model.theta * (model.Qi[g, s, t, c, h] - model.Qr[s, g, t, c, h])
            )
        return Constraint.Skip
    model.SInventory2 = Constraint(model.s, model.g, model.TT, model.CC, model.h, rule=sinventory2_rule)


    # Maximum injection rate
    def max_inj_rule(model, s,g,t, c, h):
        if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.h:
            return model.Qi[(g, s), t, c, h] <= model.QImax[s] * model.NS[s, g, t]
        return Constraint.Skip

    model.MaxInjConstraint = Constraint( model.GS, model.TT, model.CC, model.h, rule=max_inj_rule)


    # Maximum retrieval rate
    def max_retr_rule(model, s, g, t, c, h):
        if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.h:
            return model.Qr[s, g, t, c, h] <= model.QRmax[s] * model.NS[s, g, t]
        return Constraint.Skip
    model.MaxRetrConstraint = Constraint(model.s,model.g, model.TT, model.CC, model.h, rule=max_retr_rule)

    # Underground storage capacity
    def s_capacity_u_rule(model, sc, g, t, c, h):
        if (g,sc) in model.GS2 and t in model.TT and c in model.CC and h in model.h:
            return model.InvS[sc, g, t] <= sum(model.Yst[d1, g, sc, t] for d1 in model.d1)
        return Constraint.Skip

    model.SCapacityUConstraint = Constraint(model.GS2, model.TT, model.CC, model.h, rule=s_capacity_u_rule)

    
    # Storage capacity constraints
    def s_capacity1_rule(model, s, g, t, c, h):
        if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.HH:
            return model.St[s, g, t, c, h] >= model.SCap[s] * model.scap_min[s] * model.NS[s, g, t]
        return Constraint.Skip

    model.SCapacity1Constraint = Constraint(model.s,model.g, model.TT, model.CC, model.HH, rule=s_capacity1_rule)
    
    def s_capacity2_rule(model, s, g, t, c, h):
        if (g, s) in model.GS and t in model.TT and c in model.CC and h in model.h:
            return model.St[s, g, t, c, h] <= model.SCap[s] * model.scap_max[s] * model.NS[s, g, t]
        return Constraint.Skip

    model.SCapacity2Constraint = Constraint(model.s,model.g, model.TT, model.CC, model.h, rule=s_capacity2_rule)



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
    def s_final_rule(model, s, g, t, c):
        if (s, g) in model.GS and t in model.TT and c in model.CC:
            return model.St[(s, g), t, c, '24'] == 0
        return Constraint.Skip

    model.SFinalConstraint = Constraint(model.s,model.g, model.TT, model.CC, rule=s_final_rule)



    #---------- RENEWABLES CONSTRAINTS --------------*
    # %%  RENEWABLES CONSTRAINTS ---------------------
    # Electricity production for electrolysis
    def elec_prod_rule(model, g, t, c, h):
            return model.Pr['WE', g, t, c, h] == model.eta['WE', t] * (
                sum(model.Pre[e, g, t, c, h] for e in model.e) - model.CL[g, t, c, h]
            )

    model.ElecProdConstraint = Constraint(model.g, model.TT, model.CC, model.h, rule=elec_prod_rule)


    # Renewables availability
    def renew_av_rule(model, e, g, t, c, h):
        if t in model.TT and c in model.CC and h in model.h:
            return model.Pre[e, g, t, c, h] ==  0.7*model.AV[c, h, g, e] * model.NR[e, g, t]

    model.RenewAvConstraint = Constraint(model.e, model.g, model.TT, model.CC, model.h, rule=renew_av_rule)



    def renew_cap_rule(model, e, g, t):
        if t in model.TT:
                return model.NR[e, g, t] == (model.NR[e, g, t - 1] if t >model.y1 else 0)+ model.InvR[e, g, t]
        return Constraint.Skip

    model.RenewCapConstraint = Constraint(model.e, model.g, model.TT, rule=renew_cap_rule)


    def land_availability_rule(model, e, g, t):
        if t in model.TT:
            return 0.001*model.NR[e, g, t] <= 0.001*model.landAV[e, g]
        return Constraint.Skip

    model.LandAvailabilityConstraint = Constraint(model.e, model.g, model.TT, rule=land_availability_rule)

    '''
    def curtailment_limit_rule(model, c, h):
        if c in model.CC and h in model.h:
            return sum(model.CL[g, t, c, h] for g in model.g for t in model.TT) <= 0.1 * sum(model.Pre[e, g, t, c, h] for e in model.e for g in model.g for t in model.TT)
        return Constraint.Skip

    model.CurtailmentLimitConstraint = Constraint(model.CC, model.h, rule=curtailment_limit_rule)
   '''

    # %%  Hydrogen and CO2 blance --------------------
    # HA2 Monolithic Version


    def flow_balance_rule(model, g, t, c, h):
        return (
            sum(model.Pr[p, g, t, c, h] for p in model.p) +
            sum(model.Q['Pipe', g1, g, t, c, h] for g1 in model.g if (g1, g) in model.Npipe) +
            (model.IMP[g, t, c, h] if g in model.Gimp else 0) +
            sum(model.Qr[s, g, t, c, h] for s in model.s if (g, s) in model.GS)
            ==
            sum(model.Q['Pipe', g, g1, t, c, h] for g1 in model.g if (g, g1) in model.Npipe) +
            sum(model.Qi[g, s, t, c, h] for s in model.s if (g, s) in model.GS) +
            model.dem[g, t, c, h]
        )

    model.FlowBalance = Constraint(model.g, model.TT, model.CC, model.h, rule=flow_balance_rule)



    # Co2 Balanace
    def co2_mass_balance_rule(model, g, t, c, h):
        if t in model.TT and c in model.CC and h in model.h:
            return (
                sum(model.Qon[g1, g, t, c, h] for g1 in model.g if (g1, g) in model.N) +
                sum(model.y_c[p, t] * model.Pr[p, g, t, c, h] for p in model.p)
             == 
                sum(model.Qon[g, g1, t, c, h] for g1 in model.g if (g, g1) in model.N) +
                sum(model.Qoff[g, r, t, c, h] for r in model.r if (g, r) in model.GR)
            )
        return Constraint.Skip

    model.CO2MassBalanceConstraint = Constraint(model.g, model.TT, model.CC, model.h, rule=co2_mass_balance_rule)




    #---------- RESERVIORS Constraints --------------*
    # %%  RESERVIORS Constraints ---------------------
    # Inventory
    def res_inventory_rule(model, r, t):
        if t in model.TT: 
          return model.RI[r, t] == (model.RI[r, t - 1] if t>model.y1 else  model.ri0[r] / 1000)+ model.dur * sum(
            model.WF[c] * model.theta * model.Qoff[(g, r), t, c, h] for g in model.g if 
            (g, r) in model.GR  for c in model.CC for h in model.h
             ) / 1000
       

    model.ResInventoryConstraint = Constraint(model.r, model.TT, rule=res_inventory_rule)

    
    # %%  Hydrogen Import Limit ----------------------
    # Import limit
    def imp_limit_rule(model, t, c, h):
        if t in model.TT and c in model.CC and h in model.h:
            return sum(model.IMP[g, t, c, h] for g in model.Gimp) <= 0.1*sum(model.dem[g, t, c, h] for g in model.g)
        return Constraint.Skip
    model.ImpLimitConstraint = Constraint(model.TT, model.CC, model.h, rule=imp_limit_rule)



    #---------- EMISSION --------------*
    # %%  Emission Target Limit ----------------------
    # Emissions target
    def emissions_rule(model, t):
        if t in model.TT:
            return model.em[t] == sum(
                model.WF[c] * model.y_e[p, t] * model.theta * model.Pr[p, g, t, c, h]
                for p in model.p
                for g in model.g
                for c in model.CC
                for h in model.h
            )
        return Constraint.Skip
    model.EmissionConstraint = Constraint(model.TT, rule=emissions_rule)

    # Emissions target equation
    def em_target_rule(model, t):
       if t in model.TT:
            return 0.001*model.em[t] <= 0.001*model.emtarget[t]
       
    model.EmTargeteqConstraint = Constraint(model.TT, rule=em_target_rule)
    # %%  Tighting -----------------------------------
    # Tight Gas
    '''
    # TightGas Constraint
    def tight_gas_rule(model, t):
        if t in model.TT:
            return sum(
                model.InvP[p, g, t] for g in model.g for p in model.p if model.ord_p[p] <= 2
            ) <= 40
        return Constraint.Skip

    model.TightGasConstraint = Constraint(model.TT, rule=tight_gas_rule)


    # TightBio Constraint
    def tight_bio_rule(model, p, t):
        if model.ord_p[p] == 3 and t in model.TT:
            return sum(
                model.InvP[p, g, t] for g in model.g
            ) <= 30
        return Constraint.Skip

    model.TightBioConstraint = Constraint(model.p, model.TT, rule=tight_bio_rule)


    # TightInvWE Constraint
    def tight_inv_we_rule(model, p, t):
        if model.ord_p[p] == 4 and t in model.TT:
            return sum(
                model.InvP[p, g, t] for g in model.g
            ) <= 200
        return Constraint.Skip

    model.TightInvWEConstraint = Constraint(model.p, model.TT, rule=tight_inv_we_rule)


    # TightInvStorage Constraint
    def tight_inv_storage_rule(model, s, t):
        if model.ord_s[s] > 4 and t in model.TT:
            return sum(
                model.InvS[s, g, t] for g in model.g
            ) <= 5*50
        return Constraint.Skip

    model.TightInvStorageConstraint = Constraint(model.s, model.TT, rule=tight_inv_storage_rule)
    '''
    # %%  PIPELINE CONSTRAINTS------------------------
    #------Hydrogen Pipeline Limit ------

    # Maximum flowrate for pipelines

    def h2pipe_max_rule(model, g, g1, t, c, h):
        if (g, g1) in model.Npipe:
            return model.Q['Pipe', (g, g1), t, c, h] <= sum(model.qHmax[d1] * (
                (model.AY[d1, (g, g1), t] if model.ord_g[g] < model.ord_g[g1] else 0)+
                (model.AY[d1, (g1, g), t] if model.ord_g[g1] < model.ord_g[g] else 0) 
                )
                for d1 in model.d1)
        return Constraint.Skip

    model.H2PipeMax = Constraint(model.Npipe, model.TT, model.CC, model.h, rule=h2pipe_max_rule)



    def onshorepipe_max_rule(model, g, g1, t, c, h):
        if (g, g1) in model.N:
            return 0.001*model.Qon[g, g1, t, c, h] <= 0.001*sum(model.qCmax[d2] * (
                    (model.AYon[d2, g, g1, t] if model.ord_g[g] < model.ord_g[g1] else 0) +
                    (model.AYon[d2, g1, g, t] if model.ord_g[g1] < model.ord_g[g] else 0)
                )
                for d2 in model.d2
            )
        return Constraint.Skip

    model.OnshorePipeMax = Constraint(model.N, model.TT, model.CC, model.h, rule=onshorepipe_max_rule)


    def offshorepipe_max_rule(model, g, r, t, c, h):
        if (g, r) in model.GR:
            return 0.001*model.Qoff[(g, r), t, c, h]  <= 0.001*sum(model.qCmax[d2] * model.AYoff[d2, (g, r), t] for d2 in model.d2)
        return Constraint.Skip
    model.OffshorePipeMax = Constraint(model.GR, model.TT, model.CC, model.h, rule=offshorepipe_max_rule)


    # Availability of pipelines
    def H2PAvailability_rule(model, d1, g, g1, t):
        if (g,g1) in model.Npipe and t in model.TT and model.ord_g[g] < model.ord_g[g1]:
            return model.AY[d1, g, g1, t] == (
                model.AY[d1, g, g1, t - 1] if t > model.y1 else 0
            ) + (model.ayHR0[d1, g, g1] if t == model.y1 else 0) + model.Yh[d1, g, g1, t]
        return Constraint.Skip

    model.H2PAvailability = Constraint(model.d1, model.Npipe, model.TT, rule=H2PAvailability_rule)


    def onp_availability_rule_simple(model, d2, g, g1, t):
           if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1]:
                return model.AYon[d2, (g, g1), t] == (
                    model.AYon[d2, (g, g1), t - 1] if t>model.y1 else 0
                    )+ (model.ayC0[d2, (g, g1)] if t ==model.y1 else 0 ) + model.Yon[d2, (g, g1), t]
           return Constraint.Skip
    model.OnPAvailability = Constraint(model.d2, model.N, model.TT, rule=onp_availability_rule_simple)


    def offp_availability_rule(model, d2, g, r, t):
         if (g, r) in model.GR and t in model.TT: 
             return model.AYoff[d2, (g, r), t] == (
                 model.AYoff[d2, (g, r), t-1] if t> model.y1 else 0
                 )+ (model.aeC0[r] if t==model.y1 else 0) + model.Yoff[d2, (g, r), t]
         return Constraint.Skip

    model.OffPAvailability = Constraint(model.d2, model.GR, model.TT, rule=offp_availability_rule)

    def pipest_availability_rule(model, d1, g, sc, t):
          if (g, sc) in model.GS2 and t in model.TT: 
               return model.AYst[d1, (g, sc), t] == (
                   model.AYst[d1, g, sc, t-1]  if t>model.y1 else 0)+ model.Yst[d1, (g, sc), t]
          return Constraint.Skip
    model.PipeStAvailability = Constraint(model.d1, model.GS2, model.TT, rule=pipest_availability_rule)


    # One diameter size
    def h2pipe_rule(model, g, g1, t):
         if (g,g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1] and t in model.TT:   
           return sum(model.AY[d1, (g, g1), t] for d1 in model.d1) <= 1
         return Constraint.Skip
    model.H2Pipe = Constraint(model.Npipe, model.TT, rule=h2pipe_rule)



    def onpipe_rule(model, g, g1, t):
        if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1] and t in model.TT:
            return sum(model.AYon[d2, g, g1, t] for d2 in model.d2) <= 1
        return Constraint.Skip

    model.OnPipeConstraint = Constraint(model.N, model.TT, rule=onpipe_rule)



    def offpipe_rule(model, g, r, t):
         if (g,r) in model.GR and t in model.TT:  
            return sum(model.AYoff[d2, (g, r), t] for d2 in model.d2) <= 1
            return Constraint.Skip
    model.OffPipe = Constraint(model.GR, model.TT, rule=offpipe_rule)

    def stpipe_rule(model, g, sc, t):
        if (g,sc) in model.GS2:
            return sum(model.AYst[d1, (g, sc), t] for d1 in model.d1) <= 1
        return Constraint.Skip
    model.StPipe = Constraint(model.GS2, model.TT, rule=stpipe_rule)
    
    # %% # %%  Solving the model
    import tkinter as tk
    from pyomo.environ import SolverFactory, SolverManagerFactory
    import os


    def center_window(win, width=400, height=300):
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")


    def get_solver_mode():
        def submit():
            nonlocal selected_mode
            selected_mode = var.get()
            dialog.destroy()
            root.quit()

        root = tk.Tk()
        root.withdraw()

        selected_mode = None

        dialog = tk.Toplevel(root)
        dialog.title("Select Solver Mode")
        dialog.configure(bg="#2c3e50")
        center_window(dialog, 400, 250)

        tk.Label(
            dialog,
            text="Choose Solver Mode:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        var = tk.StringVar(value="local")

        modes = [
            ("Local Solver", "local"),
            ("NEOS Solver", "neos")
        ]

        for text, value in modes:
            tk.Radiobutton(
                dialog,
                text=text,
                variable=var,
                value=value,
                font=("Arial", 11, "bold"),
                fg="black",
                bg="#ecf0f1",
                anchor="w"
            ).pack(fill="x", padx=20, pady=5)

        tk.Button(
            dialog,
            text="Confirm",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#2980b9",
            width=15,
            height=2,
            command=submit
        ).pack(pady=15)

        dialog.grab_set()
        root.mainloop()

        return selected_mode


    def get_solver():
        def submit():
            nonlocal selected_solver
            selected_solver = var.get()
            dialog.destroy()
            root.quit()

        root = tk.Tk()
        root.withdraw()

        selected_solver = None

        dialog = tk.Toplevel(root)
        dialog.title("Select Local Solver")
        dialog.configure(bg="#2c3e50")
        center_window(dialog, 400, 300)

        tk.Label(
            dialog,
            text="Choose a solver:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        var = tk.StringVar(value="gurobi")

        solvers = [
            ("Gurobi", "gurobi"),
            ("CPLEX", "cplex"),
            ("GLPK", "glpk"),
            ("HiGHS", "highs")
        ]

        for text, value in solvers:
            tk.Radiobutton(
                dialog,
                text=text,
                variable=var,
                value=value,
                font=("Arial", 11, "bold"),
                fg="black",
                bg="#ecf0f1",
                anchor="w"
            ).pack(fill="x", padx=20, pady=5)

        tk.Button(
            dialog,
            text="Confirm",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#2980b9",
            width=15,
            height=2,
            command=submit
        ).pack(pady=15)

        dialog.grab_set()
        root.mainloop()

        return selected_solver


    def get_solver_settings():
        time_limit = 3600
        mip_gap = 0.05

        def submit_settings():
            nonlocal time_limit, mip_gap

            try:
                time_limit = int(time_limit_entry.get())
                mip_gap = float(mip_gap_entry.get())
            except ValueError:
                error_label.config(
                    text="Invalid input! Enter numbers only.",
                    fg="red"
                )
                return

            settings_dialog.destroy()

        settings_dialog = tk.Toplevel()
        settings_dialog.title("Solver Settings")
        settings_dialog.configure(bg="#34495e")
        center_window(settings_dialog, 400, 250)

        tk.Label(
            settings_dialog,
            text="Enter Solver Settings",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#34495e"
        ).pack(pady=10)

        tk.Label(
            settings_dialog,
            text="Time Limit (seconds):",
            font=("Arial", 12),
            fg="white",
            bg="#34495e"
        ).pack()

        time_limit_entry = tk.Entry(settings_dialog, font=("Arial", 12))
        time_limit_entry.insert(0, str(time_limit))
        time_limit_entry.pack(pady=5)

        tk.Label(
            settings_dialog,
            text="MIP Gap (e.g. 0.05):",
            font=("Arial", 12),
            fg="white",
            bg="#34495e"
        ).pack()

        mip_gap_entry = tk.Entry(settings_dialog, font=("Arial", 12))
        mip_gap_entry.insert(0, str(mip_gap))
        mip_gap_entry.pack(pady=5)

        error_label = tk.Label(
            settings_dialog,
            text="",
            font=("Arial", 10, "bold"),
            bg="#34495e"
        )
        error_label.pack()

        tk.Button(
            settings_dialog,
            text="Apply",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#27ae60",
            width=15,
            height=2,
            command=submit_settings
        ).pack(pady=15)

        settings_dialog.grab_set()
        settings_dialog.wait_window()

        return time_limit, mip_gap


    def get_neos_email():
        email = "m.hemmati@ucl.ac.uk"

        def submit_email():
            nonlocal email
            email = email_entry.get().strip()

            if not email:
                error_label.config(
                    text="Email cannot be empty.",
                    fg="red"
                )
                return

            dialog.destroy()

        dialog = tk.Toplevel()
        dialog.title("NEOS Settings")
        dialog.configure(bg="#34495e")
        center_window(dialog, 400, 220)

        tk.Label(
            dialog,
            text="Enter NEOS Email",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#34495e"
        ).pack(pady=10)

        email_entry = tk.Entry(dialog, font=("Arial", 12), width=35)
        email_entry.insert(0, email)
        email_entry.pack(pady=10)

        error_label = tk.Label(
            dialog,
            text="",
            font=("Arial", 10, "bold"),
            bg="#34495e"
        )
        error_label.pack()

        tk.Button(
            dialog,
            text="Confirm",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2980b9",
            width=15,
            height=2,
            command=submit_email
        ).pack(pady=15)

        dialog.grab_set()
        dialog.wait_window()

        return email


    # =========================
    # Main Flow
    # =========================

    solver_mode = get_solver_mode()

    if solver_mode == "local":
        solver_name = get_solver()

        if not solver_name:
            print("No local solver selected.")
            exit()

        print(f"Selected local solver: {solver_name}")

        time_limit, mip_gap = get_solver_settings()

        opt = SolverFactory(solver_name)
        opt.options["Threads"] = 36
        opt.options["Presolve"] = 2
        opt.options["MIPGap"] = mip_gap
        opt.options["TimeLimit"] = time_limit
        opt.options["Heuristics"] = 0.1

        results = opt.solve(model, tee=True)


    elif solver_mode == "neos":
        email = get_neos_email()

        print(f"Using NEOS email: {email}")

        os.environ["NEOS_EMAIL"] = email

        solver_manager = SolverManagerFactory("neos")

        results = solver_manager.solve(
            model,
            opt="cplex",
            tee=True,
            keepfiles=False,
            load_solutions=True,
            timelimit=3600
        )

    else:
        print("No solver mode selected.")
        exit()


    print("Solver finished successfully.")
   
    
    
    


    from openpyxl import Workbook
    


    wb = Workbook()

    all_variables = []

    objective_value = model.TC()  
    all_variables.append({"Name": "Objective", "Index": "-", "Value": objective_value})

    for var in model.component_objects(Var, active=True):
        var_name = var.name
        for index in var:
            value = var[index]()
            all_variables.append({"Name": var_name, "Index": index, "Value": value})

    df = pd.DataFrame(all_variables)

    df.to_excel("resultsHA1_2.xlsx", index=False, sheet_name="All Data")

    print("All variables and objective saved in 'resultsHA1_2.xlsx'")

# %% Solving two steps 
fixed_values_InvP, fixed_values_InvS = First_step()
Second_step(fixed_values_InvP, fixed_values_InvS)




#%%
import geopandas as gpd
import matplotlib
#matplotlib.use('Qt5Agg')  # Needed to manipulate figure windows

import matplotlib.pyplot as plt
from shapely.geometry import LineString
import numpy as np
import ctypes  # For screen size on Windows

# Screen dimensions
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
half_width = screen_width // 2

# Load shapefile
nuts1 = gpd.read_file("NUTS1_Jan_2018_SGCB_in_the_UK.shp")

# Map NUTS codes to LDZ
ldz_map = {
    'UKC': 'NO', 'UKD': 'NW', 'UKE': 'NE', 'UKF': 'EM', 'UKG': 'WM',
    'UKH': 'EA', 'UKI': 'NT', 'UKJ': 'SO & SE', 'UKK': 'SW',
    'UKL': 'WS & WN', 'UKM': 'SC',
}
nuts1['LDZ'] = nuts1['nuts118cd'].map(ldz_map)

# Get centroids
ldz_centroids = {
    ldz: row.geometry.centroid
    for ldz, row in nuts1.dropna(subset=['LDZ']).drop_duplicates('LDZ').set_index('LDZ').iterrows()
}

# Define connections
connections = {
    ('NO', 'SC'): ['Type 1'],
    ('NE', 'NW'): ['Type 1'],
    ('NT', 'SO & SE'): ['Type 1'],
    ('SW', 'SO & SE'): ['Type 1'],
    ('WM', 'EM'): ['Type 1'],
    ('EA', 'EM'): ['Type 1'],
    ('EA', 'SO & SE'): ['Type 1']
}

# Offset helper
def offset_line(p1, p2, offset=0.15):
    dx, dy = p2.x - p1.x, p2.y - p1.y
    length = np.hypot(dx, dy)
    if length == 0:
        return LineString([p1, p2])
    nx, ny = -dy / length, dx / length
    offset_vec = np.array([nx * offset, ny * offset])
    return LineString([p1.coords[0] + offset_vec, p2.coords[0] + offset_vec])

# ---------------- First Figure (Left Half)
fig1, ax1 = plt.subplots(figsize=(15, 15))
try:
    manager1 = plt.get_current_fig_manager()
    manager1.window.setGeometry(0, 0, half_width, screen_height)  # Left half
except Exception as e:
    print("Figure 1 move failed:", e)

nuts1.plot(column='LDZ', ax=ax1, cmap='Paired', edgecolor='gray')
for (ldz1, ldz2), types in connections.items():
    p1 = ldz_centroids.get(ldz1)
    p2 = ldz_centroids.get(ldz2)
    if not p1 or not p2:
        continue
    for i, t in enumerate(types):
        offset = (i - (len(types) - 1) / 2) * 0.2
        line = offset_line(p1, p2, offset)
        ax1.plot(*line.xy, linestyle='-', linewidth=1.5, color='black')

for ldz, pt in ldz_centroids.items():
    ax1.text(pt.x, pt.y, ldz, fontsize=12, ha='center', va='center', weight='bold')
ax1.set_title("H2 Pipelines between regions", fontsize=20, color='darkblue')
ax1.axis('off')

# ---------------- Second Figure (Right Half)


# Show both
plt.show()

#%%
import geopandas as gpd
import matplotlib
#matplotlib.use('Qt5Agg')  # For figure window manipulation
import matplotlib.pyplot as plt
import ctypes  # For screen size on Windows

# Screen dimensions
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Load shapefile
nuts1 = gpd.read_file("NUTS1_Jan_2018_SGCB_in_the_UK.shp")

# Map NUTS codes to LDZ
ldz_map = {
    'UKC': 'NO', 'UKD': 'NW', 'UKE': 'NE', 'UKF': 'EM', 'UKG': 'WM',
    'UKH': 'EA', 'UKI': 'NT', 'UKJ': 'SO & SE', 'UKK': 'SW',
    'UKL': 'WS & WN', 'UKM': 'SC',
}
nuts1['LDZ'] = nuts1['nuts118cd'].map(ldz_map)

# Example capacity data (MW) – replace with your real numbers
capacity_data = {
    'NO': 1200,
    'NW': 1800,
    'NE': 900,
    'EM': 1500,
    'WM': 1100,
    'EA': 1300,
    'NT': 2000,
    'SO & SE': 2500,
    'SW': 1000,
    'WS & WN': 800,
    'SC': 1700,
}

# Add capacity to GeoDataFrame
nuts1['Capacity_MW'] = nuts1['LDZ'].map(capacity_data)

# Get centroids for label placement
ldz_centroids = {
    ldz: row.geometry.centroid
    for ldz, row in nuts1.dropna(subset=['LDZ']).drop_duplicates('LDZ').set_index('LDZ').iterrows()
}

# Create figure
fig, ax = plt.subplots(figsize=(12, 12))
try:
    manager = plt.get_current_fig_manager()
    manager.window.setGeometry(0, 0, screen_width, screen_height)  # Full screen
except Exception as e:
    print("Window resize failed:", e)

# Plot regions colored by installed capacity with green colormap
nuts1.plot(column='Capacity_MW', ax=ax, cmap='Greens', edgecolor='gray', legend=True)

# Add labels with capacity values
for ldz, pt in ldz_centroids.items():
    cap = capacity_data.get(ldz, None)
    if cap is not None:
        ax.text(pt.x, pt.y, f"{cap} MW", fontsize=10, ha='center', va='center', weight='bold', color='darkgreen')

# Title and clean up
ax.set_title("BECCS Installed Capacity per Region (MW)", fontsize=20, color='darkgreen')
ax.axis('off')

plt.show()

#%%
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import json
import webbrowser
from threading import Timer

# ---------- بارگذاری GeoJSON ----------
with open("NUTS1_Jan_2018_SGCB_in_the_UK_2022_7531557960096889953.geojson") as f:
    geojson = json.load(f)


region_key = "nuts118nm"

regions = [feat["properties"][region_key] for feat in geojson["features"]]

region_values = np.random.rand(len(regions)) * 100

kpi_values = {
    "Total Demand (GW)": 1000,
    "Peak Region": regions[int(np.argmax(region_values))],
    "Peak Value": round(region_values.max(), 1),
    "Emission": 250
}

# ---------- ساخت اپ ----------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("UK Energy Dashboard", style={"color": "white"}))
    ], style={"marginBottom": 10, "textAlign": "center"}),

    # KPI ها
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Demand", className="card-title"),
                html.H3(f"{kpi_values['Total Demand (GW)']} GW")
            ])
        ], color="primary", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Peak Region", className="card-title"),
                html.H3(kpi_values["Peak Region"])
            ])
        ], color="info", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Peak Value", className="card-title"),
                html.H3(f"{kpi_values['Peak Value']} GW")
            ])
        ], color="danger", inverse=True), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Emission", className="card-title"),
                html.H3(f"{kpi_values['Emission']} tCO2")
            ])
        ], color="danger", inverse=True), width=4),
        
    ], style={"marginBottom": 10}),
    

    # نقشه UK
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=go.Figure(
                    go.Choroplethmap(
                        geojson=geojson,
                        featureidkey=f"properties.{region_key}",
                        locations=regions,
                        z=region_values,
                        colorscale="Viridis",
                        marker_line_width=0.5,
                        marker_line_color="white"
                    )
                ).update_layout(
                    template="plotly_dark",
                    geo=dict(
                        fitbounds="locations",  # فقط UK
                        visible=False
                    ),
                    margin=dict(l=20, r=20, t=20, b=20),
                )
            )
        ], width=12)
    ])
], fluid=True)


if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    Timer(1, lambda: webbrowser.open(url)).start()
    app.run(debug=True)




#%%
import geopandas as gpd
import matplotlib
matplotlib.use('Qt5Agg')  # Needed to manipulate figure windows

import matplotlib.pyplot as plt
from shapely.geometry import LineString
import numpy as np
import ctypes  # For screen size on Windows

# Screen dimensions
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
half_width = screen_width // 2

# Load shapefile
nuts2 = gpd.read_file("NUTS1_Jan_2018_SGCB_in_the_UK.shp")

# Map NUTS codes to LDZ
ldz_map = {
    'UKC': 'NO', 'UKD': 'NW', 'UKE': 'NE', 'UKF': 'EM', 'UKG': 'WM',
    'UKH': 'EA', 'UKI': 'NT', 'UKJ': 'SO & SE', 'UKK': 'SW',
    'UKL': 'WS & WN', 'UKM': 'SC',
}
nuts2['LDZ'] = nuts2['nuts118cd'].map(ldz_map)

# Get centroids
ldz_centroids = {
    ldz: row.geometry.centroid
    for ldz, row in nuts2.dropna(subset=['LDZ']).drop_duplicates('LDZ').set_index('LDZ').iterrows()
}

# Define connections
connections = {
    ('NO', 'NW'): ['Type 1'],
    ('NW', 'EM'): ['Type 1'],
    ('NW', 'WS & WN'): ['Type 1'],
    ('WS & WN', 'WM'): ['Type 1'],
    ('WM', 'EM'): ['Type 1'],
    ('EA', 'EM'): ['Type 1'],
    ('WM', 'SO & SE'): ['Type 1'],
    ('NT', 'SO & SE'): ['Type 1'],
    ('SW', 'SO & SE'): ['Type 1']
}

# Offset helper
def offset_line(p1, p2, offset=0.15):
    dx, dy = p2.x - p1.x, p2.y - p1.y
    length = np.hypot(dx, dy)
    if length == 0:
        return LineString([p1, p2])
    nx, ny = -dy / length, dx / length
    offset_vec = np.array([nx * offset, ny * offset])
    return LineString([p1.coords[0] + offset_vec, p2.coords[0] + offset_vec])

# ---------------- First Figure (Left Half)
fig1, ax1 = plt.subplots(figsize=(10, 10))
try:
    manager2 = plt.get_current_fig_manager()
    manager2.window.setGeometry(half_width, 0, half_width, screen_height)  # Left half
except Exception as e:
    print("Figure 1 move failed:", e)

nuts2.plot(column='LDZ', ax=ax1, cmap='Paired', edgecolor='gray')
for (ldz1, ldz2), types in connections.items():
    p1 = ldz_centroids.get(ldz1)
    p2 = ldz_centroids.get(ldz2)
    if not p1 or not p2:
        continue
    for i, t in enumerate(types):
        offset = (i - (len(types) - 1) / 2) * 0.2
        line = offset_line(p1, p2, offset)
        ax1.plot(*line.xy, linestyle='-', linewidth=2, color='black')

for ldz, pt in ldz_centroids.items():
    ax1.text(pt.x, pt.y, ldz, fontsize=12, ha='center', va='center', weight='bold')
ax1.set_title("Onshore CO2 Pipelines ", fontsize=20, color='darkblue')
ax1.axis('off')

# ---------------- Second Figure (Right Half)


# Show both
plt.show()


#%%

import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
pio.renderers.default = 'browser'

# منابع و کشورهای پایه
source_labels = ["Gas Boiler", "Hydrogen Boiler", "ASHP"]
country_labels_raw = [
    "EA", "EM", "NE", "NO", "NT", "NW",
    "SC", "SE", "SO", "SW", "WM","WN", "WS",
    
]  # 13 کشور

# لینک‌ها
sources = (
    [0]*13 +  # Solar to each country
    [1]*13 +  # Wind to each country
    [2]*13    # Battery+EV to each country
)

targets = list(range(3, 16)) * 3  # کشورهای مقصد: indexهای 3 تا 15 = 13 کشور

values = [
    0, 7111, 4289, 6712, 0, 2342, 0, 2260, 5290, 2570, 0, 0, 0,   # Solar
    4906, 22249, 12560, 8445, 0, 0, 9249, 0, 0, 2299, 3933, 469, 7842,   # Wind
    20833, 11314, 2245, 0, 47322, 32915, 25462, 31878, 16761, 14137, 23135, 2798, 8341    # Battery+EV
]  # جمعاً 39 مقدار

# محاسبه مجموع انرژی برای هر کشور
country_totals = np.zeros(13)
for i in range(39):
    idx = targets[i] - 3  # چون کشورها از index 3 شروع میشن
    country_totals[idx] += values[i]

# افزودن مقدار عددی به لیبل کشورها
country_labels = [
    f"{name} " for name, total in zip(country_labels_raw, country_totals)
]

# ترکیب نهایی برچسب‌ها
labels = source_labels + country_labels  # مجموع = 3 + 13 = 16 برچسب (index 0 تا 15)

# رنگ نودها
node_colors = [
    "rgba(255, 223, 0, 1.0)",     # Solar
    "rgba(0, 150, 0, 1.0)",       # Wind
    "rgba(255, 105, 180, 1.0)",   # Battery+EV
] + ["rgba(160, 160, 160, 1.0)"] * 13  # رنگ کشورهای خاکستری

# رنگ لینک‌ها
link_colors = (
    ["rgba(255, 223, 0, 0.4)"] * 13 +    # Solar flows
    ["rgba(0, 150, 0, 0.4)"] * 13 +      # Wind flows
    ["rgba(255, 105, 180, 0.4)"] * 13    # Battery+EV flows
)

# ساخت شکل Sankey
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors
    )
)])

fig.update_layout(
    title_text="Energy Flow from Renewable Sources to 13 regions",
    font_size=13,
    margin=dict(l=10, r=10, t=40, b=10)
)

fig.show()






