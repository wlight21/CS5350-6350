import DictionaryExtentions, InformationGain

def ID3(examples, attributes):

    # if all examples in this data subset have the same label, return a node with that label
    tuple = UnifiedLabel(examples);
    if tuple[0]: 
        if len(attributes) == 0:
            pass # return most common label from examples
        return Vertex(tuple[1]);

    return 0
