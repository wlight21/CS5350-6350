import DecisionTree, ID3

def LoadCSVFile(filename):

    with open(filename, 'r') as file:

        dict = {}

        for line in file:
            line = line.rstrip(); line = line.split(",")
            dict[str(line[0:5]).replace('[', '').replace(']','')] = line[6]

        return dict

def LoadTxtFile(filename):

    with open(filename, 'r') as file:

        dict = {}

        for line in file:
            line = line.rstrip(); line = line.split(":")

            if len(line) > 1:
                dict[line[0]] = str(line[1]).lstrip().replace('.','');

        return dict
            
def main():

    train = LoadCSVFile("C:\\Users\\glend\\Source\\Repos\\CS5350-6350\\DecisionTree\\Data\\train.csv")
    att = LoadTxtFile("C:\\Users\\glend\\Source\\Repos\\CS5350-6350\\DecisionTree\\Data\\data-desc.txt")

    ID3(train, att)



main()