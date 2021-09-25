import math
import copy

# class to represent a vertex in a Decision Tree.  Decision Tree Vertices are
# defined as having a
# label and list of out edges with string defined edge weights
class Vertex(object):
        
    def __init__(self, name):
        self.Name = name
        self.OutEdges = {}

    def AddBranch(self, weight):
        self.OutEdges[weight] = None

    def AddLeaf(self, weight, v):
        self.OutEdges[weight] = v

    def ToString(self):
        if len(self.OutEdges) == 0:
            return self.Name

        str = ""
        for weight in self.OutEdges:
            str += self.Name + " -- " + weight + " --> " + self.OutEdges[weight].ToString() + "\n"
        return str

    def Predict(self, data, columns):
        if len(self.OutEdges) == 0:
            return self.Name

        values = data.split(',')
        col = columns[self.Name]

        return self.OutEdges[values[col].strip()].Predict(data, columns)


#
#   Functions to read input files
#
def LoadCSVFile(filename):

    with open(filename, 'r') as file:

        dict = {}

        for line in file:
            line = line.strip()
            line = line.split(",")
            dict[str(line[0:len(line)]).replace('[', '').replace(']','').replace("'", '')] = line[len(line)-1]

        return dict

def LoadTxtFile(filename):

    with open(filename, 'r') as file:

        att = {}
        col = {}

        lineNum = 0
        for line in file:

            if lineNum > 5 and lineNum < 12:
               line = line.split(':')
               att[line[0]] = str(line[1]).strip().replace('.','')

            if lineNum == 14:
               line = line.strip().split(',')

               colNum = 0
               for word in line:
                    col[word] = colNum
                    colNum += 1

            lineNum += 1

        return att, col
          
#
#   The ID3 Algorithm
#
def ID3(examples, attributes, columns, gain, maxLevels):

    tuple = UnifiedLabel(examples)
    if tuple[0]: 
        if len(attributes) == 0:
            return MostCommonLabel(examples)
        return Vertex(tuple[1])

    else:

        if gain == 0: root = BestAttributeEntropy(examples, attributes, columns)
        elif gain == 1: root = BestAttributeGI(examples, attributes, columns)
        else: root = BestAttributeME(examples, attributes, columns)

        for value in attributes[root.Name].split(','):
            value = value.strip()

            # add branch corresponding to attribute value
            root.AddBranch(value)

            if maxLevels == 1:
                root.AddLeaf(value, MostCommonLabel(examples))
                continue

            # find data subset where all examples have this attribute value
            subset = FindSubset(examples, value, columns[root.Name])

            if len(subset) == 0:
                root.AddLeaf(value, MostCommonLabel(examples))
            else:
                subatt = copy.deepcopy(attributes)
                subatt.pop(root.Name)
                root.AddLeaf(value, ID3(subset, subatt, columns, gain, maxLevels-1))

    return root


#
#   Dictionary helper functions
#
def UnifiedLabel(dict):
    values = list(dict.values())

    for value in values:
        if value != values[0]: return False, values[0]

    return True, values[0]

# returns the most common value from the dictionary
def MostCommonLabel(dict):
    values = list(dict.values())
    counts = {}

    for value in values:
        if value not in counts:
            counts[value] = 1
        else:
            counts[value] += 1

    maxLabel = None
    maxCount = 0

    for key in counts.keys():
        if counts[key] > maxCount:
            maxLabel = key
            maxCount = counts[key]

    return Vertex(maxLabel)

def MaxLabel(dict):
    maxValue = 0
    maxLabel = None

    for key in dict.keys():
        if dict[key] >= maxValue:
            maxValue = dict[key]
            maxLabel = key

    return maxLabel

def FindSubset(examples, value, column):
    subset = {}

    for key in examples:
        items = key.split(',')
        if items[column].strip() == value:
            subset[key] = examples[key]

    return subset

def ValueCount(dict, value):
    sum = 0
    for num in dict[value].values():
        sum += num
    return sum    


#
#   Subroutines for evaluating information gain
#
def BestAttributeEntropy(examples, attributes, columns):

    # compute information gains for each attribute and return vertex representing attribute with highest gain
    gains = ComputeInformationGainsEntropy(examples, attributes, columns, Hofs(examples))
    return Vertex(MaxLabel(gains))

def BestAttributeGI(examples, attributes, columns):

    # compute information gains for each attribute and return vertex representing attribute with highest gain
    gains = ComputeInformationGainsGI(examples, attributes, columns, GIofs(examples))
    return Vertex(MaxLabel(gains))

def BestAttributeME(examples, attributes, columns):
    
    # compute information gains for each attribute and return vertex representing attribute with highest gain
    gains = ComputeInformationGainsME(examples, attributes, columns, MEofs(examples))
    return Vertex(MaxLabel(gains))

def ComputeInformationGainsME(examples, attributes, columns, MEofs):

    gains = {}

    for att in attributes:

        attCounts = {}
        col = columns[att]

        for example in examples.keys():

            label = examples[example]
            atts = example.split(',')

            # if attribute is not yet in dictionary, create it with a dictionary
            if atts[col].strip() not in attCounts:
                attCounts[atts[col].strip()] = {label: 1}

            # if label had not yet been counted for the attribute value
            elif examples[example] not in attCounts[atts[col].strip()]:
                attCounts[atts[col].strip()][label] = 1
            
            # increment label counter for attribute value    
            else:
                attCounts[atts[col].strip()][label] += 1

        MEofa = 0
        for value in attCounts.keys():
            majCount = max(attCounts[value].values())
            valueCount = int(math.fsum(attCounts[value].values()))

            MEofa += valueCount/len(examples) * (valueCount - majCount)/valueCount

        gains[att] = MEofs - MEofa

    return gains

