# How to play

Click letter tiles in the first row of the board to form words. Words must be
present in the built-in 178,691 word Tournament Word List and also must be at
least 3 letters long. 

You can use only the tiles in the first row of the board, but each time you
pull a tile, any tiles underneath it move up.

Click **Apply** to accept the currently formed word (only clickable when the
formed word is valid) and add the word's score (total point values of letters
multiplied by the length of the word) to your total score. The game will end
when there are no remaining words on the board.

Click **Undo** to remove the last tile added to the current word area and move it
back to where it came from.

Click **Clear** to remove all tiles in current word area and move them each back
to where they came from.

# Development notes

The `src` directory contains an old version of the game written with [PyGTK][].

The `wx` directory contains the newer version of the game written with [wxPython][].

To set this up on a Mac, install the official Python.org installer for Python
2.7 and then `pip install wxpython`.

To run the game, do:

```
cd wx
python WordUp.py
```


[PyGTK]: https://pypi.org/project/PyGTK/
[wxPython]: https://wxpython.org/
