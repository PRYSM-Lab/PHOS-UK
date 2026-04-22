# PHOS-UK
PHOS-UK is a Graphical User Interface (GUI) tool,  developed for examining integrated heat and power decarbonisation, through electrification, hydrogen and hybrid pathways in the United Kingdom. It allows users to configure model settings, select optimisation approaches, prepare input data, and execute simulations. At current stage of development, PHOS-UK can be executed using different optimisation approaches:

•	Deterministic optimisation  (Hydrogen and power)
•	Two-stage stochastic optimisation (Hydrogen only)
•	(Adapative) Robust optimisation (Hydrogen only)

These approaches enable users to analyse the system under different levels of uncertainty.
 

### Deterministic Optimisation
In deterministic optimisation, all parameters such as demand, renewable generation, and fuel costs are assumed to be known with certainty.

### Two-stage stochastic optimisation
In two-stage stochastic optimisation, uncertainty is explicitly represented through multiple scenarios. These scenarios may represent variations in renewable availability, energy demand, or other uncertain parameters.
    The stochastic formulation is implemented using two-stage stochastic programming.Scenario generation and reduction is be performed using the SCENREDPY tool. The Fast Forward Selection (FFS) algorithm is used to reduce the number of scenarios while preserving the statistical properties of the original dataset.

### Robust Optimisation
Robust optimisation considers uncertainty using predefined uncertainty sets. In PHOS-UK, uncertainty can be represented using a polyhedron uncertainty set.
Two robust approaches are considered:
•	Static robust optimisation
•	Adaptive robust optimisation
After selecting the optimisation method and preparing the input data, the model can be solved using an optimisation solver. The optimisation model is formulated as a Mixed-Integer Linear Programming (MILP) problem.
_______ 

Users can run the model either:
•	locally on their machine, or
•	using the NEOS optimisation server.
The user may specify the optimality gap as a termination criterion for the solver.



# Running PHOS-UK using the GUI
This section describes the step-by-step procedure to run the PHOS-UK model using the GUI. 
Step 0 – Install PHOS-UK
First, install the PHOS-UK system from the official repository as follows:
 
Step 1 – Install Required Python Packages
Before running the model, install all required Python dependencies.
The required packages are listed in the file: Requirement.txt

Step 2 – Run the PHOS-UK Script
Run the main PHOS-UK script as follows: PHOS-UK.py
 
This will start the graphical user interface like the following window:
In this step, user must select the decarbonisation pathway through hydrogen led decarbonisation or hybrid approach. 
 
Step 3 – Select Optimisation Method: Decarbonisation through Hydrogen
After launching the GUI, and selecting the decarbonisation pathway, the user must select the optimisation method through the next panel as follows
 

Available options include:
•	Deterministic
•	Stochastic
•	Robust
Step 4 – Select Model Architecture: Deterministic Approach 
By selecting the deterministic approach, the PHOS-UK framework supports multiple solution architectures that integrated optimisation techniques for reducing time-solving. It should be noted that the hyperlink provided in the panel direct the user to the associated reference published by our team. 
•	Monolithic
•	Hierarchical 1
•	Hierarchical 2
 
Step 5 – Provide Input Data
The GUI requires input data files depending on the selected optimisation method.
Examples of input files include:
•	Deterministic model: InputDeterministic.xlsx
•	Stochastic model: InputStochastic.xlsx
•	Robust model: InputRobust.xlsx
•	Hybrid model: InputDataForHybrid.xlsx
 
Step 6 – Configure Representative Days
Users can specify the number of representative days used in the model.
The GUI provides tools to generate representative days based on clustering techniques.
The clustering algorithm is implemented in:
kmedoid.py
This script performs k-medoids clustering to identify representative days.
 



Step 7 – Choose Solver
The optimisation problem can be solved using local and NEOS server as follows:
•	Local solver
•	NEOS server
 
Local Solver
If the local option is selected, the model will be solved using the installed optimisation solver on the user's machine as follows:
 
NEOS Server
If the NEOS option is selected, the optimisation model will be submitted to the NEOS server.
The user must choose a solver (e.g., CPLEX) and provide an email address for receiving the results as follows:
 
5. Output Results
After the optimisation process finishes, the results will be generated and saved. The GUI allows users to visualise model outputs and analyse system performance under different scenarios.

Selecting the Stochastic Method
When the stochastic optimisation method is selected as follows:
 
A MILP sub-problem is solved to determine the duration slices. The user can solve this sub-problem for any number of slices between 0 and 24.
 
It should be noted that increasing the number of slices increases:
•	Number of variables in the optimisation problem
•	Computational complexity
•	Overall solution time
Running the Fast Forward Selection Algorithm
At this stage, the user can select the desired number of scenarios. The Fast Forward Selection (FFS) algorithm is used to reduce the number of scenarios generated by the stochastic model. Initially, more than 1000 scenarios may be produced. Using FFS, the user can reduce this large scenario set to a smaller number of representative scenarios. The algorithm selects the most representative scenarios while recalculating and assigning the probability of occurrence for each selected scenario. In this panel user must input the number of desirable scenarios for running the stochastic method as follows:
 
The remaining steps for solving the optimisation problem follow the same procedure described in Steps 4 to 6.
     
# General Comments
All modelling approaches implemented in PHOS-UK follow the procedures described in the previous steps. By executing the code and entering the required information in the corresponding fields, users can easily run the different models available in the framework.
     It should be noted that each model can also be executed independently, and it is not strictly necessary to run the main general file. Each model file contains a detailed description of the optimisation formulation, including the objective function, constraints, and other modelling components.
    The authors are available to provide further guidance and support to users in case of any questions regarding the execution of the models.

