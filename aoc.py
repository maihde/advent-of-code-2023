class InfiniteGrid:
    class RowReference:
        def __init__(self, grid, row):
            self.row = row
            self.grid = grid

        def __getitem__(self, key):
            return self.grid[ (self.row, key) ]
        
        def __setitem__(self, key, value):
            self.grid[ (self.row, key) ] = value

    def __init__(self, shape=(0,0), default='.'):
        self.dat = {}
        self.default = default
        self.ybounds = (0,0)
        self.xbounds = (0,0)

    def __getitem__(self, key):
        if type(key) == tuple:
            return self.dat.setdefault(key[0], dict()).get(key[1], self.default)
        else:
            return InfiniteGrid.RowReference(self, key)

    def __setitem__(self, key, value):
        if type(key) == tuple:
            self.dat.setdefault(key[0], dict())[ key[1] ] = value
            self.ybounds = (
                min(self.ybounds[0], key[0]),
                max(self.ybounds[1], key[0])
            )
            self.xbounds = (
                min(self.xbounds[0], key[1]),
                max(self.xbounds[1], key[1])
            )
        else:
            raise ValueError
        
    def __str__(self):
        rows = []
        for yy in range(self.ybounds[0], self.ybounds[1]+1):
            row = []
            for xx in range(self.xbounds[0], self.xbounds[1]+1):
                row.append( str(self[(yy, xx)]) )
            rows.append("".join(row))
        
        return "\n".join(rows)