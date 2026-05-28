#%%
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

Sets_data = excel_data.parse('Sets')
TechData_data = excel_data.parse('TechData')
HeatTech_data = excel_data.parse('HeatTech')
CostTech_data = excel_data.parse('CostTech')
General_data = excel_data.parse('General')
Regions_data = excel_data.parse('Regions')
Trans_data = excel_data.parse('Trans_Inter')
year_data = excel_data.parse('Calculations')

Distances_data = excel_data.parse('Distances')
General_data = excel_data.parse('General')
Emissions_data = excel_data.parse('Emissions')
Cluster_data = excel_data.parse('ClusteredDataSTOR')
Biomass_data = excel_data.parse('Biomass')
Reservoir_data = excel_data.parse('CO2Reservoirs')
#Reservoir_data = excel_data.parse('Emissions')
Pipelines_data= excel_data.parse('Pipelines')

df_eta=excel_data.parse('TechData', header=None, usecols="A:G", skiprows=101, nrows=24)
df_BR=excel_data.parse('TechData', header=None, usecols="A:G", skiprows=153, nrows=29)
df_cc_Heat=excel_data.parse('HeatTech', header=None, usecols="A:G", skiprows=2, nrows=5)
df_eta_Heat=excel_data.parse('HeatTech', header=None, usecols="A:G", skiprows=11, nrows=5)
df_cc_fix=excel_data.parse('CostTech', header=None, usecols="A:G", skiprows=2, nrows=24)
df_oc_fix=excel_data.parse('CostTech', header=None, usecols="L:R", skiprows=2, nrows=24)
df_LandAvailability=excel_data.parse('LandAvailability', header=None, usecols="A:N", skiprows=2, nrows=3)
df_NUint=excel_data.parse('InitCap', header=None, usecols="A:N", skiprows=2, nrows=4)
df_Capinit=excel_data.parse('InitCap', header=None, usecols="A:N", skiprows=10, nrows=7)
df_NUf=excel_data.parse('InitCap', header=None, usecols="A:O", skiprows=21, nrows=2)
df_Capf=excel_data.parse('InitCap', header=None, usecols="A:O", skiprows=27, nrows=2)
df_ICap=excel_data.parse('Trans_Inter', header=None, usecols="A:H", skiprows=6, nrows=12)
df_pim_y=excel_data.parse('Trans_Inter', header=None, usecols="A:G", skiprows=57, nrows=6)
df_fuel=excel_data.parse('Fuels', header=None, usecols="A:G", skiprows=3, nrows=5)
df_DistRes = excel_data.parse('Distances', header=None, usecols="B:D", skiprows=23, nrows=3)
df_DistSt = excel_data.parse('Distances', header=None, usecols="B:D", skiprows=31, nrows=4)
df_Dist = excel_data.parse('Distances', header=None, usecols="B:N", skiprows=4, nrows=13)
df_DistPipe = excel_data.parse('Distances', header=None, usecols="R:AD", skiprows=4, nrows=13)
df_ExT = excel_data.parse('Trans_Inter', header=None, usecols="B:N", skiprows=80, nrows=13)

import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import threading
import pandas as pd


# Global variables
global df_ipe, df_ElecDem, df_AV, df_Ind, df_Com, df_Dom, df_temp, df_WF, n_clusters

df_ipe = None
df_ElecDem = None
df_AV = None
df_Ind= None
df_Com= None
df_Dom= None
df_temp= None
df_WF= None
n_clusters = None  


def run_kmediods(n_clusters_input):
    print("Running FullCluster.py with clusters:", n_clusters_input)
    result = subprocess.run(
        ['python', 'FullCluster.py'],
        input=n_clusters_input,  
        capture_output=True,
        text=True
    )
    if result.stderr:
        print(f"Error: {result.stderr}")
    else:
        print(f"Output: {result.stdout}")


def select_process(root):
    global df_ipe, df_ElecDem, df_AV, df_Ind, df_Com, df_Dom, df_temp,df_WF, n_clusters

    n_clusters = simpledialog.askinteger("Input", 
                                         "Enter number of representative days:"
                                        )

    if n_clusters is None:
        n_clusters = 5  

    n_clusters_input = str(n_clusters) + '\n'
    
    root.after(0, root.quit)

    thread = threading.Thread(target=run_kmediods, args=(n_clusters_input,), daemon=False)
    thread.start()
    thread.join()
    

    process_data(n_clusters)
    root.withdraw()


def process_data(n_clusters):
    global df_ipe, df_ElecDem, df_AV, df_Ind, df_Com, df_Dom, df_temp,df_WF
    #file_path3 = r'C:\Users\Mohammed\Final_cluster.xlsx'
    file_path3 = os.path.join(os.getcwd(), 'FullClusterStor.xlsx')
    file_name = f"Cluster for 2017Cluster_{n_clusters}.xlsx"
    file_path4 = os.path.join(os.getcwd(), file_name)
    excel_data = pd.ExcelFile(file_path3, engine='openpyxl')
    excel_data4 = pd.ExcelFile(file_path4, engine='openpyxl')
    
    df_ipe=excel_data.parse('Sheet1', header=None, usecols="A:H", skiprows=1, nrows=24*(n_clusters+1))
    df_ElecDem=excel_data.parse('Sheet1', header=None, usecols="I:K", skiprows=1,nrows=24*(n_clusters+1))
    df_Ind=excel_data.parse('Sheet1', header=None, usecols="AP:BD", skiprows=1, nrows=24*(n_clusters+1))
    df_Com=excel_data.parse('Sheet1', header=None, usecols="AA:AO", skiprows=1, nrows=24*(n_clusters+1))
    df_Dom=excel_data.parse('Sheet1', header=None, usecols="L:Z", skiprows=1, nrows=24*(n_clusters+1))
    df_AV=excel_data.parse('Sheet1', header=None, usecols="BE:CS", skiprows=1, nrows=24*(n_clusters+1))
    df_temp=excel_data.parse('Sheet1', header=None, usecols="CT:DH", skiprows=1, nrows=24*(n_clusters+1))
    df_WF = excel_data4.parse('NDaysCluster', usecols="C",  nrows=n_clusters+1,header=0)
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
#%%

from pyomo.environ import *
from pyomo.environ import SolverFactory
#from pyomo.opt import SolverFactory
model = ConcreteModel()

# ---------------------------------Define Main and Additional Sets and Subsets ------------------------------
#%%SETs
b_data = Sets_data.iloc[0, 2:7].values
c_data = Sets_data.iloc[1, 2:8].values 
d_data = Sets_data.iloc[2, 2:5].values
f_data = Sets_data.iloc[3, 2:8].values
g_data = Sets_data.iloc[4, 2:15].values
h_data = Sets_data.iloc[5, 2:26].values
i_data = Sets_data.iloc[6, 2:14].values
j_data = Sets_data.iloc[7, 2:31].values
k_data = Sets_data.iloc[8, 2:8].values
r_data = Sets_data.iloc[9, 2:6].values
t_data = Sets_data.iloc[10, 2:8].values
jb_data = Sets_data.iloc[11, 2:5].values
jccs_data = Sets_data.iloc[12, 2:7].values
je_data = Sets_data.iloc[13, 2:16].values
jep_data = Sets_data.iloc[14, 2:14].values
jes_data = Sets_data.iloc[15, 2:4].values
jh_data = Sets_data.iloc[16, 2:12].values
jhe_data = Sets_data.iloc[17, 2:7].values
jhp_data = Sets_data.iloc[18, 2:6].values
jhs_data = Sets_data.iloc[19, 2:8].values
jre_data = Sets_data.iloc[20, 2:6].values
jth_data = Sets_data.iloc[21, 2:10].values
jlf_data = Sets_data.iloc[22, 2:3].values


model.b = Set(initialize=b_data)
cluster_labels = [f"c{i}" for i in range(1, n_clusters+2)]
model.c = Set(initialize=cluster_labels)
model.d = Set(initialize=d_data)
model.d2 = Set(initialize=['d1', 'd2'])
model.f = Set(initialize=f_data)
model.g = Set(initialize=g_data)
model.h = Set(initialize=h_data)
model.i = Set(initialize=i_data)
model.j = Set(initialize=j_data)
model.k = Set(initialize=k_data)
model.r = Set(initialize=r_data)
model.t = Set(initialize=[1,2,3,4,5,6])
model.TT = Set(initialize=[2,3, 4,5, 6], within=model.t)
model.jb = Set(initialize=jb_data)
model.jccs = Set(initialize=jccs_data)
model.je = Set(initialize=je_data)
model.jep = Set(initialize=jep_data)
model.jes = Set(initialize=jes_data)
model.jh = Set(initialize=jh_data)
model.jhe = Set(initialize=jhe_data)
model.jhp = Set(initialize=jhp_data)
model.jhs = Set(initialize=jhs_data)
model.jre = Set(initialize=jre_data)
model.jth = Set(initialize=jth_data)
model.jlf = Set(initialize=jlf_data)
model.JJHE = Set(initialize=['GasBoiler', 'HyBoiler', 'ASHP'], within=model.jhe)

model.per = Set(initialize=[f"p{i}" for i in range(1, 9)], doc="periods in a year")

# Define CP as a 2-dimensional set of (c, per) tuples
model.CP = Set(dimen=2, initialize=[('c3','p1'), 
                                    ('c1','p2'), 
                                    ('c3','p3'), 
                                    ('c2','p4'), 
                                    ('c3','p5'), 
                                    ('c4','p6'), 
                                    ('c5','p7'), 
                                    ('c6','p8')])




# jf(f,j) set
model.jf = Set(dimen=2, initialize=[
    ('Gas', 'CCGTCCS'), ('Gas', 'OCGT'), ('Gas', 'SMRCCS'), ('Gas', 'ATRCCS'), ('Gas', 'CCGT'),
    ('Uranium', 'Nuclear'),
    ('Bio', 'BECCS'), ('Bio', 'BGCCS'), ('Bio', 'Biomass'),
    ('GH2', 'FC'), ('GH2', 'H2CCGT'),
    ('Elec', 'WE')
])

# ig(g,i) set
model.ig = Set(dimen=2, initialize=[
    ('SC', 'MOYLE'), ('SC', 'NorthConnect'),
    ('NO', 'NSN'),
    ('EM', 'VIKINGLINK'),
    ('WS', 'Greenlink'),
    ('SW', 'Fablink'),
    ('SO', 'IFA2'),
    ('SE', 'Ifa'), ('SE', 'Britned'), ('SE', 'NEMO'), ('SE', 'ELECLink'),
    ('WN', 'EWIC')
])

# ik(k,i) set
model.ik = Set(dimen=2, initialize=[
    ('FR', 'IFA'), ('FR', 'IFA2'), ('FR', 'ELECLINK'), ('FR', 'FABLINK'),
    ('NL', 'BRITNED'),
    ('IR', 'MOYLE'), ('IR', 'EWIC'), ('IR', 'GREENLINK'),
    ('NO', 'NSN'), ('NO', 'NORTHCONNECT'),
    ('DK', 'VIKINGLINK'),
    ('BG', 'NEMO')
])

# jhef(jhe,f) set
model.jhef = Set(dimen=2, initialize=[
    ('GasBoiler', 'Gas'),
    ('HyBoiler', 'GH2'),
    ('ASHP', 'Elec'),
    ('HyGasBoiler', 'GH2'), ('HyGasBoiler', 'Gas'),
    ('HyASHP', 'Elec'), ('HyASHP', 'GH2')
])

# df(d,f) set
model.df = Set(dimen=2, initialize=[
    ('d3', 'GH2'), 
    ('d2', 'CO2')
])



region1_data = Regions_data.iloc[2:48, 2].values
region2_data = Regions_data.iloc[2:48, 3].values
Neighbourhood_Regions = list(zip(region1_data,region2_data))

region3_data = Regions_data.iloc[2:34, 8].values
region4_data = Regions_data.iloc[2:34, 9].values
Neighbourhood_Regionswithpipline = list(zip(region3_data,region4_data))

fuel_data = Regions_data.iloc[2:14, 20].values
interconnection_data = Regions_data.iloc[2:14, 21].values
region5_data = Regions_data.iloc[2:14, 22].values
Interconnection_Regions = list(zip(fuel_data,interconnection_data,region5_data))
fuel2_data = Regions_data.iloc[18:23, 20].values
region6_data = Regions_data.iloc[18:23, 21].values
Interconnection_Regions2 = list(zip(fuel2_data,region6_data))

region7_data = Regions_data.iloc[2:84, 16].values
region8_data = Regions_data.iloc[2:84, 17].values
GJh_data=list(zip(region7_data,region8_data))

region9_data = Trans_data.iloc[2:179, 14].values
region10_data = Trans_data.iloc[2:179, 15].values
TransDistance_data=list(zip(region9_data,region10_data))

ldd_data = Trans_data.iloc[2:179, 16]
Distance_dict = dict(zip(TransDistance_data, ldd_data))

GR_data=[(g_data[0], r_data[2]), (g_data[5], r_data[3]), (g_data[6], r_data[0])]
model.GR = Set(dimen=2, initialize=[(g,r) for g in model.g for r in model.r if (g,r) in GR_data])


model.N = Set(dimen=2, initialize=[(g,g1) for g in model.g for g1 in model.g if (g,g1) in Neighbourhood_Regions])
model.GimpE=Set(dimen=3, initialize= Interconnection_Regions)   
   
model.GimpH=Set(dimen=2, initialize=[(f,g) for f in model.f for g in model.g if (f,g) in Interconnection_Regions2])
model.TransDis=Set(dimen=2, initialize=[(g,g1) for g in model.g for g1 in model.g if (g,g1) in TransDistance_data])


region_order = {region: i + 1 for i, region in enumerate(model.g)}
model.ord_g = Param(model.g, initialize=region_order)


year_order = {region: i + 1 for i, region in enumerate(model.t)}
model.ord_t = Param(model.t, initialize=year_order)

time_order = {time: i + 1 for i, time in enumerate(model.h)}
model.ord_h = Param(model.h, initialize=time_order)


tech_order = {tech: i+1 for i, tech in enumerate(model.j)}
model.ord_j= Param(model.j,initialize=tech_order)


Hydrostorage_order = {Hydrostorage: i+1 for i, Hydrostorage in enumerate(model.jhs)}
model.ord_jhs= Param(model.jhs,initialize=Hydrostorage_order)

#%% Read data
Capunit_data =TechData_data.iloc[1:19, 1].values
Capunit_df=TechData_data.iloc[1:19, [0,1]]
Capunit_map={str(k).strip(): v for k, v in zip(Capunit_df.iloc[:,0], Capunit_df.iloc[:,1])}

CHmax_data =TechData_data.iloc[1:7, 6]
Chmax_df = TechData_data.iloc[1:7, [5, 6]]  
Chmax_map={str(k).strip(): v for k, v in zip(Chmax_df.iloc[:,0], Chmax_df.iloc[:,1])}


