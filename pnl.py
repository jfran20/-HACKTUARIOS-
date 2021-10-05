import re 
import pandas as pd 
import nltk
import os
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
print('\n')

##### ====> LIMPIEZA GENERAL DEL ARCHIVO <===== ######
to_process = os.listdir('./Preprocesados')
for my_file in to_process:
    f = open('Preprocesados/' + my_file,'r',encoding='utf8').readlines()
    with open('PNL/Solo texto/' + my_file, 'w',encoding='utf8') as nf:
        for line in f:
            # Crear lineas que contengan toda una idea (Separar en parrafos)
            text = re.sub('(?<!\.)\n',' ',line)
            text = re.sub('[^a-zA-záéíóúñ\n ]',' ',text) # Solo los caracteres alfabetico 
            text = re.sub(' +',' ',text)                 # Quitar espacios repetidos
            text = re.sub(' .{3,3} ','',text)            # Quitar monedas y otros
            text = re.sub('\[.*','',text)                # Quitar Comentarios

            text = text.lower()
            nf.write(text)

    # Cargamos las stopwords de nltk
    stop = stopwords.words('spanish')


    ### =====> METODO 1 PARA RESUMEN DE TEXTO <===== ###
    ''' Este metodo consiste en entrenar un modelo LDA para la seleccion de palabras o 
    tokens previamente pesado y obtener aquellos que resuman mejor el texto '''

    # Realizamos la tokenizacion
    lines = open('PNL/Solo texto/' + my_file, 'r',encoding='utf8').readlines()

    # Se realiza un pesado de cada token y se eliminan stop words
    count = CountVectorizer(stop_words = stop,max_df = 0.1,max_features=5000)
    X = count.fit_transform(lines)

    ### Se entrena un modelo LDA 
    lda = LatentDirichletAllocation(n_components = 1, random_state = 1, learning_method = 'batch')
    X_topics = lda.fit_transform(X)

    ### LAS 15 PALABRAS QUE MEJOR RESUMEN EL TEXTO ###
    n_top_words = 15
    lda_words = []
    feature_names = count.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        lda_words.append([feature_names[i] for i in topic.argsort()[:-n_top_words -1:-1]])
    print(my_file + '-LDA_WORDS: ',lda_words)

    #####  =====> METODO 2 PARA RESUMEN DE TEXTO <===== #######
    ''' Este metodo para resumir consiste, contrario al otro, en obtener las palabras
    con mayor frecuencia dentro del corpus despues de una limpieza y eliminacion de stopwords
    su eficacia consiste mas que nada de la calidad de limpieza que se de'''

    words = []
    for line in lines:
        # Realizamos la tokenizacion de las lineas de texto
        words.append(line.split())

    # Realizamos un 'unnest' a la lista y quitamos las palabras 'stop'
    words = [word for sub in words for word in sub if word not in stop]

    # Contamos las repeticiones de las palabras 
    data =  pd.DataFrame.from_dict(Counter(words),orient='index',columns=['N'])
    # Guardamos
    file_name = my_file.strip('.txt')
    data = data.sort_values('N',ascending=False).head(30)
    data.to_csv('./PNL/Completado' + file_name + '.csv')


