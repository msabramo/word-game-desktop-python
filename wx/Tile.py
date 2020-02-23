import random


class Tile(object):

    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        if self.letter is not None:
            return '[%s %2d]' % (self.letter, self.num_points)
        else:
            return '      '

    @property
    def num_points(self):
##         return num_points_for_letter(self.letter)
        for point_value, letters in self._letter_point_values:
            if self.letter in letters: return point_value

    @staticmethod
    def get_random_tiles():
        tiles = map(Tile, list(
            1 * 'KJXQZ' + 2 * 'BCMPFHVWY' + 3 * 'G' + 4 * 'LSUD' +
            6 * 'NRT' + 8 * 'O' + 9 * 'AI' + 12 * 'E'))
        random.shuffle(tiles)
        return tiles


_letter_point_values = (
    (1, 'EAIONRTLSU'),
    (2, 'DG'),
    (3, 'BCMP'),
    (4, 'FHVWY'),
    (5, 'K'),
    (8, 'JX'),
    (10, 'QZ'))

def num_points_for_letter(letter):
    for point_value, letters in self._letter_point_values:
        if letter in letters: return point_value