DHmax_data =TechData_data.iloc[1:7, 12].values
DHmax_df=TechData_data.iloc[1:7, [11,12]]
DHmax_map = {str(k).strip(): v for k, v in zip(DHmax_df.iloc[:, 0], DHmax_df.iloc[:, 1])}


UT_data =TechData_data.iloc[25:33, 1].values
UT_df = TechData_data.iloc[25:33, [0, 1]]
UT_map = {str(k).strip(): v for k, v in zip(UT_df.iloc[:, 0], UT_df.iloc[:, 1])}


LT_data =TechData_data.iloc[37:61, 1].values
LT_df = TechData_data.iloc[37:61, [0, 1]]
LT_map = {str(k).strip(): v for k, v in zip(LT_df.iloc[:, 0], LT_df.iloc[:, 1])}


Pmin_data =TechData_data.iloc[65:77, 1].values
Pmin_df = TechData_data.iloc[65:77, [0, 1]]
Pmin_map = {str(k).strip(): v for k, v in zip(Pmin_df.iloc[:, 0], Pmin_df.iloc[:, 1])}


Pmax_data =TechData_data.iloc[65:77, 6].values
Pmax_df = TechData_data.iloc[65:77, [5, 6]]
Pmax_map = {str(k).strip(): v for k, v in zip(Pmax_df.iloc[:, 0], Pmax_df.iloc[:, 1])}


Stmin_data =TechData_data.iloc[65:70, 11].values
Stmin_df = TechData_data.iloc[65:71, [10, 1]]
Stmin_map = {str(k).strip(): v for k, v in zip(Stmin_df.iloc[:, 0], Stmin_df.iloc[:, 1])}

Stmax_data =TechData_data.iloc[65:70, 16].values
Stmax_df = TechData_data.iloc[65:71, [15, 16]]
Stmax_map = {str(k).strip(): v for k, v in zip(Stmax_df.iloc[:, 0], Stmax_df.iloc[:, 1])}


RD_data =TechData_data.iloc[83:95, 1].values
RD_df = TechData_data.iloc[83:95, [0, 1]]
RD_map = {str(k).strip(): v for k, v in zip(RD_df.iloc[:, 0], RD_df.iloc[:, 1])}


RU_data =TechData_data.iloc[83:95, 6].values
RU_df = TechData_data.iloc[83:95, [5, 6]]
RU_map = {str(k).strip(): v for k, v in zip(RU_df.iloc[:, 0], RU_df.iloc[:, 1])}


SD_data =TechData_data.iloc[83:90, 11].values
SD_df = TechData_data.iloc[83:90, [10, 11]]
SD_map = {str(k).strip(): v for k, v in zip(SD_df.iloc[:, 0], SD_df.iloc[:, 1])}


SU_data =TechData_data.iloc[83:90, 16].values
SU_df = TechData_data.iloc[83:90, [15, 16]]
SU_map = {str(k).strip(): v for k, v in zip(SU_df.iloc[:, 0], SU_df.iloc[:, 1])}


Sdur_data =TechData_data.iloc[127:129, 1].values
Sdur_df = TechData_data.iloc[127:129, [0, 1]]
Sdur_map = {str(k).strip(): v for k, v in zip(Sdur_df.iloc[:, 0], Sdur_df.iloc[:, 1])}



drf_data =TechData_data.iloc[133:147, 1].values
drf_df = TechData_data.iloc[133:147, [0, 1]]
drf_map = {str(k).strip(): v for k, v in zip(drf_df.iloc[:, 0], drf_df.iloc[:, 1])}

Ifmin_data =TechData_data.iloc[184:208, 1].values
Ifmin_df = TechData_data.iloc[184:208, [0, 1]]
Ifmin_map = {str(k).strip(): v for k, v in zip(Ifmin_df.iloc[:, 0], Ifmin_df.iloc[:, 1])}


Ifmax_data =TechData_data.iloc[184:208, 5].values
Ifmax_df = TechData_data.iloc[184:208, [4, 5]]
Ifmax_map = {str(k).strip(): v for k, v in zip(Ifmax_df.iloc[:, 0], Ifmax_df.iloc[:, 1])}


etasef_data =TechData_data.iloc[212:220, 1].values
etasef_df = TechData_data.iloc[212:220, [0, 1]]
etasef_map = {str(k).strip(): v for k, v in zip(etasef_df.iloc[:, 0], etasef_df.iloc[:, 1])}


EtP_data =TechData_data.iloc[224:232, 1].values
EtP_df = TechData_data.iloc[224:232, [0, 1]]
EtP_map = {str(k).strip(): v for k, v in zip(EtP_df.iloc[:, 0], EtP_df.iloc[:, 1])}

LT_heat_data =HeatTech_data.iloc[19:24, 1].values
LT_heat_df = HeatTech_data.iloc[19:24, [0, 1]]
LT_heat_map = {str(k).strip(): v for k, v in zip(LT_heat_df.iloc[:, 0], LT_heat_df.iloc[:, 1])}


cstart_data =CostTech_data.iloc[29:40, 1].values
cstart_df = CostTech_data.iloc[29:40, [0, 1]]
cstart_map = {str(k).strip(): v for k, v in zip(cstart_df.iloc[:, 0], cstart_df.iloc[:, 1])}




cshut_data =CostTech_data.iloc[29:40, 5].values
cshut_df = CostTech_data.iloc[29:40, [4, 5]]
cshut_map = {str(k).strip(): v for k, v in zip(cshut_df.iloc[:, 0], cshut_df.iloc[:, 1])}



oc_var_data =CostTech_data.iloc[1:25, 23].values
oc_var_df = CostTech_data.iloc[1:25, [22, 23]]
oc_var_map = {str(k).strip(): v for k, v in zip(oc_var_df.iloc[:, 0], oc_var_df.iloc[:, 1])}


oc_var_ch_data =CostTech_data.iloc[1:9, 31].values
oc_var_ch_df = CostTech_data.iloc[1:9, [30, 31]]
oc_var_ch_map = {str(k).strip(): v for k, v in zip(oc_var_ch_df.iloc[:, 0], oc_var_ch_df.iloc[:, 1])}

dur_data=General_data.iloc[6,0]
ir_data=General_data.iloc[16,0]
nel_data=General_data.iloc[21,0]
iph_data=General_data.iloc[26,0]
goc_data=General_data.iloc[36,0]
CM_data=General_data.iloc[42,0]
cVOLL_data=General_data.iloc[47,0]
ctr_data=Trans_data.iloc[1,0]
triup_data=Trans_data.iloc[21,0]
Population_data=General_data.iloc[19:32,14].values
Population_df = General_data.iloc[19:32, [13, 14]]
Population_map = {str(k).strip(): v for k, v in zip(Population_df.iloc[:, 0], Population_df.iloc[:, 1])}


drfl_data=Trans_data.iloc[25:37,1].values
drfl_df = Trans_data.iloc[25:37, [0, 1]]
drfl_map = {str(k).strip(): v for k, v in zip(drfl_df.iloc[:, 0], drfl_df.iloc[:, 1])}

loss_data=Trans_data.iloc[40:52,1].values
loss_df = Trans_data.iloc[40:52, [0, 1]]
loss_map = {str(k).strip(): v for k, v in zip(loss_df.iloc[:, 0], loss_df.iloc[:, 1])}



#WF_data=Cluster_data.iloc[2:8,114].values
#WF_df = Cluster_data.iloc[2:8, [113, 114]]
#WF_map = {str(k).strip(): v for k, v in zip(WF_df.iloc[:, 0], WF_df.iloc[:, 1])}

values = df_WF.iloc[:, 0].tolist()  

init_dict = {f"c{i+1}": values[i] for i in range(len(values))}



breg_data = Biomass_data.iloc[2:14, 2]
breg_df =Biomass_data.iloc[2:15, [1, 2]]
breg_map = {str(k).strip(): v for k, v in zip(breg_df.iloc[:, 0], breg_df.iloc[:, 1])}

Vbiomax_data = Biomass_data.iloc[20, 1:7]
Vbiomax_df =Biomass_data.iloc[22:28,[1,2]]
Vbiomax_map = {int(k): v for k, v in zip(Vbiomax_df.iloc[:, 0], Vbiomax_df.iloc[:, 1])}


rcap_data=Reservoir_data.iloc[1:5, 1]
rcap_df = Reservoir_data.iloc[1:5, [0, 1]]
rcap_map = {str(k).strip(): v for k, v in zip(rcap_df.iloc[:, 0], rcap_df.iloc[:, 1])}

ri0_data=Reservoir_data.iloc[9:13, 1]
ri0_df = Reservoir_data.iloc[9:13, [0, 1]]
ri0_map = {str(k).strip(): v for k, v in zip(ri0_df.iloc[:, 0], ri0_df.iloc[:, 1])}


yc_data=Emissions_data.iloc[7:18, 1]
yc_df = Emissions_data.iloc[7:18, [0, 1]]
yc_map = {str(k).strip(): v for k, v in zip(yc_df.iloc[:, 0], yc_df.iloc[:, 1])}


ye_data=Emissions_data.iloc[22:33, 1]
ye_df = Emissions_data.iloc[22:33, [0, 1]]
ye_map = {str(k).strip(): v for k, v in zip(ye_df.iloc[:, 0], ye_df.iloc[:, 1])}

ct_data=Emissions_data.iloc[1:7, 9]
ct_df = Emissions_data.iloc[1:7, [8, 9]]
ct_map = {int(k) : int(v) for k, v in zip(
    Emissions_data.iloc[1:7, 8],
    Emissions_data.iloc[1:7, 9]
)}

et_data=Emissions_data.iloc[37:43, 9]
et_df = Emissions_data.iloc[37:43, [8, 9]]
et_map = {int(k): int(v) for k, v in zip(
    Emissions_data.iloc[37:43, 8],
    Emissions_data.iloc[37:43, 9]
)}

diaH_data=Pipelines_data.iloc[9:12, 1]
diaH_df = Pipelines_data.iloc[9:12, [0, 1]]
diaH_map = {str(k).strip(): v for k, v in zip(diaH_df.iloc[:, 0], diaH_df.iloc[:, 1])}


diaC_data=Pipelines_data.iloc[9:11, 2]
diaC_df = Pipelines_data.iloc[9:11, [0, 2]]
diaC_map = {str(k).strip(): v for k, v in zip(diaC_df.iloc[:, 0], diaC_df.iloc[:, 1])}


qHmax_data=Pipelines_data.iloc[20:23, 1]
qHmax_df = Pipelines_data.iloc[20:23, [0, 1]]
qHmax_map = {str(k).strip(): v for k, v in zip(qHmax_df.iloc[:, 0], qHmax_df.iloc[:, 1])}


qCmax_data=Pipelines_data.iloc[20:22, 2]
qCmax_df = Pipelines_data.iloc[20:22, [0, 2]]
qCmax_map = {str(k).strip(): v for k, v in zip(qCmax_df.iloc[:, 0], qCmax_df.iloc[:, 1])}


pc_H2_data=Pipelines_data.iloc[31:34, 1]
pc_H2_df = Pipelines_data.iloc[31:34, [0, 1]]
pc_H2_map = {str(k).strip(): v for k, v in zip(pc_H2_df.iloc[:, 0], pc_H2_df.iloc[:, 1])}


pc_COnshore_data=Pipelines_data.iloc[31:33, 2]
pc_COnshore_df = Pipelines_data.iloc[31:33, [0, 2]]
pc_COnshore_map = {str(k).strip(): v for k, v in zip(pc_COnshore_df.iloc[:, 0], pc_COnshore_df.iloc[:, 1])}


pc_COffshore_data=Pipelines_data.iloc[31:33, 6]
pc_COffshore_df = Pipelines_data.iloc[31:33, [0, 6]]
pc_COffshore_map = {str(k).strip(): v for k, v in zip(pc_COffshore_df.iloc[:, 0], pc_COffshore_df.iloc[:, 1])}

dom_year_df = year_data.iloc[54:60,[9,10]]
dom_year_map = {int(k): v for k, v in zip(dom_year_df.iloc[:, 0], dom_year_df.iloc[:, 1])}

com_year_df = year_data.iloc[54:60,[9,11]]
com_year_map = {int(k): v for k, v in zip(com_year_df.iloc[:, 0], com_year_df.iloc[:, 1])}

Ind_year_df = year_data.iloc[54:60,[9,12]]
Ind_year_map = {int(k): v for k, v in zip(Ind_year_df.iloc[:, 0], Ind_year_df.iloc[:, 1])}

elec_year_df  = year_data.iloc[39:45,[15,16]]
elec_year_map = {int(k): v for k, v in zip(elec_year_df.iloc[:, 0], elec_year_df.iloc[:, 1])}


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
    if df_Dist.iloc[i, j] > 0
    }

DistSt_data = {(g, s): df_DistSt.iloc[i,2] 
          for i, g in enumerate(df_DistSt.iloc[:, 0])
          for j, s in enumerate(df_DistSt.iloc[:, 1])
          if i==j}

techs = df_eta.iloc[:, 0].str.strip()

eta_data = {
    (techs[i], t): df_eta.iloc[i, t_idx + 1] 
    for i in range(len(techs))
    for t_idx, t in enumerate(model.t)
}



techs1 = df_BR.iloc[:, 0].str.strip()

cols_to_use = [2,3, 4,5, 6]

BR_data = {
    (tech, t): df_BR.iloc[i, col]
    for i, tech in enumerate(techs1)
    for col, t in zip(cols_to_use, [model.t[2],model.t[3], model.t[4],model.t[5], model.t[6]]) }



techs2 = df_cc_Heat.iloc[:, 0].str.strip()
cc_Heat_data = {
    (techs2[i], t): df_cc_Heat.iloc[i, t_idx + 1] 
    for i in range(len(techs2))
    for t_idx, t in enumerate(model.t)
}

techs2 = df_eta_Heat.iloc[:, 0].str.strip()
eta_Heat_data = {
    (techs2[i], t): df_eta_Heat.iloc[i, t_idx + 1] 
    for i in range(len(techs2))
    for t_idx, t in enumerate(model.t)
}

techs3 = df_cc_fix.iloc[:, 0].str.strip()
cc_fix_data = {
    (techs3[i], t): df_cc_fix.iloc[i, t_idx + 1] 
    for i in range(len(techs3))
    for t_idx, t in enumerate(model.t)
}



oc_fix_data = {
    (techs3[i], t): df_oc_fix.iloc[i, t_idx + 1] 
    for i in range(len(techs3))
    for t_idx, t in enumerate(model.t)
}

techs4 = df_LandAvailability.iloc[:, 0].str.strip()
LandAvailability_data = {
    (techs4[i], g): df_LandAvailability.iloc[i, g_idx + 1] 
    for i in range(len(techs4))
    for g_idx, g in enumerate(model.g)
}

techs5 = df_NUint.iloc[:, 0].str.strip()
NUint_data = {
    (techs5[i], g): df_NUint.iloc[i, g_idx + 1] 
    for i in range(len(techs5))
    for g_idx, g in enumerate(model.g)
}

