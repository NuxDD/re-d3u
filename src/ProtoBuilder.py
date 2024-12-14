import re, sys
from enum import Enum

class ProtoBuilder:

    proto_type=None
    proto_name=None
    proto_data=None

    KNOWN_PROTOBUFF_TYPES = ['int64', 'int32', 'string', 'bool']
    
    MATCHING_PROTOBUFF_TYPES = {
        'long': 'int64',
        'int': 'int32',
        'string': 'string',
        'bool': 'bool'
    }

    class PROTOTYPE(Enum):
        CLASS=1
        ENUM=2

    CLASS_PATTERN = r'class\s+(\w+)\s:.*\s\{([\s\S]*)\}'
    ENUM_PATTERN = r'enum\s+(\w+)\s+\{([\s\S]*)\}'

    def __init__(self, cs_buffer):
        self.determine_proto_type(cs_buffer)
        self.get_fields(cs_buffer)

    def __repr__(self):
        return f"Name={self.proto_name}; Type={self.proto_type};\nData={self.proto_data}"

    def determine_proto_type(self, buffer):
        if len(re.findall(self.CLASS_PATTERN, buffer)) > 0:
            self.proto_type = self.PROTOTYPE.CLASS
        elif len(re.findall(self.ENUM_PATTERN, buffer)) > 0:
            self.proto_type = self.PROTOTYPE.ENUM

    def get_fields(self, buffer):
        match self.proto_type:
            case self.PROTOTYPE.CLASS:
                cs_match = re.findall(self.CLASS_PATTERN, buffer)
                PATTERN = r'private\s+(\w+)\s(\w+);'
            case self.PROTOTYPE.ENUM:
                cs_match = re.findall(self.ENUM_PATTERN, buffer)
                PATTERN = r'\[OriginalName\("(.*?)"\)]'
            case _:
                #FIXME
                print("err: non-implemented")
                sys.exit(1)

        if len(cs_match) != 1:
            print("err: buffer should contain at most 1 class/enum")
            sys.exit(1)

        self.proto_name = cs_match[0][0]
        match_content = cs_match[0][1]

        fields_matches = re.findall(PATTERN, match_content)

        match self.proto_type:
            case self.PROTOTYPE.CLASS:
                self.data_from_cs_fields(fields_matches)
            case self.PROTOTYPE.ENUM:
                self.proto_data = fields_matches
            case _:
                #FIXME
                print("err: non-implemented")
                sys.exit(1)

    def data_from_cs_fields(self, matches: list):
        self.proto_data = dict()
        for _, (field_type, field_name) in enumerate(matches):
            if field_type == 'UnknownFieldSet':
                #FIXME: is this an important field ?
                continue
            if field_type in self.KNOWN_PROTOBUFF_TYPES:
                self.proto_data[field_name]=self.MATCHING_PROTOBUFF_TYPES[field_type]
            else:
                self.proto_data[field_name]=field_type

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        sys.exit(1)
        
    cs_file_path = sys.argv[1]
    file_buffer=""

    with open(cs_file_path, 'r') as f:
        file_buffer = f.read()
    
    print(ProtoBuilder(file_buffer))
