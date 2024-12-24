import re, sys
from enum import Enum

class PATTERN_TYPE(Enum):
    CLASS=1; ENUM=2; CLASS_FIELD=3; ENUM_FIELD=4; IMESSAGE_CLASS=5

class Patterns():

    @staticmethod
    def get_pattern(pattern: PATTERN_TYPE, depth: int) -> str:
        if depth < 0:
            print("err: invalid depth.")
            sys.exit(1)

        indent = r"^"
        if depth != 0:
            indent = indent + r"\t"*depth
        
        match pattern:
            case PATTERN_TYPE.IMESSAGE_CLASS:
                return indent + r'public\ssealed\sclass\s(\w+)\s:\sIMessage.*?\n' + indent + r'\{([\s\S]+?)' + indent + r'\}'
            case PATTERN_TYPE.CLASS:
                return indent + r'public\sstatic\sclass\s(\w+)\n' + indent + r'\{([\s\S]+?)' + indent + r'\}'
            case PATTERN_TYPE.ENUM:
                return indent + r'public\senum\s(\w+)\n' + indent + r'\{([\s\S]+?)' + indent + r'\}'
            case PATTERN_TYPE.CLASS_FIELD:
                return indent + r'public\sconst\sint\s[\w]+\s=\s([0-9]);\n.*?\n' + indent + r'\[FieldOffset\(Offset\s=\s".*?"\)\]\n' + indent + r'private\s+(\w+[\.\w]+?)\s(\w+);'
            case PATTERN_TYPE.ENUM_FIELD:
                return indent + r'\[OriginalName\(\"(.*?)\"\)\]'
            case _:
                print("err: non-implemented")
                sys.exit(1)

    @staticmethod
    def get_messages(buffer: str, depth: int):
        return re.findall(Patterns.get_pattern(PATTERN_TYPE.IMESSAGE_CLASS, depth), buffer, re.MULTILINE)

    @staticmethod
    def get_classes(buffer: str, depth: int):
        return re.findall(Patterns.get_pattern(PATTERN_TYPE.CLASS, depth), buffer, re.MULTILINE)
        
    @staticmethod
    def get_enums(buffer: str, depth: int):
        return re.findall(Patterns.get_pattern(PATTERN_TYPE.ENUM, depth), buffer, re.MULTILINE)

    @staticmethod
    def get_class_fields(buffer: str, depth: int):
        return re.findall(Patterns.get_pattern(PATTERN_TYPE.CLASS_FIELD, depth), buffer, re.MULTILINE)

    @staticmethod
    def get_enum_fields(buffer: str, depth: int):
        return re.findall(Patterns.get_pattern(PATTERN_TYPE.ENUM_FIELD, depth), buffer, re.MULTILINE)
