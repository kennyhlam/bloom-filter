import hashlib


class BloomFilter:
    '''
    Class for a Bloom filter, which can probabilistically determine if
    a member has been added to the filter before (with high probability)

    Can return false positives, but will never return a false negative for
    membership query

    Members cannot be removed from a bloom filter
    '''

    def __init__(self, k=10000, hashes=None):
        '''
        Initializer for BloomFilter class

        Inputs:
        (int) k - length of bitarray
        (func) hashes - function which produces an array of hash values
                        each hash value must be a hexadecimal string
        '''
        self.bitarray = [False]*k
        if hashes:
            self.hashes = hashes
        else:
            self.hashes = BloomFilter.default_hashes

    @staticmethod
    def default_hashes(x):
        '''
        Static method which produces 'multiple hashes' for an input.
        Cryptographic hashes can be sampled to 'produce' many hashes; in
        this case, sha512 is sampled 4 times to produce 4 'different' hashes

        https://en.wikipedia.org/wiki/Bloom_filter

        Inputs:
        (str) x - value to be hashed

        Returns:
        (array) of hexadecimal strings
        '''
        h = hashlib.sha512(x).hexdigest()
        return [h[:32], h[32:64], h[64:96], h[96:]]

    def add(self, member):
        '''
        Adds a member into this bloom filter by updating the bitarray entries
        at the relevant locations specified by the hashes

        Inputs:
        (str) member - string to add into bloom filter

        Returns:
        None
        '''
        for h in self.hashes(member):
            idx = int(h, 16) % len(self.bitarray)
            self.bitarray[idx] = True

    def check(self, member):
        '''
        Queries if a specific member has been added into this bloom filter
        previously, may return a false positive

        Inputs:
        (str) member - string to query the membership of

        Returns:
        (bool) indicating if the member is in the bloom filter
        '''
        for h in self.hashes(member):
            idx = int(h, 16) % len(self.bitarray)
            if self.bitarray[idx] != True:
                return False
        return True
