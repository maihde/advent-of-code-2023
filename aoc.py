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
    
def split_intervals(s, t):
    """
    Given two ranges, such as s=(5, 10) and t=(7, 15), returns
    a set of non-overlapping ranges split into:

    lower_difference = range of s lower than t[0]
    intersection = range of s overlapping with t
    upper_difference = range of s higher than t[1]
    """
    if s[0] >= t[0]:
        lower_difference = None
    else:
        lower_difference = ( 
            s[0],
            min(s[1], t[0]-1)
        )

    if s[0] <= t[1] and s[1] >= t[0]:
        intersection = ( 
            max(s[0], t[0]),
            min(s[1], t[1])
        )
    else:
        intersection = None

    if s[1] <= t[1]:    
        upper_difference = None
    else:
        upper_difference = ( 
            max(s[0], t[1]+1),
            s[1]
        )
    
    return lower_difference, intersection, upper_difference

def merge_intervals(intervals):
    # From https://www.geeksforgeeks.org/merging-intervals/#
    # Sort the array on the basis of start values of intervals.
    stack = []
    if not intervals:
        return stack
     
    intervals.sort()
    # insert first interval into stack
    stack.append(intervals[0])
    for i in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1] = stack[-1][0], max(stack[-1][-1], i[-1])
        else:
            stack.append(i)

    return stack

def appendable_iter(a_list):
    """
    Iterates through a_list, allowing for append's to occur at the end.
    ```
    a_list = [1 ,2, 3]
    for value in appendable_iter(a_list):
        ... take action on value, possibly appending to a_list ...
    ```

    Equivalent to:

    ```
    a_list = [ 1, 2, 3]
    ii = 0
    while ii < len(a_list)
        value = a_list[ii]
        ... take action on value, possibly appending to a_list ...
        ii += 1
    ```
    """
    ii = 0
    while ii < len(a_list):
        yield a_list[ii]
        ii += 1

def appendable_pop_iter(a_list):
    """
    Iterates through a_list, allowing for append's to occur at the end while popping items off of a_list.
    ```
    a_list = [1 ,2, 3]
    for value in appendable_pop_iter(a_list):
        ... take action on value, possibly appending to a_list ...
    ```

    Equivalent to:

    ```
    a_list = [ 1, 2, 3]
    while True:
        try:
            value = a_list.pop(0)
        except IndexError:
            break
        ... take action on value, possibly appending to a_list ...
    ```
    """
    while True:
        try:
            value = a_list.pop(0)
        except IndexError:
            break

        yield value