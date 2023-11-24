import nltk
import re
import unicodedata
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def REMOVE_SPECIAL(string):
    text = re.sub(r'@\S+', ' ', string) #Removes all mentions. OPTIONAL. SEE EXTRACT MENTION BELOW.
    text = re.sub(r'#\S+', ' ', string) #Removes all hashtags. OPTIONAL. SEE EXTRACT MENTION BELOW.
    return text

def TEXT_PREPROCESS(string):
    text = string.lower() #Lowercases all text
    text = re.sub(r'https\S+', ' ', text) #Removes all hyperlinks, OPTIONAL
    text = re.sub('^"?[a-zA-Z]+.? [0-9]+ +20[0-9]{2} ','',text) #Deletes starting date in cell (only for ConsumerReviews data)
    text = re.sub('read full review','',text) #Deletes "Read full review" (only for ConsumerReviews data)
    text = re.sub('mcdonalds|mcdonald\'s|mcdonald s|mcd\b','mcdonalds',text) #Fixes alternative naming
    text = re.sub('&','and',text)
    text = re.sub("ain't",'aint',text)
    text = re.sub("won't",'will not',text)
    text = re.sub("can't",'cannot',text)
    text = re.sub("n't",' not',text)
    text = re.sub("'ll",' will',text)
    text = re.sub("'m",' am',text)
    text = re.sub("'re",' are',text)
    text = re.sub("'ve",' have',text)
    # text = re.sub('<[^>]+>',' ',text) #Ignores all text inside angle brackets. OPTIONAL. CUSTOMIZE
    # text = re.sub(r'[^a-zA-Z0-9\s,.:;<>?!$@#]',' ',text) #Removes everything but letters, numbers,spaces or the special characters included. OPTIONAL. CUSTOMIZE
    text = re.sub('\s+',' ',text) #Removes extra spaces
    return text

def REMOVE_STOPWORDS(preprocessedtext,customstopwords=[],customtodo='add'): #Remove stopwords. By default remove English stopwords. Customstopwords can be defined and then set to "replace" the regular English stopwords, or to "add" to them
    tokenized = word_tokenize(preprocessedtext)
    if customtodo == 'replace':
        stopwlist = customstopwords
    else:
        stopwlist = set(stopwords.words('english') + customstopwords)
    return ' '.join([i for i in tokenized if not i in stopwlist])

def LEMMATIZE(preprocessedtext):
    def get_wordnet_pos(w):
        tag = nltk.pos_tag([w])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)
    lem = WordNetLemmatizer()
    tokenized = word_tokenize(preprocessedtext)
    lemmatized = [lem.lemmatize(w, get_wordnet_pos(w)) for w in tokenized]
    return ' '.join([i for i in lemmatized])

def EXTRACT_DATE(string):
    date = re.findall('^"?[a-zA-Z]+.? [0-9]+ +20[0-9]{2}',string) #Find the starting data on a text
    return date
def EXTRACT_HASH(string):
    hash = re.findall('#\S+',string) #Find all words with # on the left
    return hash
def EXTRACT_MENTION(string):
    hash = re.findall('@\S+',string) #Find all words with @ on the left
    return hash

def REMOVE_SPECIAL_CHAR(string):
    text = re.sub(r'[^a-zA-Z0-9\s,.:;<>?!$@#]', ' ', string)
    text = re.sub(r':','', text)
    text = re.sub(r'"', '', text)
    text = text.replace("?","")
    return(text)

def slugify(value, allow_unicode=False): #converts link into a file name standard
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

