#!/usr/bin/env python3

import argparse
import glob
import os
import puz
import sys

from itertools import zip_longest

class PuzEntry():
    def __init__(self, path):
        self.path = path

        self.puzfile = puz.read(path)
        self.title = self.puzfile.title
        self.author = self.puzfile.author

        self.fill = self.puzfile.fill

        filled = [char for char in self.fill if char.isalpha()]
        total = [char for char in self.fill if char != '.']

        self.progress = len(filled)/len(total)

        self.line_width = os.get_terminal_size().columns

    @property
    def list_output(self):
        width = self.line_width - 6 - 2
        column = int(width/3)
        inner = column - 4
        return (f'{self.progress:5.0%} {self.title:{column}.{inner}}'
                f'{self.author:{column}.{inner}}{self.path:{column}.{inner}}')

    @property
    def info_output(self):
        puzzle_rows = ['PUZZLE PROGRESS','']
        puzzle_rows.extend(format_puzzle(self.fill, self.puzfile.width))
        puzzle_info = ['PUZZLE INFO', '', self.title, self.author, '',
                        f'{self.progress:.0%} complete']

        column_width = min(int(self.line_width/2), len(puzzle_rows[-1]) + 10)

        display = zip_longest(puzzle_rows, puzzle_info, fillvalue='')

        display_block = '\n'.join(
                [f'{row[0]:{column_width}}{row[1]:{column_width}}'
                    for row in display])

        return display_block



def format_puzzle(fill, width):
    fill_rows = [fill[r:r+width] for r in range(0, len(fill), width)]

    formatted_rows = []

    for row in fill_rows:
        formatted_row = '▐' if row[0] == '.' else '|' 
        for c in range(len(row) - 1):
            formatted_row += row[c]
            if not row[c] == '.' and not row[c+1] == '.':
                div_char = '|'
            elif not row[c] == '.' and row[c+1] == '.':
                div_char = '▐'
            elif row[c] == '.' and not row[c+1] == '.':
                div_char = '▌'
            else:
                div_char = '.'
            formatted_row += div_char
        formatted_row += row[-1]
        formatted_row += '▌' if row[-1] == '.' else '|'

        formatted_row = formatted_row.replace('-','_').replace('.','█')

        formatted_rows.append(formatted_row)

    return formatted_rows


def list_puzzles():
    puz_paths = glob.glob('*.puz')
    puzzles = []

    for path in puz_paths:
        try:
            xw = PuzEntry(path)
        except:
            continue
        
        puzzles.append(xw)

    sorted_puzzles = sorted(puzzles, key=lambda x: x.progress, reverse=True)

    for puzzle in sorted_puzzles:
        print(puzzle.list_output)

def puzzle_info(puzfile):
    try:
        xw = PuzEntry(puzfile)
    except:
        sys.exit(f'Cannot read {puzfile} as a puz file.')

    print(xw.info_output)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--info', '-i')

    args = parser.parse_args()

    if args.info:
        puzzle_info(args.info)

    else:
        list_puzzles()

if __name__ == '__main__':
    main()
