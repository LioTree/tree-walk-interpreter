import sys
import os

if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output filename>")
        os._exit(0)
    else:
        output_filename = sys.argv[1]
    source = ""
    expr = '''from abc import ABCMeta, abstractmethod

class Expr(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
      pass

'''
    source += expr
    define_ast = {
        # 'Binary':['left','operator','right'],
        # 'Grouping':['expression'],
        # 'Literal':['value'],
        # 'Unary':['operator','right']
        # 'Expression':['expression'],
        # 'Print':['expression']
        # 'Var':['name','initializer'],
        # 'Variable':['name']
        # 'Assign':['name','value']
        # 'Class':['name','methods']
        # "Get":['obj','name']
        # "Set":['obj','name','value']
        # "This":['keyword']
        "Super":["keyword","method"]
    }
    for name,fields in define_ast.items():
        temp = "class {}(Expr):\n".format(name)
        temp += "    def __init__(self"
        for f in fields:
            temp += ",{}".format(f)
        temp += "):\n"
        for f in fields:
            temp += "        self.{}={}\n".format(f,f)
        temp += "\n"
        temp += "    def accept(self,visitor):\n        return visitor.visit{}Expr(self)\n\n".format(name)
        source += temp
        
    source += "class Visitor(metaclass=ABCMeta):\n"
    for name in define_ast.keys():
        source += "    @abstractmethod\n    def visit{}Expr(self,exp):\n        pass\n\n".format(name)

    print(source)
    open(output_filename,'w').write(source)