
# Library imports
import json
import string

class Lang:

    NEGATE = "na'"

    def __init__(self, lang_file="lang.json"):

        with open(lang_file, "r") as fp:
            self.data = json.load(fp=fp)
            self.rdata = {}
            for enc, dat in self.data.items():
                for word in dat["def"]:
                    self.rdata[word] = (enc, True)
                for word in dat["neg"]:
                    self.rdata[word] = (enc, False)

    def translate_word(self, word: str):
        """ Translate word from English """
        word = word.lower()
        if word in self.rdata.keys():
            trans, pos = self.rdata[word]
            return trans if pos else self.NEGATE+trans
        else:
            return "[{}]".format(word)

    def untranslate_word(self, word):
        """ Translate word into English """
        word = word.lower()
        neg = False
        if word.startswith(self.NEGATE):
            neg = True
            word = word[len(self.NEGATE):]
        if word in self.data.keys():
            if neg:
                return self.data[word]["neg"][0]
            else:
                return self.data[word]["def"][0]
        else:
            return "[{}]".format(word)

    def translate_string(self, in_string):
        """ Translate string of words from English """
        translation = ""
        for word in in_string.split(" "):
            clean_word = self._strip_punctuation(word)
            translation += self.translate_word(clean_word)
            if word.endswith(('.', ',')):
                translation += word[-1]
            translation += " "
        return translation.strip()

    def untranslate_string(self, in_string):
        """ Translate string of words into English """
        translation = ""
        for word in in_string.split(" "):
            clean_word = self._strip_punctuation(word)
            translation += self.untranslate_word(clean_word)
            if word.endswith(('.', ',')):
                translation += word[-1]
            translation += " "
        return translation.strip()

    def dictionary(self):
        return {eng: trans if pos else self.NEGATE+trans for eng, (trans, pos) in self.rdata.items()}

    def _strip_punctuation(self, in_string):
        punc = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~' # list doesn't include apostrophe '
        return in_string.translate(str.maketrans('', '', punc))


if __name__ == "__main__":

    l = Lang()

    eng = "make circle, break apple, fire candle, free spirit"
    resp = l.translate_string(eng)
    print(eng)
    print(resp)
    print(l.untranslate_string(resp))

    pass
