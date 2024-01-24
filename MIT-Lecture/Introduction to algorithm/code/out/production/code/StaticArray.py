class StaticArray:
    def __init__(self, n):
        self.data = [None] * n

    def get_at (self, i):
        self.check(i)
        return self.data[i]

    def set_at(self, i, x):
        self.check(i)
        self.data[i] = x

    def check(self, i):
        if not (o <= i < len(self.data)) : raise IndexError


def birthday_match(students):
    '''
    '''

    n = len(students) # O(1)
    record = StaticArray(n) O(n)

    for k in range(n): #n
        (name1, bday1) = students[k] #O(1)

        for i in range(k):  # k
            (name2, bday2) = record.get_at(i)
            if bday1 == bday2:
                return (name1, name2)
        record.set_at(k, (name1, bday1))

    return None
