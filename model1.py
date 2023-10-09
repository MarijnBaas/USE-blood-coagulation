#import relevant libraries
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel('Dataset Xa vs ACT goed.xlsx')
Anti_Xa = list(data['Antifactor Xa (IU/mL)'])
ACT_data = list(data['ACT (s)'])


# Define the parameters for the model
v_c_baseline = 3.1 
v_c = 3.1 
v_p = 2.23 
q = 4.67   
c_l = 0.841  
dosed_i = 30000.0  
dosed_d = 0
td = 1 
b_vc_bw = 1.02 
bw_i = 77.5 
wi_vc = 0

#calculate patient specific central volume through bodyweight
def patient_vci(v_c_baseline, b_vc_bw, bw_i, wi_vc):
    v_ci = v_c_baseline + b_vc_bw * np.log10(bw_i / 70.0) + wi_vc
    return v_ci

v_ci = patient_vci(v_c_baseline, b_vc_bw, bw_i, wi_vc)

#solve the differential equations through solve_ivp
def pk_model(y, t, dose_i, dose_d, t_d, v_c, v_p, q, cl):
    c_c, c_p = y
    input_t = dose_d / v_c if t % t_d == 0 else 0
    dc_c_dt = input_t + q * (c_p / v_p - c_c / v_c) - (cl / v_c) * c_c
    dc_p_dt = q * (c_c / v_c - c_p / v_p)

    return [dc_c_dt, dc_p_dt]

initial_conditions = [dosed_i / v_c, 0.0]
t = np.linspace(0, 25, 100)

y = odeint(pk_model, initial_conditions, t, args=(dosed_i, dosed_d, td, v_c, v_p, q, c_l))

c_c = y[:, 0]
c_p = y[:, 1]
initial_conditions = [dosed_i / v_c, 0.0]

plt.plot(t, c_c/1000, label='c_c')
plt.plot(t, c_p/1000, label='c_p')
plt.xlabel('Time (h)')
plt.ylabel('Anti-factor Xa activity (IU/mL)')
plt.legend()
plt.show()

#calculate ACT values
ACT0 = 116.0  
Emax = 600.0  
C50 = 3490
def ACT(ACT0, Emax, C50, c_c):
    """This function calculates the ACT values."""
    ACT = ACT0 + (Emax * c_c) / (C50 + c_c)
    return ACT

ACT = ACT(ACT0, Emax, C50, c_c)

plt.plot(t, ACT, label='ACT', color='red')
plt.xlabel('Time (h)')
plt.ylabel('ACT (s)')
plt.legend()
plt.show()

plt.plot(c_c/1000, ACT)
plt.scatter(Anti_Xa, ACT_data, s=5, color='red')
plt.yticks(np.arange(0, 1100, step=250))
plt.xlabel('Anti-factor Xa activity (IU/mL)')
plt.ylabel('ACT (s)')
plt.title('ACT vs Xa activity')
plt.show()




