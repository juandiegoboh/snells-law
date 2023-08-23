# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 13:48:31 2022

@author: Juan Diego Bohórquez
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

class CalculoSnell:
    '''
    Clase que genera los calculos correspondientes a la ley de Snell para reflexión y transmisión de onda P y S dada una onda incidente de cualquier tipo.
    '''
    def __init__(self, incidente, alpha1, beta1, alpha2, beta2, tipo):
        self.incidente = incidente
        self.alpha1 = alpha1
        self.beta1 = beta1
        self.alpha2 = alpha2
        self.beta2 = beta2
        self.tipo = tipo.upper()
        self.rad_inc = self.angle_to_rad(incidente,6)
        # Atributos calculados
        self.ang_critico_p, self.ang_critico_s = self.calcular_angulo_critico()
        self.reflexion_crit = self.calcular_reflexion_crit()
        
        self.rad_s_ref, self.ang_s_ref, self.rad_p_ref, self.ang_p_ref = self.reflexion(self.rad_inc)
        self.rad_p_trans, self.ang_p_trans, self.rad_s_trans, self.ang_s_trans = self.transmision(self.rad_inc)


    def __str__(self):
        onda_i = f'Onda {self.tipo} incidente'
        angulo = f'Angulo incidente: {self.incidente}'
        reflexiones = f'Ángulo onda P reflejada: {self.ang_p_ref}\nÁngulo onda S reflejada: {self.ang_s_ref}'
        transmisiones =f'Ángulo onda P transmitida: {self.ang_p_trans}\nÁngulo onda S transmitida: {self.ang_s_trans}'
        angulo_critico = f'Ángulo crítico P transmitida: {self.ang_critico_p}\nÁngulo crítico S transmitida: {self.ang_critico_s}\nÁngulo crítico de reflexión: {self.reflexion_crit}'
        
        return f'{onda_i}\n{angulo}\n\nAngulos Críticos:\n{angulo_critico}\n\nReflexiones:\n{reflexiones}\n\nTransmisiones:\n{transmisiones}'


    def rad_to_angle(self, rads, rounded=3):
        angles = round(rads*180/np.pi,rounded)
        return angles


    def angle_to_rad(self, angle, rounded=3):
        rads = round(angle*np.pi/180,rounded)
        return rads
        
        
    def calcular_reflexion_crit(self):
        beta1_over_alpha1 = (self.beta1/self.alpha1)
        
        # Pueden haber reflexiones mayores a 90 de onda S incidente
        if self.tipo == 'S':
            if self.alpha1 > self.beta1:
                rad_crit = np.arcsin(beta1_over_alpha1)
                ang_crit = self.rad_to_angle(rad_crit,4)
            else:
                ang_crit = "No existe"
        else:
            ang_crit = "No existe"
            
        return ang_crit       


    def reflexion(self, rad_inc):
        post_text = 'Postcrítico'
        beta1_over_alfa1 = (self.beta1/self.alpha1)
        alpha1_over_beta1 = (self.alpha1/self.beta1)
        
        angle_s = np.sin(rad_inc)*(beta1_over_alfa1)
        angle_p = np.sin(rad_inc)*(alpha1_over_beta1)
        
        if self.tipo == 'P':
            rad_p_ref = np.float64(rad_inc)
            ang_p_ref = self.rad_to_angle(rad_p_ref)
            
            rad_s_ref = np.arcsin(angle_s)
            ang_s_ref = self.rad_to_angle(rad_s_ref)
            
        # En una onda incidente S puede haber reflexion critica de onda P
        elif self.tipo == 'S':  
            rad_s_ref = rad_inc
            ang_s_ref = self.rad_to_angle(rad_s_ref)
            
            # Comprobar que el angulo existe
            if angle_p < 1:    
                rad_p_ref = np.arcsin(angle_p)
                ang_p_ref = self.rad_to_angle(rad_p_ref)
            else:
                rad_p_ref = ang_p_ref = post_text
        
        return rad_s_ref, ang_s_ref, rad_p_ref, ang_p_ref
    
    
    def transmision(self, rad_inc):
        post_text = 'Postcrítico'
        # Calculos transmisión - refracción
        alpha2_over_alpha1 = (self.alpha2/self.alpha1)
        beta2_over_alpha1 = (self.beta2/self.alpha1)
        alpha2_over_beta1 = (self.alpha2/self.beta1)
        beta2_over_beta1 = (self.beta2/self.beta1)
            
        if self.tipo == 'P':
            angle_p = np.sin(rad_inc)*(alpha2_over_alpha1)
            angle_s = np.sin(rad_inc)*(beta2_over_alpha1)
            
        elif self.tipo == 'S':
            angle_p = np.sin(rad_inc)*(alpha2_over_beta1)
            angle_s = np.sin(rad_inc)*(beta2_over_beta1)
            
        # Comprobar que el angulo existe
        if angle_p < 1 and angle_s < 1:    
            rad_p_trans = np.arcsin(angle_p)
            rad_s_trans = np.arcsin(angle_s)
            
        elif angle_p < 1:    
            rad_p_trans = np.arcsin(angle_p)
            rad_s_trans = ang_s_trans = post_text
            
        elif angle_s < 1: 
            rad_s_trans = np.arcsin(angle_s)
            rad_p_trans = ang_p_trans = post_text
        
        else:
            rad_s_trans = ang_s_trans = rad_p_trans = ang_p_trans = post_text

        if type(rad_p_trans) == np.float64:
            ang_p_trans = self.rad_to_angle(rad_p_trans)
        if type(rad_s_trans) == np.float64:
            ang_s_trans = self.rad_to_angle(rad_s_trans)
            
        return rad_p_trans, ang_p_trans, rad_s_trans, ang_s_trans
    
    
    def calcular_angulo_critico(self):
        if self.tipo == 'P':
            ang_crit_p, ang_crit_s = self.angulo_critico_p()
                
        elif self.tipo == 'S':
            ang_crit_p, ang_crit_s = self.angulo_critico_s()
            
        return ang_crit_p, ang_crit_s
    
    
    def angulo_critico_p(self):
        '''
        Calculo de angulo crítico para onda incidente p

        '''
        if self.alpha2 > self.alpha1:
        # Angulo critico P
            rad_crit_p = np.arcsin(self.alpha1/self.alpha2)
            ang_crit_p = self.rad_to_angle(rad_crit_p,4)
        else:
            ang_crit_p = self.mensaje_critico(self.tipo, self.alpha1, self.alpha2) 

        if self.beta2 > self.alpha1:
        # Angulo critico S
            rad_crit_s = np.arcsin(self.alpha1/self.beta2)
            ang_crit_s = self.rad_to_angle(rad_crit_s,4)
        else:
            ang_crit_s = self.mensaje_critico('S', self.alpha1, self.beta2, True)      
        
        return ang_crit_p, ang_crit_s

    
    def angulo_critico_s(self):
        '''
        Calculo de angulo crítico para onda incidente s

        '''
        if self.alpha2 > self.beta1:
        # Angulo critico P
            rad_crit_p = np.arcsin(self.beta1/self.alpha2)
            ang_crit_p = self.rad_to_angle(rad_crit_p,4)
        else:
            ang_crit_p = self.mensaje_critico('P', self.beta1, self.alpha2, True)  
            
        if self.beta2 > self.beta1:
        # Angulo critico S
            rad_crit_s = np.arcsin(self.beta1/self.beta2)
            ang_crit_s = self.rad_to_angle(rad_crit_s,4)
        else:
            ang_crit_s = self.mensaje_critico(self.tipo, self.beta1, self.beta2) 
            
        return ang_crit_p, ang_crit_s
    
    
    def mensaje_critico(self, onda_inc, vel_medio1, vel_medio2, invertidas=False):
        if invertidas == True:
            if onda_inc == 'P':
                onda_invertida = 'S'
            elif onda_inc == 'S':
                onda_invertida = 'P'
        else:
            onda_invertida = onda_inc
                
        mensaje = f'No existe ángulo crítico de onda {onda_inc}. Velocidad de onda {onda_inc} del medio 2: {vel_medio2} es igual o menor a la velocidad de onda {onda_invertida} del medio 1: {vel_medio1}'
        
        return mensaje
    
    
    def plot_snell(self):        
        # Mensajes
        medio_1_text = rf'$\alpha_1$: {self.alpha1}' '\n' rf'$\beta_1$: {self.beta1}'
        medio_2_text = rf'$\alpha_2$: {self.alpha2}' '\n' rf'$\beta_2$: {self.beta2}'

        if self.tipo == 'P':
            color_i = 'r'
            ls_i = '-'
        else:
            color_i = 'b'
            ls_i = '--'

        # Creacion figura
        fig,ax = plt.subplots(figsize=(8,6))

        # Elementos de anotación
        ax.text(x=-0.97, y=0.94, s=f"{self.incidente}\u00b0", ha='left', va='center', c=color_i)

        ax.text(x=0.97, y=0.064, s=f"{self.ang_p_ref}\u00b0", ha='right', va='center', c='r')
        ax.text(x=0.97, y=0.154, s=f"{self.ang_s_ref}\u00b0", ha='right', va='center', c='b')

        ax.text(x=0.97, y=-0.154, s=f"{self.ang_p_trans}\u00b0", ha='right', va='center', c='r')
        ax.text(x=0.97, y=-0.064, s=f"{self.ang_s_trans}\u00b0", ha='right', va='center', c='b')

        # Interfaz de reflexión
        ax.axhline(y=0, color='k')
        ax.text(x=-0.95, y=0.12, s=medio_1_text, ha='left', va='center')
        ax.text(x=-0.95, y=-0.12, s=medio_2_text, ha='left', va='center')
        # Normal
        verticalx = np.array([0,0])
        verticaly = np.array([1,-1])
        ax.plot(verticalx,verticaly,c='gray',ls='--')
        
        # Incidente
        x_i = np.array([-2*np.sin(self.rad_inc),0])
        y_i = np.array([2*np.cos(self.rad_inc),0])
        ax.plot(x_i,y_i,c=color_i,ls=ls_i)
        
        # S - Reflejada
        x_s_r = np.array([2*np.sin(self.rad_s_ref),0])
        y_s_r = np.array([2*np.cos(self.rad_s_ref),0])
        ax.plot(x_s_r,y_s_r,c='b',ls='--')
        
        # P - Reflejada
        if type(self.rad_p_ref) == np.float64:
            x_s_r = np.array([2*np.sin(self.rad_p_ref),0])
            y_s_r = np.array([2*np.cos(self.rad_p_ref),0])
            ax.plot(x_s_r,y_s_r,c='r',ls='-')
        
        # P - Transmitida
        if type(self.rad_p_trans) == np.float64 and self.alpha2 != 0:
            x_p_t = np.array([2*np.sin(self.rad_p_trans),0])
            y_p_t = np.array([-2*np.cos(self.rad_p_trans),0])
            ax.plot(x_p_t,y_p_t,c='r',ls='-')
        # S - Transmitida
        if type(self.rad_s_trans) == np.float64 and self.beta2 != 0:
            x_s_t = np.array([2*np.sin(self.rad_s_trans),0])
            y_s_t = np.array([-2*np.cos(self.rad_s_trans),0])
            ax.plot(x_s_t,y_s_t,c='b',ls='--')

        ax.set_ylim(bottom=-1, top=1)
        ax.set_xlim(left=-1, right=1)
        ax.set_title(f'Onda {self.tipo} incidente')
        
        # Esconder los ejes X y Y
        plt.xticks([]) 
        plt.yticks([]) 
        
        # Leyenda
        custom_lines = [Line2D([0], [0], color='r', lw=2),
                        Line2D([0], [0], color='b', lw=2, ls='--')]

        ax.legend(custom_lines, ['Onda P', 'Onda S'], loc='lower left')
        
        plt.show()


    def plot_raypaths(self):
        # Angulos incidencia
        angles = np.arange(0,70,10)
        rads = [self.angle_to_rad(angle,4) for angle in angles]
        # Mensajes
        medio_1_text = rf'$\alpha_1$: {self.alpha1}, $\beta_1$: {self.beta1}'
        medio_2_text = rf'$\alpha_2$: {self.alpha2}, $\beta_2$: {self.beta2}'
        
        if self.tipo == 'P':
            color_i = 'r'
            ls_i = '-'
        else:
            color_i = 'b'
            ls_i = '--'
            
        # Creacion figura
        fig,ax = plt.subplots(figsize=(8,6))
        # Limites de los ejes
        xlims = [-1,1.5]
        ylims = [-1,1]
        # Limite de ondas reflejadas y transmitidas
        wave_ylimit = 0.4
        # Interfaz de reflexión
        ax.axhline(y=0, color='k')
        ax.text(x=xlims[1]-0.05, y=ylims[1]-0.1, s=medio_1_text, ha='right', va='center')
        ax.text(x=xlims[1]-0.05, y=ylims[0]+0.1, s=medio_2_text, ha='right', va='center')
        
        # Referencia del punto de origen
        x0 = -0.75
        y0 = 0.75
        for rad in rads:
            incidencia_x = (np.tan(rad)*y0)
            
            # Puntos originales de propagacion
            x_i = np.array([x0,x0+incidencia_x])
            y_i = np.array([0.75,0]) 
            
            ax.plot(x_i,y_i,c=color_i,ls=ls_i)
            
        # Reflejadas
        for rad in rads:
            if rad == 0: # No plotear ninguna reflexion para angulo 0
                continue
            
            # Onda P
            rad_s_ref, ang_s_ref, rad_p_ref, ang_p_ref = self.reflexion(rad)
            
            incidencia_x = (np.tan(rad)*y0)
            if type(rad_p_ref) == np.float64: # Si el angulo es postcritico no se plotea
                reflexion_x = (np.tan(rad_p_ref)*wave_ylimit)
                x00 = x0 + incidencia_x # Punto de partida de la reflexion
                x_i = np.array([x00, x00+reflexion_x])
                y_i = np.array([0,wave_ylimit])

                ax.arrow(x_i[0],0,reflexion_x,y_i[1],ls='-', shape='full',color='r', head_width=.015)
    
            # Onda S
            reflexion_x = (np.tan(rad_s_ref)*wave_ylimit)
            x00 = x0 + incidencia_x # Punto de partida de la reflexion
            x_i = np.array([x00, x00+reflexion_x])
            y_i = np.array([0,wave_ylimit])

            ax.arrow(x_i[0],0,reflexion_x,y_i[1],ls='--', shape='full',color='b', head_width=.015)
            
        # Transmitidas P
        for rad in rads:
            rad_p_trans, ang_p_trans, rad_s_trans, ang_s_trans = self.transmision(rad)
            
            incidencia_x = (np.tan(rad)*y0)
            if self.tipo == 'S' and rad == 0: # El angulo 0 solo se plotea si es la incidente   
                continue
            
            if type(rad_p_trans) == np.float64: # Si el angulo es postcritico no se plotea
                transmision_x = (np.tan(rad_p_trans)*wave_ylimit)
                x00 = x0 + incidencia_x # Punto de partida de la reflexion
                x_i = np.array([x00, x00+transmision_x])
                y_i = np.array([0,-wave_ylimit])
                
                ax.arrow(x_i[0],y_i[0],transmision_x,y_i[1],ls='-', shape='full',color='r', head_width=.015)
                
        # Transmitidas S
        for rad in rads:
            rad_p_trans, ang_p_trans, rad_s_trans, ang_s_trans = self.transmision(rad)
            
            incidencia_x = (np.tan(rad)*y0)
            if self.tipo == 'P' and rad == 0: # El angulo 0 solo se plotea si es la incidente   
                continue
            
            if type(rad_s_trans) == np.float64 and self.beta2 != 0: # Si el angulo es postcritico no se plotea
                transmision_x = (np.tan(rad_s_trans)*wave_ylimit)
                x00 = x0 + incidencia_x # Punto de partida de la reflexion
                x_i = np.array([x00, x00+transmision_x])
                y_i = np.array([0,-wave_ylimit])
            
                ax.arrow(x_i[0],y_i[0],transmision_x,y_i[1],ls='--', shape='full',color='b', head_width=.015)
        
        ax.set_ylim(bottom=ylims[0], top=ylims[1])
        ax.set_xlim(left=xlims[0], right=xlims[1])
        ax.set_title(f'Onda {self.tipo} incidente')
        
        # Esconder los ejes X y Y
        plt.xticks([]) 
        plt.yticks([])
        
        # Leyenda
        custom_lines = [Line2D([0], [0], color='r', lw=2),
                        Line2D([0], [0], color='b', lw=2, ls='--')]

        ax.legend(custom_lines, ['Onda P', 'Onda S'], loc='lower left')
        
        plt.show()
        