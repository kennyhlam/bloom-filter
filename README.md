# Bloom Filter
Python implementation of a bloom filter: https://en.wikipedia.org/wiki/Bloom_filter.  
In a nutshell, the basic algorithm is to:
- have a bitarray, <strong>b</strong>, initialized to all 0's
- take a value, <strong>v</strong>, and hash it with <strong>k</strong> hash functions
- for each of these <strong>k</strong> hash values of <strong>v</strong>, set the corresponding bits in <strong>b</strong> to be 1

When you're checking for membership of some value, <strong>v'</strong>, you can check by:
- hashing <strong>v'</strong> the same <strong>k</strong> times
- for each of these <strong>k</strong> hash values of <strong>v'</strong>, if all the corresponding bits in <strong>b</strong> are 1, it's likely to have been added into the bloom filter
- if you encounter even a single 0 among the <strong>k</strong> hash values, then you know for sure it is not in the bloom filter

In this way, the Bloom filter is a probabilistic data structure, and you can get false positives sometimes if the bits for <strong>v'</strong> have all been set to be 1 by some other <strong>v</strong>. However, you will never get a false negative since Bloom filters don't support member removal (aka if you set the bits for some <strong>v</strong> to be 1, they'll always stay that way).

# Implementation
- python (2.7.12)

# Notes
The actual implementation uses a default of `SHA512`, split into blocks of 128 bits each to model four "different" hash functions (as suggested via https://en.wikipedia.org/wiki/Bloom_filter and http://codekata.com/kata/kata05-bloom-filters/). The choice of this function was simply because it's a wide cryptographic hash that can be subsampled; there's no strong rationale for the default length of the bitarray, this would depend on the number of elements expected to enter the bloom filter.

The hashes are assumed to be hexadecimal string outputs. There is no explicit checking that the length supplied or function supplied matches the spec, all inputs are assumed to conform to the requirements spec-d in the code.

The wikipedia page details possible implementations of a bloom filter which supports removal of entries (also probabilistic), but I've chosen to implement the regular version, which only supports `add`ing of entries and `check`ing of if entries have been added already.

# Spell Checking
A simple script was implemented to perform spell-checking, as suggested in http://codekata.com/kata/kata05-bloom-filters/. Important to note is that the paths are all relative, assuming you are at the root of the project. Variable results are available, but given the number of words provided in `wordlist.txt`, the number of bits must be much higher than the default for meaningful results.

```
(semantic) vagrant:bloom-filter/ (master*) $ python spell_check.py text/body.txt --num-bits 5000000
Misspelled words: ['festing', 'sdlkfj', 'tre', 'wond', 'goned', 'sdfweew', 'wekflj', 'wejfhn']

(semantic) vagrant:bloom-filter/ (master*) $ python spell_check.py text/body.txt --num-bits 5000000 --dictionary text/bad-dict.txt
Misspelled words: []
```