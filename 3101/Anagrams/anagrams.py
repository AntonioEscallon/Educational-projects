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
        A = []
        i ,j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                A.append(left[i])
                i += 1
            else:
                A.append(right[j])
                j += 1
        A += left[i:]
        A += right[j:]
        return A
    
    def mergeString(self, left, right, length):
        A = []
        newString = ''
        i ,j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                A.append(left[i])
                newString = newString + A[len(A) - 1]
                #print(newString)
                i += 1
            else:
                A.append(right[j])
                newString = newString + A[len(A) - 1]
                #print(newString)
                #print(A)
                j += 1
        #print(left[i:], 'hm')
        #print(right[j:], "hmmm")
        A += left[i:]
        A += right[j:]
        newString = newString + A[len(A) - 1]
        print(len(newString))
        if(len(newString) == length):
            print(newString)

        return A


    def mergesort(self, A, length):
        A = list(A)
        if len(A) > 1:
            q = len(A) // 2
            left = self.mergesort(A[:q], length)
            right = self.mergesort(A[q:], length)
            return self.mergeString(left, right, length)
        return A

    def algo(self, inputList):
        finalList = []
        for elements in inputList:
            new_elements = list(elements)
            print(new_elements, len(new_elements))
            length = len(new_elements)
            finalList = finalList +  [self.mergesort(elements, length)]
            print(elements)
        return finalList

    
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
    print(pf.dictionary)
    newDict = pf.algo(pf.dictionary)
    #newDict = pf.mergesort(pf.dictionary)
    print(newDict)
    pf.getAnagrams()
