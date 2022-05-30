# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 13:54:33 2022

@author: engen
"""

import numpy as np
import matplotlib.pyplot as plt

mat = {
    'SA-516-70':    {'temp':40, 'e_y':200e+9, 's_ys':260e+6, 's_uts':483e+6, 'e_ys':0.002, 'e_p':2e-5},
    'SA-240 TP304': {'temp':40,'e_y':200e+9, 's_ys':275e+6, 's_uts':483e+6, 'e_ys':0.002, 'e_p':2e-5},

}

class AsmeCurves:

    def true_stress_strain_curve_aco(mat_asme, flag):

        e_y =   mat[mat_asme]['e_y']
        s_ys =  mat[mat_asme]['s_ys']
        s_uts = mat[mat_asme]['s_uts']
        e_ys =  mat[mat_asme]['e_ys']
        e_p =   mat[mat_asme]['e_p']
        r = s_ys/s_uts
        m2 = 0.6*(1-r)
        s_utst = s_uts*np.exp(m2)
        s_t =np.linspace(0.1,s_utst,20)   
        k = (1.5*r**1.5)-(0.5*r**2.5)-(r**3.5)
        h = 2*(s_t-(s_ys+k*(s_uts-s_ys)))/(k*(s_uts-s_ys))
        m1 = (np.log(r)+(e_p-e_ys))/(np.log(np.log(1+e_p)/np.log(1+e_ys)))   
        a1 = s_ys*(1+e_ys)/(np.log(1+e_ys))**m1
        a2 = s_uts*np.exp(m2)/(m2**m2)
        e1 = (s_t/a1)**(1/m1)
        e2 = (s_t/a2)**(1/m2)
        y1 = (e1/2)*(1+np.tanh(h))
        y2 = (e2/2)*(1+np.tanh(h))  
        e_t = (s_t/e_y)+y1+y2
        
        if not flag:
            plt.ylabel('Stress')
            plt.xlabel('Strain')
            plt.title(mat_asme)
            plt.plot(e_t,s_t)
            plt.show()

        if flag:
            np.savetxt('true_stress_strain_curve_'+mat_asme+'.txt', np.column_stack([e_t, s_t]), delimiter=' ', fmt='%s')

    def local_failure_strain_limit():
        s1 =  -5.5862e+6
        s2 =  -48.137e+6
        s3 =  -373.38e+6
        se =   348.47e+6
        ep =   0.1038
        s_ys = 207e+6
        s_uts =517e+6
        r =    s_ys/s_uts
        m2 =   0.75*(1-r)
        asl =  0.6
        elu =  m2
        el =   elu*2.71828**(-(asl/(1+m2))*abs(((s1+s2+s3)/(3*se))-1/3))
        sld =  ep/el
        
        
        lines = [
            '     --------------------------------------',
            '     TENSÕES E DEFORMAÇÕES (Análise FEA)',
            '     --------------------------------------',
            f'     Tensão principal máxima (S1)         = {s1/1e+6} MPa', 
            f'     Tensão principal média  (S2)         = {s2/1e+6} MPa',
            f'     Tensão principal mínima (S3)         = {s3/1e+6} MPa',
            f'     Tensão equivalente (Se)              = {se/1e+6} MPa',
            f'     Deformação plástica equivalente (ep) = {round(ep,3)} mm/mm',
            '     ----------------------------------------------------------------',
            '     LIMITE DE DEFORMAÇÃO TRIAXIAL (ASME Sec. VIII Div. 2, eq. 5.6)' ,
            '     ----------------------------------------------------------------',
            f'     Relação tensão escoamento/ruptura (R)  = {round(r,3)}',
            f'     Constante de material (m2 -> Aço inox) = {round(m2,3)} mm/mm',
            f'     Fator de material (asl -> Aço inox)    = {round(asl,3)}',               
            f'     Deformação Uniaxial (eLU)              = {round(elu,3)} mm/mm',
            f'     Limite de Deformação Triaxial (eL)     = {round(el,3)} mm/mm',
            '     ----------------------------------------------------------------',
            '     MÁXIMO DANO DE DEFORMAÇÃO' ,
            '     ----------------------------------------------------------------',
            f'     Dano de Deformação (De = eL/ep)        = {round(sld,2)}',
 
             '    ----------------------------------------------------------------',
            f'     Ansys equation --> copy the text below and paste on Ansys user define output',
            '     ----------------------------------------------------------------',
            f'      EPPLEQV_RST/({elu}*2,71828**({-asl/(1+m2)}*abs((s1+s2+s3)/(3*seqv)-1/3)))'
        ]
        
        with open ('SAIDA.txt', 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')
        
        return el, sld













