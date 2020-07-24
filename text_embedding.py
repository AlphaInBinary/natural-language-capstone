from nltk.tokenize import word_tokenize
import string
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
from mappings import Mappings
from collections import Counter
import re

def text_embed(text, glove, all_captions, all_captions_tokens, idfs):
    """
    generates embedding for the text
    
    Parameters
    ----------
    text: string - text to be embedded
    
    Returns
    ----------
    embedded_text: np.array(50,)
    """

    #remove punctuation, all lowercase, split by space
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, "")
    tokens = word_tokenize(text)
    
    #for IDFs - set up counter for words across all documents
    N = len(all_captions)
    
    #set up counter
    c = Counter(all_captions_tokens)
    
    #generate Glove-50 embeddings for all words in text, shape: (len(tokens), 50)
    embedded_text = np.zeros((len(tokens), 50))
    for word_idx in range(len(tokens)):
        nt = c[tokens[word_idx]] #num times word appears across all documents
        idf = idfs[tokens[word_idx]]
        try:
            embedded_text[word_idx] = idf * glove[tokens[word_idx]]
        except KeyError:
            embedded_text = np.zeros((len(tokens), 50))
            break
    
    #sum embeddings across all words in the text, shape: (50,)
    embedded_text = np.sum(embedded_text, axis=0)
    
    return embedded_text

def get_all_captions_tokens(all_captions):
    #join all captions, lowercase, no punctuation, split by space
    all_captions_tokens = " "
    all_captions_tokens = all_captions_tokens.join(all_captions)
    all_captions_tokens = all_captions_tokens.lower()
    for p in string.punctuation:
        all_captions_tokens = all_captions_tokens.replace(p, "")
    all_captions_tokens = word_tokenize(all_captions_tokens)

    return all_captions_tokens

from collections import Counter
from typing import Dict, List, Iterable

def get_words(text: str) -> List[str]:
    """ Returns all the words in a string, removing punctuation.

    Parameters
    ----------
    text : str
        The text whose words to return.

    Returns
    -------
    List[str]
        The words in `text`, with no punctuation.
    """
    _PUNC_REGEX = re.compile("[{}]".format(re.escape(string.punctuation)))

    return _PUNC_REGEX.sub(" ", text.lower()).split()

def _compute_doc_freq(documents: Iterable[str]) -> Counter:
    """ Computes document frequency (the "DF" in "TF-IDF").
        
        Parameters
        ----------
        documents : List(str)
        The list of documents.
        
        Returns
        -------
        collections.Counter[str, int]
        The dictionary's keys are words and its values are number of documents the word appeared in.
        """
    
    df = Counter()
    for doc in documents:
        df.update(set(get_words(doc)))
    
    return df


def inverse_document_frequency(documents: Iterable[str]) -> Dict[str, int]:
    """ Computes the inverse document frequency document frequency (the "DF" in "TF-IDF").
        
        Parameters
        ----------
        documents : List(str)
        The list of documents.
        
        Returns
        -------
        collections.Counter[str, int]
        The dictionary's keys are words and its values are number of documents the word appeared in.
        """
    df = _compute_doc_freq(documents)
    return {word: np.log(len(documents) / (1.0 + count)) for word, count in df.items()}

"""
Run this once to load the glove 50 set *also will need to change path later*, pass into text_embed to use
"""
#path = r"./glove.6B.50d.txt.w2v"
#glove = KeyedVectors.load_word2vec_format(path, binary=False)