def ComputeInformationGainsGI(examples, attributes, columns, giofs):

    gains = {}

    for att in attributes:

        attCounts = {}
        col = columns[att]

        for example in examples.keys():

            label = examples[example]
            atts = example.split(',')

            # if attribute is not yet in dictionary, create it with a dictionary
            if atts[col].strip() not in attCounts:
                attCounts[atts[col].strip()] = {label: 1}

            # if label had not yet been counted for the attribute value
            elif examples[example] not in attCounts[atts[col].strip()]:
                attCounts[atts[col].strip()][label] = 1
            
            # increment label counter for attribute value    
            else:
                attCounts[atts[col].strip()][label] += 1

        giofa = 0
        for value in attCounts.keys():
            giofv = 0
            for label in attCounts[value].keys():

                labelCount = attCounts[value][label]
                valueCount = int(math.fsum(attCounts[value].values()))
                giofv += (labelCount / valueCount) * (labelCount / valueCount)

            giofa += valueCount/len(examples) * (1 - giofv)

        gains[att] = giofs - giofa

    return gains

def ComputeInformationGainsEntropy(examples, attributes, columns, hofs):

    gains = {}

    for att in attributes:

        attCounts = {}
        col = columns[att]

        for example in examples.keys():

            label = examples[example]
            atts = example.split(',')

            # if attribute is not yet in dictionary, create it with a dictionary
            if atts[col].strip() not in attCounts:
                attCounts[atts[col].strip()] = {label: 1}

            # if label had not yet been counted for the attribute value
            elif examples[example] not in attCounts[atts[col].strip()]:
                attCounts[atts[col].strip()][label] = 1
            
            # increment label counter for attribute value    
            else:
                attCounts[atts[col].strip()][label] += 1

        hofa = 0
        for value in attCounts.keys():
            hofv = 0
            for label in attCounts[value].keys():

                labelCount = attCounts[value][label]
                valueCount = int(math.fsum(attCounts[value].values()))
                hofv -= (labelCount / valueCount) * math.log(labelCount / valueCount, 4)

            hofa += (valueCount/len(examples)) * hofv

        gains[att] = hofs - hofa

    return gains

def GIofs(examples):

    labelCounts = {}
    for example in examples.keys():
        if examples[example] not in labelCounts:
            labelCounts[examples[example]] = 1
        else:
            labelCounts[examples[example]] += 1

    giofs = 0
    for label in labelCounts.keys():
        giofs += labelCounts[label]/len(examples) * labelCounts[label]/len(examples)

    return 1 - giofs

def MEofs(examples):

    labelCounts = {}
    for example in examples.keys():
        if examples[example] not in labelCounts:
            labelCounts[examples[example]] = 1
        else:
            labelCounts[examples[example]] += 1

    return (len(examples) - max(labelCounts.values())) / len(examples)

# determines the entropy of the dictionary, or entire data subset
def Hofs(examples):

    labelCounts = {}
    for example in examples.keys():
        if examples[example] not in labelCounts:
            labelCounts[examples[example]] = 1
        else:
            labelCounts[examples[example]] += 1

    hofs = 0
    for label in labelCounts.keys():
        hofs -= labelCounts[label]/len(examples) * math.log(labelCounts[label]/len(examples), 4)

    return hofs

#
#   Helper functions for main
#

def PredictionErrors(dt, examples, columns):
    errors = 0
    for key in examples.keys():
        if dt.Predict(key, columns) != examples[key]: errors += 1

    return errors

#
#   Main function
#
def main():

    # load csv and txt files into appropriate data structures
    train = LoadCSVFile("C:\\Users\\glend\\source\\repos\\CS5350-6350\\DecisionTree\\Data\\train.csv")
    test = LoadCSVFile("C:\\Users\\glend\\source\\repos\\CS5350-6350\\DecisionTree\\Data\\test.csv")
    tup = LoadTxtFile("C:\\Users\\glend\\source\\repos\\CS5350-6350\\DecisionTree\\Data\\data-desc.txt")

    h = 0
    gi = 1
    me = 2

    maxLevels = 10

    print("Entropy Decision Tree \n")
    print("\t Training \t Test \n")
    for i in range(1, maxLevels):
        dth = ID3(train, tup[0], tup[1], h, i)
        print("\t" + str(PredictionErrors(dth, train, tup[1])/len(train)) + "\t" + str(PredictionErrors(dth, test, tup[1])/len(test)) + "\n")

    print("\n")

    print("Gini Index Tree \n")
    print("\t Training \t Test \n")
    for i in range(1, maxLevels):
        dgi = ID3(train, tup[0], tup[1], gi, i)
        print("\t" + str(PredictionErrors(dgi, train, tup[1])/len(train)) + "\t" + str(PredictionErrors(dgi, test, tup[1])/len(test)) + "\n")

    print("Majority Error Tree \n")
    print("\t Training \t Test \n")
    for i in range(1, maxLevels):
        dtme = ID3(train, tup[0], tup[1], me, i)
        print("\t" + str(PredictionErrors(dtme, train, tup[1])/len(train)) + "\t" + str(PredictionErrors(dtme, test, tup[1])/len(test)) + "\n")

main()
