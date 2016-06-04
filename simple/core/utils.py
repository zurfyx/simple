

class WordFilter(object):
    """
    Replaces a bad word in a string with something more friendly

    Filter('annoying', '****')

    """
    FILENAME = 'core/bad_words.txt'

    def __init__(self, mask='****'):
        words_file = open(self.FILENAME, 'r')
        self.banned = set(line.strip('\n') for line in words_file)
        self.mask = mask

    def clean(self, text):
        return ' '.join([word if word not in self.banned else self.mask
                         for word in text.split()])
