# Import numpy and scipy libraries
import numpy as np
from scipy.integrate import odeint

# Define the input function
def input(t):
    # Assume the heparin doses are given at time 0, 1, and 2 h
    if t == 0:
        return 300/3.1 # Initial bolus of 300 IU/kg divided by VC
    elif t == 1 or t == 2:
        return 5000/3.1 # Additional boluses of 5000 IU divided by VC
    else:
        return 0 # No input at other times

# Define the PK/PD model
def model(y, t, Q, Vp, Cl, ACT0, Emax, C50):
    Cc, Cp = y # Anti-factor Xa activities in central and peripheral compartments[^1^][1]
    dCc_dt = input(t) + Q*(Cp/Vp - Cc/Vc) - Cl/Vc * Cc # Change in central compartment
    dCp_dt = Q*(Cc/Vc - Cp/Vp) # Change in peripheral compartment
    ACT = ACT0 + (Emax*Cc)/(C50+Cc) # Activated clotting time
    return [dCc_dt, dCp_dt, ACT]

# Define the initial conditions and parameters
y0 = [0, 0, 116] # Initial anti-factor Xa activities and ACT
Q = 4.67 # Intercompartmental clearance (litres/h)
Vp = 2.23 # Peripheral volume of distribution (litres)[^2^][2]
Cl = 0.841 # Elimination clearance (litres/h)[^3^][3]
Vc = 3.1 # Central volume of distribution (litres)
ACT0 = 116 # Baseline ACT value (s)
Emax = 720 # Maximal response value (s)
C50 = 3.49 # Anti-factor Xa activity producing 50% of the maximal response value (IU/ml)[^4^][4]

# Define the time points
t = np.linspace(0, 6, 100) # Time from 0 to 6 h with 100 points

# Solve the differential equations
y = odeint(model, y0, t, args=(Q, Vp, Cl, ACT0, Emax, C50))

# Plot the results
import matplotlib.pyplot as plt
plt.plot(t, y[:,0], label='Cc') # Plot central compartment anti-factor Xa activity
plt.plot(t, y[:,1], label='Cp') # Plot peripheral compartment anti-factor Xa activity
plt.plot(t, y[:,2], label='ACT') # Plot activated clotting time
plt.xlabel('Time (h)')
plt.ylabel('Anti-factor Xa activity (IU/ml) or ACT (s)')
plt.legend()
plt.show()
