python early:


    def read_example(fn, line):

        fn = fn.replace("game/", "")

        with renpy.file(fn) as f:
            data = f.read()

        lines = [ i.rstrip() for i in data.split("\n") ]

        rv = [ ]

        base_indent = 0

        while True:
            l = lines[line]
            line += 1

            if not l:
                rv.append(l)
                continue

            indent = len(l) - len(l.lstrip())

            if base_indent == 0:
                base_indent = indent
                rv.append(l[4:])
            elif indent >= base_indent:
                rv.append(l[4:])
            else:
                break


        for i in rv:
            print(i)

    def parse_example(l):
        read_example(l.filename, l.number)
        return {}

    def next_example(data, first):
        return first

    def execute_example(data):
        return

    renpy.register_statement("example", parse=parse_example, execute=execute_example, next=next_example, block="script")
