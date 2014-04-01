# PSET3, Problem 3-1

# This is the Mathematically Intricate Technologies (MIT) dictionary
# that you have to work with to implement your Set ADT.
class Dict:
    def __init__(self):
        self.d = {}

    def Search(self, key):
        if key in self.d:
            return self.d[key]
        else:
            return None

    def Insert(self, key, value):
        self.d[key] = value

    def Delete(self, key):
        del self.d[key]

# This is our sample implementation of the Set ADT. Note that we only
# use calls to the MIT dictionary data type to implement our Set ADT. We 
# never use the Python dictionary in our Set ADT implementation. If we did
# we woul have a *much* easier time iterating over the dictionary keys, 
# and thus over the numbers in our Set ADT. The point of this problem 
# however, was to figure out how to implement this easy iteration yourself,
# as opposed to using a keys() method on your dictionary.
class Set:
    def __init__(self):
        self.d = Dict()
        self.l = []
        self.size = 0
        #print "Empty set created, d = ", self.d, ", l =", self.l, ", size = ", self.size
        #self.Print()

    def Has(self, x):
        return self.d.Search(x) != None

    def Insert(self, x):
        if self.Has(x) == False:
            self.l.append(x)
            self.d.Insert(x, self.size)
            self.size += 1

    def Delete(self, x):
        p = self.d.Search(x)
        if p != None:
            if(self.size > 1):
                last = self.l[self.size - 1]    # fetch the last element in the array 
                self.l[p] = last                # replace x with the last element in the array 
                self.d.Delete(last)             # delete dictionary entry for the last element
                self.d.Insert(last, p)          # recreate the dictionary entry for the last element with its new position
            self.d.Delete(x)                # delete x from the dictionary
            self.size -= 1                  # decrease the size of the set by 1
            self.l.pop()                    # delete the last element from the array

    def Print(self, s = ""):
        print s, setToUnorderedList(self)

def unorderedListToSet(a):
    s = Set()

    for i in range(0, len(a)):
        #print "Looking at a[", i, "] = ", a[i]
        
        if s.d.Search(a[i]) == None:    # Takes O(1) time
            #print " * Added a[", i, "] = ", a[i], "to dictionary"
            s.l.append(a[i])            # Takes O(1) time
            s.d.Insert(a[i], s.size)    # Takes O(1) time
            s.size += 1                 # Takes O(1) time
        #else:
            #print " * a[", i, "] = ", a[i], "was previously added"
    
    return s

def setToUnorderedList(s):
    ul = []

    for i in range(0, len(s.l)):
        ul.append(s.l[i])           # Takes O(1) time

    return ul

def unionSets(s1, s2):
    s = Set()

    for i in range(0, len(s1.l)):
        s.Insert(s1.l[i])

    for i in range(0, len(s2.l)):
        s.Insert(s2.l[i])         # Insert() will check if the element already is in the set

    return s

def intersectSets(s1, s2):
    s = Set()

    for i in range(0, len(s1.l)):
        if s2.Has(s1.l[i]) == True:
            s.Insert(s1.l[i])
    
    return s

def diffSets(s1, s2):
    s = Set()

    for i in range(0, len(s1.l)):
        if s2.Has(s1.l[i]) == False:
            s.Insert(s1.l[i])
    
    return s

s1 = unorderedListToSet([1, 2, 1, 3, 2, 5])
s1.Insert(9)
s1.Insert(9)
s1.Print("s1 =")

s2 = unorderedListToSet([1, 2, 7, 8, 8, 9, 2, 4]);
if s2.Has(3) == True:
    print "INTERNAL ERROR: test failed. 3 is not in s2."
s2.Delete(9)
s2.Delete(9)
s2.Print("s2 =")

intersectSets(s1, s2).Print("s1 \intersect s2 =")
unionSets(s1, s2).Print("s1 \union s2 =")
diffSets(s1, s2).Print("s1 - s2 =")

for e in [1, 2, 4, 7, 8, 9]:
    print "Deleting ", e, " from s2..."
    s2.Delete(e)
    s2.Print()
