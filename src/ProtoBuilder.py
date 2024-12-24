import re, sys
from Patterns import PATTERN_TYPE, Patterns
from TreeNode import NODE_TYPE, TreeNode

class ProtoBuilder():
    tree_head: TreeNode = None

    MATCHING_PROTOBUFF_TYPES = {
        'long': 'int64',
        'int': 'int32',
        'string': 'string',
        'bool': 'bool'
    }

    def __init__(self, buffer):
        self.tree_head = self.build_tree(buffer, 0)[0]

    def build_tree(self, buffer, depth: int) -> TreeNode:
        cl_matches = Patterns.get_classes(buffer, depth)
        enum_matches = Patterns.get_enums(buffer, depth)
        mess_matches = Patterns.get_messages(buffer, depth)

        node = []
        current_node = None
        enum_count = 0
        child = None

        if depth == 0:
            if len(mess_matches)+len(enum_matches) != 1:
                print("err: tree should have a single head")
                sys.exit(1)

        for _, (mess_name, mess_content) in enumerate(mess_matches):
            current_node = TreeNode(NODE_TYPE.MESSAGE, mess_name)
            children = self.build_tree(mess_content, depth+1)
            if children != None:
                for child in children:
                    current_node.add_child(child)
            mess_fields_matches = Patterns.get_class_fields(mess_content, depth+1)
            for _, (field_number, field_type, field_name) in enumerate(mess_fields_matches):
                # is this an important field ?
                if field_type != 'UnknownFieldSet':
                    if field_type in self.MATCHING_PROTOBUFF_TYPES.keys():
                        field_type = self.MATCHING_PROTOBUFF_TYPES[field_type]
                    current_node.add_child(TreeNode(NODE_TYPE.CLASS_FIELD, field_name, field_type, int(field_number)))
            node.append(current_node)

        for _, (class_name, class_content) in enumerate(cl_matches):
            current_node = TreeNode(NODE_TYPE.CLASS, class_name)
            children = self.build_tree(class_content, depth+1)
            if children != None:
                for child in children:
                    current_node.add_child(child)
            cl_fields_matches = Patterns.get_class_fields(class_content, depth+1)
            for _, (field_number, field_type, field_name) in enumerate(cl_fields_matches):
                # is this an important field ?
                if field_type != 'UnknownFieldSet':
                    if field_type in self.MATCHING_PROTOBUFF_TYPES.keys():
                        field_type = self.MATCHING_PROTOBUFF_TYPES[field_type]
                    current_node.add_child(TreeNode(NODE_TYPE.CLASS_FIELD, field_name, field_type, int(field_number)))
            node.append(current_node)

        for _, (enum_name, enum_content) in enumerate(enum_matches):
            current_node = TreeNode(NODE_TYPE.ENUM, enum_name)
            enum_fields_matches = Patterns.get_enum_fields(enum_content, depth+1)
            for field_name in enum_fields_matches:
                current_node.add_child(TreeNode(NODE_TYPE.ENUM_FIELD, field_name, None, int(enum_count)))
                enum_count += 1
            node.append(current_node)

        return node

if __name__ == "__main__":
    file_path = sys.argv[1]
    with open(file_path, 'r') as f:
        file_buffer = f.read()

    tmp_pb = ProtoBuilder(file_buffer)
    #print(tmp_pb.tree_head)
    tmp_pb.tree_head.pretty_display()
