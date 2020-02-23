class PlayedWord(object):
    
    def __init__(self, word_tiles, time):
        self.word_tiles = word_tiles
        self.time = time

    @property
    def word(self):
        return ''.join([tile.letter for tile in self.word_tiles])


