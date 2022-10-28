# Do not change the name of this file or the class name.
from typing import final
from numpy import kaiser


class Anagram(object):

    def __init__(self, filename):
        self.load_dictionary(filename)

    """
    Helper method to load the dictionary file.
    You may read it in some other way if you want to but do not change the function signature.
    """
    def load_dictionary(self, filename):
        with open(filename) as handle:
            self.dictionary = set(w.strip() for w in handle)
   
   
    """
   * Implement the algorithm here. Do not change the function signature.
   *
   * @returns - List of lists, where each element of the outer list is a list containing all the words in that anagram class.
   * example: [['pots', 'stop', 'tops'], ['brake', 'break']]
    """

    def sortWord(self, word):
        sorted = list(word)

        for i in range(len(sorted)):
            for j in range(len(sorted)):
                if sorted[j]>sorted[i]:
                    temp = sorted[i]
                    sorted[i] = sorted[j]
                    sorted[j] = temp
        sorted = "".join(sorted)
        return sorted

    def getAnagrams2(self):
        working_list = list(self.dictionary)   #the input has been made a list from dictionary form 
        anagram_class = []
        edit_list = []
        finalList = []

        #final result should be edit list which has a bunch of anagrams Classes edit_list = [[anagram_class], [anagram_class]]
        temp_elem = ""
    
        for i in range(len(working_list)):
            word = working_list[i]
            alphabetized = self.sortWord(word) #check 
            edit_list += [alphabetized + " " + word]

        edit_list = sorted(edit_list)

        for k, elem in enumerate(edit_list):
            if len(edit_list) == 0:
                anagram_class = []
                finalList += [anagram_class]
            else:
                if (temp_elem == ""):
                    temp_elem = edit_list[k].split(" ")[:1][0]
                    anagram_class = [edit_list[k].split(" ")[1:][0]]
                else:
                    if (temp_elem == edit_list[k].split(" ")[:1][0]):
                        print(edit_list[k].split(" ")[:1][0], 'hmmmm')
                        anagram_class.append(edit_list[k].split(" ")[1:][0])
                        if k == len(edit_list) - 1:
                            finalList += [anagram_class]
                    else:
                        finalList += [anagram_class]
                        anagram_class = []
                        anagram_class = [edit_list[k].split(" ")[1:][0]]
                        if k == len(edit_list) - 1:
                            finalList += [anagram_class]
                        temp_elem = edit_list[k].split(" ")[:1][0]
        #go thru the list to find which words match
        #match the index on the edit_list to what the actual word is in pf and add that to the anagram class
        return finalList


"""
You can use this for debugging if you wish.
"""

if __name__ == "__main__":
    pf = Anagram("dict3.txt")
    #print(pf.dictionary)
    finalList = pf.getAnagrams2()
    print(finalList)