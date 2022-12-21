import tqdm
from datetime import datetime as dt

def entorch(modelo, nomMod, lotesEnt, lotesDev=[], numEpo=1):
    print(f"Inicio de {numEpo} epocas de entrenamiento {dt.now()}")
    
    for epo in range(numEpo):
        for lote in lotesEnt:
            modelo.inicEntr()

            for data in tqdm.tqdm(lote, ascii=" >="):
                modelo += data
            
            modelo.recaMod()
        
        modelo.escrMod(nomMod)

        modelo.inicEval()
        for lote in lotesDev:
            for data in tqdm.tqdm(lote, ascii=" >="):
                modelo.addEval(data)
        if lotesDev:
            modelo.recaEval()
            modelo.printEval(epo)
    print(f"Completadas {numEpo} epocas de entrenamiento {dt.now()}")


