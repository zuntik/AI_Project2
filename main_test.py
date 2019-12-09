if __name__ == "__main__":
    import sys
    sys.path.append('./aima-python')

from probability import *

rs = ['R01','R02','R03']
P = 0.07549526619046759   

TPR = 0.942314
FPR = 0.121552

fire = BayesNet([
    (rs[0], '', 0.5),
    (rs[1], '', 0.5),
    (rs[2], '', 0.5),
    ('s', rs[2], {T:TPR, F:FPR}),
    (rs[0]+'_1', rs[0], {T:1,F:0}),
    (rs[1]+'_1', rs[1]+' '+rs[2], {(T, T):1, (T, F):1 ,(F, T ):P,(F, F):0}),
    (rs[2]+'_1', rs[2]+' '+rs[1], {(T, T):1, (T, F):1 ,(F, T ):P,(F, F):0}),
    ('s_1', rs[2]+'_1', {T:TPR, F:FPR}),
    (rs[0]+'_2', rs[0]+'_1', {T:1,F:0}),
    (rs[1]+'_2', rs[1]+'_1'+' '+rs[2]+'_1', {(T, T):1, (T, F):1 ,(F, T ):P,(F, F):0}),
    (rs[2]+'_2', rs[2]+'_1'+' '+rs[1]+'_1', {(T, T):1, (T, F):1 ,(F, T ):P,(F, F):0}),
    ('s_2', rs[2]+'_2', {T:TPR, F:FPR}),
    (rs[0]+'_3', rs[0]+'_2', {T:1,F:0}),
    (rs[1]+'_3', rs[1]+'_2'+' '+rs[2]+'_2', {(T, T):1, (T, F):1 ,(F, T ):P,(F, F):0}),
    (rs[2]+'_3', rs[2]+'_2'+' '+rs[1]+'_2', {(T, T):1, (T, F):1 ,(F, T ):P,(F, F):0}),
    ('s_3', rs[2]+'_3', {T:TPR, F:FPR})])
    

ev = {'s':False,'s_1':True,'s_2':True,'s_3':True}

#print(elimination_ask('R03_3', ev,fire).show_approx(numfmt='{:.10g}'))
print(elimination_ask('R03_3', ev,fire)[True])

