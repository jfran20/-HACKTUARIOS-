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
        text = re.sub('\[.*','',text)                # Quitar Comentarios
        text = text.lower()
        nf.write(text)

# Cargamos las stopwords de nltk
stop = stopwords.words('spanish')

# Realizamos la tokenizacion
lines = open('PNL\BIMBO 2021-2.txt', 'r',encoding='utf8').readlines()

# PESAMOS CADA TOKEN Y APLICAMOS LAS STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer(stop_words = stop,max_df = 0.2,max_features=5000)
X = count.fit_transform(lines)

### ENTREMAMOS UN MODELO LDA PARA OBTENER LOS TEMAS DE LAS PALABRAS
from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components = 5, random_state = 1, learning_method = 'batch')
X_topics = lda.fit_transform(X)


### IMPRIMIMOS LOS TEMAS ###
n_top_words = 5
feature_names = count.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    print('Topic: %d' % (topic_idx + 1))
    print(' '.join([feature_names[i] for i in topic.argsort()[:-n_top_words -1:-1]]))
