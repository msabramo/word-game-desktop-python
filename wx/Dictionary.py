class Dictionary(object):

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.word_set = set()
        self.prefix_sets = [set() for _ in range(16)]
        self.prefix_len_range = range(4, 13)
        self.load()

    def load(self):
        for first_letter in map(chr, range(ord('a'), ord('z') + 1)):
            words_file = file('%s/twl_%s.txt' % (self.dir_path, first_letter))
            words = [line.strip() for line in words_file]
            words_file.close()
            self.word_set.update(words)
            
        for i in self.prefix_len_range:
            for word in self.word_set:
                if len(word) >= i:
                    self.prefix_sets[i].add(word[0:i])
            
    def has_word(self, word):
        if not word or len(word) < 3: return False
        else:                         return word in self.word_set
    
    def has_word_starting_with(self, word_prefix):
        i = len(word_prefix)
        
        if i < len(self.prefix_sets) and len(self.prefix_sets[i]) > 0:
            word_prefix_frag = word_prefix[0:i]
            if word_prefix_frag not in self.prefix_sets[len(word_prefix_frag)]:
                return False

        return True
    

class FakeDict(object):
    
    def has_word(self, word): return True
    def has_word_starting_with(self, word_prefix): return True
