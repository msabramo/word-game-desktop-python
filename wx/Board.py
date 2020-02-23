import copy, datetime, random


class Board(object):

    def __init__(self, num_cols, num_rows):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.num_tiles = num_cols * num_rows
        
        tiles = list(
            1 * 'KJXQZ' + 2 * 'BCMPFHVWY' + 3 * 'G' + 4 * 'LSUD' +
            6 * 'NRT' + 8 * 'O' + 9 * 'AI' + 12 * 'E')
        random.shuffle(tiles)
        self.cols = [
            [tiles.pop() for row_idx in range(num_rows)] for col_idex in range(num_cols)]

    def pop_from_column(self, col_idx):
        try:     return self.cols[col_idx].pop(0)
        finally: self.num_tiles -= 1

    def push_to_column(self, col_idx, letter):
        try:     self.cols[col_idx].insert(0, letter)
        finally: self.num_tiles += 1
        
    def load_from_file(self, filename):
        self.load_from_string(file(filename).read())

    def load_from_string(self, input_str):
        def transposed(lists): # http://code.activestate.com/recipes/410687/
            if not lists: return []
            return map(lambda *row: list(row), *lists)

        rows = [[letter for letter in line] for line in input_str.splitlines()]
        self.cols = transposed(rows)

        self.num_tiles = 0
        for col in self.cols:
            self.num_tiles += len([item for item in col if item and item.isalpha()])

        print('load_from_string: num_tiles = %d' % self.num_tiles)

    def words_left(self, dictionary, max_num_words=1000):
##         start = datetime.datetime.now()

        word_set = set()
        queue = [('', self)]

        while len(queue) and len(word_set) < max_num_words:
            acc, board = queue.pop(0)
            if len(acc) > 14: return word_set
                
            for col_idx in range(len(board.cols)):
                if len(board.cols[col_idx]) == 0: continue
                board_copy = copy.deepcopy(board)
                letter = board_copy.pop_from_column(col_idx)
                
                if letter and letter.isalpha():
                    acc_new = acc + letter
                    if len(acc_new) >= 3 and dictionary.has_word(acc_new):
                        word_set.add(acc_new)
                    if len(acc_new) < 4 or dictionary.has_word_starting_with(acc_new):
                        queue.append((acc_new, board_copy))

##         end = datetime.datetime.now()
##         print('words_left: elapsed time: %s' % (end - start))

        return list(word_set)
