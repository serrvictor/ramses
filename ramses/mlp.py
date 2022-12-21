import numpy as np
import torch
from datetime import datetime as dt
from util import *
from mar import *

class MLP_3(torch.nn.Module):
    def __init__(self, dimIni=30, dimInt=128, dimSal=5):
        super().__init__()

        self.capa1 = torch.nn.Linear(in_features=dimIni, out_features=dimInt)
        self.capa2 = torch.nn.Linear(in_features=dimInt, out_features=dimInt)
        self.capa3 = torch.nn.Linear(in_features=dimInt, out_features=dimSal)  

    def forward(self, x):
        x = self.capa1(x[..., :])
        x = torch.nn.functional.relu(x)
        x = self.capa2(x)
        x = torch.nn.functional.relu(x)
        x = self.capa3(x)
        x = torch.nn.functional.log_softmax(x, dim=-1)

        return x.reshape(1, 1, -1)

from torch.nn.functional import nll_loss
from torch.optim import SGD
class ModMLP:
    def __init__(self, ficLisUdf=None, ficMod=None, red=None, 
            funcLoss=nll_loss, Optim=lambda params:SGD(params, lr=1e-5)):
        if ficMod:
            self.leeMod(ficMod)
        else:
            self.red = red
            self.red.unidades = leeLis(ficLisUdf)

        self.funcLoss = funcLoss
        self.optim = Optim(self.red.parameters())
    
    def escrMod(self, ficMod):
        pass
    
    def leeMod(self, ficMod):
        pass
            
    def inicEntr(self):
        self.optim.zero_grad()

    def __add__(self, data):
        salida = self.red(data.prm).swapdims(1, 2)
        loss = self.funcLoss(salida, data.trn)
        loss.backward()
        return self
    def recaMod(self):
        self.optim.step()

    def __call__(self, prm):
        return self.red.unidades[self.red(prm).argmax()]
    
    def inicEval(self):
        self.loss = 0
        self.numUni = 0
        self.cor = 0
    
    def addEval(self, data):
        salida = self.red(data.prm).swapdims(1, 2)
        self.loss += self.funcLoss(salida, data.trn).item()
        self.numUni += 1
        self.cor += self(data.prm) == self.red.unidades[data.trn.squeeze()]

    def recaEval(self):
        self.loss /= self.numUni
        self.cor /= self.numUni
    
    def printEval(self, epo):
        print(f"{epo=}  {self.loss=}   {self.cor=:.2%} {dt.now()}")
    
from collections import namedtuple

def lotesMLP(dirPrm, dirMar, ficLisUni, *ficListSen):
    unidades = leeLis(ficLisUni)
    numUni = len(unidades)
    Data = namedtuple("Data", ["sen", "prm", "trn"])
    lote = []
    for sen in leeLis(*ficListSen):
        pathMar = pathName(dirMar, sen, '.mar')
        uni = cogeTrn(pathMar)
        trn = torch.zeros(numUni)
        trn[unidades.index(uni)] = 1

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = torch.tensor(np.load(pathPrm), dtype = torch.float)

        lote.append(Data(sen=sen, prm=prm.reshape(1, 1, 1, -1), trn=torch.tensor([[unidades.index(uni)]])))
    return [lote]