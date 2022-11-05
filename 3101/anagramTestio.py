# Do not change the name of this file or the class name.
from random import sample
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

    # def sortList(self, list):
    #     sortedList = list 

    #     for i in range(len(sortedList)):
    #         for j in range(len(sortedList)):
    #             if sortedList[j].split(" ")[1:][0]>sortedList[i].split(" ")[1:][0]:
    #                 temp = sortedList[i].split(" ")[1:][0]
    #                 sortedList[i].split(" ")[1:][0] = sortedList[j].split(" ")[1:][0]
    #                 sortedList[j].split(" ")[1:][0] = temp
    #     print(sortedList)
    #     return sortedList


    def getAnagrams(self):
        working_list = list(self.dictionary)   #the input has been made a list from dictionary form 
        anagram_class = []
        edit_list = []
        finalList = []

        #final result should be edit list which has a bunch of anagrams Classes edit_list = [[anagram_class], [anagram_class]]
        temp_elem = ""
    
        for i in range(len(working_list)):
            word = working_list[i]
            alphabetized = self.sortWord(word) #check 
            edit_list += [word + " " + alphabetized]
        print(edit_list)
        
        edit_list = sorted(edit_list)    #FIX THIS FIX THIS 
        
        # print(edit_list)
        for k, elem in enumerate(edit_list):
            
            if len(edit_list) == 0:
                anagram_class = []
                finalList += [anagram_class]

            else:
                if (temp_elem == ""):
                    temp_elem = edit_list[k].split(" ")[1:][0]
                    anagram_class = [edit_list[k].split(" ")[:1][0]]

                # elif k ==  len(edit_list):
                #     anagram_class.append(edit_list[k].split(" ")[:1][0])
                #     finalList += [anagram_class]
                    
                else:
                    
                    if (temp_elem == edit_list[k].split(" ")[1:][0]):
                        anagram_class.append(edit_list[k].split(" ")[:1][0])
                      

                    else:
                        finalList += [anagram_class]
                        anagram_class = []
                        anagram_class = [edit_list[k].split(" ")[:1][0]]
                        if edit_list[-1] == edit_list[k]:
                            finalList += [anagram_class]

                        temp_elem = edit_list[k].split(" ")[1:][0]

     
        #go thru the list to find which words match
        #match the index on the edit_list to what the actual word is in pf and add that to the anagram class


        return finalList


"""
You can use this for debugging if you wish.
"""

if __name__ == "__main__":
    pf = Anagram("dict3.txt")
    print(pf.dictionary)
    pf.getAnagrams()
    