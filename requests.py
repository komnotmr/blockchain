#!/usr/bin/python3.6

import subprocess

hosts = None

def get_hosts(filename='./ports.file'):
    host='http://localhost:'
    with open(filename, 'r') as f:
        r = f.readlines()
    ports = r[0].replace('\n','').split(' ')
    return [ host+e for e in ports if e != '']

def mquit():
    exit()

def mhelp():
    for i in range(len(keys)):
        print (keys[i])
        print (f'\t {info[i]}')

def mhosts():
    for i in range(len(hosts)):
        print (f'{i} {hosts[i]}')

def mchain():
    req_addr = '/chain'
    print('choose target')
    mhosts()
    inp = int(input())
    if inp not in [ i for i in range(len(hosts))]:
        print ('target not exist')
    else:
        print(f'do {hosts[inp]}{req_addr}')
        subprocess.call(['curl', f'{hosts[inp]}{req_addr}'])

def mnodes_register():
	print('mnodes_register')

def mstart():
	mkill()
	print('START \nCount nodes:')
	inp = int(input())
	if(inp > 0):
		subprocess.call(['./start.sh', str(inp)])

def mkill():
	subprocess.call(['./start.sh', '0', 'clean'])

def mmine():
	req_addr = '/mine?difficult='
	mhosts()
	inp = int(input())
	print('difficult: ')
	dif = float(input())
	if(dif < 0 or inp not in [ i for i in range(len(hosts))] ):
		print('error')
	else:
		print(f'{hosts[inp]}{req_addr}{dif}')
		subprocess.call(['curl', f'{hosts[inp]}{req_addr}{dif}'])

def mconsensus():
	req_addr = '/nodes/resolve'
	mhosts()
	inp = int(input())
	if inp not in [ i for i in range(len(hosts))]:
		print ('target not exist')
	else:
		print(f'do {hosts[inp]}{req_addr}')
		subprocess.call(['curl', f'{hosts[inp]}{req_addr}'])

keys = ['start','kill','help', 'hosts', 'chain', 'mine','consensus','register','quit']
info = ['-start nodes','-kill nodes','-for cat help', '-cat list of hosts',
    '-do chain request to target','-mine 1 block','-consensus use','-nodes-register', '-for quit']
func = [mstart, mkill, mhelp, mhosts, mchain,mmine, mconsensus,mnodes_register, mquit]


if __name__ == '__main__':
    mstart()
    hosts = get_hosts()
    inp = ''
    while inp != 'q':
        inp = input()
        if inp in keys:
            func[keys.index(inp)]()
        else:
            print ('invalid argument\nuse \"help\" for help')

        
        