techs6 = df_Capinit.iloc[:, 0].str.strip()
Capinit_data = {
    (techs6[i], g): df_Capinit.iloc[i, g_idx + 1] 
    for i in range(len(techs6))
    for g_idx, g in enumerate(model.g)
}

techs7 = df_NUf.iloc[:, 0].str.strip()


NUF_data = {
    (j.strip(), int(t), g): df_NUf.iloc[i, 2 + gi]
    for i, (j, t) in enumerate(zip(df_NUf.iloc[:, 0], df_NUf.iloc[:, 1]))
    for gi, g in enumerate(model.g)
}



techs8 = df_Capf.iloc[:, 0].str.strip()

Capf_data = {
    (j.strip(), int(t), g): df_Capf.iloc[i, 2 + gi]
    for i, (j, t) in enumerate(zip(df_Capf.iloc[:, 0], df_Capf.iloc[:, 1]))
    for gi, g in enumerate(model.g)
}


links = df_ICap.iloc[:, 0].str.strip()   
regions = df_ICap.iloc[:, 1].str.strip() 

cols_time = range(2, 8)  

ICap_data = {
    (i, g, t): df_ICap.iloc[idx, col]
    for idx, (i, g) in enumerate(zip(links, regions))
    for col, t in zip(cols_time, model.t) 
}


Country = df_pim_y.iloc[:, 0].str.strip()
Country_data = {
    (Country[i], t): df_pim_y.iloc[i, t_idx + 1] 
    for i in range(len(Country))
    for t_idx, t in enumerate(model.t)
}



cluster = df_ipe.iloc[:, 0].str.strip()   
Hour = df_ipe.iloc[:, 1].str.strip() 

cols_time = range(2, 8)  

ipe_data = {
    (c, h, k): df_ipe.iloc[cdx, col]
    for cdx, (c, h) in enumerate(zip(cluster, Hour))
    for col, k in zip(cols_time, model.k) 
}


ElecDem_data = {
    (row[8], row[9]): row[10] for idx, row in df_ElecDem.iterrows()
}



Ind_data = {(c, h, g): df_Ind.iloc[i, 2+j] 
               for i, (c, h) in enumerate(zip(df_Ind.iloc[:, 0], df_Ind.iloc[:, 1]))  
               for j, g in enumerate(model.g)}

Com_data = {(c, h, g): df_Com.iloc[i, 2+j] 
               for i, (c, h) in enumerate(zip(df_Com.iloc[:, 0], df_Com.iloc[:, 1]))  
               for j, g in enumerate(model.g)}

Dom_data = {(c, h, g): df_Dom.iloc[i, 2+j] 
               for i, (c, h) in enumerate(zip(df_Dom.iloc[:, 0], df_Dom.iloc[:, 1]))  
               for j, g in enumerate(model.g)}

jre_filtered = ["Solar", "WindOn", "WindOff"]

AV_data = {
    (c, h, g, e): df_AV.iloc[i, 2 + 3 * g_idx + e_idx]
    for i, (c, h) in enumerate(zip(df_AV.iloc[:, 0], df_AV.iloc[:, 1]))
    for g_idx, g in enumerate(model.g)
    for e_idx, e in enumerate(jre_filtered) 
}


temp_data = {(c, h, g): df_temp.iloc[i, 2+j] 
               for i, (c, h) in enumerate(zip(df_temp.iloc[:, 0], df_temp.iloc[:, 1]))  
               for j, g in enumerate(model.g)}


fuel = df_fuel.iloc[:, 0].str.strip()
fuel_data = {
    (fuel[i], t): df_fuel.iloc[i, t_idx + 1] 
    for i in range(len(fuel))
    for t_idx, t in enumerate(model.t)
}


TRC_data = {
    (g_row, g_col): df_ExT.iloc[i, j]
    for i, g_row in enumerate(model.g)
    for j, g_col in enumerate(model.g) 
    }


#%%PARAMETERs
model.dw=Param(initialize=16.62)
model.fp=Param(initialize=1.63)
model.ge=Param(initialize=0.25)
model.fe=Param(initialize=2.3)
model.lut=Param(initialize=2)
model.me=Param(initialize=0.07)
model.sp=Param(initialize=55)
model.tcap=Param(initialize=21.66)
model.tma=Param(initialize=18)
model.tmc=Param(initialize=253000)
model.Ltroad=Param(initialize=15)
model.delta=Param(initialize=0.05)
model.LTpipe=Param(initialize=50)
model.ccurt=Param(initialize=47)
model.dur=Param(initialize=10)
model.ir=Param(initialize=0.035)
model.nel=Param(initialize=30)
model.iph=Param(initialize=127.6)
model.goc=Param(initialize=18.7)
model.CM=Param(initialize=0.088)
model.cVOLL=Param(initialize=20109)
model.ctr=Param(initialize=247)
model.crf= Param(initialize=0.05)
model.triup=Param(initialize=1500)
model.iota=Param(initialize=0.1)
model.aeC0 = Param(model.r, initialize=0, doc='Initial availability of an offshore CO2 pipeline between collection point in regions g and reservoir r (0-1)')
model.Capunit=Param(model.j, initialize=Capunit_map)
model.CHmax = Param(model.j, initialize=Chmax_map, domain=Any)
model.DHmax = Param(model.j, initialize=DHmax_map, domain=Any)
model.UT = Param(model.j, initialize=UT_map, domain=Any)
model.DT = Param(model.j, initialize=UT_map)
model.LT = Param(model.j, initialize=LT_map)
model.Pmin=Param(model.j, initialize=Pmin_map)
model.Pmax=Param(model.j, initialize=Pmax_map)
model.Stmin=Param(model.jhs, initialize=Stmin_map)
model.Stmax=Param(model.jhs, initialize=Stmax_map)
model.RD=Param(model.j, initialize=RD_map)
model.RU=Param(model.j, initialize=RD_map)
model.SD=Param(model.j, initialize=SD_map)
model.SU=Param(model.j, initialize=SU_map)
model.Sdur=Param(model.jes, initialize=Sdur_map)
model.drf=Param(model.j,initialize=drf_map)
model.Ifmin=Param(model.j, initialize=Ifmin_map)
model.Ifmax=Param(model.j, initialize=Ifmax_map)
model.etasef=Param(model.j,initialize=etasef_map)
model.EtP=Param(model.j,initialize=EtP_map)
model.LT_heat=Param(model.jhe, initialize=LT_heat_map)
model.oc_var_ch=Param(model.j,initialize=oc_var_ch_map)
model.oc_var=Param(model.j,initialize=oc_var_map)
model.cstart=Param(model.j,initialize=cstart_map)
model.cshut=Param(model.j,initialize=cshut_map)
model.Population=Param(model.g,initialize=Population_map)
model.drfl=Param(model.i,initialize=drfl_map)
model.loss=Param(model.i,initialize=loss_map)
model.WF=Param(model.c,initialize=init_dict)
model.breg=Param(model.g,initialize=breg_map)
model.Vbiomax=Param(model.t, initialize=Vbiomax_map)
model.ri0=Param(model.r, initialize=ri0_map)
model.rcap=Param(model.r, initialize=rcap_map)
model.yc=Param(model.j,initialize=yc_map)
model.ye=Param(model.j,initialize=ye_map)
model.ct=Param(model.t,initialize=ct_map)
model.et=Param(model.t,initialize=et_map)
model.diaH=Param(model.d,initialize=diaH_map)
model.diaC=Param(model.d2,initialize=diaC_map)
model.qHmax=Param(model.d,model.f, initialize={('d1', 'GH2'): 2117, ('d2', 'GH2'): 10052, ('d3', 'GH2'): 15343})
model.qCmax=Param(model.d2, model.f, initialize={('d1', 'CO2'): 1666.57, ('d2', 'CO2'): 11666.67})
model.pc_H2=Param(model.d,initialize=pc_H2_map)
model.pc_COnshore=Param(model.d2,initialize=pc_COnshore_map)
model.pc_COffshore=Param(model.d2,initialize=pc_COffshore_map)
model.ldd=Param(model.TransDis,initialize=Distance_dict)
model.DistSt = Param(model.g, model.jhs, initialize=DistSt_data, doc='distance between region g and underground storage type s')
model.DistPipe = Param(model.g, model.g, initialize=DistPipe_data, within=NonNegativeReals, doc='Delivery distance of an onshore CO2 pipeline between regions g and g1 (km)')
model.DistRes = Param(model.g, model.r, initialize=DistRes_data, doc='Distance from CO2 collection point in region g to reservoir r (km)')
model.Dist = Param(model.g, model.g, initialize=Dist_data, doc='Regional delivery distance of hydrogen transportation mode l in region g (km)')
model.TRC= Param(model.g,model.g,initialize=TRC_data)
model.eta=Param(model.j,model.t,initialize=eta_data)
model.BR = Param(model.j, model.TT, initialize=BR_data, domain=NonNegativeReals)
model.cc_Heat=Param(model.jhe,model.t,initialize=cc_Heat_data)
model.eta_Heat=Param(model.jhe,model.t,initialize=eta_Heat_data)
model.cc_fix=Param(model.j,model.t,initialize=cc_fix_data)
model.oc_fix=Param(model.j,model.t,initialize=oc_fix_data)
model.LandAvailability=Param(model.jre,model.g,initialize=LandAvailability_data)
model.NUint=Param(model.j,model.g,initialize=NUint_data,default=0)
model.Capinit=Param(model.j,model.g,initialize=Capinit_data, default=0, mutable=True)
model.ICap= Param(model.i,model.g,model.t, initialize=ICap_data)
model.pim_y=Param(model.k,model.t,initialize=Country_data)
model.ipe=Param(model.c,model.h,model.k,initialize=ipe_data)
model.ElecDem = Param(model.c, model.h, initialize=ElecDem_data)
model.Ind=Param(model.c,model.h,model.g, initialize=Ind_data)
model.Com=Param(model.c,model.h,model.g, initialize=Com_data)
model.Dom=Param(model.c,model.h,model.g, initialize=Dom_data)
model.AV = Param(model.c, model.h, model.g, model.jre, initialize=AV_data, mutable=True)

# Assign 0.45 to all c,h,g where jre = 'Hydro'
for c in model.c:
    for h in model.h:
        for g in model.g:
            model.AV[c,h,g,'Hydro'] = 0.45
model.temp=Param(model.c, model.h,model.g, initialize=temp_data)
model.fuel=Param(model.f,model.t,initialize=fuel_data)
model.NUF = Param(model.j, model.t, model.g, initialize=NUF_data, default=0)
model.Capf= Param(model.jre,model.t,model.g, initialize=Capf_data, default=0)



from pyomo.environ import value

def dfc_init(model, t):
    t_num = int(t)           
    return round(1 / (1 + value(model.ir)) ** (model.dur * t_num - model.dur), 2)

model.dfc = Param(
    model.t,
    initialize=dfc_init,
    doc='Discount factor for capital costs in time period t'
)

# Predefined values in order
dfo_values_list = [4.520, 3.690, 3.030, 2.490, 2.060, 1.710]

# Create a dictionary mapping each t in model.t to the value
dfo_values = {t: val for t, val in zip(model.t, dfo_values_list)}

# Initialize the Param
model.dfo = Param(
    model.t,
    initialize=dfo_values,
    doc='Predefined discount factor for each time period'
)


model.Npipe = Set(dimen=2,initialize=model.DistPipe.keys(), doc='Set of region pairs with nonzero pipeline distances')

model.ayHR0 = Param(model.d, model.Npipe,initialize=0, doc='Initial availability of a regional hydrogen pipeline of diameter size d between regions g and g1 (0-1)')
model.ayC0 = Param(model.d2, model.N, initialize=0, doc='Initial availability of an onshore CO2 pipeline of diameter size d between regions g and g1 (0-1)')

model.StLevelInit=Param(model.jes,model.g,model.t, initialize=0)

def ipe_t_init(model, c, h, k, t):
    return model.pim_y[k, t] * model.ipe[c, h, k]

model.ipe_t = Param(
    model.c, model.h, model.k, model.t,
    initialize=ipe_t_init,
    doc="Adjusted ipe by pim_y for each (c,h,k,t)"
)

model.y1=Param(initialize=2)

def GJh_init(model):
    jh_list = list(model.jh)  

    cond_set = [
        (g, jh)
        for g in model.g
        for jh in model.jh
        if jh_list.index(jh) < 6
    ]

    explicit_set = [
        ('NO', 'OnTeeside'),
        ('NW', 'OnChesire'),
        ('NE', 'OnYorkshire'),
        ('NW', 'OffIrishSea')
    ]

    return list(set(cond_set + explicit_set))

model.GJh = Set(dimen=2, initialize=GJh_init, within=model.g * model.jh)

model.dom_year= Param (model.t, initialize=dom_year_map)
model.com_year= Param (model.t, initialize=com_year_map)
model.Ind_year= Param (model.t, initialize=Ind_year_map)
model.elec_year= Param(model.t,initialize=elec_year_map)


def THeatDem_init(model, g, t, c, h):
    return (model.dom_year[t] * model.Dom[c, h, g] +
            model.com_year[t] * model.Com[c, h, g]) * model.eta_Heat['GasBoiler', t]

model.THeatDem = Param(model.g, model.t, model.c, model.h, initialize=THeatDem_init)

def THeatDem_max_init(model, g, t):
    return max(model.THeatDem[g, t, c, h] for c in model.c for h in model.h)

model.THeatDem_max = Param(model.g, model.t, initialize=THeatDem_max_init)

def TPowerDem_init(model, g, t, c, h):
    return model.elec_year[t] * model.Population[g] * model.ElecDem[c, h]

model.TPowerDem = Param(model.g, model.t, model.c, model.h, initialize=TPowerDem_init)

def COP_init(model, g, c, h):
    return 0.0541 * model.temp[c, h, g] + 2.6674

model.COP = Param(model.g, model.c, model.h, initialize=COP_init)

def CAPinit_init(model, tech, g):
    if tech != 'GasBoiler':
        return 0
    max_val = max(model.Dom[c, h, g] + model.Com[c, h, g]
                  for c in model.c for h in model.h)
    return max_val * model.eta_Heat['GasBoiler', 1]


for tech in ['GasBoiler']:
    for g in model.g:
        val = CAPinit_init(model, tech, g)
        model.Capinit[tech, g] = val




def IndDem_init(model, g, t, c, h):
    return model.Ind_year[t] * model.Ind[c, h, g] * model.eta_Heat['GasBoiler', t]

model.IndDem = Param(model.g, model.t, model.c, model.h, initialize=IndDem_init)

        
def Qpipe_bounds(model, f, g, g1, t, c, h):
    if f == 'GH2':
        return (0, 15343)
    elif f == 'CO2':
        return (0, 11666)
    return (0, None)


def Qres_bounds(model, g, r, t, c, h):
    return (0, 11666)
#%%Variables

