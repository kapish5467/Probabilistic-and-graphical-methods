# construct with factorset()
# can only add (not remove) factors, currently
# use fs.vars to get the set of variables mentioned in the factors
# use fs.factors to get an array of the factors

class factorset:
    def __init__(self):
        self._factors = []
        self._index = {}
        self._vars = set()

    def addfactor(self,f):
        i = len(self._factors)
        self._factors.append(f)
        self._vars.union(f.vars)
        for v in f.vars:
            if v not in self._index:
                self._index[v] = [i]
            else:
                self._index[v].append(i)

    @property
    def vars(self):
        return self._vars

    @property
    def factors(self):
        return self._factors
