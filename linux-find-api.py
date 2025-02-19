from abc import abstractmethod
from enum import Enum

"""
This is recursive find implementation
"""
class Ftype(Enum):
    FILE = 0
    DIRECTORY = 1
    SYMLINK = 2


class IFileNode:
    def __init__(self,ftype: str,  name: str,  size: int):
        self.ftype = ftype
        self.name = name
        self.size = size

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def __repr__(self):
        return f'{self.name} - {self.ftype}'

class File(IFileNode):
    def __init__(self, name: str, ext: str, size: int):
        super().__init__(Ftype.FILE, name, size)
        self.ext = ext

class Directory(IFileNode):
    def __init__(self, name: str, children: list[IFileNode] = None, size: int = 0):
        super().__init__(Ftype.DIRECTORY, name, size)
        self.children = children if children is not None else []
        
    def add_child(self, fileNode : IFileNode):
        self.children.append(fileNode)
        self.size += fileNode.get_size()
        

    def remove_child(self, fileNode: IFileNode):
        if fileNode not in self.children:
            raise ValueError(f"{fileNode} not found in {self.name} dir")
        self.children.remove(fileNode)
        self.size -= fileNode.get_size()



class Icriteria:
    @abstractmethod
    def apply(self, fileNode):
        pass

class FileNameCriteria(Icriteria):

    def __init__(self, taget_name: str):
        self.target_name = taget_name

    def apply(self, fileNode: IFileNode):
        return fileNode.get_name()  ==  self.target_name


class GreaterThanSizeCriteria(Icriteria):

    def __init__(self, target_size: int):
        self.target_size = target_size

    def apply(self, fileNode: IFileNode):
        return fileNode.get_size() >= self.target_size


class DefaultCriteria(Icriteria):
    def apply(self, fileNode):
        return True
    

class AndCriteria(Icriteria):
    def __init__(self, criteria1: Icriteria, criteria2: Icriteria):
        self.criteria1 = criteria1
        self.criteria2 = criteria2

    def apply(self, fileNode: IFileNode):
        return self.criteria1.apply(fileNode) and self.criteria2.apply(fileNode)
    

class OrCriteria(Icriteria):
    def __init__(self, criteria1: Icriteria, criteria2: Icriteria):
        self.criteria1 = criteria1
        self.criteria2 = criteria2

    def apply(self, fileNode: IFileNode):
        return self.criteria1.apply(fileNode) or self.criteria2.apply(fileNode)
    

# apply method called recursively top down
class BuildCriteria(Icriteria):

    def __init__(self):
        self.build_criteria = DefaultCriteria()

    def and_op(self, criteria: Icriteria):
        self.build_criteria = AndCriteria(self.build_criteria, criteria)
        return self

    def or_op(self, criteria: Icriteria):
        self.build_criteria = OrCriteria(self.build_criteria, criteria)
        return self
    
    def build(self):
        return self.build_criteria
    

class Find:
    def __init__(self):
        self.result = []

    def find_api(self, root: IFileNode, criteria: Icriteria):
        self.find_helper(root, criteria)
        return self.result
            
    def find_helper(self, root: IFileNode, criteria: Icriteria):
        if root.ftype == Ftype.FILE:
            self.result += [root] if criteria.apply(root) else []
            return
        for child in root.children:
            self.find_helper(child, criteria)
    


if __name__ == "__main__":
    dir1 = Directory('dir1')
    root = Directory('/')
    # print(root, root.children)
    file1 = File('file1','pdf',100)
    file2 = File('file2','xml', 20)
    file3  = File('file3', 'pdf',90)
    dir1.add_child(file1)
    dir1.add_child(file2)
    # print(dir1, dir1.children)
    root.add_child(dir1)
    # print(root, root.children)

    criteria = BuildCriteria() \
                    .and_op(FileNameCriteria("file2"))\
                    .and_op(GreaterThanSizeCriteria(50))\
                    .build()
    lib = Find()
    print(lib.find_api(root,criteria))
