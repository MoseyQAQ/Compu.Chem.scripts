from glob import glob 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d

'''
parsedpgen.py: This script is used to parse the log file of dpgen (dpgen.log) and generate the report.
Last modified: 2024-01-18
Author:        Denan Li
WARNING:       If you re-run th iter, the last iter will be cover the previous one.
'''



class dpgen:
    def __init__(self,file_name: str) -> None:
        '''
        param: file_name: the log file of dpgen
        '''
        self.file_name = file_name
        self.iters, self.start, self.end = self._get_block()
        self.block_dict, self.sys_set = self._read_blocks(self.iters,self.start,self.end)
        self.saveFile(self.block_dict, self.sys_set)
        self.plot(self.block_dict, self.sys_set,type='accurate')

    def _get_block(self) -> tuple:
        '''
        得到每个iter的起始行和终止行
        '''
        iters = []
        start = []
        end = []

        f = open(self.file_name,'r')
        lines = f.readlines()

        for index, line in enumerate(lines):
            if 'system' in line and 'task 06' in lines[index-1]:
                iter = int(lines[index-1].split()[-3][-6:])
                iters.append(iter)
                start.append(index)
            elif "accurate_ratio" in line and 'task 07' in lines[index+1]:
                end.append(index)

        if len(start) != len(end):
            print("start and end not match")
            exit(1)

        f.close()
        print(iters)
        return iters, start, end
    
    def _read_block(self,start: int,end:int):
        '''
        读取单个iter的block，返回一个字典，key为sys，value为对应的3个ratio
        '''
        f = open(self.file_name,'r')
        block = f.readlines()[start:end+1]
        f.close()

        sys = self._get_sys_in_block(block)
        ratio_dict = self._get_ratio_in_block(block,sys)

        return ratio_dict,sys

    def _get_ratio_in_block(self,block: list, sys: list) -> dict:
        '''
        获得单个iter的block中的ratio
        '''
        sys = ['{:03d}'.format(i) for i in sys]
        ratio_dict = {key:[] for key in sys}
        for line in block:
            if 'candidate :' not in line and 'failed    :' not in line and 'accurate  :' not in line:
                continue
            which_sys = [i for i in sys if 'system ' + i in line]
            if len(which_sys) == 1:
                ratio_dict[which_sys[0]].append(float(line.split()[-2]))
        return ratio_dict

    def _get_sys_in_block(self,block: list) -> list:
        '''
        获得单个iter的block中的sys
        '''
        sys = []
        for line in block:
            if 'INFO : system' in line and '%' in line:
                tmp = int(line.split()[-8])
                if tmp not in sys:
                    sys.append(tmp)
        return sys
    
    def _read_blocks(self,iters: list, start: list, end: list) -> dict:
        '''
        读取所有的iter的block，返回一个字典，key为iter，value为对应的字典，key为sys，value为对应的3个ratio
        '''
        block_dict_ = {}
        sys_set = []
        for ii,iter in enumerate(iters):
            block = self._read_block(start[ii],end[ii])
            block_dict_[iter] = block[0]
            sys_set.extend(block[1])
        sys_set = list(set(sys_set))

        return block_dict_,sys_set
    
    def saveFile(self, block_dict: dict,sys_set: list, file_name = None) -> None:
        '''
        保存文件
        '''
        if file_name is None:
            file_name = self.file_name.split('.')[0] + '.csv'
        print('sys,iter,candidate,failed,accurate',file=open(file_name,'w'))
        syss = ['{:03d}'.format(i) for i in sys_set]
        print('sys_set: ',syss)
        for sys in syss:
            for iter in block_dict.keys():
                if sys in block_dict[iter].keys():
                    print('{:s},{:02d},{:2f},{:2f},{:2f}'.format(sys,iter,block_dict[iter][sys][0],block_dict[iter][sys][1],block_dict[iter][sys][2]),file=open(file_name,'a'))
        pd.read_csv(file_name).to_excel(file_name.split('.')[0] + '.xlsx',index=False)
    
    def plot(self,block_dict: dict, sys_set: list, type: str) -> None:
        '''
        绘图
        '''
        sns.set_style('whitegrid')
        plt.figure(figsize=(20,6))
        plt.ylim(0,100)
        plt.xlabel('iter')
        plt.ylabel(type + ' ratio')
        syss = ['{:03d}'.format(i) for i in sys_set]
        # 遍历每个sys
        for sys in syss:
            x = []
            y = []

            # 遍历每个iter
            for iter in block_dict.keys():
                if sys in block_dict[iter].keys(): # 如果iter中有这个sys
                    x.append(iter)
                    if type == 'accurate':
                        y.append(block_dict[iter][sys][2])
                    elif type == 'candidate':
                        y.append(block_dict[iter][sys][0])
                    elif type == 'failed':
                        y.append(block_dict[iter][sys][1])
            if len(x) <= 3:
                continue
            print(sys,len(x),len(y))
            f = interp1d(x, y, kind='cubic')
            xnew = np.linspace(min(x),max(x),num=1000,endpoint=True)
            ynew = f(xnew)
            plt.plot(xnew,ynew,label=sys)
            plt.scatter(x,y,s=10)
        max_iter = max(block_dict.keys())
        min_iter = min(block_dict.keys())
        plt.plot([max_iter,min_iter],[90,90],linestyle='--',color='black')
        plt.legend()
        plt.title(self.file_name.split('.')[0])
        plt.savefig(self.file_name.split('.')[0] + '.png',dpi=600)
        plt.close()


def main():
    dpgen("dpgen.log")

if __name__ == '__main__':
    main()
