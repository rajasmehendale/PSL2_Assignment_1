import numpy as np
import conversion_models as CM
import matplotlib.pyplot as plt
### Importing the RTD calculation file

#import curve_fitting_code
from curve_fitting_code import std_dev, t_mean
plt.savefig('rtd data plot.pdf')
print("\nMean Residence time is % .3f " %(t_mean) + "minutes")
print("Variance is % .3f " %(std_dev) + "minutes^2")

conv_mod = CM.conversion_models()

conv_mod.sigma_sq = std_dev
conv_mod.t_mean = t_mean

## Checking the variations in conversions
## by various models with changes in rate constant
k_min = 0.001
k_max = 1.2
steps = 2000

k_range = np.linspace(k_min,k_max,steps)
x_cvdm            = np.zeros((len(k_range),1))
x_ideal_pfr       = np.zeros((len(k_range),1))
x_tanks_in_series = np.zeros((len(k_range),1))
x_single_cstr     = np.zeros((len(k_range),1))




for i in range(0,len(k_range)):
    conv_mod.k= k_range[i]
    x_cvdm[i]             = conv_mod.closed_vessel_dispersion()
    x_ideal_pfr[i]        = conv_mod.ideal_pfr()
    x_tanks_in_series[i]  = conv_mod.tanks_in_series()
    x_single_cstr[i]      = conv_mod.single_cstr()
    
## Plotting the results    
plt.figure()
plt.plot(k_range,x_ideal_pfr,'b',label = "Ideal PFR",linewidth=0.8)
plt.plot(k_range,x_cvdm,'r',label = "Closed Vessel\nDispersion Model",linewidth=0.8)
plt.plot(k_range,x_tanks_in_series,'g',label = "Tanks in Series",linewidth=0.8)
plt.plot(k_range,x_single_cstr,'k',label = "Single CSTR",linewidth=0.8)
title_aaa = "Variation of Conversion with rate constant k\n"
title_aab=  "for this Reactor for the reaction "
title_aac = r"$A \rightarrow B$"
plt.title(title_aaa+title_aab+title_aac)
plt.legend(loc="best")
plt.xlabel("k " +r"$[{(min)}^{-1}]$")
plt.ylabel("Conversion "+ r"($X_{A}$)")
plt.xlim([0, k_max])
plt.ylim([0, 1])
plt.savefig('conversion plot.pdf')
#plt.savefig('conversion plot.png',dpi = 4000)