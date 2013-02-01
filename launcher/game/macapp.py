import plistlib
import time


def write_plist(display_name, executable_name, version, filename):

    plist = dict(
        CFBundleDevelopmentRegion="English",
        CFBundleDisplayName=display_name,
        CFBundleExecutable=executable_name,
        CFBundleIconFile="icon",
        CFBundleInfoDictionaryVersion="6.0",
        CFBundleName=display_name,
        CFBundlePackageType="APPL",
        CFBundleShortVersionString=version,
        CFBundleVersion="1.0.{0}".format(int(time.time())),
        CFBundleDocumentTypes = [ 
            {
                "CFBundleTypeOSTypes" : [ "****", "fold", "disk" ],
                "CFBundleTypeRole" : "Viewer",
            }, 
            ],
        UTExportedTypeDeclarations = [ 
            { 
                "UTTypeConformsTo" : [ "public.python-script" ],
                "UTTypeDescription" : "Ren'Py Script",
                "UTTypeIdentifier" : "org.renpy.rpy",
                "UTTypeTagSpecification" : { "public.filename-extension" : [ "rpy" ] }
            },
            ],
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
    
    