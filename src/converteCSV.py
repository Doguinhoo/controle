import pandas as pd
from deps import PATH_VOL, PATH_ABR
import sys

# TODO: checar o input
tipo = sys.argv[1]

match tipo:
    case "voluntários": caminho = PATH_VOL
    case "abrigados": caminho = PATH_ABR

pd.read_csv(caminho)
pd.to_excel(f'./{tipo}.xlsx')
