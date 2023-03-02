import math
import re
from collections import defaultdict


class VecDense:

    def tokenizeDoc(self, oneDoc: str):
        """This method tokenizes a a string.

        :param oneDoc: a string.
        :return: a tokenized sting.
        """
        sanitizedStr = re.sub(r'[^a-zA-Z0-9 ]', '', oneDoc)
        tokens = sanitizedStr.lower().split(" ")
        return tokens

    def getVecLength(self, vecIn: list):
        """This method computes the length of a vector.

        :param vecIn: a list representing a vector, one element per dimension.
        :return: the length of the vector.
        """
        newlist = []
        for i in vecIn:
            newlist.append(i**2)
        f = sum(newlist)
        return math.sqrt(f)

    def normalizeVec(self, vecIn:list):
        """This method normalizes a vector to unit length.

        :param vecIn:  a list representing a vector, one element per dimension.
        :return: a list representing a vector, that has been normalized to unit length.
        """
        norm = []
        vecnorm = self.getVecLength(vecIn)
        for i in vecIn:
            norm.append(i/vecnorm)
        return norm

    def dotProductVec(self, vecInA:list, vecInB:list):
        """This method takes the dot product of two vectors.

        :param vecInA, vecInB: two lists representing vectors,
            one element per dimension.
        :return: the dot product.
        """
        return sum([x*y for x,y in zip(vecInA,vecInB)])

    def cosine(self, vecInA: list, vecInB: list):
        """This method obtains the cosine between two vectors
            (which is nominally the dot product of two vectors of unit length).

        :param vecInA, vecInB: two lists representing vectors, one element per dimension.
        :return: the cosine.
        """
        cosine = self.dotProductVec(vecInA, vecInB)/(self.getVecLength(vecInA)*self.getVecLength(vecInB))
        return cosine

    def computeCentroidVector(self, tokensIn:list, vecDict:dict):
        """This method calculates the centroid vector from a list of
            tokens. The centroid vector is the "average"
            vector of a list of tokens.
        #NOTE:  Special considerations:
            - all tokens should be converted to lower case.
            - if a vector isn't in the dictionary, it
                shouldn't be a part of the average.

        :param tokensIn: a list of tokens.
        :param vecDict: the vector library is a dictionary, 'vecDict',
            whose keys are tokens, and values are lists representing vectors.
        :return: the centroid vector, represented as a list.
        """
        
        lis = []
        centroid = []
        for token in tokensIn:
            if token.lower() in vecDict:
                lis.append(vecDict[token.lower()])
        
        
        #sum the indexes, divide by total
        for x in range(len(lis[0])):
            sumsum = 0
            for z in range(len(lis)):
                sumsum += lis[z][x]
            centroid.append(sumsum/len(lis))
        return centroid
 

