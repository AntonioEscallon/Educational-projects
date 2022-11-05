# Do not change the name of this file or the class name.
import time

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
                #newString = left[i]
                #newList = newString + newList[len(newList) - 1]
                #newString = newString + newList[len(newList) - 1]
                i += 1
            else:
                newList.append(right[j])
                #newString = right[i]
                #newList = [newString] + newList[len(newList) - 1]
                #newString = newString + newList[len(newList) - 1]
                j += 1
        newList += left[i:]
        #print(newList,'hm')
        newList += right[j:]
        newString = "".join(newList)
        return newString
    
    def merge(self, left, right):
        newList = []
        newString = ''
        i ,j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                newList.append(left[i])
                #newString = left[i]
                #newList = newString + newList[len(newList) - 1]
                #newString = newString + newList[len(newList) - 1]
                i += 1
            else:
                newList.append(right[j])
                #newString = right[i]
                #newList = [newString] + newList[len(newList) - 1]
                #newString = newString + newList[len(newList) - 1]
                j += 1
        newList += left[i:]
        #print(newList,'hm')
        newList += right[j:]

        return newList


    def mergesortString(self, newList, length, newString):
        newList = self.listMaker(newList)
        if len(newList) > 1:
            q = len(newList) // 2
            left = self.mergesort(newList[:q], length, newString)
            right = self.mergesort(newList[q:], length, newString)
            newList = self.merge(left, right)
            return newList
        
        return newList
    
    def mergesort(self, newList, length, newString):
        newList = self.listMaker(newList)
        if len(newList) > 1:
            q = len(newList) // 2
            left = self.mergesort(newList[:q], length, newString)
            right = self.mergesort(newList[q:], length, newString)
            newList = self.merge(left, right)
            return newList
        
        return newList
    
    """   
   * Implement the algorithm here. Do not change the function signature.
   *
   * @returns - List of lists, where each element of the outer list is a list containing all the words in that anagram class.
   * example: [['pots', 'stop', 'tops'], ['brake', 'break']]
    """
    def getAnagrams(self):
        #Step 1
        start = time.time()
        inputList = self.listMaker(self.dictionary)
        finalList = []
        newString = ''
        newList = []
        count = 0
        count2 = 0
        #Step 2
        for elements in inputList:
            new_elements = self.listMaker(elements)
            length = len(new_elements)
            finalList = finalList + [self.mergesortString(elements, length, newString)]
        #end = time.time()
        #print(end - start)

        #start2 = time.time()
        #print(finalList)
        #print(type(inputList[count]), 'hm')
        #print(type(finalList[0]))
        #Step 3
        for elements in finalList:
            elements = "".join(elements)
            newList = newList + [elements + ' ' + inputList[count]]
            count += 1
            newString = ''
        #end2 = time.time()

        #print(end2 - start2)
        #Step 4
        sortedFinalList = self.mergesort(newList, length, newString)
        count = 0
        createdList = []
        theFinalList = []
        oldElement = ''

        #start3 = time.time()
        #Step 5
        for elements in sortedFinalList:
            count +=1
            if ((elements.split(" ")[:1][0] != oldElement and oldElement != '')):
                theFinalList = theFinalList + [createdList]
                oldElement = elements.split(" ")[:1][0]
                createdList = []
                createdList.append(elements.split(" ")[1:][0])
            elif (oldElement == ''):
                createdList.append(elements.split(" ")[1:][0])
                oldElement = elements.split(" ")[:1][0]
            elif(count == len(sortedFinalList)):
                createdList.append(elements.split(" ")[1:][0])
                theFinalList = theFinalList + [createdList]
            else:
                createdList.append(elements.split(" ")[1:][0])

        #end3 = time.time()

        #print(end3 - start3 )
        #print(theFinalList)
        return theFinalList

"""
You can use this for debugging if you wish.
"""
if __name__ == "__main__":
    pf = Anagram("dict1.txt")
    newList = pf.getAnagrams()
    print(newList)
