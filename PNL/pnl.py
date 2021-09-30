##################### =======> PARTE 2 PNL <============== ##################
import re 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
print('\n')

f = open('Preprocesados/BIMBO 2021-2.txt','r',encoding='utf8').readlines()


#### Limpieza general del archivo
with open('PNL\BIMBO 2021-2.txt', 'w',encoding='utf8') as nf:
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

# Realizamos la tokenizacion
lines = open('PNL\BIMBO 2021-2.txt', 'r',encoding='utf8').readlines()

# PESAMOS CADA TOKEN Y APLICAMOS LAS STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer(stop_words = stop,max_df = 0.15,max_features=5000)
X = count.fit_transform(lines)

### ENTREMAMOS UN MODELO LDA PARA OBTENER LOS TEMAS DE LAS PALABRAS
from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components = 5, random_state = 1, learning_method = 'batch')
X_topics = lda.fit_transform(X)


### IMPRIMIMOS LOS TEMAS ###
n_top_words = 5
feature_names = count.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    print('Agrupacion: %d' % (topic_idx + 1))
    print(' '.join([feature_names[i] for i in topic.argsort()[:-n_top_words -1:-1]]))


### CODIGO PARA GENERAR LA LISTA DE PALABRAS POR FECUENCIA
from collections import Counter
import pandas as pd 

words = []
for line in lines:
    # Realizamos la tokenizacion de las lineas de texto
    words.append(line.split())

# Realizamos un 'unnest' a la lista
words = [word for sub in words for word in sub]
# Quitamos las palabras stop
words = [word for word in words if word not in stop]
# Generamos un dataframe con las columnas, se ordenan segun el conteo e imprime las 20 mas repetidas
data =  pd.DataFrame.from_dict(Counter(words),orient='index',columns=['N'])
print(data.sort_values('N',ascending=False).head(20))


