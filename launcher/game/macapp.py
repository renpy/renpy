import plistlib
import time


def write_plist(display_name, executable_name, version, filename):

    plist = dict(
        CFBundleDevelopmentRegion="English",
        CFBundleDisplayName=display_name,
        CFBundleExecutable=executable_name,
        CFBundleIconFiles="icon.icns",
        CFBundleInfoDictionaryVersion="6.0",
        CFBundleName=display_name,
        CFBundlePackageType="APPL",
        CFBundleShortVersionString=version,
        CFBundleVersion="1.0.{0}".format(int(time.time())),
        CFBundleDocumentTypes = {
            "CFBundleTypeOSTypes" : [ "fold" ],
            "CGBundleTypeRole" : "Viewer",
            },
            )
    
    plistlib.writePlist(plist, filename)
    
if __name__ == "__main__":
    
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("display_name")
    ap.add_argument("executable_name")
    ap.add_argument("version")
    ap.add_argument("filename")
    
    args = ap.parse_args()
    
    write_plist(args.display_name, args.executable_name, args.version, args.filename)
    
    