model.NTU = Var(model.g, model.g, model.t, domain=NonNegativeReals)
model.NU = Var(model.j, model.g, model.t, domain=NonNegativeReals)


model.DU = Var(model.j, model.g, model.t, domain=NonNegativeIntegers)
model.CU = Var(model.j, model.g, model.t, domain=NonNegativeIntegers)
model.ITU = Var(model.g, model.g, model.t, domain=Integers)
model.u = Var(model.j, model.g, model.t, model.c, model.h, domain=Integers)
model.v = Var(model.j, model.g, model.t, model.c, model.h, domain=Integers)
model.w = Var(model.j, model.g, model.t, model.c, model.h, domain=Integers)

model.Y = Var(model.f, model.d, model.Npipe, model.t, domain=Binary)
model.Y1 = Var(model.f, model.d2, model.N, model.t, domain=Binary)

model.Yres = Var(model.d2, model.GR, model.t, domain=Binary)
model.Yst = Var(model.d, model.GJh, model.t, domain=Binary)


model.AY = Var(model.f, model.d, model.Npipe, model.t, bounds=(0,1),domain=NonNegativeReals)
model.AY1 = Var(model.f, model.d2, model.N, model.t,bounds=(0,1), domain=NonNegativeReals)

model.AYres = Var(model.d2, model.GR, model.t, bounds=(0,1),domain=NonNegativeReals)
model.AYst = Var(model.d, model.g, model.jhs, model.t, bounds=(0,1),domain=NonNegativeReals)

