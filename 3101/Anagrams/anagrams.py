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

    def listMaker(self, firstSet):
        a = []
        for i in firstSet:
            a.append(i)
        return a

    def merge(self, left, right):
        newList = []
        i ,j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                newList.append(left[i])
                i += 1
            else:
                newList.append(right[j])
                j += 1
        newList += left[i:]
        newList += right[j:]
        return newList
    
    def mergeString(self, left, right):
        newList = []
        newString = ''
        i ,j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                newList.append(left[i])
                newString = newString + newList[len(newList) - 1]
                i += 1
            else:
                newList.append(right[j])
                newString = newString + newList[len(newList) - 1]
                j += 1
        newList += left[i:]
        newList += right[j:]

        return newList


    def mergesort(self, newList, length, newString):
        newList = self.listMaker(newList)
        if len(newList) > 1:
            q = len(newList) // 2
            left = self.mergesort(newList[:q], length, newString)
            right = self.mergesort(newList[q:], length, newString)
            newList = self.mergeString(left, right)
            return newList
        
        return newList
    
    """   
   * Implement the algorithm here. Do not change the function signature.
   *
   * @returns - List of lists, where each element of the outer list is a list containing all the words in that anagram class.
   * example: [['pots', 'stop', 'tops'], ['brake', 'break']]
    """
    def getAnagrams(self):
        inputList = self.listMaker(self.dictionary)
        finalList = []
        newString = ''
        newList = []
        count = 0
        for elements in inputList:
            new_elements = self.listMaker(elements)
            length = len(new_elements)
            finalList = finalList + [self.mergesort(elements, length, newString)]
        for elements in finalList:
            for letters in elements:
                newString = newString + letters
            newList = newList + [newString + ' ' + inputList[count]]
            count += 1
            newString = ''
        
        sortedFinalList = self.mergesort(newList, length, newString)
        count = 0
        createdList = []
        theFinalList = []
        oldElement = 'temp'
        for elements in sortedFinalList:
            count +=1
            if ((elements.split(" ")[:1][0] != oldElement and oldElement != 'temp')):
                theFinalList = theFinalList + [createdList]
                oldElement = elements.split(" ")[:1][0]
                createdList = []
                createdList.append(elements.split(" ")[1:][0])
            elif (oldElement == 'temp'):
                createdList.append(elements.split(" ")[1:][0])
                oldElement = elements.split(" ")[:1][0]
            elif(count == len(sortedFinalList)):
                createdList.append(elements.split(" ")[1:][0])
                theFinalList = theFinalList + [createdList]
            else:
                createdList.append(elements.split(" ")[1:][0])
        return theFinalList

"""
You can use this for debugging if you wish.
"""
if __name__ == "__main__":
    pf = Anagram("dict3.txt")