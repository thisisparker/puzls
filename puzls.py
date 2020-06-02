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
        self.title = self.puzfile.title.strip()
        self.author = self.puzfile.author.strip()

        self.fill = self.puzfile.fill

        filled = [char for char in self.fill if char.isalpha()]
        total = [char for char in self.fill if char != '.']

        self.progress = len(filled)/len(total)

        try:
            self.line_width = os.get_terminal_size().columns
        except:
            self.line_width = 80

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


def list_puzzles(directory):
    abs_path = os.path.abspath(directory)
    puz_paths = glob.glob(os.path.join(abs_path, '*.puz'))
    puzzles = []

    if not puz_paths:
        sys.exit(f'No puz files found in {abs_path}.')

    for path in puz_paths:
        try:
            xw = PuzEntry(path)
        except:
            continue
        
        puzzles.append(xw)

    sorted_puzzles = sorted(puzzles, key=lambda x: x.progress, reverse=True)

    output = '\n'.join(puzzle.list_output for puzzle in sorted_puzzles)

    print(output)

def puzzle_info(puzfile):
    try:
        xw = PuzEntry(puzfile)
    except:
        sys.exit(f'Cannot read {puzfile} as a puz file.')

    print(xw.info_output)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', nargs='?')

    args = parser.parse_args()

    if not args.input:
        list_puzzles('.')

    elif os.path.isdir(args.input):
        list_puzzles(args.input)

    elif os.path.isfile(args.input):
        puzzle_info(args.input)

    else:
        sys.exit(f'Cannot read {args.input} as a file or directory')

if __name__ == '__main__':
    main()
