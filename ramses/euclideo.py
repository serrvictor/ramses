import numpy as np
from datetime import datetime as dt
from util import *
from mar import *

class ModEucl:
    def __init__(self, ficMod=None, ficLisUni=None):
        if ficMod:
            self.leeMod(ficMod)
        else:
            self.unidades = leeLis(ficLisUni)
    
    def escrMod(self, ficMod):
        with open(ficMod, "wb") as fpMod:
            np.save(fpMod, self.medUni)
    
    def leeMod(self, ficMod):
        with open(ficMod, "rb") as fpMod:
            self.medUni = np.load(fpMod, allow_pickle=True).item()
            self.unidades = self.medUni.keys()
            
    def inicEntr(self):
        self.medUni = {unidad: 0 for unidad in self.unidades}
        self.numUni = {unidad: 0 for unidad in self.unidades}

    def __add__(self, data):
        self.medUni[data.trn] += data.prm
        self.numUni[data.trn] += 1
        return self

    def recaMod(self):
        for unidad in self.unidades:
            self.medUni[unidad] /= self.numUni[unidad]

    def __call__(self, prm):
        minDis = np.inf
        for unidad in self.unidades:
            dis = sum(abs(prm - self.medUni[unidad])**2)
            if dis<minDis:
                minDis = dis
                reco = unidad
        return reco
    
    def inicEval(self):
        self.varUni = {unidad: 0 for unidad in self.unidades}
        self.numUni = {unidad: 0 for unidad in self.unidades}
        self.cor = 0
    
    def addEval(self, data):
        self.varUni[data.trn] += abs(data.prm - self.medUni[data.trn])**2
        self.numUni[data.trn] += 1
        self.cor += self(data.prm) == data.trn

    def recaEval(self):
        varianza = numUni=0
        for unidad in self.unidades:
            varianza += sum(self.varUni[unidad])
            numUni += self.numUni[unidad]
        varianza /= numUni * len(self.varUni[unidad])
        self.sigma = varianza ** 0.5
        self.cor /= numUni
    
    def printEval(self, epo):
        print(f"{epo=}  {self.sigma=}   {self.cor=:.2%} {dt.now()}")

from collections import namedtuple

def lotesEuc(dirPrm, dirMar, *ficListSen):
    Data = namedtuple("Data", ["sen", "prm", "trn"])
    lote = []
    for sen in leeLis(*ficListSen):
        pathMar = pathName(dirMar, sen, '.mar')
        trn = cogeTrn(pathMar)

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = np.load(pathPrm)

        lote.append(Data(sen=sen, prm=prm, trn=trn))
    return [lote]