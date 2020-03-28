from nltk.corpus import stopwords
import networkx as nx

from math import sqrt
import numpy as np

import functools


def input_text(text):
    filedata = text
    article = filedata.split(". ")
    sentences = []

    replace_character = "[^a-zA-Z]" #checks for special character

    for sentence in article:
        # print(sentence)
        sentences.append(sentence.replace(replace_character, " ").split(" "))
    sentences.pop() 
    
    return sentences

def calculate_cosine_distance(vectorA,vectorB):

    dot_product = functools.reduce(lambda x,y: x+y,map(lambda Ai,Aj: Ai*Aj, vectorA, vectorB))

    vectorA_norm = sqrt(functools.reduce(lambda x,y: x+y,map(lambda Ai: Ai*Ai,vectorA)))
    vectorB_norm = sqrt(functools.reduce(lambda x,y: x+y,map(lambda Bi: Bi*Bi,vectorB)))

    cosine_similarity_score = dot_product/(vectorA_norm*vectorB_norm)

    return cosine_similarity_score

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    words_sentence_one = [w.lower() for w in sent1]

    words_sentence_two = [w.lower() for w in sent2]
 
    all_words = list(set(words_sentence_one + words_sentence_two))
 
    vector_sentence_1 = [0] * len(all_words)

    vector_sentence_2 = [0] * len(all_words)

    for w in words_sentence_one:
        if w in stopwords:
            continue
        vector_sentence_1[all_words.index(w)] += 1

    for w in words_sentence_two:
        if w in stopwords:
            continue
        vector_sentence_2[all_words.index(w)] += 1
 
    return 1 - calculate_cosine_distance(vector_sentence_1, vector_sentence_2)
 
def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: 
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(text, top_n=1):
    stop_words = stopwords.words('english')
    summarize_text = []
    sentences =  input_text(text)
    
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    return(". ".join(summarize_text))
    # print(summarize_text)

# text = "King Prithvi Narayan Shah of Gorkha in 1786 had invaded the Kathmandu Valley and unified Nepal. Before the unification, Nepal was ruled by various Kirats, Lichchavis, Thakuris and Mallas. The history mentioned that Kirats ruled Nepal during the 7th century BC. Though much was not known about Kirats,the Lichchavi dynasty followed the Kirats which lasted from the 2nd to 9th century AD. Nepal was ruled by the Thakuris who were followed by the Mallas for two centuries after The Lichchavis. Nepal was divided into many principalities and small kingdoms in the fifth centuries of Malla rule.Jang Bahadur Rana the then Prime Minister of Nepal revolted against the royalty in 1844. The famous Kot Massacre took place during this period in which numbers of noblemen were killed. The Rana took absolute power but continued to maintain the Shah family in the palace. The 104 years regime of Ranas came to and end due to their autocratic rules.It was in November 1950 King Tribhuvan restored democracy overthrowing the Rana regime with large number of Nepalese people support. He restored Shah Regime again in Nepal.After his death King Mahendra had ruled in Nepal from 13 March 1955 to 31 January 1972. Birendra ruled Nepal from 31 January 1972 –1 June 2001and he was known as one of the most noble and peaceful king of Nepal. The entire family of King Birendra was massacred in June 2001 popularly Known as Royal Massacre 2001. Prince Dipendra was crowned as King while he was on coma stage, later he died in hospital bed. After the death of Diepndra, Gyanendra Shah late King Birendra’s brother succeeded as the King of Nepal.King Gyanendra Shah was dethroned in 2006 by a decade long People’s revolution led by communist party of Nepal (Maoist) and several weeks protest by major political parties and established Federal Democratic Republic of Nepal."
# generate_summary(text, 3) #the number of sentences to summarize