import re

with open('Preprocesados\BIMBO 2021-2.txt', encoding = 'utf8') as f:
    texto = f.read()
    texto = re.sub('  ','',texto)
    print(texto)
