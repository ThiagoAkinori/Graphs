import codecs
import feedparser
import nltk
from igraph import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import numpy as np
from igraph.drawing.text import TextDrawer
import cairo



def Write_Graph(novo, g):
	with open(novo,'w') as h:
		h.write(str(g))
		h.write("\n")
		h.write(str(g.es["weight"])+"\n")
	h.close()	

def Write_File(novo, conteudo):
	with open(novo, 'w') as h:
		for i in conteudo:
			h.write(i+' ')
		h.write("\n")
	h.close()

def PlotGraph(g):
	visual_style = {}
	colours = ['#fecc5c', '#a31a1c']
	outdegree = g.outdegree()
	bins = np.linspace(0, max(outdegree), len(colours))  
	digitized_degrees =  np.digitize(outdegree, bins)
	g.vs["color"] = [colours[x-1] for x in digitized_degrees]
	visual_style["vertex_size"] = [x/max(outdegree)*50+3 for x in outdegree]
	visual_style["edge_curved"] = False
	plot = Plot("plot.png", bbox=(2000, 2000), background = 'white')
	plot.add(g, bbox=(20, 70, 1800, 1800), **visual_style, vertex_label= g.vs["name"])
	# Make the plot draw itself on the Cairo surface
	plot.redraw()
	# Save the plot
	plot.save()

def Remove_Stopwords(stoplist, texto):
	texto_filtrado=[]
	#Lendo os arquivos necessários
	with codecs.open(stoplist,'r', "utf-8") as f:
		stoplist = f.read().splitlines()
	f.close()
	with codecs.open (texto,'r', "utf-8") as g:
		texto = g.read().split()
	g.close()
	for palavra in texto:
		#deixando a palavra em minúsculo
		palavra = palavra.lower()
		#filtrando pontuãção
		palavra = palavra.replace('.','') 
		palavra = palavra.replace(',','')
		palavra = palavra.replace(';','')
		palavra = palavra.replace(':','')
		palavra = palavra.replace('?','') 
		palavra = palavra.replace('!','')
		palavra = palavra.replace('(','')
		palavra = palavra.replace(')','')
		palavra = palavra.replace('"','')
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
	return texto_filtrado

def CreateGraph(wordlist, g):
	searchlist=[]
	weights=[]
	for word in wordlist:
		try:
			position = searchlist.index(word)
		except ValueError:
			position = -1
		if position > -1:
			src = g.vs.find(name=word)
			tgt = g.vs.find(name=lastword)
			if g.are_connected(src,tgt):
				for idx, edge in enumerate(g.es):
					if (edge.source == src.index and edge.target == tgt.index) or (edge.target == src.index and edge.source == tgt.index):
						weights[idx]=weights[idx]+1
						break
			else:
				g.add_edge(lastword, word)
				weights.append(1)
		else:
			g.add_vertices(word)
			if len(searchlist) > 0:
				g.add_edge(lastword, word)
				weights.append(1)
			searchlist.append(word)
		lastword = word
	searchlist=[]
	g.es["weight"]=weights
	return g

def AnaliseText(g, texto):
	filtrado = []
	lemma = WordNetLemmatizer()
	lemantized = []
	st = PorterStemmer()
	stemm = []
	#filtrando stopswords
	filtrado = Remove_Stopwords("stopwordEN.txt", texto)
	#Pos Tagging pos_tag = nltk.pos_tag(filtrado) 
	#Lematização
	for word in filtrado:
		lemantized.append(lemma.lemmatize(word))
	filtrado=[]
	#Stemming
	for word in lemantized:
		stemm.append(st.stem(word))
	lemantized=[]
	return stemm

def Text2Graph(texto):
	g = Graph()
	stemmed = AnaliseText(g, texto)
	g = CreateGraph(stemmed, g)
	return g



graph = Text2Graph("TextoTeste.txt")
Write_Graph("Novo.txt",graph)
PlotGraph(graph)

