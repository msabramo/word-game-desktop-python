import copy, datetime, Utils, Board
pickle = Utils.import_cPickle_or_pickle()


class Game(object):

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.board = Board.Board(12, 7)
        self.orig_board = copy.deepcopy(self.board)
        self.info = dict(start_time=datetime.datetime.now().replace(microsecond=0))
        self.total_score = 0
        for attr in ('board_column_change_callbacks',
                     'word_tiles_change_callbacks',
                     'word_tile_added_callbacks',
                     'word_tiles_removed_callbacks',
                     'word_added_callbacks',
                     'no_words_left_callbacks',
                     'word_tiles',
                     'words'):
            setattr(self, attr, [])

    @staticmethod    
    def load(filename):
        print('Loading game from %s' % filename)
        return pickle.load(file(filename, 'rb'))

    def save(self, filename):
        return pickle.dump(self, file(filename, 'wb'))

    def __getstate__(self):
        """
        We don't want to pickle the dictionary, since it's huge and we
        omit callbacks, becauswe the pickle module can't handle
        instance methods.
        """
        
        d = self.__dict__.copy()
        d.update(dictionary=None,
                 board_column_change_callbacks=[],
                 word_tiles_change_callbacks=[],
                 word_tile_added_callbacks=[],
                 word_tiles_removed_callbacks=[],
                 word_added_callbacks=[],
                 no_words_left_callbacks=[])
        return d

    def notify_board_column_change(self, col_idx, letter_added=None, letter_removed=None):
        for cb in self.board_column_change_callbacks:
            cb(col_idx, self.board.cols[col_idx],
               letter_added=letter_added,
               letter_removed=letter_removed)

    def notify_word_tiles_change(self):
        for cb in self.word_tiles_change_callbacks:
            cb(self.current_word())

    def notify_word_tile_added(self, letter):
        for cb in self.word_tile_added_callbacks:
            cb(letter)

    def notify_word_tiles_removed(self, num):
        for cb in self.word_tiles_removed_callbacks:
            cb(num)

    def notify_word_added(self):
        for cb in self.word_added_callbacks:
            cb(self.current_game_time(), self.current_word(), self.current_word_score(), self.total_score)
    def notify_no_words_left(self):
        for cb in self.no_words_left_callbacks:
            cb()

    def push_tile(self, col_idx):
        letter = self.board.pop_from_column(col_idx)
        self.notify_board_column_change(col_idx, letter_removed=letter)
        self.word_tiles.append((letter, col_idx))
        self.notify_word_tiles_change()
        self.notify_word_tile_added(letter)

    def pop_tile(self):
        self.pop_tiles(num=1)

    def pop_all_tiles(self):
        self.pop_tiles(num=len(self.word_tiles))

    def pop_tiles(self, num):
        for _ in range(num):
            letter, col_idx = self.word_tiles.pop()
            self.board.push_to_column(col_idx, letter)
            self.notify_board_column_change(col_idx, letter_added=letter)

        self.notify_word_tiles_change()
        self.notify_word_tiles_removed(num)

    def check_words_left(self):
        if not self.board.words_left(self.dictionary, max_num_words=1) and \
           not self.dictionary.has_word(self.current_word()):
            self.notify_no_words_left()
            
    def add_word(self):
        if len(self.word_tiles) > 0:
            self.total_score += self.current_word_score()
            self.words.append((self.word_tiles, self.current_game_time()))
            self.notify_word_added()
            num_tiles_to_remove = len(self.word_tiles)
            self.word_tiles = []
            self.notify_word_tiles_removed(num_tiles_to_remove)
            self.notify_word_tiles_change()
            self.check_words_left()

    def current_word(self):
        return ''.join([tup[0] for tup in self.word_tiles])

    def current_word_score(self):
        return self.calc_word_score(self.current_word())

    def calc_word_score(self, word):
        return len(word) * sum(map(Utils.num_points_for_letter, word))

    def current_game_time(self):
        return datetime.datetime.now().replace(microsecond=0) - self.info['start_time']
