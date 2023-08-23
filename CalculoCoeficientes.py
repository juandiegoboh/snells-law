# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:16:14 2022

@author: Juan Diego Bohórquez
"""

import numpy as np
from CalculoSnell import CalculoSnell

class CalculoCoeficientes(CalculoSnell):
    '''
    Clase que hereda de la clase CalculoSnell, genera los calculos correspondientes a los coeficientes de reflexión y de transmisión para onda P y S en incidencia vertical (90). Calcula también las tasas de flujo de energía transmitida y reflejada con respecto a la incidente. 
    '''
    # Clase que hereda de CalculoSnell
    def __init__(self, incidente, alpha1, beta1, alpha2, beta2, tipo, rho1, rho2):
        super().__init__(incidente, alpha1, beta1, alpha2, beta2, tipo)
        self.rho1 = rho1
        self.rho2 = rho2
        self.coef_reflexion, self.coef_reflexion_r = self.calculo_reflexion()
        self.coef_transmision, self.coef_transmision_r = self.calculo_transmision()
        self.ratio_energia_ref, self.ratio_energia_trans = self.calculo_energia()
    
    def __str__(self):
        incidente = f"Onda incidente: {self.tipo}"
        coef_T_R = f"Coeficiente T12: {self.coef_transmision}\nCoeficiente R12: {self.coef_reflexion}"
        coef_T_R_r = f"Coeficiente T21: {self.coef_transmision_r}\nCoeficiente R21: {self.coef_reflexion_r}"
        flujo_e = f"Flujo de energia reflejada ER/EI: {self.ratio_energia_ref}\nFlujo de energia transmitida ET/EI: {self.ratio_energia_trans}"
        
        return f"{incidente}\n\nIncidencia del medio 1 a 2\n{coef_T_R}\n\nIncidencia del medio 2 a 1\n{coef_T_R_r}\n\nFlujo de energía\n{flujo_e}"
    
    def calculo_reflexion(self):
        if self.tipo == 'P':
            # R12
            num_R = (self.rho1*self.alpha1 - self.rho2*self.alpha2)
            denom_R = (self.rho1*self.alpha1 + self.rho2*self.alpha2)
            R12 = num_R/denom_R
            
            num_R = (self.rho2*self.alpha2 - self.rho1*self.alpha1)
            denom_R = (self.rho2*self.alpha2 + self.rho1*self.alpha1)
            R21 = num_R/denom_R
            
        elif self.tipo == 'S':
            # R12
            num_R = (self.rho1*self.beta1 - self.rho2*self.beta2)
            denom_R = (self.rho1*self.beta1 + self.rho2*self.beta2)
            R12 = num_R/denom_R
            
            # R21
            num_R = (self.rho2*self.beta2 - self.rho1*self.beta1)
            denom_R = (self.rho2*self.beta2 + self.rho1*self.beta1)
            R21 = num_R/denom_R
            
        R12, R21 = round(R12,3), round(R21,3)
            
        return R12, R21
    
    
    def calculo_transmision(self):
        if self.tipo == 'P':
            # T12
            num_T = (2*self.rho1*self.alpha1)
            denom_T = (self.rho1*self.alpha1+self.rho2*self.alpha2)
            T12 = num_T/denom_T

            # T21
            num_T = (2*self.rho2*self.alpha2)
            denom_T = (self.rho2*self.alpha2+self.rho1*self.alpha1)
            T21 = num_T/denom_T
            
        elif self.tipo == 'S':
            # T12
            num_T = (2*self.rho1*self.beta1)
            denom_T = (self.rho1*self.beta1+self.rho2*self.beta2)
            T12 = num_T/denom_T
            
            # T21
            num_T = (2*self.rho2*self.beta2)
            denom_T = (self.rho2*self.beta2+self.rho1*self.beta1)
            T21 = num_T/denom_T
            
        T12, T21 = round(T12,3), round(T21,3)
        
        return T12, T21
    
    
    def calculo_energia(self):
        if self.tipo == 'P':
            numerador = (self.rho2*self.alpha2)
            denominador = (self.rho1*self.alpha1)
            energy_ratio_trans = (self.coef_transmision**2)*(numerador/denominador)
            
        elif self.tipo == 'S':
            numerador = (self.rho2*self.beta2*np.cos(self.rad_s_trans))
            denominador = (self.rho1*self.beta1*np.cos(self.rad_inc))
            
            energy_ratio_trans = (self.coef_transmision**2)*(numerador)/(denominador)
            
        energy_ratio_ref = self.coef_reflexion**2
            
        return round(energy_ratio_ref,4), round(energy_ratio_trans,4)
