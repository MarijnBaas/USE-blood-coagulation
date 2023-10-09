#import relevant libraries
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
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
def model(t, y):
    c_c, c_p = y
    input_t = dosed_i / v_c if t == td else 0.0
    dCc_dt = input_t + q * (c_p / v_p - c_c / v_ci) - c_l / v_ci * c_c
    dCp_dt = q * (c_c / v_ci - c_p / v_p)
    return [dCc_dt, dCp_dt]

initial_conditions = [dosed_i / v_c, 0.0]
t_span = (0.0, 25.0)

sol = solve_ivp(model, t_span, initial_conditions, t_eval=np.linspace(0.0, 25.0, 100))

t = sol.t
c_c = sol.y[0]
c_p = sol.y[1]


plt.plot(t, c_c/1000, label='c_c')
plt.plot(t, c_p/1000, label='c_p')
plt.xlabel('Time (h)')
plt.ylabel('Anti-factor Xa activity (IU/mL)')
plt.legend()
plt.show()

#calculate ACT values
ACT0 = 116.0  
Emax = 720.0  
C50 = 3490

ACT = ACT0 + (Emax * c_c) / (C50 + c_c)

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




