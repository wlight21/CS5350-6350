# class to represent a Decision Tree
# Decision Trees are DAGs with string vertices and edge weights

class DecisionTree(object):
    
    # class to represent a vertex in a Decision Tree.  Decision Tree Vertices are defined as having a 
    # label and list of out edges with string defined edge weights
    class Vertex(object):
        
        def __init__(name):
            self.Name = name
            self.OutEdges = {};

        def AddEdge(v, weight):
            self.OutEdges[v] = weight;
    
    def __init__():
        self.Vertices = {}
        self.Root

    def SetRoot(v):
        Vertices[v] = Vertex(v)
        Root = Vertices[v]

    def AddEdge(v1, v2, weight):
        if not Vertices.contains(v1):
            Vertices.add(v1, Vertex(v1))
        if not Vertices.contains(v2):
            Vertices.add(v2, Vertex(v2))

        Vertices[v1].AddEdge(v2, weight)

    def size(self):
        return len(Vertices)





