from enum import Enum

class NODE_TYPE(Enum):
    CLASS=1 #Message ?
    ENUM=2
    CLASS_FIELD=3
    ENUM_FIELD=4
    MESSAGE=5

class TreeNode():
    node_type: NODE_TYPE = None
    node_name: str = None
    node_var_type: str = None
    node_children = None
    node_field_number = None

    def __init__(self, n_type: NODE_TYPE, n_name: str, n_var_type = None, n_field_number = None):
        self.node_type = n_type
        self.node_name = n_name
        if n_type == NODE_TYPE.CLASS_FIELD:
            if n_var_type == None:
                print("err: type cannot be None for class Fields")
                sys.exit(1)
        self.node_var_type = n_var_type
        self.node_field_number = n_field_number
        self.node_children = list()

    def add_child(self, child_node):
        self.node_children.append(child_node)

    def __repr__(self):
        children_str = ""
        if len(self.node_children) > 0:
            children_str: str = f"\nChildren(len={len(self.node_children)})=[\n"
            for _, c in enumerate(self.node_children):
                children_str += f"\t{c}\n"
            children_str += f"]"
        if self.node_type == NODE_TYPE.CLASS_FIELD:
            return f"Name={self.node_name}: Type={self.node_var_type}"
        if self.node_type == NODE_TYPE.ENUM_FIELD:
            return f"Name={self.node_name}"
        return f"Name={self.node_name}; Type={self.node_type};{children_str}"

    def pretty_display(self, depth = 0):
        indent = "   "*depth
        print(f"{self.node_var_type}:{self.node_name} ({self.node_field_number}); node={self.node_type};")
        for _, child in enumerate(self.node_children):
            print(indent + "---> ", sep="", end="")
            child.pretty_display(depth+1)
