import ast
import string
from nltk.corpus import stopwords
# import nltk
# nltk.download("stopwords")


def prettyPrint(message):
    print("\n" + " " + "#"*15 + " " + message + " " + "#"*15)


# Function that extract keys from the nested dictionary
def extract_keys(attr, key):
    if attr == None:
        return "{}"
    if key in attr:
        return attr.pop(key)


# convert string to dictionary
def str_to_dict(attr):
    if attr != None:
        return ast.literal_eval(attr)
    else:
        return ast.literal_eval("{}")


class Text_process:
    stop = []

    def abc(self):
        for word in stopwords.words('english'):
            s = [char for char in word if char not in string.punctuation]
            self.stop.append(''.join(s))

    def text_process(self, mess):
        """
        Takes in a string of text, then performs the following:
        1. Remove all punctuation
        2. Remove all stopwords
        3. Returns a list of the cleaned text
        """
        # Check characters to see if they are in punctuation
        nopunc = [char for char in mess if char not in string.punctuation]

        # Join the characters again to form the string.
        nopunc = ''.join(nopunc)

        # Now just remove any stopwords
        return " ".join([word for word in nopunc.split() if word.lower() not in self.stop])
