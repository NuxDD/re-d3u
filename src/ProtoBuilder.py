import re, sys
from Patterns import PATTERN_TYPE, Patterns
from TreeNode import NODE_TYPE, TreeNode

class ProtoBuilder():
    tree_head: TreeNode = None

    def __init__(self, buffer):
        self.tree_head = self.build_tree(buffer, 0)

    def build_tree(self, buffer, depth: int) -> TreeNode:
        cl_matches = Patterns.get_classes(buffer, depth)
        enum_matches = Patterns.get_enums(buffer, depth)

        node = None
        child = None

        if depth == 0:
            if len(cl_matches)+len(enum_matches) != 1:
                print("err: tree should have a single head")
                print(cl_matches)
                print(enum_matches)
                sys.exit(1)

        for _, (class_name, class_content) in enumerate(cl_matches):
            if node == None:
                node = TreeNode(NODE_TYPE.CLASS, class_name)
            child = self.build_tree(class_content, depth+1)
            if child != None:
                node.add_child(child)
            cl_fields_matches = Patterns.get_fields(class_content, depth+1)
            for _, (field_type, field_name) in enumerate(cl_fields_matches):
                node.add_child(TreeNode(NODE_TYPE.FIELD, field_name, field_type))

        for _, (enum_name, enum_content) in enumerate(enum_matches):
            if node == None:
                node = TreeNode(NODE_TYPE.ENUM, enum_name)
            node.add_child(self.build_tree(enum_content, depth+1))

        return node

if __name__ == "__main__":
    file_path = sys.argv[1]
    with open(file_path, 'r') as f:
        file_buffer = f.read()

    tmp_pb = ProtoBuilder(file_buffer)
    print(tmp_pb.tree_head)
