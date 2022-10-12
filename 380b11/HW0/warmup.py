#
# COMPSCI 383 Homework 0
#
# Fill in the missing bodies of the functions as specified by the comments and docstrings.
#
# If you execute this file, the main() function below will test your implementations.  You can 
# compare your results to the answers in the comments.
#


# Exercise 1 (6 points)
from ast import Num
from itertools import count
from typing import Counter


def max_unique(lst):
    """Returns the largest element of a list that appears only once"""
    new_array = []
    #checking for repeated numbers and finding the max
    for elements in lst:
        if elements in new_array:
            new_array.remove(elements)
        else:
            new_array.append(elements)
    #
    # fill in function body here
    #
    return max(new_array)  # fix this line!

# Exercise 2 (6 points)
def splice_em(list_one, list_two):
    """Splice two equal-length lists together.
    
    Returns a list with alternating elements from the two lists given as arguments.  For example:
    splice_em(['a', 'b', 'c'], [1, 2, 3]) should return the list ['a', 1, 'b', 2, 'c', 3]
    
    Hint: you'll probably want to use a for or while loop to iterate.  The enumerate() and/or zip() 
    built-in functions might be helpful here: https://docs.python.org/3/library/functions.html    
    """
    #
    # fill in function body here
    #
    new_array = []
    new_one = list_one
    new_two = list_two

    while len(new_one) != 0 or len(new_one) != 0:
        holder_1 = new_one.pop()
        holder_2 = new_two.pop()
        new_array.append(holder_2)
        new_array.append(holder_1)
    
    new_array.reverse()

    return new_array  # fix this line!


# Exercise 3 (8 points)
def reverse_dict_list(d):
    """Reverse a dictionary that maps keys to lists of values.
    
    Given a dictionary that maps each key k1, k2, etc. to a list of values v1, v2, ..., create a 
    new dictionary keyd by v1, v2, mapping them to lists k1, k2, etc.  

    For example, reverse_dict_list({'a':[1, 2, 3], 'b':[1, 3, 5, 7], 'c':[4, 5, 6]}) should return 
    the dictionary {1:['a', 'b'], 2:['a'], 3:['a', 'b'], 5:['b', 'c'], 7:['b'], 4:['c'], 6:['c']}
    """
    #
    # fill in function body here
    #
    swap_d = {}
    sameK_arr = []
    lonely_arr = []
    #Parsing through the dict
    for key in d:
        #Parsing through eveyr element in a dictionary field 
        for elements in d[key]:
            #If we see that we have already added this key to the dict, then we will append the values to an array and add that array to the dict
            
            if elements in swap_d:
                #If we have seen an element it means the key already exists, and thus we need to make sure that we only take the values that will pertain to this given key value
                sameK_arr = swap_d[elements]
                sameK_arr.append(key)
                swap_d[elements] = sameK_arr
            #Else, we will add a lonely array to the dict
            else:
                lonely_arr = [key]
                swap_d[elements] = lonely_arr
                if key in sameK_arr:
                    continue
                #Making sure all keys are added to the sameK_arr, even if they won't be repeated
                else:
                   sameK_arr.append(key)

    return swap_d  # fix this line!


# Exercise 4 (8 points)
def char_counts(some_text):
    """Return a dictionary containing each character in the text as keys, and the number of times
    they occur as values.

    Hint: recall that since a string is a sequence, you can loop through it as you would a list.
    For help with dictionaries, see the Python docs: 
    https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

    """
    #
    # fill in function body here
    #
    char_dic = {}
    temp = 0
    for char in some_text:
        if char not in char_dic:
            temp = 1
            char_dic[char] = temp
        #If the character is already in the dictionary
        else:
            temp = char_dic[char]
            temp += 1
            char_dic[char] = temp
    return char_dic  # fix this line!


# Exercise 5 (10 points)
# [ For this exercise, you only need to modify the methods in the ClubStudents class --- you should not 
#   change anything in the StudentClubs class. ]
class StudentClubs:
    """Class to store student club memberships, constituting many-to-many relatinoships"""
    def __init__(self):
        self.student__clubs = {}  # student_name -> [club1, club2, ...]

    def add_club_roster(self, club, member_list):
        """Store the student-club relationships gleaned from a club roster."""
        for member in member_list:
            if member not in self.student__clubs:
                self.student__clubs[member] = []
            self.student__clubs[member].append(club)

    def get_membership_tuples(self):
        """Return a list of (student club) tuples, grouped by student."""
        tups = []
        for student, clubs in self.student__clubs.items():
            for club in clubs:
                tups.append((student, club))
        return tups

class ClubStudents (StudentClubs):
    #
    # fill in any additional methods here (not necessary, but okay)
    #

    def get_membership_tuples(self):
        """Return a list of (student club) tuples, sorted and grouped by club."""
        #
        # fill in function body here
        #
        d = self.student__clubs
        
        new_k = []
        for keys in d:
            for elements in d[keys]:
                new_k.append((keys, elements))

        #Sort the two array elements, using x[1] as the first elements to sort by and then x[0] as the second key to sort by.
        new_k.sort(key=lambda x: (x[1], x[0]))

        return new_k  # fix this!


