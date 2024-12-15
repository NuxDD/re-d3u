import re, sys
from enum import Enum

class PATTERN_TYPE(Enum):
    CLASS=1; ENUM=2; CLASS_FIELD=3; ENUM_FIELD=4

class Patterns():
    CLOSE_PATTERN=r')\}'
    OPEN_PATTERN=r'.*?'
    MIDDLE_PATTERN=r'\s(\w+).*$\s+\{([\s\S]+?'

    @staticmethod
    def get_pattern(pattern: PATTERN_TYPE, depth: int) -> str:
        if depth < 0:
            print("err: invalid depth.")
            sys.exit(1)

        indent = r"^"
        if depth != 0:
            indent = indent + r"\t"*depth
            prefix = r''
        else: 
            prefix = r'^[^\t]'
        
        match pattern:
            case PATTERN_TYPE.CLASS:
                pattern_type=r'class'
            case PATTERN_TYPE.ENUM:
                pattern_type=r'enum'
            case PATTERN_TYPE.CLASS_FIELD:
                return indent + r'private\s+(\w+[\.\w]+?)\s(\w+);'
            case PATTERN_TYPE.ENUM_FIELD:
                return indent + r'\[OriginalName\(\"(.*?)\"\)\]'
            case _:
                print("err: non-implemented")
                sys.exit(1)

        return indent + prefix + Patterns.OPEN_PATTERN + pattern_type + Patterns.MIDDLE_PATTERN + indent + Patterns.CLOSE_PATTERN

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
