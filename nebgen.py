import argparse
import os
from ase import io
from ase.neb import NEB
from sys import argv
from os import path
def write_st(images):
    k=0
    for i in images:
        os.mkdir(f'0{k}')
        os.chdir(f'0{k}')
        io.write(images = i,format = 'vasp',filename = f'POSCAR')
        k+=1
        os.chdir('..')
def neb_generator(images,method):
    neb = NEB(images)
    if ((method == 'IDPP') or (method == 'idpp')):
        neb.interpolate(method='idpp')
        write_st(images)
        io.write('XDATCAR', images)
    elif ((method == 'Li') or (method == 'li')):
        neb.interpolate()
        write_st(images)
        io.write('XDATCAR', images)
    else:
        print('Unvaild method.\n');
        exit(1);
def main():
    parser = argparse.ArgumentParser(prog='nebgen',description='A transition state structures generator.')
    parser.add_argument('-i','--input',help="2个输入结构文件",nargs="+")
    parser.add_argument('-m','--method',default='IDPP',help="生成结构方法，IDPP和LI方法可用")
    parser.add_argument('-n','--number',default=1,help = "插入images数量，默认为1")
    args = parser.parse_args()
    if len(args.input) != 2:
        print("2 input structures are required!")
        exit(-1)
    start = io.read(args.input[0])
    end = io.read(args.input[1])
    images = [start] + [start.copy() for i in range(int(args.number))] + [end]
    neb_generator(images,args.method)

main()