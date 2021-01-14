import pandas as pd
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

#####
data = pd.read_excel("rtd_data.xlsx")#,header=None, index_col=None,names=None)
display(data)
rtd_data = data.to_numpy()

t  = rtd_data[:,0] ## minutes
conc = rtd_data[:,1] ## mg/L
no_of_data_points = len(t)
#t = t.reshape(no_of_data_points, 1)
#conc = conc.reshape(no_of_data_points, 1)

## splitting the rtd time in 2 parts
i=0
diff=-2
while diff<0:
    diff =conc[i+0]-conc[i+1]
    i+=1
    
t_head = t[0:i]
t_tail = t[(i-1):]
conc_head = conc[0:i]
conc_tail = conc[(i-1):]

#### fitting curves

c1 = np.polyfit(t_head,conc_head, 3)
c2 = np.polyfit(t_tail,conc_tail, 6)
####
def integrand1(x,c1):
    return c1[0]*x**3 + c1[1]*x**2 + c1[2]*x + c1[3]

def integrand2(x,c2):
    return c2[0]*x**6 +c2[1]*x**5 + c2[2]*x**4+ c2[3]*x**3 + c2[4]*x**2 + c2[5]*x + c2[6]

def integrand3(x,c1):
    return (c1[0]*x**3 + c1[1]*x**2 + c1[2]*x + c1[3])*x

def integrand4(x,c2):
    return (c2[0]*x**6 +c2[1]*x**5 + c2[2]*x**4+ c2[3]*x**3 + c2[4]*x**2 + c2[5]*x + c2[6])*x

def integrand5(x,c1,t_mean):
    return (c1[0]*x**3 + c1[1]*x**2 + c1[2]*x + c1[3])*(x-t_mean)**2

def integrand6(x,c2,t_mean):
    return (c2[0]*x**6 +c2[1]*x**5 + c2[2]*x**4+ c2[3]*x**3 + c2[4]*x**2 + c2[5]*x + c2[6])*(x-t_mean)**2


I1 = quad(integrand1, 0, t[i-1], args=(c1))   
I2 = quad(integrand2, t[i-1], t[-1], args=(c2))
I3 = quad(integrand3, 0, t[i-1], args=(c1))   
I4 = quad(integrand4, t[i-1], t[-1], args=(c2))  

area = I1[0] + I2[0]
t_mean = (I3[0] + I4[0])/area #minutes

I5 = quad(integrand5, 0, t[i-1], args=(c1,t_mean))   
I6 = quad(integrand6, t[i-1], t[-1], args=(c2,t_mean))
std_dev = (I5[0] + I6[0])/area #minutes^2    





####
pp = 100 ## plot points
plt.figure()
plt.scatter(t, conc, s=50, facecolors='k', marker='x', label = "Experimental Data")
plt.plot(np.linspace(0,t[i-1],pp),np.polyval(c1,np.linspace(0,t[i-1],pp)),'r',label = "fitted curve",linewidth=0.8)
plt.plot(np.linspace(t[i-1],t[-1],pp),np.polyval(c2,np.linspace(t[i-1],t[-1],pp)),'b',label = "fitted curve",linewidth=0.8)
plt.title("RTD Profile for a Tubular Reactor")
plt.legend(loc="best")
plt.xlabel("Time (t) (minutes)")
plt.ylabel("Concentration " + r"$(\frac{mg}{L})$")
plt.xlim([0, 16])
plt.ylim([-0.5, 12])
#plt.savefig('rtd data plot.pdf')



