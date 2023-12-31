# import re
# import gensim
# from gensim.models import Phrases
# from gensim.models.phrases import Phraser
# from gensim import corpora
# from gensim.models import LdaModel
# import spacy

# def preprocess_text(text, spacy_model):
#     text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
#     doc = spacy_model(text)
#     tokens = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words]
#     return tokens

# def run_lda_algorithm(content, existing_topics, spacy_model):
#     processed_content = preprocess_text(content, spacy_model)
#     print(processed_content, "              pppppppppppppppppppppppppppppppppppppp")
    
#     # Create bigrams
#     bigram = Phraser(Phrases([processed_content], min_count=1, threshold=1))

#     # Apply bigrams
#     processed_content_bigram = bigram[processed_content]

#     # Create a dictionary and corpus
#     id2word = corpora.Dictionary([processed_content_bigram])
#     corpus = [id2word.doc2bow(processed_content_bigram)]

#     # Build LDA model
#     lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=1, passes=10)

#     # Print topics
#     topics = lda_model.print_topics(num_words=5)

#     # Extract topic names from the result
#     topic_names = [re.findall(r'"([^"]*)"', topic[1]) for topic in topics][0]

#     # Extract existing topic names
#     existing_topic_names = [existing_topic.name for existing_topic in existing_topics]
#     print(existing_topics, " this ie eeeeeeeeeeeeeeee")
#     disimilar_scores = []
#     unchanged_list = []
#     for t in topic_names:
#         sc = 0
#         key = -1
#         for index, existing_topic in enumerate(existing_topic_names):
#             similarity_scores = spacy_model(t).similarity(spacy_model(existing_topic))
#             if similarity_scores > sc:
#                 sc = similarity_scores
#                 key = index
#         if sc >= 0.7:
#             unchanged_list.append(existing_topic_names[key])
#         else:
#             disimilar_scores.append(t)
#             unchanged_list.append(t)

#     return disimilar_scores, unchanged_list




import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim import corpora
from gensim.models import LdaModel
import spacy

nlp = spacy.load('en_core_web_sm')
# Define preprocess_text function
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    # tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens





def run_lda_algorithm(content, existing_topics):
    processed_content = preprocess_text(content)
    print(processed_content,"              pppppppppppppppppppppppppppppppppppppp")
    if not processed_content:
        return [],[]

    # Create bigrams
    bigram = Phraser(Phrases([processed_content], min_count=1, threshold=1))

    # Apply bigrams
    processed_content_bigram = bigram[processed_content]

    # Create a dictionary and corpus
    id2word = corpora.Dictionary([processed_content_bigram])
    corpus = [id2word.doc2bow(processed_content_bigram)]

    # Build LDA model
    lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=1, passes=10)

    # Print topics
    topics = lda_model.print_topics(num_words=5)

    # Extract topic names from the result
    topic_names = [re.findall(r'"([^"]*)"', topic[1]) for topic in topics][0]

    # Extract existing topic names
    existing_topic_names = [existing_topic.name for existing_topic in existing_topics]
    print(existing_topics," this ie eeeeeeeeeeeeeeee")
    disimilar_scores=[]
    unchanged_list=[]
    for t in topic_names:
        sc=0
        key=-1
        for index, existing_topic in enumerate(existing_topic_names):
            similarity_scores=nlp(t).similarity(nlp(existing_topic))
            if similarity_scores>sc:
                sc=similarity_scores
                key=index
        if sc>=0.7:
            unchanged_list.append(existing_topic_names[key])
        else:
            disimilar_scores.append(t)
            unchanged_list.append(t)

            

    return disimilar_scores,unchanged_list








































#without spacy


# from gensim.models import Phrases
# from gensim.models.ldamodel import LdaModel
# from gensim import corpora
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk import bigrams, pos_tag
# import re

# def preprocess_text(text):
#     # Tokenize and remove non-alphabetic characters
#     tokens = word_tokenize(text.lower())
#     tokens = [re.sub(r'[^a-zA-Z]', '', token) for token in tokens if token.isalpha()]
    
#     # Part-of-speech tagging and keep only nouns
#     tagged_tokens = pos_tag(tokens)
#     tokens = [token for token, pos in tagged_tokens if pos.startswith('N')]
    
#     # Remove stopwords
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words]
    
#     # Lemmatization
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
#     return tokens

# def run_lda_algorithm(content, existing_topics):
#     processed_content = preprocess_text(content)

#     # Create bigrams
#     bigram = Phrases([processed_content], min_count=1, threshold=1)
#     processed_content_bigram = [bigram[token] for token in bigrams(processed_content)]

#     # Create a dictionary and corpus
#     id2word = corpora.Dictionary([processed_content_bigram])
#     corpus = [id2word.doc2bow(processed_content_bigram)]

#     # Build LDA model
#     lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=1, passes=10)

#     # Print topics
#     topics = lda_model.print_topics(num_words=5)

#     # Extract topic names from the result
#     topic_names = [re.findall(r'"([^"]*)"', topic[1]) for topic in topics][0]

#     # Extract existing topic names
#     existing_topic_names = [existing_topic.name for existing_topic in existing_topics]
    
#     disimilar_scores = []
#     for t in topic_names:
#         similarity_scores = [similar_words(t, existing_topic) for existing_topic in existing_topic_names]
#         max_similarity = max(similarity_scores)
#         if max_similarity < 0.7:
#             disimilar_scores.append(t)

#     return disimilar_scores

# def similar_words(word1, word2):
#     # Implement your own similarity scoring method here
#     # You can use methods like Jaccard similarity, Cosine similarity, etc.
#     # For simplicity, let's just use a placeholder value for now
#     return 0.5  # Placeholder value, replace with your own similarity calculation

# # Example usage
# existing_topics = ["technology", "science", "art"]
# content = "The topic is about new scientific discoveries in technology."
# result = run_lda_algorithm(content, existing_topics)
# print(result)
