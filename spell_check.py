#!/usr/bin/env python

from bloom_filter import BloomFilter
import argparse

parser = argparse.ArgumentParser(
    description='Spell checking utility for a body of text using a list' +
    ' of correctly spelled words'
)

parser.add_argument('text_file', metavar='TXT_FILE', type=str,
                    help='Text file to spell check')
parser.add_argument('--num-bits', metavar='BITARRAY_LENGTH', type=int,
                    dest='num_bits',
                    help='Number of bits in the bitarray of the bloom filter')
parser.add_argument('--dictionary', metavar='DICTIONARY', type=str,
                    dest='dictionary', default='text/wordlist-utf8.txt',
                    help='Name of file with a list of correctly spelled words')

args = parser.parse_args()

if args.num_bits:
    b = BloomFilter(k=args.num_bits)
else:
    b = BloomFilter()

with open(args.dictionary, 'rb') as f:
    for line in f:
        word = line.strip()
        b.add(word)

misspelled_words = []
with open(args.text_file, 'rb') as f:
    for line in f:
        for word in line.strip().split():
            if not b.check(word):
                misspelled_words.append(word)

print "Misspelled words:", misspelled_words
print ''
