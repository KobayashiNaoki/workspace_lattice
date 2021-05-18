from collections import Counter
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text-file', required=True, type=Path)
    parser.add_argument('--vocab-file', default=None, type=Path)
    args = parser.parse_args()
    text_file = args.text_file  # 'data/neko.txt.wakati'
    vocab_file = args.vocab_file

    counter = Counter()
    with open(text_file) as f:
        for line in f:
            line = line.rstrip('\n')
            words = line.split(' ')
            counter.update(words)

    output = []
    for word, freq in counter.most_common():
        if word == '':
            continue
        output.append(f'{freq}\t{word}')

    f = sys.stdout if vocab_file is None else open(vocab_file, 'w')
    print('\n'.join(output), file=f)
    f.close()

    return


def read_vocab(fname):
    vocab = {}
    with open(fname) as f:
        for line in f:
            line = line.rstrip('\n').lstrip()
            freq, word = line.split('\t')
            vocab[word] = int(freq)

    return vocab


if __name__ == '__main__':
    main()
