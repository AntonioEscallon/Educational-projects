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

    # def mergeHelper(self, firstHalf, secondHalf, finalList = []):
    #     if len(firstHalf) == 0:
    #         return finalList + secondHalf
    #     elif len(secondHalf) == 0:
    #         return finalList + firstHalf
    #     else:
    #         firstElement = firstHalf[0]
    #         secondElement = secondHalf[0]
    #         if firstElement <= secondElement:
    #             return self.mergeHelper(firstHalf[1:], secondHalf, finalList + [firstElement])
    #         else:
    #             return self.mergeHelper(firstHalf, secondHalf[1:], finalList + [secondElement])
    
    # def mergeStringHelper(self, firstHalf, secondHalf, finalList = ''):
    #     if len(firstHalf) == 0:
    #         return finalList + secondHalf[0]
    #     elif len(secondHalf) == 0:
    #         return finalList + firstHalf[0]
    #     else:
    #         firstElement = firstHalf[0]
    #         secondElement = secondHalf[0]
    #         newFHalf = firstHalf[1:]
    #         newSHalf = secondHalf[1:]
    #         if firstElement <= secondElement:
    #             return self.mergeStringHelper(newFHalf, secondHalf, finalList + firstElement)
    #         else:
    #             # print(secondHalf[1:], secondHalf[0:])
    #             # print(finalList + secondElement, 'hm')
    #             return self.mergeStringHelper(firstHalf, newSHalf, finalList + secondElement)
    
    # def mergeSort(self, inputSet):
    #     inputList = list(inputSet)
    #     listLength = len(inputList)

    #     if listLength<2:
    #         return inputList
    #     else:
    #         middle = listLength//2
    #         return (self.mergeStringHelper(self.mergeSort(inputList[0:middle]), self.mergeSort(inputList[middle:])))
        
    # def mergeSortString(self, inputSet):
    #     inputList = list(inputSet)
    #     listLength = len(inputList)
    #     finalStr = str(inputSet)

    #     if listLength<2:
    #         return inputList
    #     else:
    #         middle = listLength//2
    #         return (self.mergeStringHelper(self.mergeSort(inputList[0:middle]), self.mergeSort(inputList[middle:]))) + ' ' + finalStr
    
    # def algo(self, inputList):
    #     finalList = []
    #     for elements in inputList:
    #         finalList = finalList +  [self.mergeSortString(elements)]
    #     return finalList

    # def mergeHelper(self, inputList, p, q, r):
    #     n1 = q - p + 1
    #     n2 = r  - q

    #     left = []
    #     right = []

    #     for i in range(0, n1):
    #         left[i] = inputList[p + i]
    #     for j in range(0, n2):
    #         right[j] = inputList[q + j]
    #     #left[n1] = 10000000
    #     #right[n2] = 10000000
    #     print(left)
    #     print(right)
        
    #     i = 0
    #     j = 0

    #     for k in range(p, r + 1):
    #         if left[i] <= right[j]:
    #             inputList[k] = left[i]
    #             i+=1
    #         else:
    #             inputList[k] = right[j]
    #             j+=1
    
    # def mergeSort(self, inputList, p, r):
    #     inputSet = list(inputList)
    #     print(inputSet)
    #     if(p<r):
    #         q = (p + r) // 2
    #         self.mergeSort(inputSet, p, q)
    #         self.mergeSort(inputSet, q+1, r)
    #         self.mergeHelper(inputSet, p, q, r)

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
    
    def mergeString(self, left, right, length):
        newList = []
        newString = ''
        i ,j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                newList.append(left[i])
                newString = newString + newList[len(newList) - 1]
                #print(newString)
                i += 1
            else:
                newList.append(right[j])
                newString = newString + newList[len(newList) - 1]
                #print(newString)
                #print(A)
                j += 1
        #print(left[i:], 'hm')
        #print(right[j:], "hmmm")
        newList += left[i:]
        newList += right[j:]

        return newList


    def mergesort(self, newList, length, newString):
        newList = self.listMaker(newList)
        if len(newList) > 1:
            q = len(newList) // 2
            left = self.mergesort(newList[:q], length, newString)
            right = self.mergesort(newList[q:], length, newString)
            newList = self.mergeString(left, right, length)
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
        #print(sortedFinalList)
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
            #print(elements, 'these are')
            # if(count == 0):
            #     if(sortedFinalList[count].split(" ")[:1][0] == sortedFinalList[count + 1].split(" ")[:1][0]):
            #         finalElement = elements.split(" ")[:1][0]
            #         createdList.append(finalElement)
            #         theFinalList = theFinalList + [createdList]
            # elif (sortedFinalList[count].split(" ")[:1][0] == sortedFinalList[count - 1].split(" ")[:1][0]):
            #     finalElement = elements.split(" ")[:1][0]
            #     createdList.append(finalElement)
            #     theFinalList = theFinalList + [createdList]
            # else:
            #     theFinalList = theFinalList + [createdList]
            # count+=1
            # print(theFinalList)
            #finalRealList = finalRealList + 
        return theFinalList

"""
You can use this for debugging if you wish.
"""
if __name__ == "__main__":
    pf = Anagram("dict3.txt")
    #newDict = pf.getAnagrams()
   # print(newDict)
