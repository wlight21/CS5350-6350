# indicates whether the dictionary has a unified value, and outputs the value
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

    maxLabel
    maxCount = 0

    for key in count.keys():
        if count[key] > maxCount:
            maxLabel = key
            maxCount = count[key]


    return maxLabel
