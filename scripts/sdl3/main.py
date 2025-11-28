import argparse
import pathlib
import re

try:
    from clang import cindex
    from clang.cindex import CursorKind
except ImportError as e:
    print("ERROR: libclang Python bindings not available (install libclang)", file=sys.stderr)
    raise


class Generator:

    def __init__(self, sdl3_path: pathlib.Path):
        """
        `sdl3_path`
            The path to the SDL3 directory.
        """

        self.sdl3_path: pathlib.Path = sdl3_path

        self.declarations: list[tuple[pathlib.Path, str]] = [ ]
        """
        Aa list of (header, declaration_text) tuples.
        """

        self.declared_names = set()

    def declare(self, cursor: cindex.Cursor, decl: str):
        """
        Add a declaration to the list of declarations.

        `cursor`
            The cursor that corresponds to the declaration.
        `decl`
            The declaration text.
        """

        if cursor.location.file is None:
            return

        header = pathlib.Path(cursor.location.file.name).relative_to(self.sdl3_path)
        self.declarations.append((header, decl))

    def generate(self):
        old_header: pathlib.Path|None = None

        print
        print("from libc.stdint cimport *")
        print("from libc.stddef cimport wchar_t")
        print("from libcpp cimport bool as cbool")
        print("ctypedef struct va_list")
        print()


        for header, decl in self.declarations:
            if header != old_header:
                if old_header is not None:
                    print()

                print(f"cdef extern from \"{header}\":")

                old_header = header

            print(decl)


    def is_relevant(self, node: cindex.Cursor) -> bool:
        """
        Returns True if the node exists in the SDL3 directory, False otherwise. T
        """

        if node.location.file is None:
            return False

        return pathlib.Path(node.location.file.name).is_relative_to(self.sdl3_path)


    def check_new_name(self, name: str) -> bool:
        """
        Check if the name has already been declared. If not, add it to the set of declared names.

        `name`
            The name to check.

        Returns True if the name is new, False otherwise.
        """

        if name in self.declared_names:
            return False

        self.declared_names.add(name)
        return True

    def enum(self, node: cindex.Cursor):
        if not self.is_relevant(node):
            return

        if not self.check_new_name(node.spelling):
            return

        self.declare(node, f"    cpdef enum {node.spelling}:")
        for child in node.get_children():
            if child.kind == CursorKind.ENUM_CONSTANT_DECL:
                self.declare(child, f"        {child.spelling}")

    def elide_tokens(self, t: cindex.Cursor) -> str:
        tokens = t.get_tokens()
        parts = []
        for token in tokens:
            if token.spelling in { "typedef", "struct", "union", "enum", "__attribute__", "__extension__", "__inline__", "SDLCALL" }:
                continue

            if token.spelling == "bool":
                parts.append("cbool")
            else:
                parts.append(token.spelling)

        joined = " ".join(parts)

        joined = re.sub(r'\( ', '(', joined)
        joined = re.sub(r' \)', ')', joined)
        joined = re.sub(r'\) \(', ')(', joined)
        joined = re.sub(r' ,', ',', joined)
        joined = re.sub(r'\* ', '*', joined)
        joined = re.sub(r'\(void\)', '()', joined)

        return joined

    def type_spelling(self, t: cindex.Type) -> str:
        spelling = t.spelling

        spelling = re.sub(r'\b(struct|union|enum)\b\s*', '', spelling)
        return spelling.strip()

    def function(self, node: cindex.Cursor):
        if not self.is_relevant(node):
            return

        name = node.spelling

        if not self.check_new_name(name):
            return

        ret_type = node.result_type.spelling
        params = []
        for arg in node.get_arguments():

            params.append(self.elide_tokens(arg))

            # param_type = arg.type.spelling
            # param_name = arg.spelling or "_"  # Cython permits unnamed but keep underscore
            # if param_type.endswith("*"):
            #     params.append(f"{param_type}{param_name}")
            # else:
            #     params.append(f"{param_type} {param_name}")

        if ret_type.endswith("*"):
            sig = f"{ret_type}{name}({', '.join(params)})"
        else:
            sig = f"{ret_type} {name}({', '.join(params)})"

        self.declare(node, f"    {sig}")

    def struct(self, node: cindex.Cursor):
        if not self.is_relevant(node):
            return

        if not self.check_new_name(node.spelling):
            return

        self.declare(node, f"    cdef struct {node.spelling}:")

        has_fields = False

        for child in node.get_children():
            if child.kind == CursorKind.FIELD_DECL:
                self.declare(child, f"        {self.elide_tokens(child)}")
                has_fields = True

        if not has_fields:
            self.declare(node, f"        pass")

    def union(self, node: cindex.Cursor):
        if not self.is_relevant(node):
            return

        if "unnamed at" in node.spelling:
            return

        if not self.check_new_name(node.spelling):
            return

        self.declare(node, f"    cdef union {node.spelling}:")

        has_fields = False

        for child in node.get_children():
            if child.kind == CursorKind.FIELD_DECL:
                self.declare(child, f"        {self.elide_tokens(child)}")
                has_fields = True

        if not has_fields:
            self.declare(node, f"        pass")

    def typedef(self, node: cindex.Cursor):
        if not self.is_relevant(node):
            return

        if not self.check_new_name(node.spelling):
            return

        decl = self.elide_tokens(node)

        if not decl.strip():
            self.declare(node, f"    # Skipping empty typedef {node.spelling}")
            return

        self.declare(node, f"    ctypedef {decl}")

    def traverse(self, node: cindex.Cursor, depth: int):

        if node.spelling == "SDL_GamepadBinding":
            return

        # print("  " * depth, node.kind, node.location, repr(node.spelling)[:100])

        for child in node.get_children():
            self.traverse(child, depth+1)

        if node.kind == CursorKind.FUNCTION_DECL:
            self.function(node)

        elif node.kind == CursorKind.TYPEDEF_DECL:
            self.typedef(node)

        elif node.kind == CursorKind.ENUM_DECL:
            self.enum(node)

        elif node.kind == CursorKind.STRUCT_DECL:
            self.struct(node)

        if node.kind == CursorKind.UNION_DECL:
            self.union(node)

def main():
    ap = argparse.ArgumentParser(description="SDL3 Binding Generator")

    ap.add_argument("header", help="Path to the SDL3/SDL.h header file.", type=pathlib.Path)

    args = ap.parse_args()

    sdl_h_path: pathlib.Path = args.header.absolute()
    "The path to the SDL3/SDL.h header file, made absolute."

    sdl3_path: pathlib.Path = sdl_h_path.parent
    "If SDL3 is in /usr/include/SDL3/SDL.h, then sdl3_path is /usr/include/SDL3."

    include_dir: pathlib.Path = sdl3_path.parent
    "If SDL3 is in /usr/include/SDL3, then include_dir is /usr/include."

    index = cindex.Index.create()
    options = cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    index_args = [f"-I{include_dir}", "-DSDL_MAIN_HANDLED" ]

    tu = index.parse(str(args.header), args=index_args, options=options)

    generator = Generator(sdl3_path)
    generator.traverse(tu.cursor, 0)
    generator.generate()

if __name__ == "__main__":
    main()
