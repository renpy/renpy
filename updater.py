# This code applies an update.

import tarfile
import threading
import traceback
import os
import urlparse
import urllib
import json
import subprocess
import hashlib

try:
    from renpy.exports import fsencode
except:
    def fsencode(s):
        return s

class UpdateError(Exception):
    """
    Used to report known errors.
    """

class UpdateCancelled(Exception):
    """
    Used to report the update being cancelled.
    """

class Updater(threading.Thread):
    """
    Applies an update.
    
    Fields on this object are used to communicate the state of the update process.
    
    self.state
        The state that the updater is in.
        
    self.message
        In an error state, the error message that occured.
        
    self.progress
        If not None, a number between 0.0 and 1.0 giving some sort of 
        progress indication.
        
    self.can_cancel
        A boolean that indicates if cancelling the update is allowed.
    
    """

    # Here are the possible states.
    
    # An error occured during the update process.
    # self.message is set to the error message.
    ERROR = 0
    
    # Checking to see if an update is necessary.
    CHECKING = 1
    
    # We are up to date. The update process has ended.
    # Calling proceed will return to the main menu.
    UPDATE_NOT_AVAILABLE = 2
    
    # An update is available.
    # The interface should ask the user if he wants to upgrade, and call .proceed()
    # if he wants to continue. 
    UPDATE_AVAILABLE = 3
    
    # Preparing to update by packing the current files into a .update file.
    # self.progress is updated during this process.
    PREPARING = 4
    
    # Downloading the update.
    # self.progress is updated during this process.
    DOWNLOADING = 5
    
    # Unpacking the update.
    # self.progress is updated during this process.
    UNPACKING = 6
    
    # Finishing up, by moving files around, deleting obsolete files, and writing out
    # the state.
    FINISHING = 7
    
    # Done. The update completed successfully.
    # Calling .proceed() on the updater will trigger a game restart.
    DONE = 8
    
    # The update was cancelled.
    CANCELLED = 9
    
    def __init__(self, url, base, force=False):
        """
        `force`
            Force the update to occur even if the version numbers are 
            the same. (Used for testing.)
        """


        # The main state.
        self.state = Updater.CHECKING
        
        # An additional message to show to the user.
        self.message = None
        
        # The progress of the current operation, or None.
        self.progress = None

        # True if the user can click the cancel button.
        self.can_cancel = True
        
        # True if the user can click the proceed button.
        self.can_proceed = False

        # True if the user has clicked the cancel button.
        self.cancelled = False
        
        # True if the user has clocked the proceed button.
        self.proceeded = False
        
        # The url of the updates.json file.
        self.url = url

        # Force the update?
        self.force = force
        
        # The base path of the game that we're updating, and the path to the update
        # directory underneath it.
        self.base = os.path.abspath(base)
        self.updatedir = os.path.join(self.base, "update")

        # A condition that's used to coordinate things between the various 
        # threads.
        self.condition = threading.Condition()

        # The logfile that update errors are written to.
        try:
            self.log = open(os.path.join(self.updatedir, "log.txt"), "w")
        except:
            self.log = None

        self.update()

        
 
    
    def run(self):
        """
        The main function of the update thread, handles errors by reporting 
        them to the user.
        """
        
        try:
            update()
    
        except UpdateCancelled as e:
            self.can_cancel = True
            self.can_proceed = False
            self.progress = None
            self.message = None
            self.state = self.CANCELLED
        
        except UpdateError as e:
            self.message = e.message
            self.can_cancel = True
            self.can_proceed = False
            self.state = self.ERROR
        
        except Exception as e:
            self.message = unicode(e)
            self.can_cancel = True
            self.can_proceed = False
            self.state = self.ERROR

            if self.log:
                traceback.print_exc(None, self.log)

        
    def update(self):
        """
        Performs the update.        
        """
        
        self.load_state()
        self.test_write()
        self.check_updates()
        self.check_versions()

        if not self.modules:
            self.can_cancel = False
            self.can_proceed = True
            self.state = self.UPDATE_NOT_AVAILABLE
            return
        
        # TODO: Enter and leave the update available state.

        if self.cancelled:
            raise UpdateCancelled()
        
        self.new_state = dict(self.current_state)

        self.progress = 0.0
        self.state = self.PREPARING
        
        for i in self.modules:
            self.prepare(i)

        self.progress = 0.0
        self.state = self.DOWNLOADING

        for i in self.modules:
            self.download(i) 
        
        return
        
    def url(self, suffix):
        """
        Joins the URL together.
        """
            
    def load_state(self):
        """
        Loads the current update state from update/current.json
        """
        
        fn = os.path.join(self.updatedir, "current.json")
        
        if not os.path.exists(fn):
            raise UpdateError("Either this project does not support updating, or the update status file was deleted.")
        
        with open(fn, "r") as f:
            self.current_state = json.load(f)
   
    def test_write(self):
        fn = os.path.join(self.updatedir, "test.txt")

        try:
            with open(fn, "w") as f:
                f.write("Hello, World.")
                
            os.unlink(fn)
        except:
            raise UpdateError("This account does not have permission to perform an update.")

        if not self.log:
            raise UpdateError("This account does not have permission to write the update log.")
        
    def check_updates(self):
        """
        Downloads the list of updates from the server, parses it, and stores it in 
        self.updates
        """
        
        fn = os.path.join(self.updatedir, "updates.json")
        urllib.urlretrieve(self.url, fn)
        
        with open(fn, "r") as f:
            self.updates = json.load(f)
        
    def check_versions(self):
        """
        Decides what modules need to be updated, if any.
        """
        
        # A list of names of modules we want to update.
        self.modules = [ ]
        
        # We update the modules that are in both versions, and that are out of date.
        for name, data in self.current_state.iteritems():
            
            if name not in self.updates:
                continue
            
            if data["version"] == self.updates[name]["version"]:
                if not self.force:
                    continue
            
            self.modules.append(name)

    def update_filename(self, module, new):
        """
        Returns the update filename for the given module.
        """
        
        rv = os.path.join(self.updatedir, module + ".update")
        if new:
            return rv + ".new"
            
        return rv

    def prepare(self, module):
        """
        Creates a tarfile creating the files that make up module. 
        """
        
        state = self.current_state[module]
        
        xbits = set(state["xbit"])
        directories = set(state["directories"])
        all = state["files"] + state["directories"] 
        all.sort()

        # Add the update directory and state file. 
        all.append("update")
        directories.add("update")
        all.append("update/current.json")

        tf = tarfile.TarFile(self.update_filename(module, False), "w")

        for i, name in enumerate(all):

            if self.cancelled:
                raise UpdateCancelled()
            
            self.progress = 1.0 * i / len(all)
            
            directory = name in directories
            xbit = name in xbits
            
            # TODO: Mac translation support.

            path = os.path.join(self.base, name)
            
            if directory:
                info = tarfile.TarInfo(name)
                info.size = 0
                info.type = tarfile.DIRTYPE
            else:
                if not os.path.exists(path):
                    continue
                
                info = tf.gettarinfo(path, name)

                if not info.isreg():
                    continue
                
            info.uid = 1000
            info.gid = 1000
            info.mtime = 0
            info.uname = "renpy"
            info.gname = "renpy"
                
            if xbit or directory:
                info.mode = 0777
            else:
                info.mode = 0666
                
            if info.isreg():
                with open(path, "rb") as f:
                    tf.addfile(info, f)
            else:
                tf.addfile(info)
                
        tf.close()

    def download(self, module):
        """
        Uses zsync to download the module.
        """
        
        start_progress = None
        
        new_fn = self.update_filename(module, True)
        
        cmd = [ 
            "./zsync",
            "-o", new_fn, 
            "-k", os.path.join(self.updatedir, module + ".zsync")
            ]
        
        for i in self.modules:
            cmd.append("-i")
            cmd.append(self.update_filename(module, False))
            
        cmd.append(urlparse.urljoin(self.url, module + ".zsync"))
        
        cmd = [ fsencode(i) for i in cmd ]
        
        self.log.flush()
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)

        while True:
            l = p.stdout.readline()
            if not l:
                break
        
            self.log.write(l)
            
            if l.startswith("PROGRESS "):
                _, raw_progress = l.split(' ', 1)
                raw_progress = float(raw_progress) / 100.0
                
                if raw_progress == 1.0:
                    self.progress = 1.0
                    continue
                
                if start_progress is None:
                    start_progress = raw_progress
                    self.progress = 0.0
                    continue
                
                self.progress = (raw_progress - start_progress) / (1.0 - start_progress)
                print self.progress
                
            if l.startswith("ENDPROGRESS"):
                start_progress = None
                self.progress = None
        
        p.wait()
        
        # Check the existence of the downloaded file.
        if not os.path.exists(new_fn):
            raise UpdateError("The update file was not downloaded.")
        
        # Check that the downloaded file has the right digest.    
        import hashlib    
        with open(new_fn, "r") as f:
            hash = hashlib.sha256()
            
            while True:
                data = f.read(1024 * 1024)

                if not data:
                    break

                hash.update(data)
                
            digest = hash.hexdigest()
            
        if digest != self.updates[module]["digest"]:
            raise UpdateError("The update file does not have the correct digest - it may have been corrupted.")
        
        
   
if __name__ == "__main__":
   import argparse
   ap = argparse.ArgumentParser()
   
   ap.add_argument("url")
   ap.add_argument("base")
   
   args = ap.parse_args()
   
   Updater(args.url, args.base)
                
        
        
        
        
    
    
    
    
    
    
    