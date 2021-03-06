# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    return 'test for double_out pass'

####

singles = dict( [('S'+str(x), x) for x in range(1, 21)] + [('SB', 25)] )
doubles = dict( [('D'+str(x), 2*x) for x in range(1, 21)] +[('DB', 50)] )
triples = dict( [('T'+str(x), 3*x) for x in range(1, 21)] )
ordered_points = [0] + sorted(set(singles.values() + doubles.values() + triples.values()), reverse=True)

def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""

    for dart1 in ordered_points:
        for dart2 in ordered_points:
            for dart3 in doubles.values():
                if dart1+dart2+dart3 == total:
                    if (dart2):
                        if (dart1):
                            return [get_name(dart1), get_name(dart2), get_name(dart3)]
                        else:
                            return [get_name(dart2), get_name(dart3)]
                    else:
                        return [get_name(dart3)]
    return None

def get_name(dart):
    if dart == 0: return None
    for name, value in triples.iteritems():
        if value == dart: return name
    for name, value in doubles.iteritems():
        if value == dart: return name
    for name, value in singles.iteritems():
        if value == dart: return name
    raise ValueError

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  (??) But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring. (??)

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."

    ring = target[0]
    section = target[1:]

    if section == 'B': return bullseye_outcome(ring, miss)
    if ring == 'T':    return triple_outcome(miss, section)
    elif ring == 'D':  return double_outcome(miss, section)
    elif ring == 'S':  return single_outcome(miss, section)

    raise ValueError

def triple_outcome(miss, section):
    outcome = {}
    outcome['T' + str(section)] = (1 - miss) * (1 - miss) # hit
    for neighbor in neighbors(section):
        outcome['T' + str(neighbor)] = (1 - miss) * (miss / 2)
        outcome['S' + str(neighbor)] = miss * (miss / 2)
    outcome['S' + str(section)] = miss * (1 - miss)
    return outcome

def double_outcome(miss, section):
    outcome = {}
    outcome['D' + str(section)] = (1 - miss) * (1 - miss)
    for neighbor in neighbors(section):
        outcome['D' + str(neighbor)] = (1 - miss) * (miss / 2)
        outcome['S' + str(neighbor)] = miss * (miss / 4)
    outcome['S' + str(section)] = miss * (1 - miss) / 2
    return outcome

def single_outcome(miss, section):
    outcome = {}
    outcome['S' + str(section)] = (1 - miss) * (1 - miss / 5)
    for neighbor in neighbors(section):
        outcome['S' + str(neighbor)] = (1 - miss / 5) * (miss / 2)
    for ring in ['D', 'T']:
        for neighbor in neighbors(section):
            outcome[ring + str(neighbor)] = (miss / 5) * (miss / 2) / 2
        outcome[ring + str(section)] = (miss / 5) * (1 - miss) / 2
    return outcome

def bullseye_outcome(ring, miss):
    if ring == 'D':
        return dict([('DB', 1 - 3 * miss), ('SB', miss)] + [('S' + str(x), 2 * miss / 20) for x in range(1, 21)])
    elif ring == 'S':
        return dict([('DB', miss / 5), ('SB', 1 - miss * 6 / 5)] + [('S' + str(i), miss / 20)  for i in range(1, 21)])
    else: raise ValueError

section_order = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20]

def neighbors(section):
    section = int(section)
    if section == 20: return (5, 1)
    index = section_order.index(section)
    return (section_order[index-1], section_order[index+1])

def best_target(miss):
    "Return the target that maximizes the expected score."
    return max(
        singles.keys()+doubles.keys()+triples.keys(),
        key=lambda target: expected_score(outcome(target, miss))
    )

def expected_score(outcome):
    score = 0
    for target, probability in outcome.iteritems():
        score += float(get_value(target))*probability
    return score

def get_value(target):
    ring = target[0]
    section = target[1:]
    if section == 'B': section = 25
    if ring == 'T': return 3*int(section)
    if ring == 'D': return 2*int(section)
    return int(section)

def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
        for key in set(dict1) | set(dict2))

def test_outcome():
    "test that probabilities add up correctly (to 1 or miss/2 for the double ring)"
    for miss in [x * 0.1 for x in range(0, 10)]:
        for target in triples.keys():
            assert abs(sum(outcome(target, miss).values()) - 1) < 1e-5
        for target in doubles.keys():
            if target == 'DB':
                assert abs(sum(outcome(target, miss).values()) - 1) < 1e-5
            else:
                assert abs(sum(outcome(target, miss).values()) - (1-miss/2)) < 1e-5
        for target in singles.keys():
            assert abs(sum(outcome(target, miss).values()) - 1) < 1e-5
    print 'outcome(SB, 0.2):'
    print outcome('SB', 0.2)
    return 'test_outcome pass'

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1),
            {'T20': 0.81, 'S1': 0.005, 'T5': 0.045,
             'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert same_outcome(
        outcome('SB', 0.2),
            {'S9': 0.01, 'S8': 0.01, 'S3': 0.01, 'S2': 0.01, 'S1': 0.01, 'DB': 0.04,
             'S6': 0.01, 'S5': 0.01, 'S4': 0.01, 'S19': 0.01, 'S18': 0.01, 'S13': 0.01,
             'S12': 0.01, 'S11': 0.01, 'S10': 0.01, 'S17': 0.01, 'S16': 0.01,
             'S15': 0.01, 'S14': 0.01, 'S7': 0.01, 'S20': 0.01, 'SB': 0.76})
    return 'test 2 pass'

print test_darts()
print test_outcome()
print test_darts2()