model.BS = Var(model.j, model.g, model.t, model.per, domain=NonNegativeReals)
model.CAP = Var(model.j, model.g, model.t, domain=NonNegativeReals)
model.CAPnew = Var(model.j, model.g, model.t, domain=NonNegativeReals)
model.CAPheat = Var(model.jhe, model.g, model.t, domain=NonNegativeReals)
model.CAPheat_new = Var(model.jhe, model.g, model.t, domain=NonNegativeReals)
model.CH = Var(model.j, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.DCheat = Var(model.jhe, model.g, model.t, domain=NonNegativeReals)
model.DCAP = Var(model.j, model.g, model.t, domain=NonNegativeReals)
model.totdem_elec = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.hedem_elec = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.totdem_hydro = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.totdem_gas = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.hedem_hydro = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.hedem_gas = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.DC = Var(model.j, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.ETC = Var(model.t, domain=NonNegativeReals)
model.FCC = Var(model.t, domain=NonNegativeReals)
model.FOC = Var(model.t, domain=NonNegativeReals)
model.HC = Var(model.t, domain=NonNegativeReals)
model.HGDC = Var(model.t, domain=NonNegativeReals)
model.HGOC = Var(model.t, domain=NonNegativeReals)
model.IMPh = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.indem_elec = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.indem_gas = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.indem_hydro = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.LC = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.LS = Var(model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.Lelec = Var(model.g, model.t, domain=NonNegativeReals)
model.Lgas = Var(model.g, model.t, domain=NonNegativeReals)
model.Lhydro = Var(model.g, model.t, domain=NonNegativeReals)
model.P = Var(model.j, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.PeakDemand = Var(model.t, domain=NonNegativeReals)
model.Qelec = Var(model.g, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.Qroad = Var(model.f, model.g, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.Qpipe = Var(model.f, model.g, model.g, model.t, model.c, model.h, domain=NonNegativeReals, bounds=Qpipe_bounds)
model.Qres = Var(model.g, model.r, model.t, model.c, model.h, domain=NonNegativeReals,bounds=Qres_bounds)
model.PCC = Var(model.TT, domain=NonNegativeReals)
model.POC = Var(model.TT, domain=NonNegativeReals)
model.RCC = Var(model.t, domain=NonNegativeReals)
model.Rdown = Var(model.j, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.RI = Var(model.r, model.t, domain=NonNegativeReals)
model.ROC = Var(model.t, domain=NonNegativeReals)
model.Rup = Var(model.j, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.S = Var(model.j, model.g, model.t, model.c, model.h, domain=NonNegativeReals)
model.TCC = Var(model.TT, domain=NonNegativeReals)
model.TOC = Var(model.TT, domain=NonNegativeReals)
model.TRCnew = Var(model.g, model.g, model.t, domain=NonNegativeReals)
model.TRI = Var(model.g, model.g, model.TT, domain=NonNegativeReals)
model.Vf = Var(model.f, model.j, model.g, model.t, domain=NonNegativeReals)
model.THeatDem_max1 = Var(model.g, model.t, domain=NonNegativeReals)
    
model.CEC = Var(model.t)
model.Etotal = Var(model.t)
model.Ee = Var(model.t)
model.Eh = Var(model.t)
model.Eg = Var(model.t)
model.IIC = Var(model.t)
model.GasC = Var(model.t)
model.Imp = Var()
model.IMPe = Var(model.i, model.g, model.t, model.c, model.h)
model.PipeCost = Var(domain=NonNegativeReals)


model.CapDC=Var(model.TT, model.g,domain=NonNegativeReals)
model.CapDCNew=Var(model.TT, model.g,domain=NonNegativeReals)

model.TDemandDC=Var(model.g,model.TT,model.c,model.h, domain=NonNegativeReals)


#%%
# Facilities capital cost
def FCC_rule(model, t):
    return (
       0.001* model.FCC[t]
        == 0.001*sum(
            model.cc_fix[j, t] * model.Capunit[j] * model.CU[j, g, t]
            for g in model.g
            for j in model.j
            if ((g, j) in model.GJh or j in model.jth)
        )
        +0.001* sum(
            model.cc_fix[j, t] * model.CAPnew[j, g, t]
            for g in model.g
            for j in model.j
            if (j in model.jes or j in model.jre)
        )
    )

model.FCCConstraint = Constraint(model.TT, rule=FCC_rule)

def ETC_rule(model, t):
    if t in model.TT:
        return 0.001*model.ETC[t] == 0.001*sum(
            model.ctr * model.ldd[g, g1] * model.TRI[g, g1, t] / 2
            for g in model.g for g1 in model.g if (g, g1) in model.N
        )
    return Constraint.Skip

model.ETConstraint = Constraint(model.TT, rule=ETC_rule)


def PCC_rule(model, t):
    if t in model.TT:
        return 0.001*model.PCC[t] == 0.001*(
            # 1st sum: Hydrogen pipelines
            sum(
                model.pc_H2[d] * model.DistPipe[g,g1] * model.Y[f,d,g,g1,t]
                for d in model.d
                for f in model.f if f=="f2"
                for g in model.g
                for g1 in model.g
                if (g,g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1] and (d,f) in model.df
            )
            +
            # 2nd sum: CO2 onshore
            sum(
                model.pc_COnshore[d2] * model.Dist[g,g1] * model.Y1[f,d2,g,g1,t]
                for d2 in model.d2
                for f in model.f if f=="f3"
                for g in model.g
                for g1 in model.g
                if (g,g1) in model.N and model.ord_g[g] < model.ord_g[g1] and (d2,f) in model.df
            )
            +
            # 3rd sum: CO2 offshore
            sum(
                model.pc_COffshore[d2] * model.DistRes[g,r] * model.Yres[d2,g,r,t]
                for d2 in model.d2
                for g in model.g
                for r in model.r
                if (g,r) in model.GR
            )
            +
            # 4th sum: Hydrogen storage
            sum(
                model.pc_H2[d] * model.DistSt[g,jhs] * model.Yst[d,g,jhs,t]
                for d in model.d
                for g in model.g
                for jhs in model.jhs
                if (g,jhs) in model.GJh and jhs in ['OnTeeside','OnChesire','OnYorkshire','OffIrishSea']
            )
        )
    return Constraint.Skip

model.PCCConstraint = Constraint(model.TT, rule=PCC_rule)



def POC_rule(model, t):
    if t in model.TT:
        return 0.001*model.POC[t] == 0.001*(
            model.delta * model.crf * (
                # 1st sum: Hydrogen pipelines
                sum(
                    model.pc_H2[d] * model.DistPipe[g,g1] * model.AY[f,d,g,g1,t]
                    for d in model.d
                    for f in model.f if f=="f2"
                    for g in model.g
                    for g1 in model.g
                    if (g,g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1] and (d,f) in model.df
                )
                +
                # 2nd sum: CO2 onshore
                sum(
                    model.pc_COnshore[d2] * model.Dist[g,g1] * model.AY1[f,d2,g,g1,t]
                    for d2 in model.d2
                    for f in model.f if f=="f3"
                    for g in model.g
                    for g1 in model.g
                    if (g,g1) in model.N and model.ord_g[g] < model.ord_g[g1] and (d2,f) in model.df
                )
                +
                # 3rd sum: CO2 offshore
                sum(
                    model.pc_COffshore[d2] * model.DistRes[g,r] * model.AYres[d2,g,r,t]
                    for d2 in model.d2
                    for g in model.g
                    for r in model.r
                    if (g,r) in model.GR
                )
                +
                # 4th sum: Hydrogen storage
                sum(
                    model.pc_H2[d] * model.DistSt[g,jhs] * model.AYst[d,g,jhs,t]
                    for d in model.d
                    for g in model.g
                    for jhs in model.jhs
                    if (g,jhs) in model.GJh and jhs in ['OnTeeside','OnChesire','OnYorkshire','OffIrishSea']
                )
            )
        )
    return Constraint.Skip

model.POCConstraint = Constraint(model.TT, rule=POC_rule)






def FOC_rule(model, t):
    if t in model.TT:
        return 0.001*model.FOC[t] == 0.001*(

            # 1st sum: (j,g) in Gjh(g,j) or jth(j)
            sum(
                model.oc_fix[j, t] * model.Capunit[j] * model.NU[j, g, t]
                for j in model.j
                for g in model.g
                if ((g, j) in model.GJh or j in model.jth)
            )
            +
            # 2nd sum: (j,g) in jes(j) or jre(j)
            sum(
                model.oc_fix[j, t] * model.CAP[j, g, t]
                for j in model.j
                for g in model.g
                if (j in model.jes or j in model.jre)
            )
            +
            # 3rd sum: (j,g,c,h) with jhp(j) or jep(j)
            sum(
                model.WF[c] * model.oc_var[j] * model.P[j, g, t, c, h]
                for j in model.j
                for g in model.g
                for c in model.c
                for h in model.h
                if (j in model.jhp or j in model.jep)
            )
            +
            # 4th sum: (f,j,g) in jf
            sum(
                model.fuel[f, t] * model.Vf[f, j, g, t]
                for f in model.f
                for j in model.j
                for g in model.g
                if (f, j) in model.jf
            )
            +
            # 5th sum: (j,g,c,h) with jhs(j) or jes(j)
            sum(
                model.WF[c] * model.oc_var[j] * model.S[j, g, t, c, h]
                for j in model.j
                for g in model.g
                for c in model.c
                for h in model.h
                if (j in model.jhs or j in model.jes)
            )
            +
            # 6th sum: (j,g,c,h,f) with jhs(j) or jes(j)
            sum(
                model.WF[c] * model.oc_var_ch[j] * model.CH[j, g, t, c, h]
                for j in model.j
                for g in model.g
                for c in model.c
                for h in model.h
                for f in model.f
                if (j in model.jhs or j in model.jes)
            )
            +
            # 7th sum: curtailment cost
            sum(
                model.WF[c] * model.ccurt * model.LC[g, t, c, h]
                for g in model.g
                for c in model.c
                for h in model.h
            )
            +
            # 8th sum: Value of Lost Load
            sum(
                model.WF[c] * model.cVOLL*2 * model.LS[g, t, c, h]
                for g in model.g
                for c in model.c
                for h in model.h
            )
        )
    return Constraint.Skip

model.FOCConstraint = Constraint(model.TT, rule=FOC_rule)

def CEC_rule(model, t):
    if t in model.TT:
        return 0.001*model.CEC[t]==0.001*model.ct[t]*model.Etotal[t]
    return Constraint.Skip
model.CECConstraint = Constraint(model.TT, rule=CEC_rule)   


def IIC_rule(model, t):
    if t in model.TT:
        return 0.001*model.IIC[t] == 0.001 *(
            # 1st sum: Electric imports
            sum(
                model.WF[c] * model.ipe_t[c, h, k, t] * model.IMPe[i, g, t, c, h]
                for g in model.g
                for c in model.c
                for h in model.h
                for i in model.i
                for k in model.k
                if ('Elec', i, g) in model.GimpE and (k, i) in model.ik
            )
            +
            # 2nd sum: Hydrogen imports
            sum(
                model.WF[c] * model.iph * model.IMPh[g, t, c, h]
                for g in model.g
                for c in model.c
                for h in model.h
                if ('GH2', g) in model.GimpH
            )
        )
    return Constraint.Skip

model.IICConstraint = Constraint(model.TT, rule=IIC_rule)
'''
def GasC_rule(model,t):
    if t in model.TT:
        return model.GasC[t] == model.dfo[t]*(
            # 1st sum: gas use in technologies
            sum(
                model.Vf['Gas', j, g, t]
                for j in model.j
                for g in model.g
                if ('Gas', j) in model.jf 
            )
            +
            # 2nd sum: total gas demand
            sum(
                model.WF[c] * model.totdem_gas[g, t, c, h]
                for g in model.g
                for c in model.c
                for h in model.h
                
            )
        )
    return Constraint.Skip   
model.GasCeq = Constraint(model.TT,rule=GasC_rule)
'''
# Heating capacity cost
def HC_rule(model, t):
    if t in model.TT:
        return 0.001*model.HC[t] == 0.001*sum(
            model.cc_Heat[jhe, t] * model.CAPheat_new[jhe, g, t]
            for jhe in model.jhe
            for g in model.g
        )
    return Constraint.Skip

model.HCConstraint = Constraint(model.TT, rule=HC_rule)


# Direct Gas Cost for heating
def HGDC_rule(model, t):
    if t in model.TT:
        return 0.001*model.HGDC[t] == 0.001*sum(
            model.WF[c] * model.fuel['Gas', t] * model.totdem_gas[g, t, c, h]
            for g in model.g
            for c in model.c
            for h in model.h
           
        )
    return Constraint.Skip

model.HGDCConstraint = Constraint(model.TT, rule=HGDC_rule)


# Operating Gas Cost for heating
def HGOC_rule(model, t):
    if t in model.TT:
        return 0.001*model.HGOC[t] == 0.001*sum(
            model.WF[c] * model.goc * model.totdem_gas[g, t, c, h]
            for g in model.g
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip

model.HGOCConstraint = Constraint(model.TT, rule=HGOC_rule)



def TCC_rule(model,t):
    if t in model.TT:
      return model.TCC[t]==model.PCC[t]+model.FCC[t]+model.ETC[t]+model.HC[t]
    return Constraint.Skip
model.TCCConstraint=Constraint(model.TT,rule=TCC_rule)


def TOC_rule(model,t):
    if t in model.TT:
      return model.TOC[t]==model.POC[t]+model.FOC[t]+model.CEC[t]+model.IIC[t]+model.HGDC[t]+model.HGOC[t]#+model.GasC[t]
    return Constraint.Skip
model.TOCConstraint=Constraint(model.TT,rule=TOC_rule)


def TC_rule(model):
    return sum(model.dfc[t]*model.TCC[t] +  model.dfo[t]*model.TOC[t] for t in model.TT)+ 0.1 * sum(
        (model.Qpipe['GH2', g, g1, t, c, h] if (g, g1) in model.Npipe else 0)
        + (model.Qpipe['CO2', g, g1, t, c, h] if (g, g1) in model.N else 0)
        for g in model.g
        for g1 in model.g
        for t in model.TT
        for c in model.c
        for h in model.h
    )
        

model.TC = Objective(rule=TC_rule, sense=minimize)


#%% Heating Calculation
def HeatElec_rule(model, g, t, c, h):
    if t in model.TT:
        return model.hedem_elec[g, t, c, h] == model.Lelec[g, t] * model.THeatDem[g, t, c, h]
    return Constraint.Skip

model.HeatElec = Constraint(model.g, model.TT, model.c, model.h, rule=HeatElec_rule)

# Heating hydrogen demand
def HeatHydro_rule(model, g, t, c, h):
    if t in model.TT:
        return model.hedem_hydro[g, t, c, h] == model.Lhydro[g, t] * model.THeatDem[g, t, c, h]
    return Constraint.Skip

model.HeatHydro = Constraint(model.g, model.TT, model.c, model.h, rule=HeatHydro_rule)

# Heating gas demand
def HeatGas_rule(model, g, t, c, h):
    if t in model.TT:
        return model.hedem_gas[g, t, c, h] == model.Lgas[g, t] * model.THeatDem[g, t, c, h]
    return Constraint.Skip

model.HeatGas = Constraint(model.g, model.TT, model.c, model.h, rule=HeatGas_rule)

# Heat summation for flexible system
def HeatSum_rule(model, g, t, c, h):
    if t in model.TT:
        return model.hedem_elec[g, t, c, h] + model.hedem_hydro[g, t, c, h] + model.hedem_gas[g, t, c, h] == model.THeatDem[g, t, c, h]
    return Constraint.Skip

model.HeatSum = Constraint(model.g, model.TT, model.c, model.h, rule=HeatSum_rule)

# Lambda coefficient summation
def Lcoefsum_rule(model, g, t):
    if t in model.TT:
        return model.Lelec[g, t] + model.Lhydro[g, t] + model.Lgas[g, t] == 1
    return Constraint.Skip

model.Lcoefsum = Constraint(model.g, model.TT, rule=Lcoefsum_rule)

# Upper bounds for lambda coefficients
#def Lelec2_rule(model, g, t):
   # if t in model.TT:
        #return model.Lelec[g, t] <= 1
    #return Constraint.Skip

#model.Lelec2 = Constraint(model.g, model.TT, rule=Lelec2_rule)


#def Lgas3_rule(model, g, t):
    #if t in model.TT:
        #return model.Lgas[g, t] <= 1
    #return Constraint.Skip

#model.Lgas3 = Constraint(model.g, model.TT, rule=Lgas3_rule)


# Industrial heating demand
def IndHeat_rule(model, g, t, c, h):
    if t in model.TT:
        return (model.indem_elec[g, t, c, h] + model.indem_hydro[g, t, c, h] +
                model.indem_gas[g, t, c, h] == model.IndDem[g, t, c, h])
    return Constraint.Skip

model.IndHeat = Constraint(model.g, model.TT, model.c, model.h, rule=IndHeat_rule)

# Fixing variables
for g in model.g:
    for t in model.t:
        for c in model.c:
            for h in model.h:
                model.indem_hydro[g, t, c, h].fix(0)

                if t == 6:
                    model.indem_elec[g, t, c, h].fix(model.IndDem[g, t, c, h])

def HeatPen1_rule(model, g, t):
    if t in model.TT and model.ord_t[t] > model.y1:
        t_prev = model.ord_t[t] - 1  
        t_prev_label = [tt for tt in model.TT if model.ord_t[tt] == t_prev]
        if len(t_prev_label) == 0:
            return Constraint.Skip
        t_prev_label = t_prev_label[0]
        return sum(model.hedem_hydro[g, t_prev_label, c, h] for c in model.c for h in model.h) <= \
               sum(model.hedem_hydro[g, t, c, h] for c in model.c for h in model.h)
    return Constraint.Skip

model.HeatPen1 = Constraint(model.g, model.TT, rule=HeatPen1_rule)

def HeatPen2_rule(model, g, t):
    if t in model.TT and model.ord_t[t] > model.y1:
        t_prev = model.ord_t[t] - 1
        t_prev_label = [tt for tt in model.TT if model.ord_t[tt] == t_prev]
        if len(t_prev_label) == 0:
            return Constraint.Skip
        t_prev_label = t_prev_label[0]
        return sum(model.hedem_elec[g, t_prev_label, c, h] for c in model.c for h in model.h) <= \
               sum(model.hedem_elec[g, t, c, h] for c in model.c for h in model.h)
    return Constraint.Skip

model.HeatPen2 = Constraint(model.g, model.TT, rule=HeatPen2_rule)
#%%
def total_elec_demand_rule(model, g, t, c, h):
    if t in model.TT and c in model.c and h in model.h:
        return model.totdem_elec[g,t,c,h] == (
            model.TPowerDem[g,t,c,h]+
            + sum(model.P[j,g,t,c,h]/model.eta[j,t] for j in model.j if ('Elec', j) in model.jf)
            + model.hedem_elec[g,t,c,h]/model.COP[g,c,h]+
            + model.indem_elec[g,t,c,h]
        )
    return Constraint.Skip

model.TotalElecDemand = Constraint(model.g, model.TT, model.c, model.h, rule=total_elec_demand_rule)

def total_hydro_demand_rule(model, g, t, c, h):
    if t in model.TT and c in model.c and h in model.h:
        return model.totdem_hydro[g,t,c,h] == (
            sum(model.P[j,g,t,c,h]/model.eta[j,t] for j in model.j if ('GH2', j) in model.jf)
            + (model.hedem_hydro[g,t,c,h] + model.indem_hydro[g,t,c,h]) / model.eta_Heat['HyBoiler',t]
        )
    return Constraint.Skip

model.TotalHydroDemand = Constraint(model.g, model.TT, model.c, model.h, rule=total_hydro_demand_rule)

def total_gas_demand_rule(model, g, t, c, h):
    if t in model.TT and c in model.c and h in model.h:
        return model.totdem_gas[g,t,c,h] == (
            (model.hedem_gas[g,t,c,h] + model.indem_gas[g,t,c,h]) / model.eta_Heat['GasBoiler',t]
        )
    return Constraint.Skip

model.TotalGasDemand = Constraint(model.g, model.TT, model.c, model.h, rule=total_gas_demand_rule)


#%%
#Electricity Balance
def elec_balance_rule(model, f, g, t, c, h):
    if t in model.TT and f == 'Elec':
        return (
            sum(model.P[j, g, t, c, h] for j in model.j if j in model.jep) +
            sum(model.Qelec[g1, g, t, c, h] for g1 in model.g if (g1, g) in model.N) +
            sum(model.DC[j, g, t, c, h] for j in model.jes) +
            sum((1 - model.loss[i]) * model.IMPe[i, g, t, c, h] for i in model.i if ('Elec', i, g) in model.GimpE) +
            model.LS[g, t, c, h]
            ==
            sum(model.Qelec[g, g1, t, c, h] for g1 in model.g if (g, g1) in model.N) +
            sum(model.CH[j, g, t, c, h] for j in model.jes) +
            model.LC[g, t, c, h] +
            model.totdem_elec[g, t, c, h]
        )
    return Constraint.Skip

model.ElecBalance = Constraint(model.f, model.g, model.TT, model.c, model.h, rule=elec_balance_rule)


#%%
# Hydrogen Balance
def hydro_balance_rule(model, f, g, t, c, h):
    if t in model.TT and c in model.c and h in model.h and f == 'GH2':
        return (
            sum(model.P[j, g, t, c, h] for j in model.j if j in model.jhp) +
            sum(model.Qpipe[f, g1, g, t, c, h] for g1 in model.g if (g1, g) in model.Npipe) +
            sum(model.DC[jhs, g, t, c, h] for jhs in model.jhs if (g, jhs) in model.GJh)
            ==
            sum(model.Qpipe[f, g, g1, t, c, h] for g1 in model.g if (g, g1) in model.Npipe) +
            sum(model.CH[jhs, g, t, c, h] for jhs in model.jhs if (g, jhs) in model.GJh) +
            model.totdem_hydro[g, t, c, h]
        )
    return Constraint.Skip

model.HydroBalance = Constraint(model.f, model.g, model.TT, model.c, model.h, rule=hydro_balance_rule)


#%%
#CO2 Balance
def co2_balance_rule(model, f, g, t, c, h):
    if t in model.TT and c in model.c and h in model.h and f == 'CO2':
        return (
            sum(model.Qpipe[f, g1, g, t, c, h] for g1 in model.g if (g1, g) in model.N) +
            sum(model.yc[jccs] * model.P[jccs, g, t, c, h] for jccs in model.jccs)
            ==
            sum(model.Qpipe[f, g, g1, t, c, h] for g1 in model.g if (g, g1) in model.N) +
            sum(model.Qres[g, r, t, c, h] for r in model.r if (g, r) in model.GR)
        )
    return Constraint.Skip

model.CO2Balance = Constraint(model.f, model.g, model.TT, model.c, model.h, rule=co2_balance_rule)


#%%
from pyomo.environ import value

def ElecInv1_rule(model, jth, g, t):
    t0 = value(model.LT[jth]) / 5   # numeric value

    if t in model.TT:
        return  model.NU[jth,g,t] == (
            (model.NUint[jth,g] if  (t==model.y1 and t<=t0) else 0)
            - (model.NUint[jth,g] if t==t0 else 0)
            + (model.NU[jth,g,t-1] if t>model.y1 else 0)
            + model.NUF[jth,t,g] 
            + model.CU[jth,g,t] 
            - model.DU[jth,g,t]
            - (model.CU[jth,g,t-t0] if t-t0 in [2,3,4,5,6] else 0)
        )
    return Constraint.Skip
 
model.ElecInv1 = Constraint(model.jth, model.g, model.TT, rule=ElecInv1_rule)


from pyomo.environ import value, Constraint

def ElecInv2_rule(model, j, g, t):
    if t in model.TT and (j in model.jre or j in model.jes):
        t0 = value(model.LT[j]) / 5  # numeric shift
        return model.CAP[j, g, t] == (
            (model.Capinit[j, g] if t == model.y1 else 0)
            + (model.CAP[j, g, t-1] if t > model.y1 else 0)
            + (model.Capf[j, t, g] if  j in ['Solar', 'WindOff'] else 0)
            + model.CAPnew[j, g, t]
            - model.DCAP[j, g, t]
            - (model.CAPnew[j, g, t - t0] if (t - t0) in model.TT else 0)
        )
    return Constraint.Skip

model.ElecInv2 = Constraint(model.j, model.g, model.TT, rule=ElecInv2_rule)





def Buildrate_rule(model, j,t):
    if t in model.TT and j in ['SMRCCS','ATRCCS','BGCCS','WE','MPSV','HPSV','FC','H2CCGT','Nuclear','OCGT','CCGTCCS','BECCS','Biomass','CCGT']:
        return sum(model.CU[j,g,t]*model.Capunit[j] for g in model.g) <= model.BR[j,t]
    return Constraint.Skip
model.BuildrateCon= Constraint(model.j, model.TT, rule=Buildrate_rule)

def Build2_rule(model,j,t):
    if t in model.TT and (j in model.jre or j in model.jes):
        return sum(model.CAPnew[j,g,t] for g in model.g)<= model.BR[j,t]
    return Constraint.Skip
model.Build2Con=Constraint(model.j,model.TT, rule=Build2_rule)

def LandAvailability_rule(model,jre,g,t):
    if t in model.TT and jre in ['Solar', 'WindOn', 'WindOff']:
        return model.CAP[jre,g,t]<= (model.LandAvailability[jre,g]+model.Capinit[jre,g])
    return Constraint.Skip
model.LandAVCon=Constraint(model.jre,model.g, model.TT, rule=LandAvailability_rule)
#%%
# Fuel consumption for power generation and hydrogen production units

def Fuel_rule(model,f,j,g,t):
    if t in model.TT and (f,j) in model.jf:
        return model.Vf[f,j,g,t]==sum(model.WF[c]*model.P[j,g,t,c,h]/model.eta[j,t] for c in model.c for h in model.h)
    return Constraint.Skip
model.FuelCon=Constraint(model.f,model.j,model.g,model.TT, rule=Fuel_rule)



#%% Power generation

def ThermalCap1_rule(model,j,g,t,c,h):
    if t in model.TT and j in ['Nuclear', 'OCGT', 'H2CCGT']:
        return model.P[j,g,t,c,h]>= model.Pmin[j]*model.Capunit[j]*model.NU[j,g,t]
    return Constraint.Skip
#model.ThermalCap1Con=Constraint(model.j,model.g,model.TT,model.c,model.h,rule=ThermalCap1_rule)

def ThermalCap2_rule(model,j,g,t,c,h):
    if t in model.TT and j in model.jth:
        return model.P[j,g,t,c,h]<= model.Pmax[j]*model.Capunit[j]*model.NU[j,g,t]
    return Constraint.Skip
model.ThermalCap2Con=Constraint(model.j,model.g,model.TT,model.c,model.h,rule=ThermalCap2_rule)

def ReCap_rule(model,j,g,t,c,h):
    if t in model.TT and j in model.jre:
        return model.P[j,g,t,c,h]==model.AV[c,h,g,j]*model.CAP[j,g,t]
    return Constraint.Skip
model.ReCapCon=Constraint(model.j,model.g,model.TT,model.c,model.h, rule=ReCap_rule)

def Curtailment_rule (model,g,t,c,h):
    if t in model.TT:
        return model.LC[g,t,c,h]<= sum(model.P[j,g,t,c,h] for j in model.j if j in model.jre)
    return Constraint.Skip
model.CurtailCon=Constraint(model.g,model.TT,model.c,model.h, rule=Curtailment_rule)


#%% Thermal Ramp Constraints
h_list = list(model.h)  
h_index = {h:i for i,h in enumerate(h_list)} 


def ThermalRampUp_rule(model, j,g,t,c,h):
    if t in model.TT and h_index[h] > 0 and j in ['FC','H2CCGT','Nuclear','CCGTCCS','OCGT','BECCS', 'Biomass', 'CCGT', 'SMRCCS', 'ATRCCS', 'BGCCS','WE']:
        prev_h = h_list[h_index[h]-1]  
        return model.P[j,g,t,c,h] - model.P[j,g,t,c,prev_h] <= model.RU[j]*model.Capunit[j]*model.NU[j,g,t]
    return Constraint.Skip
model.thermalRampCON=Constraint(model.j,model.g,model.TT,model.c,model.h, rule=ThermalRampUp_rule)
    
def ThermalRampDown_rule(model, j,g,t,c,h):
    if t in model.TT and h_index[h] > 0 and j in ['FC','H2CCGT','Nuclear','CCGTCCS','OCGT','BECCS', 'Biomass', 'CCGT', 'SMRCCS', 'ATRCCS', 'BGCCS','WE']:
        prev_h = h_list[h_index[h]-1]  
        return model.P[j,g,t,c,prev_h] - model.P[j,g,t,c,h] <= model.RD[j]*model.Capunit[j]*model.NU[j,g,t]
    return Constraint.Skip
model.thermalRampdownCON=Constraint(model.j,model.g,model.TT,model.c,model.h, rule=ThermalRampDown_rule)
      


#%% *Capacity of the transmission
def TrCapacity_rule(model,f,g,g1,t,c,h):
    if f in ['Elec'] and t in model.TT and (g,g1) in model.N:
        return model.Qelec[g,g1,t,c,h]<= model.TRCnew[g,g1,t]
    return Constraint.Skip
model.TrCapacityCon=Constraint(model.f,model.N,model.TT,model.c,model.h, rule=TrCapacity_rule)


    
def TrInvest_rule(model, g, g1, t):
    if (g, g1) in model.N and t in model.TT:
        
        return model.TRCnew[g, g1, t] ==(model.TRC[g,g1] if t==model.y1 else 0)
    + (model.TRCnew[g, g1, t-1] if t> model.y1 else 0)
    + model.TRI[g, g1, t]
    return Constraint.Skip

model.TrInvest = Constraint(model.N, model.TT, rule=TrInvest_rule)

    
'''
def TrInvest_rule(model, g, g1, t):
    if t in model.TT and (g, g1) in model.N:
        i = t_index[t]
        if i == 0:  # first period
            prev_val = 0
        else:
            prev_t = t_list[i-1]
            prev_val = model.TRC[g, g1, prev_t]
        return model.TRC[g, g1, t] == prev_val + model.TRI[g, g1, t]
    return Constraint.Skip

model.TrInvest = Constraint(model.N, model.TT, rule=TrInvest_rule)
'''


def TrInvest2_rule(model,g,g1,t):
    if t in model.TT and (g,g1) in model.N:
        return model.TRCnew[g,g1,t]==model.TRCnew[g1,g,t]
    return Constraint.Skip
model.TrInvest2Con= Constraint(model.N,model.TT,rule=TrInvest2_rule)

def TrInvestUp_rule(model,g,g1,t):
    if t in model.TT and (g,g1) in model.N:
        return model.TRI[g,g1,t]<=model.triup
    return Constraint.Skip
model.TrInvestUpCon= Constraint(model.N,model.TT,rule=TrInvestUp_rule)


def InterCapacity1_rule(model,f,i,g,t,c,h):
    if f in ['Elec'] and (f,i,g) in model.GimpE and t in model.TT:
        return model.IMPe[i,g,t,c,h]<= model.ICap[i,g,t]
    return Constraint.Skip
model.InterCapacity1Con= Constraint(model.f,model.i,model.g, model.TT,model.c,model.h, rule=InterCapacity1_rule)

def InterCapacity2_rule(model,f,i,g,t,c,h):
    if f in ['Elec'] and (f,i,g) in model.GimpE and t in model.TT:
        return model.IMPe[i,g,t,c,h]>= -model.ICap[i,g,t]
    return Constraint.Skip
model.InterCapacity2Con= Constraint(model.f,model.i,model.g, model.TT,model.c,model.h, rule=InterCapacity2_rule)



#%% Energy Storage
def ChargeBound_rule(model,jes,g,c,h,t):
    if t in model.TT:
        return model.CH[jes,g,t,c,h]<=model.CAP[jes,g,t]
    return Constraint.Skip
model.ChargeBoundCon=Constraint(model.jes,model.g,model.c,model.h,model.TT, rule=ChargeBound_rule)

def DischargeBound_rule(model,jes,g,c,h,t):
    if t in model.TT:
        return model.DC[jes,g,t,c,h]<=model.CAP[jes,g,t]
    return Constraint.Skip
model.DischargeBoundCon=Constraint(model.jes,model.g,model.c,model.h,model.TT, rule=DischargeBound_rule)

def StorageCap_rule(model,jes,g,t,c,h,per):
    if t in model.TT and (c,per) in model.CP:
        return model.S[jes,g,t,c,h]+model.BS[jes,g,t,per]<=model.EtP[jes]*model.CAP[jes,g,t]
    return Constraint.Skip
model.StorageCapCon= Constraint(model.jes,model.g,model.TT,model.c,model.h,model.per, rule=StorageCap_rule)


# build list + index for h
h_list = list(model.h)
h_index = {h: i for i, h in enumerate(h_list)} 
def StorageLevel_rule(model, jes, g, t, c, h):
    if t in model.TT:
        idx = h_index[h]
        if idx > 0:  
            prev_h = h_list[idx - 1]
            return model.S[jes, g, t, c, h] == (
                (1 - model.etasef[jes]) * model.S[jes, g, t, c, prev_h]
                + model.eta[jes, t] * model.CH[jes, g, t, c, h]
                - model.DC[jes, g, t, c, h] / model.eta[jes, t]
            )
    return Constraint.Skip

model.StorageLevelCon = Constraint(model.jes, model.g, model.TT, model.c, model.h, rule=StorageLevel_rule)




#%%PEAK DEMAND
def PeakDemand_rule(model,t,c,h):
    if t in model.TT:
        return model.PeakDemand[t]>= sum(model.totdem_elec[g,t,c,h] for g in model.g)
    return Constraint.Skip
model.PeakDemandCon=Constraint(model.TT,model.c,model.h, rule=PeakDemand_rule)

def Reserve_ruel(model,t):
    if t in model.TT:
        return sum(model.drf[jth]*model.Capunit[jth]*model.NU[jth,g,t] for jth in model.jth for g in model.g)\
            +sum(model.drf[j]*model.CAP[j,g,t] for j in['WindOn', 'WindOff','Solar', 'Hydro', 'LeadBat', 'PumpHy'] for g in model.g)\
                +sum(model.drfl[i]*model.ICap[i,g,t] for i in model.i for g in model.g for f in model.f if f in ['Elec'] and (f,i,g) in model.GimpE )\
                    >= (1+model.CM)*model.PeakDemand[t]                  
    return Constraint.Skip
model.ReserveCon= Constraint(model.TT, rule=Reserve_ruel)



#%%
#def HydrogenCap1_rule(model,jhp,g,t,c,h):
   # if t in model.TT :
       # return model.P[jhp,g,t,c,h]>= model.Pmin[jhp]*model.Capunit[jhp]*model.NU[jhp,g,t]
    #return Constraint.Skip
#model.HydrogenCap1Con=Constraint(model.jhp,model.g,model.TT,model.c,model.h,rule=HydrogenCap1_rule)

# Ordered list of time periods


from pyomo.environ import value

def HydroInv_rule(model, jh, g, t):
    t0 = value(model.LT[jh]) / 5   # numeric value

    if t in model.TT and (g, jh) in model.GJh:
        return model.NU[jh, g, t] == (
            (model.NU[jh, g, t-1] if t > model.y1 else 0)
            + (model.NUF[jh, t, g] if jh in ['WE'] else 0)
            + model.CU[jh, g, t]
            - (model.CU[jh, g, t-t0] if t-t0 in model.TT else 0)
        )
    return Constraint.Skip

model.HydroInv = Constraint(model.jh, model.g, model.TT, rule=HydroInv_rule)





'''
def HydroInv_rule(model, jh, g, t):
    # Only define constraint if time step and GJh exist
    if t in model.TT and (g, jh) in model.GJh:
        LTjh = model.LT[jh].value
        t1 = model.ord_t[t] - model.dur.value // 5
        t2 = model.ord_t[t] - LTjh // 5

        return model.NU[jh, g, t] == (
            (model.NU[jh, g, t1] if model.ord_t[t] > model.y1 and t1 in model.TT else 0)
            + model.NUF[jh, t, g]
            + model.CU[jh, g, t]
            - (model.CU[jh, g, t2] if t2 in model.TT else 0)
        )
    return Constraint.Skip

model.HydroInv = Constraint(model.jh, model.g, model.TT, rule=HydroInv_rule)

'''


def HydrogenCap2_rule(model,jhp,g,t,c,h):
    if t in model.TT :
        return model.P[jhp,g,t,c,h]<= model.Pmax[jhp]*model.Capunit[jhp]*model.NU[jhp,g,t]
    return Constraint.Skip
model.HydrogenCap2Con=Constraint(model.jhp,model.g,model.TT,model.c,model.h,rule=HydrogenCap2_rule)


h_list = list(model.h)  
h_index = {h:i for i,h in enumerate(h_list)} 

def HydrogenRampDown_rule(model, jhp,g,t,c,h):
    if t in model.TT and h_index[h] > 0:
        prev_h = h_list[h_index[h]-1]  
        return model.P[jhp,g,t,c,prev_h] - model.P[jhp,g,t,c,h] <= model.RD[jhp]*model.Capunit[jhp]*model.NU[jhp,g,t]
    return Constraint.Skip
model.HydrogenRampdownCON=Constraint(model.jhp,model.g,model.TT,model.c,model.h, rule=HydrogenRampDown_rule)
  


def HydrogenRampUP_rule(model, jhp,g,t,c,h):
    if t in model.TT and h_index[h] > 0:
        prev_h = h_list[h_index[h]-1]  
        return model.P[jhp,g,t,c,h]- model.P[jhp,g,t,c,prev_h]  <= model.RD[jhp]*model.Capunit[jhp]*model.NU[jhp,g,t]
    return Constraint.Skip
model.HydrogenRampUPCON=Constraint(model.jhp,model.g,model.TT,model.c,model.h, rule=HydrogenRampUP_rule)
  

#%% Hydrogen Storage
def HydrogenSCap1_rule(model,jhs,g,t,c,h,per):
    if t in model.TT and (c,per) in model.CP and (g,jhs) in model.GJh:
        return model.S[jhs,g,t,c,h]+model.BS[jhs,g,t,per]<=model.Stmax[jhs]*model.Capunit[jhs]*model.NU[jhs,g,t]
    return Constraint.Skip
model.HydroSCap1CON= Constraint(model.jhs,model.g,model.TT,model.c, model.h,model.per, rule=HydrogenSCap1_rule)


def HydrogenSCap2_rule(model,jhs,g,t,c,h,per):
    if t in model.TT and (c,per) in model.CP and (g,jhs) in model.GJh:
        return model.S[jhs,g,t,c,h]+model.BS[jhs,g,t,per]>=model.Stmin[jhs]*model.Capunit[jhs]*model.NU[jhs,g,t]
    return Constraint.Skip
model.HydroSCap2CON= Constraint(model.jhs,model.g,model.TT,model.c, model.h,model.per, rule=HydrogenSCap2_rule)

def MaxInj_rule(model,f,jhs,g,t,c,h):
    if t in model.TT and f in ['GH2'] and (g,jhs) in model.GJh:
        return model.CH[jhs,g,t,c,h]<=model.CHmax[jhs]
    return Constraint.Skip
model.MaxInjCON= Constraint(model.f,model.jhs,model.g,model.TT,model.c,model.h, rule=MaxInj_rule)

def MaxRet_rule(model,f,jhs,g,t,c,h):
    if t in model.TT and f in ['GH2'] and (g,jhs) in model.GJh:
        return model.DC[jhs,g,t,c,h]<=model.DHmax[jhs]
    return Constraint.Skip
model.MaxRetCON= Constraint(model.f,model.jhs,model.g,model.TT,model.c,model.h, rule=MaxRet_rule)


# build list + index for h
h_list = list(model.h)
h_index = {h: i for i, h in enumerate(h_list)} 
def HydStorageLevel_rule(model, jhs, g, t, c, h):
    if t in model.TT:
        idx = h_index[h]
        if idx > 0:  
            prev_h = h_list[idx - 1]
            return model.S[jhs, g, t, c, h] == (
                (1 - model.etasef[jhs]) * model.S[jhs, g, t, c, prev_h]
                + model.eta[jhs, t] * model.CH[jhs, g, t, c, h]
                - model.DC[jhs, g, t, c, h] / model.eta[jhs, t]
            )
    return Constraint.Skip

model.HydStorageLevelCon = Constraint(model.jhs, model.g, model.TT, model.c, model.h, rule=HydStorageLevel_rule)


# %%  RESERVIORS Constraints ---------------------
# Inventory 
def res_inventory_rule(model, r, t):
    if t in model.TT: 
       
        return model.RI[r, t] == (
            model.RI[r, t-1] if  t > model.y1 else model.ri0[r]
        ) + model.dur * sum(
            model.WF[c] * model.Qres[(g, r), t, c, h] 
            for g in model.g if (g, r) in model.GR
            for c in model.c for h in model.h
        )
    return Constraint.Skip

model.ResInventoryConstraint = Constraint(model.r, model.TT, rule=res_inventory_rule)


def ResCapacity_rule(model,r,t):
    if t in model.TT:
        return 0.001*model.RI[r,t]<=0.001*model.rcap[r]
    return Constraint.Skip
model.ResCapacityCON=Constraint(model.r,model.TT, rule=ResCapacity_rule)


#%% BIOMASS AVAILABILITY
def BioAvailability_rule(model,g,t):
    if t in model.TT:
        return 0.001*sum (model.Vf['Bio', j,g,t] for j in model.jb) <= 0.001*0.5*1000000*model.breg[g]*model.Vbiomax[t]
    return Constraint.Skip
model.BioAvailCON=Constraint(model.g,model.TT, rule=BioAvailability_rule)


#%%INTERSEASONAL STORAGE
'''
def BSeq1_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p1'] == model.BS[j, g, t, 'p8'] \
             + model.WF['c6'] * (model.S[j, g, t, 'c6', 'h24'] - model.S[j, g, t, 'c6', 'h1'])
    return Constraint.Skip
model.BSeq1 = Constraint(model.j, model.g, model.TT, rule=BSeq1_rule)

def BSeq2_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p2'] == model.BS[j, g, t, 'p1'] \
             + 18 * (model.S[j, g, t, 'c3', 'h24'] - model.S[j, g, t, 'c3', 'h1'])
    return Constraint.Skip
model.BSeq2 = Constraint(model.j, model.g, model.TT, rule=BSeq2_rule)

def BSeq3_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p3'] == model.BS[j, g, t, 'p2'] \
             + 1 * (model.S[j, g, t, 'c1', 'h24'] - model.S[j, g, t, 'c1', 'h1'])
    return Constraint.Skip
model.BSeq3 = Constraint(model.j, model.g, model.TT, rule=BSeq3_rule)

def BSeq4_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p4'] == model.BS[j, g, t, 'p3'] \
             + 5 * (model.S[j, g, t, 'c3', 'h24'] - model.S[j, g, t, 'c3', 'h1'])
    return Constraint.Skip
model.BSeq4 = Constraint(model.j, model.g, model.TT, rule=BSeq4_rule)

def BSeq5_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p5'] == model.BS[j, g, t, 'p4'] \
             + 1 * (model.S[j, g, t, 'c2', 'h24'] - model.S[j, g, t, 'c2', 'h1'])
    return Constraint.Skip
model.BSeq5 = Constraint(model.j, model.g, model.TT, rule=BSeq5_rule)

def BSeq6_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p6'] == model.BS[j, g, t, 'p5'] \
             + 65 * (model.S[j, g, t, 'c3', 'h24'] - model.S[j, g, t, 'c3', 'h1'])
    return Constraint.Skip
model.BSeq6 = Constraint(model.j, model.g, model.TT, rule=BSeq6_rule)

def BSeq7_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p7'] == model.BS[j, g, t, 'p6'] \
             + model.WF['c4'] * (model.S[j, g, t, 'c4', 'h24'] - model.S[j, g, t, 'c4', 'h1'])
    return Constraint.Skip
model.BSeq7 = Constraint(model.j, model.g, model.TT, rule=BSeq7_rule)

def BSeq8_rule(model, j, g, t):
    if t in model.TT and (j in model.jhs or j in model.jes):
        return model.BS[j, g, t, 'p8'] == model.BS[j, g, t, 'p7'] \
             + model.WF['c5'] * (model.S[j, g, t, 'c5', 'h24'] - model.S[j, g, t, 'c5', 'h1'])
    return Constraint.Skip
model.BSeq8 = Constraint(model.j, model.g, model.TT, rule=BSeq8_rule)
'''

#%% EMISSION

def ElecEmissions_rule(model, t):
    if t in model.TT:
        return 0.001*model.Ee[t] == 0.001*sum(
            model.WF[c] * model.ye[j] * model.P[j, g, t, c, h]
            for j in model.j if j in ['FC', 'Biomass', 'BECCS', 'CCGT', 'CCGTCCS', 'OCGT', 'Nuclear']
            for g in model.g
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip
model.ElecEmissionsCon = Constraint(model.TT, rule=ElecEmissions_rule)


def H2Emissions_rule(model, t):
    if t in model.TT:
        return model.Eh[t] == sum(
            model.WF[c] * model.ye[j] * model.P[j, g, t, c, h]
            for j in model.j if j in ['SMRCCS', 'ATRCCS', 'BGCCS', 'WE']
            for g in model.g
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip
model.H2EmissionsCon = Constraint(model.TT, rule=H2Emissions_rule)


def GasEmissions_rule(model, t):
    if t in model.TT:
        return 0.001*model.Eg[t] == 0.001*sum(
            model.WF[c] * 0.203 * model.totdem_gas[g, t, c, h]
            for g in model.g
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip
model.GasEmissionsCon = Constraint(model.TT, rule=GasEmissions_rule)


def TotEmissions_rule(model, t):
    if t in model.TT:
        return model.Etotal[t] == model.Ee[t] + model.Eh[t] + model.Eg[t]
    return Constraint.Skip
model.TotEmissionsCon = Constraint(model.TT, rule=TotEmissions_rule)


def TotEmissionsTarget_rule(model, t):
    if t in model.TT:
        return model.Etotal[t] <= model.et[t]
    return Constraint.Skip
model.TotEmissionsTargetCon = Constraint(model.TT, rule=TotEmissionsTarget_rule)

model.Ee1=Var(model.t,model.g)
model.Eh1=Var(model.t,model.g)
model.Eg1=Var(model.t,model.g)

def ElecEmissions1_rule(model, t,g):
    if t in model.TT:
        return 0.001*model.Ee1[t,g] == 0.001*sum(
            model.WF[c] * model.ye[j] * model.P[j, g, t, c, h]
            for j in model.j if j in ['FC', 'Biomass', 'BECCS', 'CCGT', 'CCGTCCS', 'OCGT', 'Nuclear']
           
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip
model.ElecEmissionsCon1 = Constraint(model.TT,model.g, rule=ElecEmissions1_rule)


def H2Emissions1_rule(model, t,g):
    if t in model.TT:
        return model.Eh1[t,g] == sum(
            model.WF[c] * model.ye[j] * model.P[j, g, t, c, h]
            for j in model.j if j in ['SMRCCS', 'ATRCCS', 'BGCCS', 'WE']
           
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip
model.H2EmissionsCon1 = Constraint(model.TT, model.g,rule=H2Emissions1_rule)


def GasEmissions1_rule(model, t,g):
    if t in model.TT:
        return 0.001*model.Eg1[t,g] == 0.001*sum(
            model.WF[c] * 0.203 * model.totdem_gas[g, t, c, h]
            
            for c in model.c
            for h in model.h
        )
    return Constraint.Skip
model.GasEmissionsCon1 = Constraint(model.TT,model.g, rule=GasEmissions1_rule)



#%% Heat Technology
# Assume TT is ordered
from pyomo.environ import value

def HeatInv_rule(model, jhe, g, t):
    t0 = value(model.LT_heat[jhe]) / 5  # numeric shift
    if t in model.TT and jhe in model.JJHE:
        return model.CAPheat[jhe, g, t] == (
            (model.Capinit[jhe, g] if t == model.y1 else 0)
            + (model.CAPheat[jhe, g, t-1] if t > model.y1 else 0)
            + model.CAPheat_new[jhe, g, t]
            - model.DCheat[jhe, g, t]
            - (model.CAPheat_new[jhe, g, t - t0] if (t - t0) in model.TT else 0)
        )
    return Constraint.Skip

model.HeatInv = Constraint(model.jhe, model.g, model.TT, rule=HeatInv_rule)



'''
t_list = list(model.TT)
ord_to_t = {i+1: t for i, t in enumerate(t_list)}  # map ord(t) back to t label

def HeatInv_rule(model, jhe, g, t):
    if t not in model.TT or jhe not in model.JJHE:
        return Constraint.Skip

    t_shift = model.ord_t[t] - model.dur / 5
    prev_t = ord_to_t[t_shift] if t_shift in ord_to_t else None

    return model.CAPheat[jhe, g, t] == (
        (model.Capinit[jhe, g] if model.ord_t[t] == model.y1 else 0)
        + (model.CAPheat[jhe, g, prev_t] if prev_t else 0)
        + model.CAPheat_new[jhe, g, t]
        - (model.CAPheat_new[jhe, g, prev_t] if prev_t else 0)
        - model.DCheat[jhe, g, t]
    )

model.HeatInv = Constraint(model.JJHE, model.g, model.TT, rule=HeatInv_rule)
'''


def Boiler_rule(model,jhe,g,t):
    if t in model.TT and jhe in ['GasBoiler']:
        return model.CAPheat['GasBoiler', g, 6]== 0
    return Constraint.Skip
model.BoilerCons=Constraint(model.jhe, model.g, model.TT, rule=Boiler_rule)




def HeatCap_rule(model,g,t,c,h):
    if t in model.TT:
        return sum(model.CAPheat[jhe,g,t] for jhe in model.jhe if jhe in model.JJHE) ==model.THeatDem_max[g,t]
    return Constraint.Skip
model.HeatCapCON=Constraint(model.g,model.TT, model.c,model.h, rule=HeatCap_rule)

def ElecHeat_rule(model,g,t,c,h):
    if t in model.TT:
        return sum(model.CAPheat[jhe,g,t] for jhe in model.jhe for f in ['Elec'] if (jhe,f) in model.jhef and jhe in model.JJHE)>= model.hedem_elec[g,t,c,h]
    return Constraint.Skip
model.ElecHeatCON= Constraint(model.g,model.TT,model.c,model.h, rule=ElecHeat_rule)

def HyHeat_rule(model,g,t,c,h):
    if t in model.TT:
        return sum(model.CAPheat[jhe,g,t] for jhe in model.jhe for f in ['GH2'] if (jhe,f) in model.jhef and jhe in model.JJHE)>= model.hedem_hydro[g,t,c,h]
    return Constraint.Skip
model.HyHeatCON= Constraint(model.g,model.TT,model.c,model.h, rule=HyHeat_rule)

def GasHeat_rule(model,g,t,c,h):
    if t in model.TT:
        return sum(model.CAPheat[jhe,g,t] for jhe in model.jhe for f in ['Gas'] if (jhe,f) in model.jhef and jhe in model.JJHE)>= model.hedem_gas[g,t,c,h]
    return Constraint.Skip
model.GasHeatCON= Constraint(model.g,model.TT,model.c,model.h, rule=GasHeat_rule)
#%% PIPELINE CONSTRAINTS------------------------
#------Hydrogen Pipeline Limit ------

# Maximum flowrate for pipelines

def h2pipe_max_rule(model,f, d,g, g1, t, c, h):
    if (g, g1) in model.Npipe and t in model.TT and f in ['GH2'] and (d,f) in model.df:
        return 0.001*model.Qpipe[f, (g, g1), t, c, h] <= 0.001*model.qHmax[d,f] * (
            (model.AY[f,d, (g, g1), t] if model.ord_g[g] < model.ord_g[g1] else 0)+
            (model.AY[f,d, (g1, g), t] if model.ord_g[g1] < model.ord_g[g] else 0) 
            )
            
    return Constraint.Skip

model.H2PipeMax = Constraint(model.f, model.d,model.Npipe, model.TT, model.c, model.h, rule=h2pipe_max_rule)



def onshorepipe_max_rule(model, f, d2, g, g1, t, c, h):
    if (g, g1) in model.N and t in model.TT and f in ['CO2'] and (d2,f) in model.df:
        return 0.001*model.Qpipe[f,g, g1, t, c, h] <= 0.001*model.qCmax[d2,f] * (
                (model.AY1[f,d2, g, g1, t] if model.ord_g[g] < model.ord_g[g1] else 0) +
                (model.AY1[f,d2, g1, g, t] if model.ord_g[g1] < model.ord_g[g] else 0)
            )
           
    return Constraint.Skip

model.OnshorePipeMax = Constraint(model.f, model.d2, model.N, model.TT, model.c, model.h, rule=onshorepipe_max_rule)



def offshorepipe_max_rule(model, f,d2,g, r, t, c, h):
    if (g, r) in model.GR and t in model.TT and f in ['CO2']  and (d2,f) in model.df:
        return 0.001*model.Qres[(g, r), t, c, h]  <= 0.001*model.qCmax[d2,f] * model.AYres[d2, (g, r), t] 
    return Constraint.Skip
model.OffshorePipeMax = Constraint(model.f,model.d2, model.GR, model.TT, model.c, model.h, rule=offshorepipe_max_rule)




# Availability of pipelines
# Create a list and index for TT
t_list = list(model.TT)
t_index = {t: i for i, t in enumerate(t_list)}

def H2PAvailability_rule(model, f, d, g, g1, t):
    if (g, g1) in model.Npipe and t in model.TT and f in ['GH2'] and (d, f) in model.df and model.ord_g[g] < model.ord_g[g1]:
        # previous time index
        prev_t = t_list[t_index[t] - 1] if t_index[t] > 0 else None
        
        # lag time for LTpipe/dur
        lag_offset = int(model.LTpipe / model.dur)
        lag_t = t_list[t_index[t] - lag_offset] if t_index[t] >= lag_offset else None

        return model.AY[f, d, g, g1, t] == (
            (model.AY[f, d, g, g1, prev_t] if prev_t else 0) 
            + (model.ayHR0[d, g, g1] if model.ord_t[t] == model.y1 else 0)
            + model.Y[f, d, g, g1, t]
            - (model.Y[f, d, g, g1, lag_t] if lag_t and model.ord_t[t] > model.y1 else 0)
        )
    return Constraint.Skip

model.H2PAvailability = Constraint(model.f, model.d, model.Npipe, model.TT, rule=H2PAvailability_rule)


def onp_availability_rule(model, f, d2, g, g1, t):
    if (g, g1) in model.N and t in model.TT and f in ['CO2'] and (d2, f) in model.df and model.ord_g[g] < model.ord_g[g1]:
        # previous time index
        prev_t = t_list[t_index[t] - 1] if t_index[t] > 0 else None
        
        # lag time for LTpipe/dur
        lag_offset = int(model.LTpipe / model.dur)
        lag_t = t_list[t_index[t] - lag_offset] if t_index[t] >= lag_offset else None

        return model.AY1[f, d2, g, g1, t] == (
            (model.AY1[f, d2, g, g1, prev_t] if prev_t else 0) 
            + (model.ayC0[d2, g, g1] if model.ord_t[t] == model.y1 else 0)
            + model.Y1[f, d2, g, g1, t]
            - (model.Y1[f, d2, g, g1, lag_t] if lag_t and model.ord_t[t] > model.y1 else 0)
        )
    return Constraint.Skip

model.onp_availability = Constraint(model.f, model.d2, model.N, model.TT, rule=onp_availability_rule)



def offp_availability_rule(model, f, d2, g, r, t):
    if (g, r) in model.GR and t in model.TT and f in ['CO2'] and (d2, f) in model.df:
        # previous time index
        prev_t = t_list[t_index[t] - 1] if t_index[t] > 0 else None
        
        # lag time for LTpipe/dur
        lag_offset = int(model.LTpipe / model.dur)
        lag_t = t_list[t_index[t] - lag_offset] if t_index[t] >= lag_offset else None

        return model.AYres[ d2, g, r, t] == (
            (model.AYres[ d2, g, r, prev_t] if prev_t else 0) 
            + (model.aeC0[r] if model.ord_t[t] == model.y1 else 0)
            + model.Yres[ d2, g, r, t]
            - (model.Yres[ d2, g, r, lag_t] if lag_t and model.ord_t[t] > model.y1 else 0)
        )
    return Constraint.Skip

model.offp_availability = Constraint(model.f, model.d2, model.GR, model.TT, rule=offp_availability_rule)


# Create t_list and t_index if not already done
t_list = list(model.TT)
t_index = {t: i for i, t in enumerate(t_list)}

def PipeStAvailability_rule(model, f, d, g, jhs, t):
    if (g, jhs) in model.GJh and t in model.TT and f in ['GH2'] and (d, f) in model.df and jhs in ['OnTeeside', 'OnChesire', 'OnYorkshire', 'OffIrishSea']:
        # previous time index
        prev_t = t_list[t_index[t] - 1] if t_index[t] > 0 else None
        
        # lag for LTpipe/dur + dur/5
        lag_offset = int(model.LTpipe / model.dur + model.dur / 5)
        lag_t = t_list[t_index[t] - lag_offset] if t_index[t] >= lag_offset else None

        return model.AYst[d, g, jhs, t] == (
            (model.AYst[d, g, jhs, prev_t] if prev_t else 0)
            + model.Yst[d, g, jhs, t]
            - (model.Yst[d, g, jhs, lag_t] if lag_t and model.ord_t[t] > model.y1 else 0)
        )
    return Constraint.Skip

model.PipeStAvailability = Constraint(model.f, model.d, model.g, model.jhs, model.TT, rule=PipeStAvailability_rule)


def CavernPipe_rule(model, jhs, g, t, f):
    if t in model.TT and (g, jhs) in model.GJh and f in ['GH2'] and jhs in ['OnTeeside', 'OnChesire', 'OnYorkshire', 'OffIrishSea']:
        return model.CU[jhs, g, t] <= sum(
            model.Yst[d, g, jhs, t] for d in model.d if (d, f) in model.df
        )
    return Constraint.Skip

model.CavernPipeCon = Constraint(model.jhs, model.g, model.TT, model.f, rule=CavernPipe_rule)



# One diameter size
def h2pipe_rule(model, g, g1, t,f):
     if (g,g1) in model.Npipe and model.ord_g[g] < model.ord_g[g1] and t in model.TT and f in ['GH2']:   
       return sum(model.AY[f, d, (g, g1), t] for d in model.d if (d,f) in model.df) <= 1
     return Constraint.Skip
model.H2Pipe = Constraint(model.Npipe, model.TT,model.f, rule=h2pipe_rule)



def onpipe_rule(model, g, g1, t,f):
    if (g, g1) in model.N and model.ord_g[g] < model.ord_g[g1] and t in model.TT and f in ['CO2']:
        return sum(model.AY1[f,d2, g, g1, t] for d2 in model.d2 if (d2,f) in model.df) <= 1
    return Constraint.Skip

model.OnPipeConstraint = Constraint(model.N, model.TT,model.f, rule=onpipe_rule)



def offpipe_rule(model, g, r, t,f):
     if (g,r) in model.GR and t in model.TT and f in ['CO2']:  
        return sum(model.AYres[d2, (g, r), t] for d2 in model.d2 if (d2,f) in model.df) <= 1
     return Constraint.Skip
model.OffPipe = Constraint(model.GR, model.TT,model.f, rule=offpipe_rule)

def stpipe_rule(model, g, jhs, t,f):
    if (g,jhs) in model.GJh and t in model.TT and f in ['GH2'] and jhs in ['OnTeeside', 'OnChesire', 'OnYorkshire', 'OffIrishSea']:
        return sum(model.AYst[d, (g, jhs), t] for d in model.d if (d,f) in model.df) <= 1
    return Constraint.Skip
model.StPipe = Constraint(model.g,model.jhs, model.TT,model.f, rule=stpipe_rule)



#%% UPPER BOUND

for jhs in model.jhs:
    for g in model.g:
        for t in model.TT:
            if model.ord_jhs[jhs] <= 4 and (g, jhs) in model.GJh:
                model.CU[jhs, g, t].setub(1)

            if (g, jhs) not in model.GJh:
                model.CU[jhs, g, t].setub(0)

# Specific technologies banned
for g in model.g:
    for t in model.TT:
        model.CU['OCGT', g, t].setub(0)
        model.CU['CCGT', g, t].setub(0)
        model.CU['Biomass', g, t].setub(0)
        model.CAPnew['Hydro', g, t].setub(0)
        model.CAPheat_new['GasBoiler', g, t].setub(0)
        

# %%  Solving the model

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

#%%
from openpyxl import Workbook

wb = Workbook()

all_variables = []

objective_value = model.TC()  
all_variables.append({"Name": "Objective", "Index": "-", "Value": objective_value})

for var in model.component_objects(Var, active=True):
    var_name = var.name
    for index in var:
        value = var[index]()
        if value is not None and abs(value) > 1e-6:  
            all_variables.append({
                "Name": var_name,
                "Index": index,
                "Value": value
            })

df = pd.DataFrame(all_variables)
df.to_excel("resultHybrid.xlsx", index=False, sheet_name="All Data")


#%%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

years = ['2030', '2035','2040','2045', '2050']
categories = ['Electricity', 'H2', 'Heating']

# ======================
# دیتای واقعی (ساختار درست)
# ======================
data = {
    '2030': {
        'Electricity': {
            'Solar': 39,
            'Wind Onshore': 15,
            'Wind Offshore': 35,
            'Battery': 30,
            'Nuclear': 15,
            'H2CCGT': 10,
            'FC': 0,
            'CCGT': 33,
            'CCGTCCS': 10,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 0,
            'SMRCCS': 10,
            'ATRCCS': 10,
            'BGCCS': 3.5
        },
        'Heating': {
            'ASHP': 70,
            'HyBoiler': 24,
            'Gas Boiler': 83
        }
    },
    
    '2035': {
        'Electricity': {
            'Solar': 50,
            'Wind Onshore': 20,
            'Wind Offshore': 50,
            'Battery': 45,
            'Nuclear': 18,
            'H2CCGT': 20,
            'CCGT': 33,
            'CCGTCCS': 15,
            'FC': 0,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 0,
            'SMRCCS': 20,
            'ATRCCS': 20,
            'BGCCS': 3.5
        },
        'Heating': {
            'ASHP': 150,
            'HyBoiler': 32,
            'Gas Boiler': 10
        }
    },
    
    
    

    '2040':{
        'Electricity': {
            'Solar': 50,
            'Wind Onshore': 26,
            'Wind Offshore': 60,
            'Battery': 60,
            'Nuclear': 19,
            'H2CCGT': 30,
            'FC': 0,
            'CCGT': 33,
            'CCGTCCS': 20,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 1,
            'SMRCCS': 30,
            'ATRCCS': 30,
            'BGCCS': 4.5
        },
        'Heating': {
            'ASHP': 162,
            'HyBoiler': 52,
            'Gas Boiler': 0}
        },
    '2045': {
        'Electricity': {
            'Solar': 53,
            'Wind Onshore': 28,
            'Wind Offshore': 67,
            'Battery': 60,
            'Nuclear': 21,
            'H2CCGT': 40,
            'CCGT': 33,
            'CCGTCCS': 25,
            'FC': 5,
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 1,
            'SMRCCS': 38,
            'ATRCCS': 40,
            'BGCCS': 6
        },
        'Heating': {
            'ASHP': 177,
            'HyBoiler': 67,
            'Gas Boiler': 83
        }
    },


    '2050': {
        'Electricity': {
            'Solar': 68,
            'Wind Onshore': 35,
            'Wind Offshore': 75,
            'Battery': 60,
            'Nuclear': 24,
            'H2CCGT': 49,
            'FC': 15,
            'CCGT': 0,
            'CCGTCCS': 30,
           
            'BECCS': 0,
            'Biomass': 3.5,
        },
        'H2': {
            'WE': 1,
            'SMRCCS': 49,
            'ATRCCS': 50,
            'BGCCS': 7.5
        },
        'Heating': {
            'ASHP': 182,
            'HyBoiler': 99,
            'Gas Boiler': 0
        }
        }
}

# ======================
# colormap جدا برای هر سکتور
# ======================
# ======================
# تعریف رنگ‌های اختصاصی (اصلاح شده)
# ======================

# ۱. رنگ‌های بخش الکتریسیته
labels_e = ["Solar","Wind Onshore","Wind Offshore","Battery","CCGT","Nuclear","H2CCGT","FC","BECCS","CCGTCCS","Biomass"]
colors_e = ["#FFFF00","#00FF00","#228b22","#00FFFF","#8b0000","#0000FF","#8000FF","#FF00FF","#FF0080","#FF0000","#ffa54f"]

# ۲. رنگ‌های بخش هیدروژن
labels_h2 = ["SMRCCS","ATRCCS","BGCCS","WE"]
colors_h2 = ["#6c7b8b", "#9fb6cd", "#96cdcd","#afeeee"]

# ۳. رنگ‌های بخش گرمایش
labels_ht = ["HyBoiler", "ASHP", "Gas Boiler"]
colors_ht = ["#8b5a00", "#cd8500", "#5d4037"] # رنگ سوم برای Gas Boiler اصلاح شد

# ایجاد دیکشنری نهایی رنگ‌ها
colors = {}
colors.update(dict(zip(labels_e, colors_e)))
colors.update(dict(zip(labels_h2, colors_h2)))
colors.update(dict(zip(labels_ht, colors_ht)))

# ======================
# ادامه کد رسم (بدون تغییر نسبت به قبل)
# ======================
# ======================
# موقعیت
# ======================
x = np.arange(len(years)) * 2.5
width = 0.4

fig, ax = plt.subplots(figsize=(10,9))

# برای legend جدا
legend_e = {}
legend_h2 = {}
legend_ht = {}

# ======================
# رسم
# ======================
for i, year in enumerate(years):
    for j, cat in enumerate(categories):
        xpos = x[i] + (j - 1) * width * 1.2

        bottom = 0
        for tech, value in data[year][cat].items():
            bar = ax.bar(
                xpos,
                value,
                width,
                bottom=bottom,
                color=colors[tech],
                edgecolor='black',
                linewidth=0.3
            )

            # ذخیره برای legend جدا
            if cat == 'Electricity' and tech not in legend_e:
                legend_e[tech] = bar
            elif cat == 'H2' and tech not in legend_h2:
                legend_h2[tech] = bar
            elif cat == 'Heating' and tech not in legend_ht:
                legend_ht[tech] = bar

            bottom += value

# ======================
# محور x
# ======================
all_positions = []
all_labels = []

for i, year in enumerate(years):
    for j, cat in enumerate(categories):
        xpos = x[i] + (j - 1) * width * 1.3
        all_positions.append(xpos)
        all_labels.append(cat)

ax.set_xticks(all_positions)
ax.set_xticklabels(all_labels, rotation=90,  fontsize=14)

# سال‌ها
for i, year in enumerate(years):
    ax.text(
        x[i],
        -0.2 * ax.get_ylim()[1],
        
        year,
        ha='center',
        va='top',
        fontsize=16,
        fontweight='bold'
    )

# ======================
# legend های جدا (حرفه‌ای)
# ======================
leg1 = ax.legend(
    [legend_e[k][0] for k in legend_e],
    legend_e.keys(),
    title='Electricity',
    loc='upper right',
    bbox_to_anchor=(1.28, 0.8),
    fontsize=11,
    frameon=False
)
leg1.get_title().set_fontweight('bold')
leg2 = ax.legend(
    [legend_h2[k][0] for k in legend_h2],
    legend_h2.keys(),
    title='H2', 
    loc='upper right',
    bbox_to_anchor=(1.24, 0.35),
    fontsize=11,
    frameon=False
)
leg2.get_title().set_fontweight('bold')
leg3 = ax.legend(
    [legend_ht[k][0] for k in legend_ht],
    legend_ht.keys(),
    title='Heating',
    loc='upper right',
    bbox_to_anchor=(1.25, 0.15),
    fontsize=11,
    frameon=False
)
leg3.get_title().set_fontweight('bold')
ax.add_artist(leg1)
ax.add_artist(leg2)

# ======================
# استایل
# ======================
ax.set_ylabel('Installed capacity (GW)', fontsize=18,fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
#%%
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'

# Years for the x-axis
years = [2030, 2035, 2040, 2045, 2050]

# Replace these lists with your actual data for each technology
data = {
    "CCGTCCS": [33, 39, 53, 60,60],
    "CCGT": [15, 16.5, 9, 5, 0],
    "H2CCGT": [0.5, 0.5, 1, 1,1],
    "LeadBat": [10, 17, 21, 24, 39],
    "Nuclear": [124, 130, 145, 160, 168],
    "Solar": [55, 70, 70, 73, 89],
    "WindOff": [130, 185, 225, 236, 241],
    "WindOn": [47, 63, 78, 93, 108],
    "Hydro": [5, 5, 5, 5, 5]
}

# Define colors to match your image as closely as possible
colors = [
    "#FF0000", # CCGTCCS - Grey
    "#8b0000", # CCGT - Black
    "#8000FF", # H2CCGT - Orange
    "#00FFFF", # LeadBat - Red/Coral
    "#0000FF", # Nuclear - Purple
    "#FFFF00", # Solar - Yellow
    "#228b22", # WindOff - SeaGreen
    "#00FF00", # WindOn - LightGreen
    "#1F77B4"  # Hydro - Blue
]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Stackplot generates the filled areas
ax.stackplot(years, data.values(), labels=data.keys(), colors=colors)

# Formatting the visual elements
#ax.set_title("Projected Energy Generation (TWh)")
ax.set_ylabel("Electricity Generation (TWh)", fontsize=16, fontweight='bold')
ax.set_xlabel("Year", fontsize=16, fontweight='bold')
ax.set_xlim(2030, 2050)
ax.set_xticks(years)
ax.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Move the legend to the bottom and arrange in columns
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False, fontsize=13)

plt.tight_layout()
plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
plt.rcParams['font.family'] = 'Serif'

# -----------------------------
# Data
# -----------------------------

tech = ["Wind onshore", "Wind offshore", "Solar", "Battery", "Nuclear", "Gas", "H2CCGT", "Biomass"]

phos = [35, 83, 70, 50, 30, 30, 49, 2]

Wind_on  = [30,35,37,50]
Wind_off = [75, 90, 93, 104]
Solar    = [52, 62, 90, 101]
Battery    = [27, 30, 33, 40]
Nuclear    = [10, 12, 20, 27]
Gas    = [0,20,33,50]
H2CCGT    = [17,30,45,55]
Biomass    = [1,1,2,5]

scenario_data = [Wind_on, Wind_off, Solar, Battery, Nuclear, Gas, H2CCGT, Biomass]

# -----------------------------
# Plot
# -----------------------------

fig, ax = plt.subplots(figsize=(9,5))

x = np.arange(len(tech))

box = ax.boxplot(
    scenario_data,
    positions=x-0.15,
    widths=0.25,
    patch_artist=True,
    showfliers=False
)

# All boxes same color
for patch in box['boxes']:
    patch.set_facecolor("#2CB9FF")
    patch.set_alpha(0.7)
    patch.set_edgecolor("black")

for median in box['medians']:
    median.set_color("black")

# -----------------------------
# Mean of scenarios
# -----------------------------



# -----------------------------
# PHOS bars
# -----------------------------

ax.bar(
    x+0.2,
    phos,
    width=0.35,
    color="#F28E2B",
    edgecolor="black",
    linewidth=1.5
)

# -----------------------------
# Labels
# -----------------------------

ax.set_ylabel("Capacity (GW)", fontsize=16)
ax.set_xlabel("Technology", fontsize=16)

ax.set_xticks(x)
ax.set_xticklabels(tech)

# -----------------------------
# Legend
# -----------------------------

legend_elements = [

    Patch(facecolor="#2CB9FF",
          edgecolor="black",
          label="FES scenario range"),

    Line2D([0],[0],
           color="black",
           lw=3,
           label="Mean of FES scenarios"),

    Patch(facecolor="#F28E2B",
          edgecolor="black",
          label="PHOS-UK result")
]

ax.legend(handles=legend_elements, frameon=False)

# -----------------------------
# Style
# -----------------------------

ax.grid(axis="y", linestyle="--", alpha=0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()