import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import pickle
from sklearn.decomposition import LatentDirichletAllocation as LDA
from pymystem3 import Mystem
from string import punctuation
from stop_words import get_stop_words

from nltk.tag.api import TaggerI
from nltk.tag.util import str2tuple, tuple2str, untag
from nltk.tag.sequential import (
    SequentialBackoffTagger,
    ContextTagger,
    DefaultTagger,
    NgramTagger,
    UnigramTagger,
    BigramTagger,
    TrigramTagger,
    AffixTagger,
    RegexpTagger,
    ClassifierBasedTagger,
    ClassifierBasedPOSTagger,
)
from nltk.tag.brill import BrillTagger
from nltk.tag.brill_trainer import BrillTaggerTrainer
from nltk.tag.tnt import TnT
from nltk.tag.hunpos import HunposTagger
from nltk.tag.stanford import StanfordTagger, StanfordPOSTagger, StanfordNERTagger
from nltk.tag.hmm import HiddenMarkovModelTagger, HiddenMarkovModelTrainer
from nltk.tag.senna import SennaTagger, SennaChunkTagger, SennaNERTagger
from nltk.tag.mapping import tagset_mapping, map_tag
from nltk.tag.crf import CRFTagger
from nltk.tag.perceptron import PerceptronTagger

from nltk.data import load, find
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

RUS_PICKLE = (
    'taggers/averaged_perceptron_tagger_ru/averaged_perceptron_tagger_ru.pickle'
)

# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian") + ['наш', 'сообщество', 'хороший', 'com', 'который', 'самый', 'свой',
                                                  'instagram'] + get_stop_words('ru')

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_ru')


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def remove_URL(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", sample)


def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)
    return text


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[0-9_]+|[www]+[com]+', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in russian_stopwords:
            new_words.append(word)
    return new_words


def _get_tagger(lang=None):
    if lang == 'rus':
        tagger = PerceptronTagger(False)
        ap_russian_model_loc = 'file:' + str(find(RUS_PICKLE))
        tagger.load(ap_russian_model_loc)
    else:
        tagger = PerceptronTagger()
    return tagger


def _pos_tag(tokens, tagset=None, tagger=None, lang=None):
    # Currently only supoorts English and Russian.
    if lang not in ['eng', 'rus']:
        raise NotImplementedError(
            "Currently, NLTK pos_tag only supports English and Russian "
            "(i.e. lang='eng' or lang='rus')"
        )
    else:
        tagged_tokens = tagger.tag(tokens)
        if tagset:  # Maps to the specified tagset.
            if lang == 'eng':
                tagged_tokens = [
                    (token, map_tag('en-ptb', tagset, tag))
                    for (token, tag) in tagged_tokens
                ]
            elif lang == 'rus':
                # Note that the new Russion pos tags from the model contains suffixes,
                # see https://github.com/nltk/nltk/issues/2151#issuecomment-430709018
                tagged_tokens = [
                    (token, map_tag('ru-rnc-new', tagset, tag.partition('=')[0]))
                    for (token, tag) in tagged_tokens
                ]
        return tagged_tokens


def pos_tag(tokens, tagset=None, lang='rus'):
    tagger = _get_tagger(lang)
    return _pos_tag(tokens, tagset, tagger, lang)


def pos_tag_sents(sentences, tagset=None, lang='rus'):
    tagger = _get_tagger(lang)
    return [_pos_tag(sent, tagset, tagger, lang) for sent in sentences]


def preprocess_docs(text):
    text = list(map(strip_html, text))
    text = list(map(remove_between_square_brackets, text))
    text = list(map(replace_contractions, text))
    text = list(map(remove_URL, text))
    text = list(map(preprocess_text, text))
    text = list(map(lambda x: [i for i in x.split(' ') if len(i) > 2 and i not in russian_stopwords], text))
    text = list(map(to_lowercase, text))
    text = list(map(remove_punctuation, text))
    text = list(map(lambda x: ' '.join(x), text))
    text = list(filter(lambda x: len(x) > 2, text))
    text = list(map(lambda x: [i for i in x.split(' ') if pos_tag([i])[0][1] == 'S'], text))

    return list(map(lambda x: ' '.join(x), text))


def group_topics(groups):
    text = []
    for group in groups:
        text.append(group['name'])
        text.append(group['description'])

    docs = preprocess_docs(text)

    n_samples = 1000
    n_features = 100
    n_components = 9
    n_top_words = 2

    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       max_features=n_features,
                                       stop_words='english')

    tfidf = tfidf_vectorizer.fit_transform(docs)

    # Fit the NMF model
    nmf = NMF(n_components=n_components, random_state=1,
              alpha=.1, l1_ratio=.5).fit(tfidf)

    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    return [tfidf_feature_names[i] for topic in nmf.components_ for i in topic.argsort()[:-n_top_words - 1:-1]]
