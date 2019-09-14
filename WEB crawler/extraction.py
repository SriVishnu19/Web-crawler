import math
from collections import Counter
import operator
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle

N=3000      #No of documents
idf={}       #To store IDF values
doc_length_1={}

def tf_idf(word, doc):
    # putting tfidf into inverted index
    inverted_index_tfidf[word][doc] = inverted_index_tfidf[word][doc] * idf[word]
    return inverted_index_tfidf[word][doc]

def compute_idf(inverted_index_tfidf):
    df={}
    idf={}
    for key in inverted_index_tfidf.keys():
        df[key] = len(inverted_index_tfidf[key].keys())
        idf[key] = math.log(N / df[key], 2)

    return idf

def compute_all_tf_idf():
    for word in inverted_index_tfidf:
        for doc_key in inverted_indextfidf[word]:
            inverted_index_tfidf[word][doc_key] = inverted_index_tfidf[word][doc]*idf[word]
    return inverted_index_tfidf

def compute_lengths(docs_tokens):
    for code in range(N+1):
        doc_length_1[str(code)] = compute_doc_length(str(code), docs_tokens[str(code)])
    return doc_length_1

def compute_doc_length(code, tokens):
    words_accounted_for = []
    length = 0
    for token in tokens:
        if token not in words_accounted_for:
            length += tf_idf(token, code) ** 2
            words_accounted_for.append(token)
    return math.sqrt(length)

#doc_length=compute_lengths(docs)



def cosine_similarities(query,doc_length):
    length = 0
    cnt = Counter()
    similarity = {}
    query_length=0
    #inverted_indextfidf=compute_all_tf_idf()
    for w in query:
        cnt[w] += 1
    for w in cnt.keys():
        length += (cnt[w]*idf.get(w, 0)) ** 2
        
    query_length=math.sqrt(length)
    
    for word in query:
        wq = idf.get(word, 0)
        if wq != 0:
            for doc in inverted_index_tfidf[word].keys():
                similarity[doc] = similarity.get(doc, 0) + inverted_index_tfidf[word][doc] * wq
      
    for doc in similarity.keys():
        similarity[doc] = similarity[doc] / doc_length[doc] / query_length
             
    return similarity

def retrieve_most_relevant(query_tokens,doc_length):
    similarity=cosine_similarities(query_tokens,doc_length)
    order=sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    return order


def add_page_rank_scores_and_reorder(best_ranked, page_ranks):
    best_dict = dict(best_ranked)
    for doc_code in best_dict:
        best_dict[doc_code] = best_dict[doc_code] + page_ranks[doc_code] * PAGE_RANK_MULTIPLIER

    return rank_docs(best_dict)

def print_output(top,n):
    for i in range(n,n+10):
        l=top[i][0]
        if(links[int(l)]==None):
            exit()
        elif(links[int(l)]!=None):
            print(links[int(l)])
        else:
            break

    
with open('inverted_index.pickle', 'rb') as f:
    inverted_index_tfidf=pickle.load(f)

with open('docs_tokens.pickle', 'rb') as f:
    docs=pickle.load(f)

with open('url.pickle', 'rb') as f:
    links=pickle.load(f)                    #Stores links


idf=compute_idf(inverted_index_tfidf)
doc_length=compute_lengths(docs)


stop_words = set(stopwords.words('english'))
query=str(input("Enter your search:"))
ps = PorterStemmer()

for c in string.punctuation:
    query=query.replace(c,"")           #Removes Punctuations

query = ''.join(i for i in query if not i.isdigit())          #Removes Numbers from the text
query=query.lower()         
f = word_tokenize(query)
f= [ps.stem(x) for x in f if x not in stop_words]              #Removes stop words and performs stemming

unique=set(f)                                                       #To remove duplicates
top=retrieve_most_relevant(unique,doc_length)                              #Similarities using cosine similarity
n=0
print_output(top,n)
n=n+10
u=input("Do you want more pages? Enter yes/no:")
while(u=='yes'):
    print(n)
    print_output(top,n)
    n=n+10
    u=input("Do you want more pages? Enter yes/no:")