class VecSparseTFIDF:
    """This class calculates TF-IDF vector
    """
    def tokenizeDoc(self, oneDoc: str):
        """This method tokenizes a text.

        :param oneDoc: a string of text.
        :return: a tokenized text.
        """
        sanitizedStr = re.sub(r'[^a-zA-Z0-9 ]', '', oneDoc)
        tokens = sanitizedStr.lower().split(" ")
        return tokens

    def getTermFreq(self, oneDoc: str):
        """This method obtains term frequency.

        :param oneDoc: a string of text, called a document. e.g. "the cat saw the hat"
        :return: a defaultionary representing the term frequency
            counts in that document. Keys are tokens,
            values are counts.
        #NOTE: The input document should be tokenized using tokenizeDoc method.
        """
        token = self.tokenizeDoc(oneDoc)
        termFreq = defaultdict(lambda: 0)
        for word in token:
            if word in termFreq:
                termFreq[word] += 1
            else:
                termFreq[word]=1
        return termFreq

    def getDocFreqs(self, allDocs: list):
        """This method obtains document frequencies.

        :param allDocs: a list of strings.  Each string is one document.
        :return: a default dictionary representing the document frequency
            counts across all documents. Keys are tokens,
            values are counts.
        """
        docFreq = defaultdict(lambda: 0)
        for sublist in allDocs:
            newstring = self.tokenizeDoc(sublist)
            templist = []
            for x in newstring:
                if x in templist:
                    continue
                else:
                    if x in docFreq:
                        docFreq[x] += 1
                    else:
                        docFreq[x] = 1
                templist.append(x)
                
                    
                
            

        return docFreq

    def makeTFIDFVec(self, oneDoc: str, docFreqs: defaultdict, numDocs: int):
        """This method creates a TF-IDF vector for a given document.

        :param oneDoc: a string representing one document.
        :param docFreqs: a default dictionary representing the document
            frequency counts.  Keys are tokens, values are counts.
        :param numDocs: the total number of documents in the collection.
        :return: a default dictionary representing the tf-idf vector.
            Keys are tokens, values are counts.
        #NOTE: There are many ways to calculate tf-idf vectors.
           Term frequency should be the count of the words
            in a given document.
           Document frequency should be calculated with add-one
            smoothing, as log10(numDocs+1 / docFreqOfToken + 1).
        """
        vecOut = defaultdict(lambda: 0)
        tfdict = self.getTermFreq(oneDoc)
        newDoc = self.tokenizeDoc(oneDoc)
     #   print (newDoc)
        print(docFreqs)
        for x in newDoc:
            tf = tfdict.get(x)
            docFreqOfToken = docFreqs.get(x)
            idf = math.log10(numDocs+1/docFreqOfToken+1)
            w = tf*idf
            vecOut[x] = w        
        return vecOut


    def getVecLengthSparse(self, vecIn: defaultdict):
        """This method computes the length of a sparse vector.

        :param vecIn: a default dictionary representing a sparse
            vector. keys are tokens, values are counts, default = 0.
        :return:the length of the vector.
        """
        newlist = []
        values = vecIn.values()
        for i in values:
            newlist.append(i**2)
        f = sum(newlist)
        return math.sqrt(f)

    def normalizeVecSparse(self, vecIn: defaultdict):
        """This method normalizes a sparse vector to unit length.

        :param vecIn: a default dictionary representing a sparse vector.
          keys are tokens, values are counts, default = 0.
        :return: a list representing a vector, that has been
            normalized to unit length.
        """
        vecOut = defaultdict(lambda: 0)
        vecnorm = self.getVecLengthSparse(vecIn)
        for i in vecIn:
            normal = vecIn[i]/vecnorm
            vecOut[i] = normal
        return vecOut
        
    def dotProductVecSparse(self, vecInA: defaultdict, vecInB: defaultdict):
        """This method takes the dot product of two sparse vectors.

        :param vecInA, vecInB:two default dictionaries representing sparse
            vectors.  keys are tokens, values are counts, default = 0.
        :return: the dot product.
        """
        dotprod = []
        for keys in vecInA:
            t = vecInA[keys]
            s = vecInB[keys]
            dot = s*t
            dotprod.append(dot)
        return sum(dotprod)
            
            

    def cosineSparse(self, vecInA: defaultdict, vecInB: defaultdict):
        """This method obtains the cosine between two vectors (which
            is nominally the dot product of two vectors of unit length).

        :param vecInA, vecInB: two default dictionaries representing sparse
            vectors.  keys are tokens, values are counts, default = 0.
        :return: the cosine.
        """
        
        cosine = self.dotProductVecSparse(vecInA, vecInB)/(self.getVecLengthSparse(vecInA)*self.getVecLengthSparse(vecInB))
        return cosine



def loadVectors(filename:str):
    """This function loads word vectors from the file.

    :param filename:  the filename of the vectors
        (e.g. glove.subset.50d.txt)
    :return: a dictionary, key: token, value: list of numbers loaded
        from the file.
    """
    wordVecs = {}
    print("Loading word vectors from file (" + str(filename) + ")")
    #...
    f = open(filename)
    wordVecs = {}
    for line in f:
        words = line.split()
        token = words[0]
        vex = words[1:]
     #   print (token)
     #   print (vex)
        vectorsss = [float(x) for x in vex]
        wordVecs[token] = vectorsss

    print("Loaded " + str(len(wordVecs)) + " word vectors.")
    return wordVecs


def doQuestionAnsweringCentroidDense(questions:list, wordVecs:dict):
    """This function performs a baseline question answering task.
    This function implements a cosine similarity baseline question
    answering system for multiple choice questions. For each question,
    compute the centroid vector of the question text.
    Then, for each answer candidate, compute the cosine between the
    question text centroid vector, and that answer choice's centroid
    vector. Pick the answer choice that has the highest cosine
    similarity as the model's chosen answer. If the answer is correct,
     increment numCorrect. Return the total numCorrect.

    :param questions: a list of multiple questions, as included in the
        appropriate test.
    :param wordVecs: a dictionary of word vectors, loaded from
        'loadVectors()'.
    :return: the number of questions answered correctly.
    """
    vecDense = VecDense()
    numCorrect = 0
    for question in questions:
        centroid = vecDense.computeCentroidVector(vecDense.tokenizeDoc(question["question"]), wordVecs)
        cos = 0
        ind = 0
        for index in range(len(question["choices"])):
            centroid2 = vecDense.computeCentroidVector(vecDense.tokenizeDoc(question["choices"][index]), wordVecs)
            cosine = vecDense.cosine(centroid, centroid2)
            if cosine > cos:
                cos = cosine
                ind = index
            else:
                continue
        if ind == question['correctIdx']:
            numCorrect += 1
            
            
    

    # Evaluate QA performance of cosine model on questions
    

    # ...

    return numCorrect


