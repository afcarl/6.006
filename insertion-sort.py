def insertion_sort(a):
    print "Sorting array:", a

    for i in range(1,len(a)):
        print "Iteration", i, "..."
        elem = a[i];
        j = i - 1;

        while(j >= 0 and a[j] > elem):
            print "Shifting element at pos.", j, "to pos.", j+1
            a[j+1] = a[j]
            j -= 1

        if(i != j+1):
            print "Placing element at pos.", i, " in pos.", j+1
        else:
            print "Element at pos. ", i, "remained there."

        a[j + 1] = elem

        print "Array after iteration", i, ":", a
        print

v = [9, 8, 7, 6, 5, 4]
#v = [1, 2, 3, 4, 5]
#v = [5, 1, 2, 3, 4]
insertion_sort(v)

print "Sorted array:", v
