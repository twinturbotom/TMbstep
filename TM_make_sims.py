import multiprocessing  # the module we will be using for multiprocessing
import time
import numpy as np
from itertools import product
import subprocess

def get_inputs():

    max_x = 2.2
    max_y = 0.411
    n = 10

    origin = np.linspace(0,max_x*0.5,n)
    xs = np.linspace(max_x*.05,max_x*0.25,n)
    ys = np.linspace(max_y*.25,max_y*0.75,n)
    cs = list(product(origin, xs, ys))
    # a = zip(origin, xs, ys)
    # cs = [c for c in combinations(a,1)]

    return cs

def build_que_list(cmd_args):
    ql = open('que_list.log','w')
    que_list = []
    for i,c in enumerate(cmd_args):
        oxy = ' '.join( map(str,c) )
        ex = f'./TMbstep2d {oxy} tmp/{i}'
        ql.write(f'{ex}\n')
        que_list.append(ex)
    ql.close()
    return que_list

def work(sim):
    print(f'SIM: {sim}')
    log_dir = sim.split(' ')[-1]
    subprocess.check_call(sim.split(' '), stdout=open(f'{log_dir}_sim.log','w+'))
    
if __name__ == "__main__":  # Allows for the safe importing of the main module
    print("There are %d CPUs on this machine" % multiprocessing.cpu_count())
    print(f'Number of cores: {multiprocessing.cpu_count()}')
    number_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(number_processes)
    tasks = build_que_list(get_inputs())
    print(f'num of tasks: {len(tasks)}')
    for t in tasks:
        pool.apply_async(work, (t,))
    pool.close()
    pool.join()
    print('Done')