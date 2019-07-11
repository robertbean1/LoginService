import hashlib, json

class ExtendedDictionary(object):

    
    
    def __init__(self, instance=None, hash_type='NoHash', hash_value=True, use_hex=True):
        self.hashtable = {}
        self.hashing_mode = hash_type
        self.hash_value = hash_value
        self.use_hex = True
        self.n = 0
        if instance:
            if isinstance(instance, list): #Why haven't we been able to do this?
                for n, item in enumerate(instance):
                    self.__setitem__(n, item)
        super().__init__()
        

    def __setitem__(self, k, v):
        if self.hash_value:
            self.hashtable[self._hash(k)] = self._hash(v)
        else:
            self.hashtable[self._hash(k)] = v

    def __getitem__(self, k):
        key_digest = self._hash(k)
        assert key_digest in self.hashtable
        return self.hashtable[key_digest]

    def __len__(self):
        return len(self.hashtable)
    
    def __str__(self):
        return 'ExtendedDictionary(\n    length:' + str(len(self.hashtable)) + '\n    hash:' + self.hashing_mode + '\n)'

    def __next__(self):
        if self.n < len(self):
            self.n += 1
            return self.items[self.n-1]
        else:
            raise StopIteration

    def __iter__(self):
        self.n = 0
        return self

    def _decode(self, bytestr):
        if self.use_hex:
            return bytestr
        else:
            return int(bytestr, 16)

    def __contains__(self, k):
        return self._hash(k) in self.hashtable

    def _hash(self, k):
        if self.hashing_mode == 'NoHash':
            return k
        else:
            k = str.encode(''.join([str(i) for i in str.encode(str(k))]))
            if self.hashing_mode == 'md5':
                return self._decode(hashlib.md5(k).hexdigest())
            if self.hashing_mode == 'SHA1':
                return self._decode(hashlib.sha1(k).hexdigest())
            if self.hashing_mode == 'SHA224':
                return self._decode(hashlib.sha224(k).hexdigest())
            if self.hashing_mode == 'SHA256':
                return self._decode(hashlib.sha256(k).hexdigest())
            if self.hashing_mode == 'SHA384':
                return self._decode(hashlib.sha384(k).hexdigest())
            if self.hashing_mode == 'SHA512':
                return self._decode(hashlib.sha512(k).hexdigest())
            if self.hashing_mode == 'builtin':
                return self._decode(str.encode(str(hash(k) + 2**64)))
        
    def csv_digest(self):
        digest = []
        for k, v in self.hashtable.items():
            digest.append('"' + str(k) + '","' + str(v) + '"')
        return '\n'.join(digest)

    def json_digest(self):
        return json.dumps(self.hashtable, indent=4)

    def load_json(self, contents):
        return json.loads(contents)
    
    @property
    def items(self):
        return tuple(self.hashtable.items())