# Exercise 6 (10 points)
def is_monotonicish(lst):
    """Return True if list of numbers is "mostly monotonic", False otherwise.

    A list of numbers is "mostly increasing" if two conditions are met: (a) the last number must 
    be greater than the first, and (b) the difference between each entry and the one before
    it is no less than -1.  That is, [1, 3, 5, 7] and [1, 3, 2, 2] are "mostly increasing", while
    [1, 3, 1, 5] and [1, 3, 2, 1] are not.  
    
    A "mostly decreasing" list is defined simlarly, with each the last element being less than the 
    first and each successive entry being no more than one greater than the preceeding.  
    
    A "mostly monotonic" sequence of numbers is either mostly increasing or mostly decreasing. 
    """
    #
    # fill in function body here
    #
    test = True
    length = len(lst)
    for i in range(length):
        if i>0: 
            if lst[i] - lst[i-1]>= -1:
                continue
            else:
                test = False
    
    if lst[len(lst) - 1] <= lst[0]:
        test = False

    return test  # fix this line!


# Exercise 7 (2 points +10 extra credit)
def moxie_helper(lst):

    total = lst[0][2]
    num_sixes = 0
    remainder = total
    while remainder >=6:
        num_sixes += 1
        if remainder > 0:
            lst.append((0, num_sixes, total - 6*num_sixes))
        remainder = total - 6*num_sixes

    if lst[-1][1] < 4:
        return lst

    length = len(lst)
    for i in range(0, length):
        if lst[i][1] < 4:
            continue
        num_24 = 0
        total = lst[i][1]
        remainder = total
        while(remainder >= 4):
            num_24 += 1
            if remainder > 0:
                lst.append((num_24, total-4*num_24, lst[i][2]))
            remainder = total - 4*num_24

def moxie_combos(n):
    """Return a list of tuples describing all possible ways to deliver the world's best soda.

    Moxie can be packaged in single cans, six-packs of cans, or cases of 24 cans.  For example, 
    42 Moxies could be delivered in 1 case, 1 six-pack, and twelve singles, or 1 case, 3 six-packs,
    and 0 singles, or 0 cases, 2 six-packs, and 30 singles, etc.  

    For a given n, moxie_combos(n) returns a list of tuples that describe all possible ways to 
    group n cans into cases, six-packs, and singles.  It returns a list of unique three-element 
    tuples, each describing the number of cases, six-packs, and singles in that particular 
    combination.  For example, moxie_combos(19) should return the list:
    [ (0, 0, 19), (0, 3, 1), (0, 2, 7), (0, 1, 13)]

    (Note that the order of the list does not matter.)

    Hint: you may want to consider a recursive solution --- given a valid solution for n-1, how
    can you create the solution for n?  
    """
    #
    # fill in function body here
    #
    lst = []
    lst.append((0,0,n))
    moxie_helper(lst)
    return lst  # fix this line!

# The main() function below will be executed when your program is run.  Note that Python does not 
# require a main() function, but it is considered good style.  The comments on each line show
# what should be printed if your code is running correctly.
def main():
    print("1.", max_unique([9, 0, 1, 2, 5, 8, 6, 7, 5, 3, 0, 9]))      # 8
    print("2.", splice_em(['r', 'd', 'c', 'p'], [2, 2, 3, 0]))         # ['r', 2, 'd', 2, 'c', 3, 'p', 0]
    print("3.", reverse_dict_list({'a': [1, 2, 3], 'b': [2, 4, 6], 'c': [3, 0, None]}))  # {'h': [1, 2], 'e': [1], 'y': [1], 'o': [2]} #We are seeing 2 after 3, which messes up our array
    print("4.", char_counts("wowie zowie"))                            # {'w': 3, 'o': 2, 'i': 2, 'e': 2, ' ': 1, 'z': 1}
    cbs = ClubStudents()
    cbs.add_club_roster("one", ["c", "b","a"])
    cbs.add_club_roster("three", ["c", "d"])
    cbs.add_club_roster("two", ["b", "a"])
    print("5.", cbs.get_membership_tuples())                           # [('blinky', 'awesome club'), ('inky', 'awesome club'), 
                                                                       #  ('sue', 'awesome club'), ('clyde', 'orange club'), 
                                                                       #  ('sue', 'orange club')]
    print("6.", is_monotonicish([3, 5, 10, 9, 13]))                    # True
    print("7.", moxie_combos(19))                                      # [(0, 0, 19), (0, 1, 13), (0, 2, 7), (0, 3, 1)]


###################################

# The lines below are a common Python idiom for creating Python programs that can be exectuted
# directly or used as a module.  For more info, see: 
# https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/
if __name__ == '__main__':
    main()

