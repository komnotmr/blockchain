#!/usr/bin/python3.6

import subprocess
import os

from multiprocessing import Process
from time import time, sleep

host='http://localhost:'
ports = []
hosts = []

data = {
    'host': 'http://localhost:',
    'ports': [],
    'hosts': [],
    'pids': []
}

files = {
    'pids': 'pids.file',
    'ports': 'ports.file'
}

def update_data(files):
    with open(files['ports'], 'r') as f:
        if not f:
            print (f'error: can\'t open {files["ports"]}')
            print (err)
        else:
            r = f.readlines()     
    ports = [] 
    if len(r) > 0:
        ports = r[0].replace('\n','').split(' ')
    data['ports'] = [int(e) for e in ports if e != '']
    data['hosts'] = [ f'{host}{e}' for e in data['ports']]

    with open(files['pids'], 'r') as f:
        if not f:
            print (f'error: can\'t open {files["pids"]}')
            print (err)
        else:
            r = f.readlines()    
    pids = []
    if len(r) > 0:
        pids = r[0].replace('\n','').split(' ')
    data['pids'] = [e for e in pids if len(e) > 3]

def mquit():
    exit()

def mhelp():
    for i in range(len(keys)):
        print (keys[i])
        print (f'\t {info[i]}')

def mhosts():
    for i in range(len(data['hosts'])):
        print (f'{i} {data["hosts"][i]}')

def mchain():
    req_addr = '/chain'
    print('choose target')
    mhosts()
    inp = int(input())
    if inp not in [ i for i in range(len(data['hosts']))]:
        print ('target not exist')
    else:
        print(f'do {data["hosts"][inp]}{req_addr}')
        subprocess.call(['curl', f'{data["hosts"][inp]}{req_addr}'])

def mnodes_register():
    update_data(files)
    t_p = '/nodes/register'
    for i in range(len(data['hosts'])):
        d = '{ "nodes" : '
        h_t = [data['hosts'][j] for j in range(len(data['hosts'])) if j != i]
        d += str(h_t).replace('\'','"')
        d += ' }'
        subprocess.call([
            'curl',
            '-X', 
            'POST', 
            '-H', 
            'Content-Type:application/json', 
            '-d', 
            d,
            f'{data["hosts"][i]}{t_p}'
            ])
    print ('succes: nodes is registered')

def clear_file(filename):
    with open(filename, 'w') as f:
        if not f:
            print (f'error: can\'t clear file {filename}')
            print (err)
        else:
            f.write('')
        

def list_to_file(filename, li):
    with open(filename, 'w') as f:
        if not f:
            print (f'error: can\'t write to file {filename}')
            print (err)
        else:
            for e in li:
                f.write(f' {e}')

def update_file_data():
    clear_file(files['ports'])
    list_to_file(files['ports'], data['ports'])
    clear_file(files['pids'])
    list_to_file(files['pids'], data['pids'])

def mstart():
    mkill(flg=False)
    if len(data['pids']) == 0:
        print('START \ninput count nodes:')
        inp = int(input())
        if(inp > 0):
            subprocess.call(['./start.sh', str(inp)])
        else:
            print('invalid arguments')
            mquit()

def mkill(flg=True):

    if not os.path.exists(files["pids"]):
        try:
            open(files["pids"], 'x')
            return
        except FileExistsError:
            pass
    if os.stat(files["pids"]).st_size == 0:
        return
    
    if not os.path.exists(files["ports"]):
        try:
            open(files["ports"], 'x')
            return
        except FileExistsError:
            pass

    if os.stat(files["ports"]).st_size == 0:
        return
    
    update_data(files)
    if flg:
        print('choose targets \'0,1,2..n\' or \'-1\' for kill all ')
        mhosts()
        inp = input()
    else:
        inp = '-1'

    if inp == '-1' or inp == 'all':
        print ('killing all hosts')
        subprocess.call(['kill']+data['pids'])
        clear_file(files['pids'])
        clear_file(files['ports'])
        update_data(files)
    else:
        inp = inp.replace(' ','').split(',')
        inp = [int(e) for e in inp]
        for i in range(len(data['pids'])):
            if i in inp:
                subprocess.call(['kill']+[data['pids'][i]])
        data['pids'] = [ data['pids'][i] for i in range(len(data['pids'])) if i not in inp]
        data['ports'] = [ data['ports'][i] for i in range(len(data['ports'])) if i not in inp]
        data['hosts'] = [ data['hosts'][i] for i in range(len(data['hosts'])) if i not in inp]
        update_file_data()
    print ('susses')
        
def request(param, query):
    dif = float(param[1])
    n = int(param[2])
    for i in range(n):
        sleep(dif)
        subprocess.call(['curl', query])

def mmine():
    req_addr = '/mine'
    mhosts()
    print('input difficulties and n for hosts as <node number>:<difficulty>:<count block>,')
    inp = input().split(',')
    conf = [ e.split(':') for e in inp]
    print (conf)
    p = []
    for i in range(len(conf)):
        query = f'{data["hosts"][int(conf[i][0])]}{req_addr}'
        p.append( Process(target=request, args=(conf[i], query)) )
        p[i].start()

def mresolve():
	req_addr = '/nodes/resolve'
	mhosts()
	inp = int(input())
	if inp not in [ i for i in range(len(data['hosts']))]:
		print ('target not exist')
	else:
		print(f'do {data["hosts"][inp]}{req_addr}')
		subprocess.call(['curl', f'{data["hosts"][inp]}{req_addr}'])

keys = ['start','kill','help', 'hosts', 'chain', 'mine','resolve','register','quit']
info = ['-start nodes','-kill nodes','-for cat help', '-cat list of hosts',
    '-do chain request to target','-mine 1 block','-resolve use','-nodes-register', '-for quit']
func = [mstart, mkill, mhelp, mhosts, mchain, mmine, mresolve, mnodes_register, mquit]

if __name__ == '__main__':
    mstart()
    update_data(files)
    inp = ''
    while inp != 'q':
        inp = input()
        if inp in keys:
            func[keys.index(inp)]()
        else:
            print ('invalid argument\nuse \"help\" for help')

        
        