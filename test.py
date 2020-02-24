import numpy as np
from itertools import combinations
from itertools import product
def get_inputs(n=10):

    max_x = 2.2
    max_y = 0.411

    origin = np.linspace(0,max_x*0.5,n)
    xs = np.linspace(0,max_x*0.25,n)
    ys = np.linspace(max_y*.25,max_y*0.75,n)
    cs = list(product(origin, xs, ys))

    return cs

def build_que_list(cmd_args):
    que_list = []
    for i,c in enumerate(cmd_args):
        oxy = ' '.join( map(str, c) )
        ex = f'./TMbstep2d {oxy} tmp/{i}'
        que_list.append(ex)
    return que_list

ql = build_que_list(get_inputs())
#ql = get_inputs()
print(ql)
#print(' '.join(  map(str, ql[0])))
