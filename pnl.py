##################### =======> PARTE 2 PNL <============== ##################
import re 
import nltk

try:
    from nltk.corpus import stopwords
except:
    nltk.download('stopwords')
    from nltk.corpus import stopwords

f = open('Preprocesados/BIMBO 2021-2.txt','r',encoding='utf8').readlines()

    # Limpieza general del archivo
with open('PNL\BIMBO 2021-2.txt', 'w',encoding='utf8') as nf:
    for line in f:
        text = re.sub('[^a-zA-z\n áéíóúñ]','',line) # Solo los caracteres alfabetico 
        text = re.sub('|(http)','',text) # Quitar URLS
        text = re.sub('|\(.*\)|\[.*\]','',text) # Quitar Comentarios
        text = re.sub('( .?..? )|( +. +)',' ',text)
        text = text.lower()
        nf.write(text)



#  Tokenizamos las palabras

# Agregamos stopwords
#stop = stopwords.words('spanish')
#clean_text = [word for word in tokenized if word not in stop]

