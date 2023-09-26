import argparse
import os

from . import filetypes

class UpdateError(Exception):
    """
    Raised when an error happens.
    """

    pass

class Plan(object):
    """
    This represents a plan for updating a single segment.
    """

    def __init__(self, block, source_filename, source_size, source_offset, compressed, target_filename, target_size, target_offset, hash):
        # Is source_fn a blockfile that might need to be downloaded?
        self.block = block

        # The source filename, size, and offset.
        self.source_filename = source_filename
        self.source_size = source_size
        self.source_offset = source_offset

        # If true, the source information is compressed.
        self.compressed = compressed

        # The target filename, size, and offset.
        self.target_filename = target_filename
        self.target_size = target_size
        self.target_offset = target_offset

        # The hash.
        self.hash = hash


class Update(object):

    def __init__(self, rpudir, newlists, targetdir, oldlists):
        self.targetdir = targetdir
        self.oldlists = oldlists
        self.sourcedir = rpudir
        self.newlists = newlists

        self.new_files = [ i for j in self.newlists for i in j.files ]
        self.old_files = [ i for j in self.oldlists for i in j.files ]
        self.block_files = [ i for j in self.newlists for i in j.blocks ]

        # A list of plan objects.
        self.plan = [ ]

        self.write_padding()
        self.find_incomplete_files()
        self.scan_old_files()
        self.remove_identical_files()
        self.create_plan()

    def log(self, message, *args):
        print(message % args)

    def rename(self, old, new):
        try:
            os.rename(old, new)
        except:
            os.unlink(new)
            os.rename(old, new)

    def find_incomplete_files(self):
        """
        Scan a directory, recursively, and add the files and directories
        found to this file test. This is intended for testing. This does
        not call .scan on the files.
        """

        root = self.targetdir

        for dn, dirs, files in os.walk(root):

            for fn in files:
                fn = os.path.join(dn, fn)

                if not fn.endswith(".new.rpu"):
                    continue

                oldfn = fn[:-len(".new.rpu")] + ".old.rpu"
                self.rename(fn, oldfn)

                relfn = os.path.relpath(oldfn, root)
                f = filetypes.File(relfn, data_filename=oldfn)
                self.old_files.append(f)

    def write_padding(self):
        """
        Writes a file containing the padding for RPAs, so it's
        not necessary to download a block file just for that.
        """

        padding = b"Made with Ren'Py."

        fn = os.path.join(self.targetdir, "_padding.old.rpa")
        with open(fn, "wb") as f:
            f.write(padding)

        f = filetypes.File("_padding.old.rpa", data_filename=fn)
        self.old_files.append(f)


    def scan_old_files(self):
        """
        Scans the old files, generating a list of segments.
        """

        # TODO: Progress

        for i in self.old_files:
            i.add_data_filename(self.targetdir)
            i.scan()

    def remove_identical_files(self):
        """
        Removes from self.source_files any file that exists and is identical
        to the file in self.target_files.
        """

        old_by_name = { i.name : i for i in self.old_files }

        new_files = [ ]

        self.log("Removing identical files:")

        for f in self.new_files:
            if f.name not in old_by_name:
                new_files.append(f)
                self.log("  new     %s", f.name)
                continue

            if f.segments != old_by_name[f.name].segments:
                new_files.append(f)
                self.log("  changed %s", f.name)
                continue

            self.log("  same    %s", f.name)

        self.log("%d files are unchanged.", len(self.new_files) - len(new_files))
        self.log("%d files are new/changed.", len(new_files))

        self.new_files = new_files


    def create_plan(self):
        """
        Creates the plan for updating everything, by finding each missing
        segment and creating a plan object.
        """

        # A map from segment hash to (block, file, segment) tuples.
        segment_locations = { }

        for f in sorted(self.block_files, key=lambda i : i.mtime):
            for s in f.segments:
                segment_locations[s.hash] = (True, f, s)

        for f in sorted(self.old_files, key=lambda i : i.mtime):
            for s in f.segments:
                segment_locations[s.hash] = (False, f, s)

        plan = [ ]

        for target_file in self.new_files:
            for target_segment in target_file.segments:
                block, source_file, source_segment = segment_locations.get(target_segment.hash, (False, None, None))

                if source_file is None:
                    self.log("Segment %s was not found.", target_segment.hash)
                    raise Exception("Segment %s was not found in index.")

                plan.append(Plan(
                    block,
                    source_file.data_filename or source_file.name,
                    source_segment.offset,
                    source_segment.size,
                    source_segment.compressed,
                    target_file.name,
                    target_segment.offset,
                    target_segment.size,
                    target_segment.hash,
                    ))

        plan.sort(key=lambda p : (p.block, p.source_filename, p.source_offset, p.source_size))

        self.log("Created a plan with %d entries.", len(plan))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sourcedir")
    ap.add_argument("targetdir")

    args = ap.parse_args()

    targetlist = filetypes.FileList()
    targetlist.scan(args.targetdir, data_filename=False)

    with open(os.path.join(args.sourcedir, "game.index.rpu"), "rb") as f:
        sourcelist = filetypes.FileList.decode(f.read())

    # from .util import dump
    # dump(sourcelist.to_json())

    Update(args.sourcedir, [ sourcelist ], args.targetdir, [ targetlist ])

if __name__ == "__main__":
    main()
