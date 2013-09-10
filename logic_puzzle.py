"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    days = range(5)
    Monday, Tuesday, Wednesday, Thursday, Friday = days
    orderings = [x for x in list(itertools.permutations(days))]

    for Hamming, Knuth, Minsky, Simon, Wilkes in orderings:
        if Knuth == Simon + 1:
            for droid, laptop, iphone, tablet, _ in orderings:
                if Wednesday == laptop and\
                   Friday != tablet and\
                   Tuesday in (iphone, tablet):
                    for writer, manager, designer, programmer, _ in orderings:
                        if Wilkes != programmer and\
                            Wilkes in (programmer, droid) and\
                            Hamming in (programmer, droid) and\
                            Minsky != writer and\
                            Knuth != manager and\
                            tablet != manager and\
                            Knuth == manager + 1 and\
                            Simon == manager and\
                            designer != Thursday and\
                            designer != droid and\
                            (Wilkes in (Monday, writer) and\
                            laptop in (Monday, writer)):
                            result = {Hamming:"Hamming", Knuth:"Knuth", Minsky:"Minsky", Simon:"Simon", Wilkes:"Wilkes"}
                            res = []
                            for day in days:
                                res.append(result[day])
                            return res
    print "No solution found"
    return None

def day_after(h1, h2):
    "Person h1 arrived 1 day after h2."
    return h1 == h2+1

def logic_puzzle1():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    days = [1, 2, 3, 4, 5]
    orderings = [x for x in list(itertools.permutations(days))]
    #print len(orderings)
    result = next((Hamming, Knuth, Minsky, Simon, Wilkes)
        for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings
        if day_after(Knuth, Simon) #6
#        if day_after(Simon, Minsky)
#        if day_after(Minsky, Wilkes)
#        if day_after(Hamming, Knuth)
        for (laptop, droid, tablet, iphone, _) in orderings
        if laptop is 3 and tablet is not 5 #1, 8,
        and ((iphone is 2) or (tablet is 2)) #! 12
        for (programmer, writer, designer, manager, _) in orderings
        #2, 4, 3
        if programmer is not Wilkes and writer is not Minsky
        if (((programmer is Wilkes) and (droid is Hamming)) or ((programmer is Hamming) and (droid is Wilkes))) #!
        if manager is not Knuth and manager is not tablet
        and designer != 4 and designer is not droid and day_after(Knuth, manager)
        #if ((laptop is writer) and (Wilkes is 1)) #or ((Wilkes is writer) and (laptop is 1))) #!

    )
#    i = 0
#    for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings:
#        for (laptop, droid, tablet, iphone, _) in orderings:
#            for (programmer, writer, designer, manager, _) in orderings:
#                if day_after(Knuth, Simon):
#                    if laptop is 3 and tablet is not 5 and ((iphone is 2) or (tablet is 2)):
#                        if programmer is not Wilkes and writer is not Minsky:
#                            if (((programmer is Wilkes) and (droid is Hamming)) or ((programmer is Hamming) and (droid is Wilkes))):
#                                if manager is not Knuth and manager is not tablet and designer != 4 and designer is not droid and day_after(Knuth, manager):
#                                #if ((laptop is writer) and (Wilkes is 1)): #or ((Wilkes is writer) and (laptop is 1))):
#                                    i += 1
#                                    result = (Hamming, Knuth, Minsky, Simon, Wilkes)

    arrived = []
    for i in result:
        if i==1: arrived.append('Hamming')
        if i==2: arrived.append('Knuth')
        if i==3: arrived.append('Minsky')
        if i==4: arrived.append('Simon')
        if i==5: arrived.append('Wilkes')
    return arrived, result

print logic_puzzle()

#print 120**3

