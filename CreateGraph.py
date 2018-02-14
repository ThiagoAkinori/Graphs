import codecs
import feedparser
import nltk
from igraph import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import numpy as np
from igraph.drawing.text import TextDrawer
import cairo
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec

def Write_Graph(novo, g):
	#Escreve grafo em um arquivo
	with open(novo,'w') as h:
		h.write(str(g))
		h.write("\n")
		h.write(str(g.es["weight"])+"\n")
		h.write(str(g.vs["name"])+"\n"+str(g.vs["weight"]))
	h.close()	


def Write_File(novo, conteudo):
	#Escreve texto em um arquivo
	with open(novo, 'w') as h:
		for i in conteudo:
			h.write(i+' ')
		h.write("\n")
	h.close()

def PlotGraph(g):
	#Plota o grafo em um png
	visual_style = {}
	colours = ['#fecc5c', '#a31a1c']
	outdegree = g.outdegree()
	bins = np.linspace(0, max(outdegree), len(colours))  
	digitized_degrees =  np.digitize(outdegree, bins)
	g.vs["color"] = [colours[x-1] for x in digitized_degrees]
	visual_style["vertex_size"] = [x/max(outdegree)*50+3 for x in outdegree]
	visual_style["edge_curved"] = False
	plot = Plot("plot.png", bbox=(2000, 2000), background = 'white')
	plot.add(g, bbox=(20, 70, 1800, 1800), *visual_style, vertex_label= g.vs["name"])
	# Make the plot draw itself on the Cairo surface
	plot.redraw()
	# Save the plot
	plot.save()

def Remove_Stopwords(stoplist, texto):
	texto_filtrado=[]
	#Lendo os arquivos necessarios
	texto=texto.split()
	with codecs.open(stoplist,'r', "utf-8") as f:
		stoplist = f.read().splitlines()
	f.close()
	for palavra in texto:
		#deixando a palavra em minusculo
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
				marcador = 1
		if marcador == 0 and palavra != '':
			texto_filtrado.append(palavra)
	return texto_filtrado

def MkGraph(wordlist, g):
	esweights=[]
	vsweights=[]
	searchlist = [] #lista de palavras encontradas
	
	# transforma wordlist em pesos para o grafo
	for word in wordlist:
		#procura palavra na lista de palavras a encontradas
		try:
			position = searchlist.index(word)
		except ValueError:
			position = -1
		#se achar aumenta o peso do vertice e cria uma aresta
		if position > -1:
			vsweights[position] = vsweights[position]+1 
			src = g.vs.find(name=word)
			tgt = g.vs.find(name=lastword)
			#verifica se existe aresta entre os vertices
			if g.are_connected(src,tgt):
				for idx, edge in enumerate(g.es):
					#verificando em qual posicao esta a aresta entre os vertices 
					if (edge.source == src.index and edge.target == tgt.index) or (edge.target == src.index and edge.source == tgt.index):
						esweights[idx]=esweights[idx]+1
						break
			#se não existir cria uma aresta entre os dois vertices
			else:
				g.add_edge(lastword, word)
				esweights.append(1)
		#se não achar cria um vertice e adiciona uma aresta se necessario
		else:
			g.add_vertices(word)
			vsweights.append(1)
			if len(searchlist) > 0:
				g.add_edge(lastword, word)
				esweights.append(1)
			searchlist.append(word)
		lastword = word
	#adiona os pesos ao grafo
	g.vs["weight"]=vsweights
	g.es["weight"]=esweights
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
	#cria grafo
	g = Graph()
	#pre processa o texto
	wordlist = AnaliseText(g, texto)
	#adiona pesos e arestas ao grafo
	g = MkGraph(wordlist, g)
	return g


def OpenBase():
	base=[]
	for i in range(1, 441):
		base.append(File2Graph('Marujo/texto'+str(i)+'.txt'))
	return base

def File2Graph(texto):
	#cria grafo
	g=Graph()
	#abre arquivo e transforma em string
	with codecs.open (texto,'r', "utf-8") as f:
		texto = f.read()
	f.close()
	#pre processa o texto
	wordlist = AnaliseText(g, texto)
	#adiona pesos e arestas ao grafo
	g = MkGraph(wordlist, g)
	return g



def FindAdj(g1, src):
	try: 
		adjacents=[]
		adjacents.append(src)
		for tgt in g1.vs["name"]:
			if g1.are_connected(src,tgt):
				adjacents.append(tgt)
		return adjacents
	except ValueError:
		return None


def CossineSimilarity(graph, query):
	graph2 = Text2Graph(query)
	g2names = graph2.vs["name"]
	g2weight = graph2.vs["weight"]
	similarities=[]
	for vs in graph2.vs["name"]:
		adjacents = FindAdj(graph, vs)
		if adjacents != None:
			g1weight = []
			for i in adjacents:
				g1weight.append(0)
			gweight = graph.vs["weight"]
			#acha os pesos da lista de adjacencia
			for idx, vs in enumerate(graph.vs["name"]):
				try:
					pos = adjacents.index(vs)
				except Exception as e:
					pos = -1
				if pos > -1:
					g1weight[pos] = gweight[idx]

			#transforma lista em set
			ing1 = set(adjacents)
			ing2 = set(g2names)
		
		
			#passa somente as palavras que não estão em g1
			onlyin2 = ing2 - ing1
			#concatena as palavras que não estão em g1 com as que estão em g1
			allnames = list(onlyin2) + adjacents
			#inicia os vetores de frequencia de termo
			tfv1=[]
			tfv2=[]
			#adiciona frequencias de palavras em v1
			for idx, name in enumerate(allnames):
				try:
					pos = adjacents.index(name)
				except ValueError:
					pos = -1
				if pos > -1:
					tfv1.append(g1weight[pos])
				else :
					tfv1.append(0)
		
			#adiciona frequencia de palavras em v2
			for idx, name in enumerate(allnames):
				try:
					pos = g2names.index(name)
				except ValueError:
					pos = -1
				if pos > -1:
					tfv2.append(g2weight[pos])
				else :
					tfv2.append(0)

			similarities.append(cosine_similarity([tfv1],[tfv2]))
	if len(similarities) > 0:
		media = np.mean(similarities)
		return media
	else:
		return 0

def Word2vec(graph, query):
	adjacents= []
	g = Text2Graph(query)
	values = []
	vocab = graph.vs["name"]
	names = g.vs["name"]
	for word in names:
		adj = FindAdj(graph, word)
		if adj != None:
			adjacents.append(adj)
	if len(adjacents):
		w2v = Word2Vec(adjacents, min_count=1)
		for word in names:
			values.append(w2v.most_similar(word, topn = 1))
		mean=[]
		for value in values:
			mean.append(value[0][1])
		media = np.mean(mean)
		return media
	else:
		return 0
	

def SearchInBase(base, query):
	means = []
	maior = 0
	index = 0
	for i in range(len(base)):
		atual = CossineSimilarity(base[i], query)
		if atual > maior:
			index = i+1
			maior = atual
	print('texto '+str(index)+' similaridade '+str(maior))



base = OpenBase()

query=''
while query != 'fim':
	query = input("Entre com a consulta (digite 'fim' para finalizar consultas): ")
	SearchInBase(base, query)

#print(CossineSimilarity(base[1]))
#print(Word2vec(base[1]))

#Write_Graph("Novo.txt",graph)

#PlotGraph(graph)

