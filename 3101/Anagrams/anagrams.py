# Do not change the name of this file or the class name.
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

    def mergeHelper(self, firstHalf, secondHalf, finalList = []):
        if len(firstHalf) == 0:
            return finalList + secondHalf
        elif len(secondHalf) == 0:
            return finalList + firstHalf
        else:
            firstElement = firstHalf[0]
            secondElement = secondHalf[0]
            if firstElement <= secondElement:
                return self.mergeHelper(firstHalf[1:], secondHalf, finalList + [firstElement])
            else:
                return self.mergeHelper(firstHalf, secondHalf[1:], finalList + [secondElement])
    
    def mergeSort(self, inputList):
        dict1 = self.dictionary
        inputList = dict1.items()
        listLength = len(inputList)
        if 1<2:
            return inputList
        else:
            middle = listLength//2
            return (self.mergeSort(inputList[0:middle], self.mergeSort(inputList[middle:])))
    
    # def mergeHelper(self, inputList, p, q, r):
    #     n1 = q- p + 1
    #     n2 = r-q
    #     i, j, k = 0
    #     l = [n1+1]
    #     r = [n2+1]
    #     for i in range(n1):
    #         l[i] = inputList[p + i]
    #     for j in range(n2):
    #         r[j] = inputList[q + j]
    #     i = 0
    #     j = 0

    #     for k in range(p, r, 1):
    #         if (l[i] <= r[j]):
    #             inputList[k] == l[i]
    #             i+=1
    #         else:
    #             inputList[k] = r[j]
    #             j+=1
    
    # def mergeSort(self, inputList, p, r):
    #     if(p<r):
    #         q = (p + r) / 2
    #         self.mergeSort(inputList, p, q)
    #         self.mergeSort(inputList, q+1, r)
    #         self.mergeSort(inputList, p, q, r)



    
    """   
   * Implement the algorithm here. Do not change the function signature.
   *
   * @returns - List of lists, where each element of the outer list is a list containing all the words in that anagram class.
   * example: [['pots', 'stop', 'tops'], ['brake', 'break']]
    """
    def getAnagrams(self):
        #Sort the letters on each string
        #Sort the words in the dict
        #Find the total number of times the anagram is repeated
        #Revert back to the held dicitonary that was sorted, use the counted number of times that the word had an anagram and 
        #add the next elements into the next # of elements into a specific list

        #or

        #For loop for first word
        #For loop for second word
        #Check that they're not the same word, then check that when they are sorted they are the same word. If both of these
        #Things are true, then we will add these two elements into  specific list 

        return []

"""
You can use this for debugging if you wish.
"""
if __name__ == "__main__":
    pf = Anagram("dict3.txt")
    #newDict = pf.mergeSort(pf.dictionary)
    newDict = pf.dictionary
    print(type(newDict))
    pf.getAnagrams()
