import math

def peak1d(a, i, j):
    #m = int(math.floor((i+j)/2))
    print "Looking at range: [", i, "", j, "]"
    m = (i + j) // 2

    print "Splitting on index", m, "= floor((", i, "+", j,") / 2)"
    if m >= 1 and a[m - 1] > a[m]:
        return peak1d(a, i, m - 1)
    elif m < len(a) - 1 and a[m] < a[m + 1]:
        return peak1d(a, m + 1, j)
    else: # a[m - 1] <= a[m] >= a[m + 1]
        return m;

#v = [1, 2, 3, 4, 5, 6]
#v = [1, 2, 3, 4, 5]
#v = [5, 4, 3, 2, 1]
#v = [5, 4, 3, 2]
#v = [1, 2, 3, 2, 1]
v = [1, 2, 3, 2]

print "Finding a peak in", v
p = peak1d(v, 0, len(v) - 1)

print "1D peak found at a[", p, "] =", v[p]

