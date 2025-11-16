"""
# Importando Bibliotecas
"""
import os
import shutil


SRC_INC = '/mnt/data/incidentes_operacionais.csv'
SRC_AGG = '/mnt/data/perdas_mensais_por_area.csv'


DST_DIR = os.path.join(os.getcwd(), '..', 'dados') if os.path.basename(os.getcwd()) == 'etl' else os.path.join(os.getcwd(), 'dados')
os.makedirs(DST_DIR, exist_ok=True)


shutil.copy2(SRC_INC, os.path.join(DST_DIR, 'incidentes_operacionais.csv'))
shutil.copy2(SRC_AGG, os.path.join(DST_DIR, 'perdas_mensais_por_area.csv'))


print('Arquivos copiados para', DST_DIR)
