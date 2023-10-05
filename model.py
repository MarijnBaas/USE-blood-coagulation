import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

dose_i = 25000   # initial bolus dose of heparin in IU
dose_d = 5000  # multiple dose of heparin in IU
t_d = 0  # dosing interval in hours
v_c = 3.1  # volume of distribution of the central compartment in liters
v_p = 2.23  # volume of distribution of the peripheral compartment in liters
q = 4.67  # intercompartmental clearance in liters per hour
cl = 0.841  # elimination clearance in liters per hour

def pk_model(y, t, dose_i, dose_d, t_d, v_c, v_p, q, cl):
    c_c, c_p = y
    input_t = dose_d/ v_c if t == t_d else 0
    dc_c_dt = input_t + q * (c_p / v_p - c_c / v_c) - (cl / v_c) * c_c
    dc_p_dt = q * (c_c / v_c - c_p / v_p)

    return [dc_c_dt, dc_p_dt]

initial_conditions = [dose_d / v_c, 0.0]
t = np.linspace(0, 10, 100)

y = odeint(pk_model, initial_conditions, t, args=(dose_i, dose_d, t_d, v_c, v_p, q, cl))

c_c = y[:, 0]
c_p = y[:, 1]

plt.plot(t, c_c, label="Central")
plt.plot(t, c_p, label="Peripheral")
plt.xlabel("Time (hours)")
plt.ylabel("Anti-factor Xa activity (IU/ml)")
plt.title("Pharmacokinetic model of heparin")
plt.legend()
plt.show()

