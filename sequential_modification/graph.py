# возможно стоит сначала определить родоначальника
class Genealogy:
    def __init__(self, child=None, forefather=None):
        self.forefather = forefather
        self.child = []
        if child != None:
            self.child.append(child)
        self.level = None


    def add_node(self, child, parent): # добавим новую пару родитель-ребенок, если родителя есть в уже добавленных детях и родителях, то к сооответвующему, если нет - тоо создаем новую пару
        if self.forefather is None:
            self.forefather = parent
            self.level = 0
            child = Genealogy(child=None, forefather=child)
            child.level = self.level + 1
            self.child.append(child)
        else:
            if self.forefather == parent:
                child = Genealogy(child=None, forefather=child)
                child.level = self.level + 1
                self.child.append(child)

            elif self.forefather == child:
                self.forefather = parent
                child = Genealogy(child=None, forefather=child)
                child.level = self.level
                self.child.append(child)

            elif parent in self.child:
                for ind, val in enumerate(self.child):
                    if parent == val:
                        child = Genealogy(child=None, forefather=child)
                        child.level = self.level + 1
                        self.child[ind].child.append(child)

            elif parent not in self.child:
                for i in self.child:
                    i.add_node(child, parent)







tree = Genealogy()
tree.add_node("Alexei", "Peter_I")
tree.add_node("Anna", "Peter_I")
tree.add_node("Elizabeth", "Peter_I")

tree.add_node("Peter_II","Alexei")
tree.add_node("Peter_III", "Anna")

tree.add_node("Paul_I", "Peter_III")

tree.add_node("Alexander_I", "Paul_I")
tree.add_node("Nicholaus_I" ,"Paul_I")



'''
Alexei Peter_I
Anna Peter_I
Elizabeth Peter_I
Peter_II Alexei
Peter_III Anna
Paul_I Peter_III
Alexander_I Paul_I
Nicholaus_I Paul_I
Anna Nicholaus_I
'''





