# Code written by a former Emory CS student - ALEX SMADJA
# THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - ALEX SMADJA
import sys
import time
import itertools
from collections import defaultdict


def apriori(transactions, threshold, output_file):
    invalids = list()                   # list of all values that do not meet threshold requirement
    counts = list()                     # list of dictionaries to keep track of valid sets
    for i in range(3):
        counts.append(defaultdict(int))

    for t in transactions:
        for s in t:                     # count how many times each value appears
            counts[0][s] += 1
        subsets = itertools.combinations(t, 2)
        for s in subsets:               # count 2-item set frequency
            counts[2][s] += 1

    for a in counts[0]:                 # discard bad values and print 1-item valid sets with their count
        if counts[0][a] >= threshold:
            output_file.write(str(a) + ' (' + str(counts[0][a]) + ')\n')
            counts[1][a] = counts[0][a]
        else:
            invalids.append(a)
    counts.pop(0)

    counts.append(defaultdict(int))
    for a in counts[1]:                 # discard bad values and print 2-item valid sets with their count
        if counts[1][a] >= threshold:
            output_file.write(" ".join(map(str, a)) + ' (' + str(counts[1][a]) + ')\n')
            counts[2][a] = counts[1][a]
    counts.pop(1)

    return apriori_aux(counts, transactions, threshold, output_file)


def apriori_aux(counts, transactions, threshold, output_file):
    k = 3
    while counts[k-2]:                  # loop until no valid sets are found
        candidates = set()              # set of possible candidates
        counts.append(defaultdict(int))
        for a in counts[k-2]:           # combine past valid sets with unique values for new candidates
            for b in counts[0]:         # unique values
                if b not in a:
                    check = True
                    tmp = list(a) + [b]
                    tmp.sort()
                    if tuple(tmp[1:]) not in counts[k - 2]:
                        continue
                    if tuple(tmp[:k - 1]) not in counts[k - 2]:
                        continue
                    for i in range(1, k - 1):
                        if tuple(tmp[:i] + tmp[i + 1:]) not in counts[k - 2]:
                            check = False
                            break
                    if check:           # add if none of above subsets aren't present in last valid sets
                        candidates.add(tuple(tmp))

        for t in transactions:          # count how many times each candidate appears in transactions
            t = set(t)
            for c in candidates:
                tmp = set(c)
                if tmp.issubset(t):
                    counts[k-1][c] += 1

        counts.append(defaultdict(int))
        for a in counts[k-1]:           # discard bad values and print k-item valid sets with their count
            if counts[k-1][a] >= threshold:
                counts[k][a] = counts[k-1][a]
                output_file.write(" ".join(map(str, a)) + ' (' + str(counts[k][a]) + ')\n')
        counts.pop(k-1)
        k += 1

    return counts


def print_error(error):
    print(error, "\nUsage: python apriori.py <input data file> <frequency threshold> <output file>")
    exit(1)


def main():
    start_time = time.time()                # start time of process
    if len(sys.argv) != 4:                  # error messages for bad arguments
        print_error("Invalid number of arguments.")
    try:
        sys.argv[2] = int(sys.argv[2])
        if sys.argv[2] < 1:
            print_error("Frequency threshold must be greater than 0.")
    except ValueError:
        print_error("Frequency threshold must be an integer.")

    input_file = open(sys.argv[1], 'r')     # open input file for reading
    output_file = open(sys.argv[3], 'w')    # open output file for writing

    transactions = list()
    for l in input_file:                    # populate transactions list from input file
        transactions.append([int(x) for x in l.strip().split(' ')])
    input_file.close()                      # no longer need input file
    counts = apriori(transactions, sys.argv[2], output_file)
    output_file.close()                     # finished writing to output file

    num_freq_sets = 0
    for c in counts:                        # calculate number of valid item sets found
        num_freq_sets += len(c)
    print("Runtime: %f seconds\nNumber of frequent item sets: %d" % (time.time()-start_time, num_freq_sets))


if __name__ == '__main__':
    main()
