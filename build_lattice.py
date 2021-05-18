import ahocorasick
import time
import networkx
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from build_vocab import read_vocab


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab-file', required=True, type=Path)
    parser.add_argument('--graph-file', default=None, type=Path)
    args = parser.parse_args()
    vocab_file = args.vocab_file  # 'data/vocab.txt'
    graph_file = args.graph_file

    vocab = read_vocab(vocab_file)
    sample_sentence = '吾輩は猫である。名前はまだない。'

    trie = build_trie(vocab)
    lattice = build_lattice(trie, sample_sentence)

    if graph_file is not None:
        networkx.draw(lattice, with_labels=True)
        plt.savefig(graph_file)

    return


def build_trie(vocab):
    # Build Trie
    trie = ahocorasick.Automaton()

    # Add words
    t = time.time()
    for idx, (word, freq) in enumerate(vocab.items()):
        trie.add_word(word, (idx, freq, word))

    elapsed = time.time() - t
    print('elapsed time: {:.4f} [sec]'.format(elapsed))

    # Check Trie
    assert '私' in trie
    assert '猫' in trie
    assert 'Hoge' not in trie

    # Enable Aho-Corasick search
    trie.make_automaton()

    return trie


def build_lattice(trie, sentence):
    # Build lattice graph
    G = networkx.DiGraph()
    add_sos, add_eos = True, True

    # Add nodes
    node_idx = 0
    if add_sos:
        G.add_node(node_idx, span=(0, 0), word='<S>')
        node_idx += 1

    for (end_idx, (insert_order, freq, word)) in trie.iter(sentence):
        start_idx = end_idx - len(word) + 1
        span = (start_idx, end_idx + 1)
        assert sentence[span[0]:span[1]] == word
        G.add_node(node_idx, span=span, word=word)
        print(f"{node_idx:2d}|{'　'*span[0]}{word}{'　'*(len(sentence)-len(word)-span[0])}|{span}")
        node_idx += 1

    if add_eos:
        G.add_node(node_idx, span=(len(sentence), len(sentence)), word='<\S>')

    # Add edges
    nodes = G.nodes()
    for i in range(len(nodes)):
        cur_node = nodes[i]
        for j in range(i, len(nodes)):
            next_node = nodes[j]
            if cur_node['span'][1] == next_node['span'][0]:
                G.add_edge(i, j)

    return G


if __name__ == '__main__':
    main()
