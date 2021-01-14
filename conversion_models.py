import numpy as np
from scipy.optimize import fsolve

class conversion_models:
    d= 10.0/100.0 # diameter in meters
    length  =6.36 #meters
    k = 0.25 # (min)^-1
    sigma_sq = 6.15 #minutes^2
    t_mean = 5.1  #minutes
    
    
    def closed_vessel_dispersion(self):
        d = self.d
        length = self.length
        k = self.k
        sigma_sq = self.sigma_sq
        t_mean = self.t_mean
        def pec_solv(x):
            return (sigma_sq)/(t_mean**2) - (2/(x**2))* (x - 1 + np.exp(-x))
        pe_r = fsolve(pec_solv, 10)
        da1 = t_mean*k
        q = np.sqrt(1 + (4*da1)/pe_r)
        per_q_by_2 = pe_r*q/2.0
        nr = (4*q*np.exp(pe_r/2.0))
        dr = ((1+q)**2*np.exp(per_q_by_2)) - (1-q)**2 * np.exp(-per_q_by_2)
        x_cvdm = 1  - nr/dr

        return x_cvdm


    def ideal_pfr(self):
        k = self.k
        t_mean = self.t_mean
        da1 = t_mean*k
        x_pfr = 1  - np.exp(-da1)
        return x_pfr
    
    def tanks_in_series(self):
        k = self.k
        sigma_sq = self.sigma_sq
        t_mean = self.t_mean
        n = (t_mean**2) / sigma_sq
        da_mod = t_mean*k/n
        dr = np.power((1+da_mod),n)
        x_tis = 1 - 1/dr

        return x_tis
    
    def single_cstr(self):
        k = self.k
        sigma_sq = self.sigma_sq
        t_mean = self.t_mean
        n = 1
        da_mod = t_mean*k/n
        dr = np.power((1+da_mod),n)
        x_single_cstr= 1 - 1/dr

        return x_single_cstr