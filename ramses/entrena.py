#! /usr/bin/python3

import tqdm

from util import *
from prm import *
from mar import *

def entrena(dirMod, dirMar, dirPrm, *guiSen):
    """
    Entrena los modelos acústicos de las unidades encontradas en los ficheros de
    entrenamiento, indicados en el fichero guía 'guiSen' escribiendo el resultado en
    el directorio 'dirMod'.

    Los ficheros de señal parametrizada se leen del directorio 'dirPrm' y el contenido
    fonético se extrae del cuarto campo de la etiqueta LBO de los ficheros de marcas
    ubicados en 'dirMar'.
    """

    modelos = {}
    numSen = {}
    for sen in tqdm.tqdm(leeLis(*guiSen)):
        pathMar = pathName(dirMar, sen, '.mar')
        mod = cogeTrn(pathMar)

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = leePrm(pathPrm)

        if mod not in modelos:
            modelos[mod] = prm
            numSen[mod] = 1
        else:
            modelos[mod] += prm
            numSen[mod] += 1

    for mod in modelos:
        modelos[mod] /= numSen[mod]
        pathMod = pathName(dirMod, mod, '.mod')
        chkPathName(pathMod)
        with open(pathMod, 'wb') as fpMod:
            np.save(fpMod, modelos[mod])


#################################################################################
# Invocación en línea de comandos
#################################################################################

if __name__ == '__main__':
    from docopt import docopt
    import sys

    Sinopsis = f"""
Entrena los modelos acústicos a partir de una base de datos de entrenamiento

Usage:
    {sys.argv[0]} [options] <guiSen>...
    {sys.argv[0]} -h | --help
    {sys.argv[0]} --version

Opciones:
    -p PATH, --dirPrm=PATH  Directorio con las señales parametrizadas [default: .]
    -a PATH, --dirMar=PATH  Directorio con los ficheros de marcas [default: .]
    -m PATH, --dirMod=PATH  Directorio con los modelos generados [default: .]

Argumentos:
    <guiSen>  Nombre del fichero guía con los nombres de las señales usadas en el
              entrenamiento. Pueden especificarse tantos ficheros guía como sea
              necesario.

Entrenamiento:
    El programa lee los contenidos fonéticos de los ficheros de marcas y entrena los
    modelos de las unidades fonéticas encontradas en ellos.
"""

    args = docopt(Sinopsis, version=f'{sys.argv[0]}: Ramses v3.4 (2020)')
    
    dirPrm = args['--dirPrm']
    dirMar = args['--dirMar']
    dirMod = args['--dirMod']

    guiSen = args['<guiSen>']

    entrena(dirMod, dirMar, dirPrm, *guiSen)
