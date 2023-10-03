import numpy as np
from scipy.integrate import solve_ivp

# Define the parameters
Vc_baseline = 3.1  # Baseline volume of distribution (mL/kg)
Vp = 2.23  # Volume of the peripheral compartment
Q = 4.67   # Flow rate between compartments
Cl = 0.841  # Clearance rate from the central compartment
Dosed = 25000.0  # Dose administered
td = 0  # Time of dosing
B_vc_bw = 1.02 #regression coefficient fo body weight on Vc
bw_i = 70 #body weight of the patient
wi_vc = 0 #random effect of patient

def define_vci(Vc_baseline, B_vc_bw, bw_i, wi_vc):
    log_Vci = Vc_baseline + B_vc_bw * np.log(bw_i / 70.0) + wi_vc
    Vci = np.exp(log_Vci)
    
    return Vci

Vci = define_vci(Vc_baseline, B_vc_bw, bw_i, wi_vc)
print(Vci)
Vci = 3.1

# Define the differential equations
def model(t, y):
    Cc, Cp = y
    input_t = Dosed / Vci if t == td else 0.0
    dCc_dt = input_t + Q * (Cp / Vp - Cc / Vci) - Cl / Vci * Cc
    dCp_dt = Q * (Cc / Vci - Cp / Vp)
    return [dCc_dt, dCp_dt]

# Initial conditions
initial_conditions = [Dosed / Vci, 0.0]

# Time span
t_span = (0.0, 10.0)  # Adjust the end time as needed

# Solve the differential equations
sol = solve_ivp(model, t_span, initial_conditions, t_eval=np.linspace(0.0, 10.0, 100))

# Extract the results
t = sol.t
Cc = sol.y[0]
Cp = sol.y[1]

# Plot the results (you can use matplotlib for this)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(t, Cc, label='Cc')
plt.plot(t, Cp, label='Cp')
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.legend()
plt.grid()
plt.show()