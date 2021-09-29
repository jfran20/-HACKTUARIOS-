import os
from tika import parser 

## GENERAR ARCHIVOS TXT POR CADA PDF EN EL SUBDIRECTORIO PDF
files = len(os.listdir('./PDF')) 
for i,my_file in enumerate(os.listdir('PDF')):
    print(i + 1 ,'/',files,'Procesando archivo:', my_file)

    # Leemos el pdf y obtenemos el texto
    try:
        raw = parser.from_file('PDF/' + my_file)
        print('Conversion exitosa')
    except:
        print('Se detecto un fallo con el archivo:',my_file)
        print('Por favor asegurate de tener Java instalado')
        break

    # Realizamos la escritura a un archivo txt
    new_path = './Preprocesados/' + my_file.strip('.pdf') + '.txt' # ===> Ubicacion del nuevo archivo
    with open(new_path, 'w',encoding='utf8') as f:
        f.write(raw['content'])
    print('Escritura exitosa')

    # Eliminamos lineas en blanco
    f = open(new_path,'r',encoding='utf8').readlines()
    with open(new_path,'w',encoding='utf8') as new_f:
        for line in f:
            if line.split():
                new_f.write(line)
    print('Preprocesado exitoso \n')


