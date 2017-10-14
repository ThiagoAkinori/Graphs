import codecs
import feedparser
import nltk
from igraph import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import numpy as np




def Write_Files(novo, conteudo):
	with open(novo,'w') as h:
		for i in conteudo:
			h.write(i+' ')
	h.close();	


def Remove_Stopwords(stoplist, texto, texto_filtrado):
	#Lendo os arquivos necessários
	with codecs.open(stoplist,'r', "utf-8") as f:
		stoplist = f.read().splitlines()
		with codecs.open (texto,'r', "utf-8") as g:
			texto = g.read().split()
	f.close();
	g.close();

	for palavra in texto:
		#deixando a palavra em minúsculo
		palavra = palavra.lower()
		#filtrando pontuãção
		if palavra.find('.')>-1:
			palavra = palavra.replace('.','') 
		if palavra.find(',')>-1:
			palavra = palavra.replace(',','')
		if palavra.find(';')>-1:
			palavra = palavra.replace(';','')
		if palavra.find(':')>-1:
			palavra = palavra.replace(':','')
		if palavra.find('?')>-1:
			palavra = palavra.replace('?','') 
		if palavra.find('!')>-1:
			palavra = palavra.replace('!','')
		if palavra.find('(')>-1:
			palavra = palavra.replace('(','')
		if palavra.find(')')>-1:
			palavra = palavra.replace(')','')
		if palavra.find('"')>-1:
			palavra = palavra.replace('"','')
		if palavra.find('‘')>-1:
			palavra = palavra.replace('‘','')
		if palavra.find("'")>-1:
			if palavra[palavra.find("'")+1:] == "re" or palavra[palavra.find("'")+1:] == "s":
				palavra = palavra[0:palavra.find("'")]
			if palavra[palavra.find("'")+1:] == "t":
				palavra = ""
		#Removendo stopwords
		marcador = 0;	
		for stopword in stoplist:
			if palavra == stopword:
				marcador = 1;
		if marcador == 0 and palavra != '':
			texto_filtrado.append(palavra)


def CreateGraph(wordlist, graph, label):
	searchlist=[]
	weights=[]
	count = 0
	for word in wordlist:
		try:
			position = searchlist.index(word)
		except ValueError:
			position = -1

		if position > -1:
			
			if (g.get_eid(word, lastword, directed=False, error=False) or g.get_eid(lastword, word, directed=False, error=False)):
				count = 0;
				for edge in g.es:
					if (edge == (lastword,word) or edge == (word, lastword)):
						weights[count] = weights[count]+1
						break
					count=count+1
			else:
				g.add_edge(word, lastword)

		else:
			g.add_vertices(word)
			if len(searchlist) > 0:
				g.add_edge(lastword, word)
				weights.append(1)
			label.append(word)
			searchlist.append(word)
		lastword = word
	searchlist=[]
	g.es["weight"]=weights
	g.es["label"]=label




filtrado = []
lemantizing = WordNetLemmatizer()
lemantized = []
weights = []
label = []
st = PorterStemmer()
stem = []
visual_style = {}

#filtrando stopswords
Remove_Stopwords("stopwordEN.txt", "TextoTeste.txt", filtrado)

#Pos Tagging
#pos_tag = nltk.pos_tag(filtrado) 

#Lematização
for word in filtrado:
	lemantized.append(lemantizing.lemmatize(word))
	label.append(word)
filtrado=[]

#Stemming
for word in lemantized:
	stem.append(st.stem(word))
lemantized=[]

#Construção do grafo
g = Graph()
CreateGraph(stem,g, label)
stem = []


#Plot grafo

colours = ['#fecc5c', '#a31a1c']
outdegree = g.outdegree()

bins = np.linspace(0, max(outdegree), len(colours))  
digitized_degrees =  np.digitize(outdegree, bins)
g.vs["color"] = [colours[x-1] for x in digitized_degrees]
visual_style["vertex_size"] = [x/max(outdegree)*30+3 for x in outdegree]
N = len(label)
visual_style["edge_curved"] = False
visual_style["layout"] = g.layout_fruchterman_reingold(weights=g.es["weight"], maxiter=1000, area=N**10, repulserad=N**3)

print(g)
#plot (g, **visual_style);