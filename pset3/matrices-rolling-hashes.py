# PSET 3, Problem 3-3

import sys
import string
import random
import time

t = [
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'c'],
    ]

s = [
        ['b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'c'],
    ]

def isSymmetricMatrix(m):
    n = len(m)

    # Some error detection code, we want to be sure t is a n \by n matrix
    for i in range(0, n):
        if n != len(m[i]):
            print "ERROR: Bad matrix, it needs to be", n, "by", n, ". Found", len(m[i]), "columns at row", i
            sys.exit(1)

    print n, "by", n

def printMatrix(m):
    for i in range(len(m)):
        print m[i]

# The O(n^2 k^2) naive solution. Note that in practice, due to large 
# constants in the O(n^2 k) and O(n^2) solutions, this actually performs 
# faster for all n < n_0. Try finding what that n_0 is. That is, if we keep
# increasing n, after which point will the k^2 in the n^2 k^2 solution 
# really start to increase the runtime of the naive solution, to the point
# that it becomes slower than the rolling hash solutions.
def searchSlowly(m, s):
    n = len(m)
    k = len(s)
    compares = 0

    for i in range(0, n):
        for j in range(0, n):
            rowsLeft = n - i
            colsLeft = n - j

            if k <= rowsLeft and k <= colsLeft:
                match = True

                for t in range(0, k):
                    if match == False:
                        break
                    for q in range(0, k):
                        compares += 1
                        if m[i + t][j + q] != s[t][q]:
                            match = False
                            break
                
                if match == True:
                    #print "Found match after", compares, "compares at pos. (", i, ",", j, ")"
                    return (i, j)

    #print "Did NOT find match after", compares, "compares."
    return (-1, -1)

# This is the O(n^2 k) solution. Note that large constants associated with
# modular arithmetic actually makes this solution slower than the O(n^2 k^2)
# solution for small enough n. However, for sufficiently large n, this solution will be faster!
def searchFast(m, s):
    n = len(m)
    k = len(s)

    # we hash the n \by n M matrix, store it into HM
    #  - we want to search for a pattern of length k in constant time
    #  - a row of n cells can have n - k + 1 start positions for the pattern of length k
    #    - thus, the HM matrix needs to store n - k + 1 hashes for each row and there are n rows
    #      - HM will be n \by (n - k + 1)
    # we hash the k \by k S matrix, store it into SM
    #  - we hash every row of length k, and there are k rows, so we get k hashes
    #    - SM is an array of k elements

    rh = 0          # the current rolling hash we are computing
    p = 1170581     # the large prime
    b = 26          # the base for the rolling hash: hash(alin) = 'a'*b^3 + 'l'*b^2 + 'i'*b + 'n'

    hs = []         # array with the k rolling hashes for each row in S

    for i in range(0, k):
        rh = 0
        for j in range(0, k):
            code = ord(s[i][j]) - ord('a')
            rh = (rh * b + code) % p
        #print "Computed rolling hash for row", i, "", s[i], "in S:", rh
        hs.append(rh)

    rh = []         # array with the current k rolling hashes of the k \by k submatrix of M that starts at pos (i, 0)
    exp = 1         # for k = 3, the rolling hash of 'cbd' is 2 * 26^2 + 1 * 26^1 + 3, and when we try and extend this
                    # rolling hash later on, we will need to remove the first character so we need to have 26^2 at hand

    for i in range(0, k - 1):
        rh.append(0)
        exp = (exp * b) % p
    rh.append(0)
                    
    for i in range(0, n - k + 1):   # we do this for every row almost: O(n)
        # compute the first set of k rolling hashes starting at (i, 0): O(k^2)
        for r in range(0, k):
            rh[r] = 0
            for c in range (0, k):
                code = ord(m[i + r][c]) - ord('a')
                rh[r] = (rh[r] * b + code) % p

        # the (n+1) is there so that we verify the match after the last iteration
        for j in range(k, n + 1):   # we do this for every column almost: O(n)
            # j is the column we will append to the rolling hash
            # j - k is the column where the rolling hash starts

            # check if it matches the rolling hash of the S matrix: O(k)
            match = True
            for r in range(0, k):
                if rh[r] != hs[r]:
                    match = False
                    break

            # make sure it's a real match: O(k^2) 
            # (this will not be entered more than a few times, if hashing works well)
            if match:
                realmatch = True
                for r in range(0, k):
                    if realmatch == False:
                        break
                    for c in range(0, k):
                        if m[i + r][j - k + c] != s[r][c]:
                            realmatch = False
                            print "WARNING: False positive!"
                            break
                
                if realmatch:
                    #print "Match found starting at position (", i, ",", j-k, ")."
                    return (i, j - k)


            # if not, extend the previously computed hashes: O(k)
            if j < n:
                for r in range(0, k):
                    # remove the character from column j-k from the rolling hash: O(1)
                    code = ord(m[i + r][j - k]) - ord('a')
                    rh[r] = (rh[r] - code * exp) % p
                    # add the character in column j to the rolling hash: O(1)
                    code = ord(m[i + r][j]) - ord('a')
                    rh[r] = (rh[r] * b + code) % p
                     
            # ... and check again
                        
        # if still not, then move to the next row

    #print "No match found!"
    return (-1, -1)

# This is the O(n^2) solution. Note that large constants associated with
# modular arithmetic actually makes this solution slower than the O(n^2 k^2)
# solution for small enough n. However, for sufficiently large n, this solution will be faster!
def searchFaster(m, s):
    n = len(m)
    k = len(s)

    # we hash all partial rows of length k in the n \by n M matrix, store it into HM
    #  - we want to search for a row pattern of length k in constant time
    #  - a row of n cells can have n-k+1 start positions for the pattern of length k
    #    - thus, the HM matrix needs to store n-k+1 hashes for each of the n rows
    #      - HM will be n \by (n-k +1)
    #
    # we hash all partial columns of length k in the n \by (n-k+1) HM matrix, store it into HHM
    #  - we want to search for a k \by k pattern in constant time
    #  - the HHM matrix needs tore n-k+1 hashes for each of the n-k+1 columns
    #    - HHM will be (n-k+1) \by (n-k+1)
    #
    # we hash all rows in the k \by k S matrix, store it into HS
    #  - we hash all rows, and there are k rows, so we get k hashes
    #    - HS is an array of k elements
    # 
    # we hash the SM column vector, an obtain a single number that is the hash of S
    #  - we store into HHS

    rh = 0          # the current rolling hash we are computing
    p = 1170581     # the large prime
    b = 26          # the base for the rolling hash: hash("alin") = 'a'*b^3 + 'l'*b^2 + 'i'*b + 'n'
    #inv26 = pow(26, p-2, p) # the multiplicative inverse for 10 in Z_p (we need this when we decrease our exponent)
    #print "Multiplicative inverse of 26 mod", p, "=", inv26
    inv26 = 1035514
    #inv10 = pow(10, p-2, p) # the multiplicative inverse for 10 in Z_p (we need this when we decrease our exponent)
    #print "Multiplicative inverse of 10 mod", p, "=", inv10
    inv10 = 1053523

    if (10 * inv10) % p != 1:
        print "INTERNAL ERROR: You shouldn't have messed with the primes. Multiplicative inverse for 10 is incorrect."
        return (-1, -1)

    if (26 * inv26) % p != 1:
        print "INTERNAL ERROR: You shouldn't have messed with the primes. Multiplicative inverse for 26 is incorrect."
        return (-1, -1)

    hs = []         # array with the k rolling hashes for each row in S
    hhs = 0         # hash of the S matrix

    hm = []         # n \by (n-k+1) matrix with row hashes of M
    hhm = []        # (n-k+1) \by (n-k+1) matrix with row and column hashes of M

    # compute the row hashes of the k rows in S: O(k^2)
    for i in range(0, k):
        rh = 0
        for j in range(0, k):
            code = ord(s[i][j]) - ord('a')
            rh = (rh * b + code) % p
        #print "Computed rolling hash for row", i, "", s[i], "in S:", rh
        hs.append(rh)

    # compute hash of single column matrix HS: O(k)
    # we interpret each number in the column as a string and we hash all the numbers as one long string
    rh = 0
    for i in range(0, k):
        numstr = str(hs[i])  # the length of this string will never be greater than the length of our prime p
        for j in range(len(numstr)):
            code = ord(numstr[j]) - ord('0')
            rh = (rh * 10 + code) % p   # this time our base is 10, because we are hashing numbers in [0, 9]
    hhs = rh
    #print "Hash of S:", hhs

    exp = 1         # Example: for k = 3, the rolling hash of 'cbd' is 2 * 26^2 + 1 * 26^1 + 3, and when we try and extend this
                    # rolling hash later on, we will need to remove the first character so we need to have 26^2 at hand

    for i in range(0, k - 1):
        exp = (exp * b) % p
     
    # compute the partial row hashes of M, store them in HM: O(n^2)
    for i in range(0, n):   # we do this for every row: O(n)
        # append a new row to the HM matrix
        hm.append([])

        # compute the rolling hash starting at (i, 0): O(k)
        rh = 0
        for j in range (0, k):
            code = ord(m[i][j]) - ord('a')
            rh = (rh * b + code) % p

        # add the hash to HM
        hm[i].append(rh)

        for j in range(k, n):   # we do this for all remaining positions where the rolling hash can start: O(n - k + 1)
            # remove the character from column j-k from the rolling hash: O(1)
            code = ord(m[i][j - k]) - ord('a')
            rh = (rh - code * exp) % p
            # add the character in column j to the rolling hash: O(1)
            code = ord(m[i][j]) - ord('a')
            rh = (rh * b + code) % p
            hm[i].append(rh)

    #print "HM matrix:"
    #for i in range(0, n):
        #print hm[i]

    # initialize the (n-k+1) \by (n-k+1) HHM matrix: O((n-k+1)*(n-k+1))
    hhm = []
    for i in range(0, n - k + 1):
        hhm.append([])
        for j in range(0, n - k + 1):
            hhm[i].append([])

    # compute the column hashes in HM, store them in HHM: O((n-k+1)*n)
    for j in range(0, n - k + 1):   # we do this for every column: O(n-k+1)
        # our "base" for the rolling hashes changes to 10 when we hash HM, and
        # we still have to keep track of the multiplier of the first digits that
        # were added to the hash, so we can remove them fast enough
        exp = inv10
        
        # compute the first rolling hash of column j: O(k)
        rh = 0
        for i in range(0, k):
            numstr = str(hm[i][j])  # the length of this string will never be greater than the length of our prime p
            #print "appending", numstr 
            for c in range(len(numstr)):
                code = ord(numstr[c]) - ord('0')
                rh = (rh * 10 + code) % p   # this time our base is 10, because we are hashing numbers in [0, 9]
                exp = (exp * 10) % p
            #print "rolling hash after adding", i+1, "elements:", rh, "exp:", exp
            #print

        #print "exp after hashing first", k, "elements on col. ", j, "->", exp
        # add the hash to HM
        #print "(", 0, ",", j, ")"
        hhm[0][j] = rh

        # extend the rolling hash of column j: O(n-k + 1)
        for i in range(k, n):
            # note that here we update the exponent as we remove and add digits to the rolling hash.
            # this is because it is possible to remove a big number and add a smaller one, which will
            # decrease the size of the hash, and thus of the exponent. so we keep track of this.
                        
            # remove the number from row i-k from the rolling hash: O(1)
            numstr = str(hm[i-k][j])  # the length of this string will never be greater than the length of our prime p
            for c in range(len(numstr)):
                code = ord(numstr[c]) - ord('0')
                rh = (rh - code * exp) % p  # this time our base is 10, because we are hashing numbers in [0, 9]
                exp = (exp * inv10) % p
            #print "removing: ", numstr, ", rh ->", rh, ", exp ->", exp

            # append the new number at row i to the rolling hash: O(1)
            numstr = str(hm[i][j])  # the length of this string will never be greater than the length of our prime p
            for c in range(len(numstr)):
                code = ord(numstr[c]) - ord('0')
                rh = (rh * 10 + code) % p   # this time our base is 10, because we are hashing numbers in [0, 9]
                exp = (exp * 10) % p
            #print "adding: ", numstr, ", rh ->", rh, ", exp ->", exp
           
            #print "(", i-k+1, ",", j, ")"
            hhm[i - k + 1][j] = rh

    #print "HHM matrix (", n - k + 1, "by", n - k + 1, "): "
    #for i in range(0, n-k+1):
    #    print hhm[i]

    for i in range(0, n-k+1):
        for j in range(0, n-k+1):
            # check if we match the 2D rolling hash of the S matrix: O(1)
            #
            # make sure it's a real match: O(k^2) 
            # (this will not be entered more than a few times, if hashing works well)
            if hhs == hhm[i][j]:
                realmatch = True
                for r in range(0, k):
                    if realmatch == False:
                        break
                    for c in range(0, k):
                        if m[i + r][j + c] != s[r][c]:
                            realmatch = False
                            print "WARNING: False positive!"
                            break
                
                if realmatch:
                    #print "Match found starting at position (", i, ",", j, ")."
                    return (i, j)
                    
    #print "No match found!"
    return (-1, -1)

def randomLetter():
    return random.choice(string.letters.lower())    

def randomRow(l):
    row = []
    for i in range(l):
        row.append(randomLetter())
    return row

def randomMatrix(l):
    matrix = []
    for i in range(l):
        matrix.append(randomRow(l))
    return matrix

def randomSubmatrix(m, size):
    n = len(m)
    s = []
    row = random.randrange(0, n - size + 1)
    col = random.randrange(0, n - size + 1)
    for i in range(size):
        s.append([])
        for j in range(size):
            s[i].append(m[row + i][col + j])
    return s, row, col

#print "Checking T matrix is symmetric..."
#isSymmetricMatrix(t)

#print "Checking S matrix is symmetric..."
#isSymmetricMatrix(s)

#print "M matrix:"
#for i in range(0, len(t)):
#    print t[i]

minn = 500
maxn = 1000
mink = 20
maxk = 200
maxtests = 50
for i in range(maxtests):
    print "Test", i+1, "out of", maxtests
    print "==========================="
    n = random.randint(minn, maxn)
    print " - Random matrix size:", n
    k = random.randint(mink, maxk)
    print " - Random submatrix size:", k
    rt = randomMatrix(n)
    rs, i, j = randomSubmatrix(rt, k)
    print " - Random submatrix location: (", i, ",", j, ")"
    print 

    t0 = time.time()
    (ii, jj) = searchSlowly(rt, rs)
    if ii == -1 and jj == -1:
	    print "ERROR: A match should have been found at (", ii, ",", jj, ")."
	    printMatrix(rt)
	    printMatrix(rs)
	    sys.exit(1)
    t1 = time.time()
    tt = t1 - t0
    print " * O(n^2 k^2): Found match at (", i, ",", j, ") in ", tt, "seconds."


    t0 = time.time()
    (ii, jj) = searchFast(rt, rs)
    if ii == -1 and jj == -1:
	    print "ERROR: A match should have been found at (", ii, ",", jj, ")."
	    printMatrix(rt)
	    printMatrix(rs)
	    sys.exit(1)
    t1 = time.time()
    tt = t1 - t0
    print " * O( n^2 k ): Found match at (", i, ",", j, ") in ", tt, "seconds."

    t0 = time.time()
    (ii, jj) = searchFaster(rt, rs)
    if ii == -1 and jj == -1:
	    print "ERROR: A match should have been found at (", ii, ",", jj, ")."
	    printMatrix(rt)
	    printMatrix(rs)
	    sys.exit(1)
    t1 = time.time()
    tt = t1 - t0
    print " * O(  n^2  ): Found match at (", i, ",", j, ") in ", tt, "seconds."

    print
