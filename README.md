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

In this version of python, there's no actual savings between using `ints` or using `True/False` ([everything's a python object and there's refcounters and such](http://stackoverflow.com/questions/10365624/sys-getsizeofint-returns-an-unreasonably-large-value)), but in the spirit of using bits, `True/False` are used within the bitarray instead of actual 0's and 1's.

# Notes
The actual implementation uses a default of `SHA512`, split into blocks of 128 bits each to model four "different" hash functions (as suggested via https://en.wikipedia.org/wiki/Bloom_filter and http://codekata.com/kata/kata05-bloom-filters/). The choice of this function was simply because it's a wide cryptographic hash that can be subsampled; there's no strong rationale for the default length of the bitarray--an ideal length would depend on the number of elements expected to enter the bloom filter, which may not always be known beforehand.

The hashes are assumed to be hexadecimal string outputs. There is no explicit checking that the length supplied or function supplied matches the spec, all inputs are assumed to conform to the requirements spec-d in the code. It is also up to the user to choose a reasonable length of the bitarray which will be sufficient for the hash outputs. 

For example, the default length of the bitarray is 10000, which corresponds to `2710` in hexadecimal. If the hash function only gave outputs of length 3, a large fraction of the bitarray would be unused. While such a situation would still be a functional bloom filter, the results may not be as expected (in this case, a compressed bitarray would lead to more false positives when performing a `check`).

The wikipedia page details possible implementations of a bloom filter which supports removal of entries (also probabilistic), but I've chosen to implement the regular version, which only supports `add`ing of entries and `check`ing of if entries have been added already.

# Spell Checking
A simple script was implemented to perform spell-checking, as suggested in http://codekata.com/kata/kata05-bloom-filters/. Basically, a "dictionary" of words is parsed and entered into a bloom filter, then a input file is parsed and each word is queried against the bloom filter to determine if that word is a valid spelling.

Important to note is that the paths are all relative, assuming you are at the root of the project. Variable results are available, but given the number of words provided in `wordlist.txt`, the number of bits must be much higher than the default for meaningful results.

The dictionary provided through the website was encoded using `iso-8859-1`, but most people providing a file will probably provide it in `utf-8` or `ascii` encoding. The default dictionary, therefore, is a `utf-8` version. An alternate choice for dictionary can be chosen using one of the options, as shown below.

```
(semantic) vagrant:bloom-filter/ (master*) $ python spell_check.py --help
usage: spell_check.py [-h] [--num-bits BITARRAY_LENGTH]
                      [--dictionary DICTIONARY]
                      TXT_FILE

Spell checking utility for a body of text using a list of correctly spelled
words

positional arguments:
  TXT_FILE              Text file to spell check

optional arguments:
  -h, --help            show this help message and exit
  --num-bits BITARRAY_LENGTH
                        Number of bits in the bitarray of the bloom filter
  --dictionary DICTIONARY
                        Name of file with a list of correctly spelled words

(semantic) vagrant:bloom-filter/ (master*) $ python spell_check.py text/body.txt --num-bits 5000000
Misspelled words: ['festing', 'sdlkfj', 'tre', 'wond', 'goned', 'sdfweew', 'wekflj', 'wejfhn']

(semantic) vagrant:bloom-filter/ (master*) $ python spell_check.py text/body.txt --num-bits 5000000 --dictionary text/bad-dict.txt
Misspelled words: []
```