from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent


def main():
    with open(ROOT / 'sphinx' / 'source' / 'config.rst') as f:
        lines = f.readlines()


    # Read in the old config.
    var = { }

    while lines:

        l = lines.pop(0)

        if l.startswith(".. var::"):
            name = l.split()[2]

            content = [ l ]

            while lines:

                if not lines[0].strip():
                    content.append(lines.pop(0))
                elif lines[0][0] == ' ':
                    content.append(lines.pop(0))
                else:
                    break

            var[name] = content


    with open(ROOT / 'sphinx' / 'source' / 'newconfig.rst') as f:
        lines = f.readlines()

    newlines = [ ]
    stash = [ ]

    for l in lines:

        if l.startswith(".. var::"):
            stash.append(l)
        else:
            if stash:
                newlines.extend(sorted(stash))
                stash = [ ]
            newlines.append(l)

    else:
        newlines.extend(sorted(stash))



    for l in newlines:

        if l.startswith(".. var::"):
            name = l.split()[2]

            if name in var:
                sys.stdout.writelines(var[name])
                del var[name]

            else:
                sys.stdout.write(l)
        else:
            sys.stdout.write(l)

    if var:
        print("Unmatched variables:")
        for k in var:
            print(k)



if __name__ == '__main__':
    main()
