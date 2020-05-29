#!/usr/bin/env python3

import argparse
import glob
import os
import puz

class PuzEntry():
    def __init__(self, path):
        self.path = path

        self.puzfile = None
        self.title = None
        self.author = None
        self.progress = 0

    def output(self, width):
        width = width - 6 - 2
        column = int(width/3)
        inner = column - 4
        return ('{puzzle.progress:5.0%} {puzzle.title:{column}.{inner}}'
                '{puzzle.author:{column}.{inner}}{puzzle.path:{column}.{inner}}').format(
                  column=column, inner=inner, puzzle=self)

def main():
    puz_paths = glob.glob('*.puz')
    puzzles = []

    for path in puz_paths:
        xw = PuzEntry(path)
        try:
            xw.puzfile = puz.read(path)
        except:
            continue
        xw.title = xw.puzfile.title
        xw.author = xw.puzfile.author
        
        filled = [char for char in xw.puzfile.fill if char.isalpha()]
        total = [char for char in xw.puzfile.fill if char != '.']

        xw.progress = len(filled)/len(total)

        puzzles.append(xw)

    sorted_puzzles = sorted(puzzles, key=lambda x: x.progress, reverse=True)

    line_width = os.get_terminal_size().columns

    for puzzle in sorted_puzzles:
        print(puzzle.output(line_width))


if __name__ == '__main__':
    main()
