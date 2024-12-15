from enum import Enum

class NODE_TYPE(Enum):
    CLASS=1 #Message ?
    ENUM=2
    FIELD=3

class TreeNode():
    node_type: NODE_TYPE = None
    node_name: str = None
    node_var_type: str = None
    node_children = None

    def __init__(self, n_type: NODE_TYPE, n_name: str, n_var_type = None):
        self.node_type = n_type
        self.node_name = n_name
        if n_type == NODE_TYPE.FIELD:
            if n_var_type == None:
                print("err: type cannot be None for Fields")
                sys.exit(1)
        self.node_var_type = n_var_type
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
        if self.node_type == NODE_TYPE.FIELD:
            return f"Name={self.node_name}; Type={self.node_var_type};{children_str}"
        return f"Name={self.node_name}; Type={self.node_type};{children_str}"
