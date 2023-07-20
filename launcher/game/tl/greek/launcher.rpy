translate greek strings:
    # game/new_project.rpy:77
    old "{#language name and font}"
    new "{font=fonts/Roboto-Light.ttf}Ελληνικά{/font}"

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "Δείτε την άδεια χρήσης"

    # add_file.rpy:28
    old "FILENAME"
    new "ΟΝΟΜΑ_ΑΡΧΕΙΟΥ"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "Δώστε το όνομα του προς δημιουργία αρχείου σεναρίου-κώδικα"

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "Το όνομα του αρχείου πρέπει να έχει την επέκταση .rpy "

    # add_file.rpy:39
    old "The file already exists."
    new "Υπάρχει ήδη αυτό το αρχείο."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Η Ren'Py αυτόματα φορτώνει όλα τα αρχεία σεναρίων-κώδικα με την κατάληξη .pry . Για να χρησιμοποιήσετε ένα \n # αρχείο, δημιουργήστε μέσα στο αρχείο προς χρήση μία ετικέτα (label) και κάντε μια μεταπήδηση στην ετικέτα (jump), από ένα άλλο αρχείο.\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Για να χτίσετε πακέτα για το Android, παρακαλούμε κατεβάστε το RAPT και τοποθετήστε το στον φάκελο της Ren'Py. Κατόπιν αυτού, επανεκκινήστε τον Εκκινητή."

    # android.rpy:31
    old "An x86 Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Αν εργάζεστε σε Windows, για τη δημιουργία πακέτων Android, απαιτείται ένα x86 Java Development Kit. Το JDK είναι διαφορετικό του JRE, οπότε μπορεί να έχετε Java χωρίς όμως να έχετε το JDK. Παρακαλoύμε λοιπόν να  {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html} κατεβάσετε κι εγκαταστήσετε από εδώ το JDK{/a} και κατόπιν να επανεκκινήσετε τον Εκκινητή της Ren'Py. "

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "Το RAPT έχει εγκατασταθεί, αλλά θα πρέπει να εγαταστήσετε το Android SDK για να μπορέσετε να χτίσετε πακέτα Android. Επιλέξτε να εγκαταστήσετε το SDK για να γίνει αυτό."

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "Το RAPT έχει εγκατασταθεί, αλλά δεν έχετε ορίσει ένα κλειδί. Παρακαλώ δημιουργήστε ένα νέο κλειδί ή επαναφέρετε το android.keystore."

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "Το συγκεκριμένο έργο δεν έχει ρυθμιστεί. Χρησιμοποιήστε το \"Ρύθμιση\" για να το ρυθμίσετε προτού το χτίσετε."

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "Επιλέξτε \"Χτίσε\" για να χτίσετε το συγκεκριμένο έργο σας ή συνδέστε μια συσκευή Android κι επιλέξτε \"Χτίσε κι εγκατέστησε\" για να το χτίσετε και να το εγκαταστήσετε στη συσκευή."

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Επιχειρεί να προσομοιώσει ένα τηλέφωνο με Android. \n\nΗ οθόνη αφής προσομοιώνεται με το ποντίκι, αλλά μόνο όταν κρατάτε πατημένο το κουμπί. Το πλήκτρο Escape αντιστοιχεί στο κουμπί menu και το PageUP στο κουμπί \"Πίσω\""

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Επιχειρεί να προσομοιώσει ένα tablet με Android. \n\n Η οθόνη αφής προσομοιώνεται με το ποντίκι, αλλά μόνο όταν κρατάτε πατημένο το κουμπί. Το πλήκτρο Escape αντιστοιχεί στο κουμπί menu και το PageUP στο κουμπί \"Πίσω\""

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Επιχειρεί να προσομοιώσει μια κονσόλα για τηλεόραση, που τρέχει Android, σαν το OUYA ή το Fire TV. \n\n Τα πλήκτρα με τα βέλη αντιστοιχούν στα πλήκτρα σταυρό με βέλη του χειριστηρίου, το Enter είναι το Select, το πλήκτρο Escape αντιστοιχεί στο κουμπί menu και το PageUP στο κουμπί \"Πίσω\""

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "Κατεβάζει κι εγκαθιστά το Android SDK και τα υποστηρικτικά πακέτα. Προαιρετικά δημιουργεί τα απαιτούμενα κλειδιά, για να δοθεί υπογραφή στο πακέτο."

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "Ρυθμίζει το όνομα του πακέτου, την έκδοση κι άλλες πληροφορίες για το έργο."

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "Ανοίγει το αρχείο που περιέχει τα κλειδιά του Google Play στον επεξεργαστή κειμένου.\n\nΑυτό θα το χρειαστέτε μόνο αν η εφαρμογή θα χρησιμοποιεί επέκταση APK. Διαβάστε τα εγχειρίδια για περισσότερς λεπτομέρεις."

    # android.rpy:44
    old "Builds the Android package."
    new "Χτίζει το πακέτο Android."

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "Χτίζει το πακέτο Android και το εγκαθιστά σε μια συσκευή Android συνδεδεμένη στον Η/Υ."

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "Χτίζει το πακέτο Android, το εγκαθιστά σε μια συσκευή Android συνδεδεμένη στον Η/Υ και το εκτελεί."

    # android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "Σύνδεση σε συσκευή Android που τρέχει ADB, με TCP/IP"

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "Αποσύνδεση από συσκευή Android που τρέχει ADB, με TCP/IP"

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "Λήψη καταγεγραμμένων συμβάντων από τη συσκευή Android  και καταγραφή τους σε αρχείο."

    # android.rpy:240
    old "Copying Android files to distributions directory."
    new "Αντιγράφονται τα αρχεία για Android στο φάκελο της διανομής"

    # android.rpy:304
    old "Android: [project.current.name!q]"
    new "Android: [project.current.name!q]"

    # android.rpy:324
    old "Emulation:"
    new "Προσομοίωση"

    # android.rpy:333
    old "Phone"
    new "Κινητό Τηλέφωνο"

    # android.rpy:337
    old "Tablet"
    new "Tablet"

    # android.rpy:341
    old "Television"
    new "Τηλεόραση"

    # android.rpy:353
    old "Build:"
    new "Χτίσε:"

    # android.rpy:361
    old "Install SDK & Create Keys"
    new "Εγκατάσταση του SDK και δημιουργία κλειδιών"

    # android.rpy:365
    old "Configure"
    new "Ρύθμιση"

    # android.rpy:369
    old "Build Package"
    new "Χτίσε το πακέτο"

    # android.rpy:373
    old "Build & Install"
    new "Χτίσε κι εγκατέστησε"

    # android.rpy:377
    old "Build, Install & Launch"
    new "Χτίσε, εγκατέστησε κι εκτέλεσε"

    # android.rpy:388
    old "Other:"
    new "Άλλο:"

    # android.rpy:396
    old "Remote ADB Connect"
    new "Απομακρυσμένη σύνδεση με το ADB"

    # android.rpy:400
    old "Remote ADB Disconnect"
    new "Απομακρυσμένη αποσύνδεση από το ADB"

    # android.rpy:404
    old "Logcat"
    new "Logcat"

    # android.rpy:437
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Προτού πακετάρετε εφαρμογές για Android, θα χρειαστείτε να κατεβάσετε το RAPT, Ren'Py Android Packaging Tool. Θέλετε να κατεβάσετε το RAPT τώρα;"

    # android.rpy:496
    old "Remote ADB Address"
    new "Διεύθυνση εξ αποστάσεως ADB."

    # android.rpy:496
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "Παρακαλώ εισάγετε τη διεύθυνση IP και τον αριθμό port που θέλετε να συνδεθείτε, υπό τη μορφή \"192.168.1.143:5555\". Συμβουλευτείτε το εγχειρίδιο χρήσης της συσκευής σας, για να κρίνετε αν υποστηρίζει απομακρυσμένο ADB κι αν ναι, τη διεύθυνση και το port που χρησιμοποιεί."

    # android.rpy:508
    old "Invalid remote ADB address"
    new "Λάθος διεύθυνση εξ αποστάσεως ADB."

    # android.rpy:508
    old "The address must contain one exactly one ':'."
    new "Η διεύθυνση πρέπει να περιέχει ακριβώς μόνο μία άνω κάτω τελεία ':'."

    # android.rpy:512
    old "The host may not contain whitespace."
    new "Ο host δε πρέπει να έχει κενά στο όνομά του."

    # android.rpy:518
    old "The port must be a number."
    new "Το port πρέπει να είναι αριθμός."

    # android.rpy:544
    old "Retrieving logcat information from device."
    new "Λαμβάνονται οι πληροφορίες του logcat για τη συσκευή."

    # choose_directory.rpy:73
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "Η Ren'Py δε μπόρεσε να τρέξει την python με το tkinter ώστε να δαλέξει το φάκελο. Παρακαλώ εγκαταστήστε το python-tk ή το πακέτο tkinter."

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "Δε μπόρεσε να αλλάξει το θέμα. Πιθανώς το αρχείο options.rpy υπέστει υπερβολικά μεγάλη τροποποίηση."

    # choose_theme.rpy:370
    old "Planetarium"
    new "Πλανητάριο"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "Επιλέξτε θέμα"

    # choose_theme.rpy:438
    old "Theme"
    new "Θέμα"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "Συνδυασμός χρωμάτων"

    # choose_theme.rpy:495
    old "Continue"
    new "Συνέχεια"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "ΠΛΗΡΟΦΟΡΙΕΣ"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    # Automatic translation.
    new "Η εντολή εκτελείται σε ένα νέο παράθυρο κονσόλας του λειτουργικού συστήματος."

    # distribute.rpy:443
    old "Scanning project files..."
    new "Γίνεται ανάγνωση των αρχείων του έργου..."

    # distribute.rpy:459
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "Το χτίσιμο της διανομής απέτυχε.\n\n Η build.directory_name μεταβλητή πρέπει να μην εμπεριέχει κενά, άνω-κάτω τελεία, ή ερωτηματικό."

    # distribute.rpy:504
    old "No packages are selected, so there's nothing to do."
    new "Δεν έχει επιλεγεί πακέτο, οπότε δεν υπάρχει κάτι να γίνει."

    # distribute.rpy:516
    old "Scanning Ren'Py files..."
    new "Σαρώνονται τα αρχεία της Ren'Py..."

    # distribute.rpy:569
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "Όλα τα πακέτα χτίσητκαν.\n\nΔεν υποστηρίζεται σε Windows το ξεπακετάρισμα κι επαναπακετάρισμα, διανομών για Linux και Macintosh, επειδή στα εν λόγω λειτουργικά συστήματα υπάρχουν πληροφορίες δικαιωμάτων χρήσης."

    # distribute.rpy:752
    old "Archiving files..."
    new "Τα αρχεία τακτοποιούνται."

    # distribute.rpy:1050
    old "Unpacking the Macintosh application for signing..."
    # Automatic translation.
    new "Αποσυσκευασία της εφαρμογής Macintosh για υπογραφή..."

    # distribute.rpy:1060
    old "Signing the Macintosh application..."
    # Automatic translation.
    new "Υπογραφή της εφαρμογής Macintosh..."

    # distribute.rpy:1082
    old "Creating the Macintosh DMG..."
    # Automatic translation.
    new "Δημιουργία του Macintosh DMG..."

    # distribute.rpy:1091
    old "Signing the Macintosh DMG..."
    # Automatic translation.
    new "Υπογραφή του DMG του Macintosh..."

    # distribute.rpy:1248
    old "Writing the [variant] [format] package."
    new "Γράφεται το [variant] [format] πακέτο."

    # distribute.rpy:1261
    old "Making the [variant] update zsync file."
    new "Κάνω το [variant] να ενημερώσει το αρχείο zsync."

    # distribute.rpy:1404
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "Επεξεργασμένα {b}[complete]{/b} από {b}[total]{/b} αρχεία."

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.name!q]"
    new "Χτίσε Διανομές: [project.current.name!q]"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "Όνομα Φακέλου:"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "Όνομα εκτελέσιμου αρχείου:"

    # distribute_gui.rpy:185
    old "Actions:"
    new "Πράξεις:"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "Επεξεργαστείτε το αρχείο options.rpy"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "Προσθήκη 'from clauses to calls', μία φορά"

    # distribute_gui.rpy:195
    old "Refresh"
    new "Ανανέωση"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    # Automatic translation.
    new "Ανέβασμα στο itch.io"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "Χτίστε τα Πακέτα:"

    # distribute_gui.rpy:234
    old "Options:"
    new "Επιλογές:"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "Χτίστε ενημερώσεις"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "Προσθήκη from clauses to calls"

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "Εξαναγκασμός επαναμεταγλώττισης:"

    # distribute_gui.rpy:246
    old "Build"
    new "Χτίσε"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "Προσθέτονται from clauses to call σε δηλώσεις οι οποίες δεν έχουν."

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "Βρέθηκαν σφάλματα κατά την εκτέλεση του έργου. Παρακαλούμε σιγουρευτείτε πως το έργο τρέχει χωρίς σφάλματα, πριν χτίσετε μια διανομή."

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "Το έργο σας δεν περιέχει πληροφορίες για το χτίσιμό του. Θέλετε να προστεθούν στο τέλος του αρχείου options.rpy;"

    # editor.rpy:150
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "{b}Συνιστάται.{/b} Ένας επεξεργαστής κειμένου σε έκδοση beta, με εύκολο περιβάλλον εργασίας και χαραχτηριστικά που σας βοηθούν, όπως π.χ. ορθογραφικό έλεγχο. Ο Editra προς το παρόν δεν υποστηρίζει IME για είσοδο κειμένου σε Κινέζικα, Ιαπωνέζικα και Κορεάτικα."

    # editor.rpy:151
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "{b}Συνιστάται.{/b} Ένας επεξεργαστής κειμένου σε έκδοση beta, με εύκολο περιβάλλον εργασίας και χαραχτηριστικά που σας βοηθούν, όπως π.χ. ορθογραφικό έλεγχο. Ο Editra προς το παρόν δεν υποστηρίζει IME για είσοδο κειμένου σε Κινέζικα, Ιαπωνέζικα και Κορεάτικα. Σε Linux ο Editra απαιτεί το wxPython."

    # editor.rpy:167
    old "This may have occured because wxPython is not installed on this system."
    new "Αυτό πιθανώς να συνέβη, διότι το wxPython δεν έχει εγκατασταθεί σε αυτό το σύστημα."

    # editor.rpy:169
    old "Up to 22 MB download required."
    new "Απαιτείται να κατέβουν έως και 22 MB."

    # editor.rpy:182
    old "A mature editor that requires Java."
    new "Ένας ώριμος επεξεργαστής κειμένου που απαιτεί Java."

    # editor.rpy:182
    old "1.8 MB download required."
    new "1.8 MB απαιτείται να κατέβει."

    # editor.rpy:182
    old "This may have occured because Java is not installed on this system."
    new "Αυτό πιθανώς να συνέβη, διότι η Java δεν έχει εγκατασταθεί σε αυτό το σύστημα."

    # editor.rpy:191
    old "Invokes the editor your operating system has associated with .rpy files."
    new "Επικαλείται τον επεξεργαστή κειμένου που στο σύστημά σας σχετίζεται με αρχεία με επέκταση .rpy"

    # editor.rpy:207
    old "Prevents Ren'Py from opening a text editor."
    new "Εμποδίζει τη Ren'Py να ανοίξει επεξεργαστή κειμένου."

    # editor.rpy:359
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "Μια προγραμματιστική εξαίρεση συνέβει κατά την εκκίνηση του επεξεργαστή κειμένου:\n[exception!q] "

    # editor.rpy:457
    old "Select Editor"
    new "Επιλέξτε επεξεργαστή κειμένου"

    # editor.rpy:472
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "Ο επεξεργαστής κειμένου είναι το πρόγραμμα που θα χρησιμοποιείτε για να τροποποιείτε τα αρχεία σεναρίων κώδικα της Ren'Py. Από εδώ μπορείτε να επιλέξετε ποιον επεξεργαστή θα χρησιμοποιεί η Ren'Py. Αν δεν είναι ήδη εγκατεστημένος, θα κατέβει και θα εγκατασταθεί αυτόματα."

    # editor.rpy:494
    old "Cancel"
    new "Ακύρωση"

    # front_page.rpy:35
    old "Open [text] directory."
    new "Άνοικε το φάκελο [text] "

    # front_page.rpy:93
    old "refresh"
    new "ανανέωση"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ Δημιουργία νέου έργου"

    # front_page.rpy:130
    old "Launch Project"
    new "Φόρτωση Έργου"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    # Automatic translation.
    new "[p.name!q] (πρότυπο)"

    # front_page.rpy:149
    old "Select project [text]."
    new "Επιλέξτε έργο [text]."

    # front_page.rpy:165
    old "Tutorial"
    new "Διδακτικό κι επεξηγηματικό παιχνίδι"

    # front_page.rpy:166
    old "The Question"
    new "Η Ερώτηση"

    # front_page.rpy:182
    old "Active Project"
    new "Ενεργό έργο"

    # front_page.rpy:190
    old "Open Directory"
    new "Άνοιγμα φακέλου"

    # front_page.rpy:195
    old "game"
    new "παιχνίδι"

    # front_page.rpy:196
    old "base"
    new "βάση"

    # front_page.rpy:197
    old "images"
    new "εικόνες"

    # front_page.rpy:198
    old "gui"
    new "gui"

    # front_page.rpy:204
    old "Edit File"
    new "Επεξεργασία αρχείου"

    # front_page.rpy:214
    old "All script files"
    new "Όλα τα αρχεία σεναρίων κώδικα"

    # front_page.rpy:223
    old "Navigate Script"
    new "Καθοδηγήστε το σενάριο κώδικα"

    # front_page.rpy:234
    old "Check Script (Lint)"
    new "Έλεγχος του σεναρίου κώδικα (Lint)"

    # front_page.rpy:237
    old "Change/Update GUI"
    # Automatic translation.
    new "Αλλαγή/ενημέρωση GUI"

    # front_page.rpy:239
    old "Change Theme"
    new "Αλλαγή θέματος"

    # front_page.rpy:242
    old "Delete Persistent"
    new "Διαγραφή επιμένων δεδομένων"

    # front_page.rpy:251
    old "Build Distributions"
    new "Χτίστε Διανομές"

    # front_page.rpy:253
    old "Android"
    new "Android"

    # front_page.rpy:254
    old "iOS"
    new "iOs"

    # front_page.rpy:255
    old "Generate Translations"
    new "Δηιμιουργία Μεταγλωττίσεων"

    # front_page.rpy:256
    old "Extract Dialogue"
    new "Εξάγετε διάλογο"

    # front_page.rpy:272
    old "Checking script for potential problems..."
    new "Έλεγχος σεναρίου κώδικα για πιθανά προβλήματα..."

    # front_page.rpy:287
    old "Deleting persistent data..."
    new "Διαγράφονται τα επιμένοντα δεδομένα..."

    # front_page.rpy:295
    old "Recompiling all rpy files into rpyc files..."
    new "Ξαναγίνεται μεταγλώττιση όλων των αρχείων rpy σε αρχεία rpc..."

    # gui7.rpy:236
    old "Select Accent and Background Colors"
    # Automatic translation.
    new "Επιλογή χρωμάτων έμφασης και φόντου"

    # gui7.rpy:250
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    # Automatic translation.
    new "Κάντε κλικ στο συνδυασμό χρωμάτων που επιθυμείτε να χρησιμοποιήσετε και, στη συνέχεια, κάντε κλικ στο κουμπί Συνέχεια. Αυτά τα χρώματα μπορούν να αλλάξουν και να προσαρμοστούν αργότερα."

    # gui7.rpy:294
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    # Automatic translation.
    new "{b}Προειδοποίηση{/b}\nΗ συνέχιση θα αντικαταστήσει τις προσαρμοσμένες εικόνες της γραμμής, του κουμπιού, της υποδοχής αποθήκευσης, της γραμμής κύλισης και του ρυθμιστικού.\n\nΤι θα θέλατε να κάνετε;"

    # gui7.rpy:294
    old "Choose new colors, then regenerate image files."
    # Automatic translation.
    new "Επιλέξτε νέα χρώματα και, στη συνέχεια, αναδημιουργήστε αρχεία εικόνας."

    # gui7.rpy:294
    old "Regenerate the image files using the colors in gui.rpy."
    # Automatic translation.
    new "Αναδημιουργήστε τα αρχεία εικόνας χρησιμοποιώντας τα χρώματα στο gui.rpy."

    # gui7.rpy:314
    old "PROJECT NAME"
    new "ΟΝΟΜΑ ΕΡΓΟΥ"

    # gui7.rpy:314
    old "Please enter the name of your project:"
    new "Παρακαλώ εισάγετε το όνομα του έργου σας:"

    # gui7.rpy:322
    old "The project name may not be empty."
    new "Το όνομα του έργου δε πρέπει να είναι κενό."

    # gui7.rpy:327
    old "[project_name!q] already exists. Please choose a different project name."
    new "Το έργο [project_name!q] υπάρχει ήδη. Παρακαλούμε επιλέξτε άλλο όνομα για το έργο σας."

    # gui7.rpy:330
    old "[project_dir!q] already exists. Please choose a different project name."
    new "Ο φάκελος [project_name!q] υπάρχει ήδη. Παρακαλούμε επιλέξτε άλλο όνομα για το έργο σας."

    # gui7.rpy:341
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    # Automatic translation.
    new "Ποια ανάλυση θα πρέπει να χρησιμοποιεί το έργο; Παρόλο που το Ren'Py μπορεί να κλιμακώσει το παράθυρο προς τα πάνω και προς τα κάτω, αυτό είναι το αρχικό μέγεθος του παραθύρου, το μέγεθος στο οποίο θα πρέπει να σχεδιαστούν τα στοιχεία και το μέγεθος στο οποίο τα στοιχεία θα είναι πιο ευκρινή.\n\nΗ προεπιλογή [default_size[0]]x[default_size[1]] είναι ένας λογικός συμβιβασμός."

    # gui7.rpy:389
    old "Creating the new project..."
    # Automatic translation.
    new "Δημιουργία του νέου έργου..."

    # gui7.rpy:391
    old "Updating the project..."
    # Automatic translation.
    new "Ενημέρωση του έργου..."

    # interface.rpy:107
    old "Documentation"
    new "Τεκμηρίωση"

    # interface.rpy:108
    old "Ren'Py Website"
    new "Ο ιστότοπος της Ren'Py"

    # interface.rpy:109
    old "Ren'Py Games List"
    new "Λίστα παιχνιδιών Ren'Py"

    # interface.rpy:117
    old "update"
    new "ενημέρωση"

    # interface.rpy:119
    old "preferences"
    new "επιλογές"

    # interface.rpy:120
    old "quit"
    new "έξοδος"

    # interface.rpy:232
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "Λόγω περιορισμών στη μορφή πακεταρίσματος, δεν επιτρέπεται να δώσετε χαρακτήρες που να μην ανήκουν στον ASCII σε ονομασίες αρχείων ή φακέλων."

    # interface.rpy:327
    old "ERROR"
    new "ΣΦΑΛΜΑ"

    # interface.rpy:356
    old "While [what!qt], an error occured:"
    new "Ενόσω [what!qt], συνέβη ένα σφάλμα:"

    # interface.rpy:356
    old "[exception!q]"
    new "[exception!q]"

    # interface.rpy:375
    old "Text input may not contain the {{ or [[ characters."
    new "Το κείμενο που εισάγετε δε πρέπει να εμπεριέχει τους χαρακτήρες {{ ή [[ "

    # interface.rpy:380
    old "File and directory names may not contain / or \\."
    new "Ονόματα αρχείων και φακέλων δε πρέπει να περιέχουν τους χαρακτήρες / ή \\"

    # interface.rpy:386
    old "File and directory names must consist of ASCII characters."
    new "Όνόματα αρχείων και φακέλων πρέπει να αποτελούνται μόνο από χαρακτήρες ASCII."

    # interface.rpy:454
    old "PROCESSING"
    new "ΓΙΝΕΤΑΙ ΕΠΕΞΕΡΓΑΣΙΑ"

    # interface.rpy:471
    old "QUESTION"
    new "ΕΡΩΤΗΣΗ"

    # interface.rpy:484
    old "CHOICE"
    new "ΕΠΙΛΟΓΗ"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Για να χτίσετε πακέτα iOS, παρακαλώ κατεβάστε το renios, αποσυμπιέστε το και τοποθετήστε το στο φάκελο της Ren'Py. Κατόπιν επανεκκινήστε τον εκκινητή."

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "Ο φάκελος στον οποίο θα τοποθετηθούν τα τα Xcode έργα, δεν έχει επιλεχτεί ακόμα. Ζρησιμοποιήστε το 'Επιλογή φακέλου' για να το επιλέξετε. "

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "Δεν υπάρχει έργο Xcode που να ανταποκρίνεται στο συγκεκριμένο έργο Ren'Py. Επιλέξτε 'Δημιουργήστε έργο Xcode' για να δημιουργήσετε ένα. "

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "Ένα αντίστοιχο έγο Xcode υπάρχει. Επιλέξτε 'Ενημέρωση του έργου Xcode' για να το ενημερώσετε με τα μεγαλύτερα αρχεία παιχνιδιού ή χρησιμοποιήστε το Xcode για να το χτίσετε κι εγκαταστήσετε."

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Απόπειρα εξομοίωσης ενός iPhone.\n\nΗ είσοδος δεδομένων αφής προσομοιώνεται με το ποντίκη, αλλά μόνο όταν κρατείται πατημένο το αριστερό κουμπί."

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Απόπειρα εξομοίωσης ενός iPad.\n\nΗ είσοδος δεδομένων αφής προσομοιώνεται με το ποντίκη, αλλά μόνο όταν κρατείται πατημένο το αριστερό κουμπί."

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Επιλέγει το φάκελο που θα τοποθετηθούν τα έργα Xcode."

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "Δημιουργεί ένα Xcode έργο που ανταποκρίνεται στο τρέχον έργο της Ren'Py."

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "Ενημερώνει το έργο Xcode με τα νεώτερα αρχεία του παιχνιδιού. Αυτό πρέπει να γίνεται κάθε φορά που ένα έργο Ren'Py αλλάζει."

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Ανοίγει ένα έργο Xcode στο Xcode."

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "Ανοίγει το φάκελο που περιέχει τα έργα Xcode."

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "To έργο Xcode υπάρχει ήδη. Θέλετε να μετονομάσουμε το παλιό έργο και να το αντικαταστήσουμε με ένα νέο;"

    # ios.rpy:211
    old "iOS: [project.current.name!q]"
    new "iOS: [project.current.name!q]"

    # ios.rpy:240
    old "iPhone"
    new "iPhone"

    # ios.rpy:244
    old "iPad"
    new "iPad"

    # ios.rpy:264
    old "Select Xcode Projects Directory"
    new "Επιλέξτε τον φάκελο που περιέχει τα έργα Xcode"

    # ios.rpy:268
    old "Create Xcode Project"
    new "Δημιουργήστε έργο Xcode"

    # ios.rpy:272
    old "Update Xcode Project"
    new "Ενημέρωση του έργου Xcode"

    # ios.rpy:277
    old "Launch Xcode"
    new "Εκτέλεση του Xcode"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "Άνοιξε το φάκελο που περιέχει τα Xcode έργα"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "Πριν πακετάρετε iOS εφαρμογές, θα πρέπει να κατεβάσετε το renios, ακρωνύμιο Ren'Py's iΟs Support. Θέλετε να κατεβάσετε το renios τώρα;"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "ΦΑΚΕΛΟΣ ΕΡΓΩΝ XCODE"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Παρακαλώ επιλέξτε το φάκελο που θα περιέχει τα έργα Xcode, χρησιμοποιώντας τον επιλογέα φακέλου.\n{b}Ο επιλογέας ίσως είναι ήδη ανοικτός πίσω απ' αυτό το παράθυρο.{/b} "

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Η Ren'Py έθεσε ως φάκελο έργων Xcode τον:"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    # Automatic translation.
    new "Οι ενσωματωμένες διανομές δεν βρέθηκαν. Παρακαλούμε επιλέξτε 'Build' και προσπαθήστε ξανά."

    # itch.rpy:91
    old "No uploadable files were found. Please choose 'Build' and try again."
    # Automatic translation.
    new "Δεν βρέθηκαν αρχεία που μπορούν να μεταφορτωθούν. Παρακαλούμε επιλέξτε 'Build' και δοκιμάστε ξανά."

    # itch.rpy:99
    old "The butler program was not found."
    # Automatic translation.
    new "Το πρόγραμμα Butler δεν βρέθηκε."

    # itch.rpy:99
    old "Please install the itch.io app, which includes butler, and try again."
    # Automatic translation.
    new "Εγκαταστήστε την εφαρμογή itch.io, η οποία περιλαμβάνει τον Butler, και δοκιμάστε ξανά."

    # itch.rpy:108
    old "The name of the itch project has not been set."
    # Automatic translation.
    new "Το όνομα του έργου itch δεν έχει οριστεί."

    # itch.rpy:108
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    # Automatic translation.
    new "Παρακαλούμε {a=https://itch.io/game/new}δημιουργήστε το έργο σας{/a}, στη συνέχεια προσθέστε μια γραμμή όπως \n{vspace=5}define build.itch_project = \"όνομα χρήστη/όνομα παιχνιδιού\"\n{vspace=5} στο options.rpy."

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.name]"
    new "Περιήγηση: [project.current.name]"

    # navigation.rpy:177
    old "Order: "
    new "Σειρά: "

    # navigation.rpy:178
    old "alphabetical"
    new "αλφαβητική"

    # navigation.rpy:180
    old "by-file"
    new "βάσει-αρχείου"

    # navigation.rpy:182
    old "natural"
    new "φυσιολογική"

    # navigation.rpy:194
    old "Category:"
    new "Κατηγορία:"

    # navigation.rpy:196
    old "files"
    new "αρχεία"

    # navigation.rpy:197
    old "labels"
    new "ετικέτες "

    # navigation.rpy:198
    old "defines"
    new "ορισμοί"

    # navigation.rpy:199
    old "transforms"
    new "μετασχηματισμοί"

    # navigation.rpy:200
    old "screens"
    new "οθόνες"

    # navigation.rpy:201
    old "callables"
    new "καλούμενα"

    # navigation.rpy:202
    old "TODOs"
    new "TODOs"

    # navigation.rpy:241
    old "+ Add script file"
    new "+ Προσθήκη αρχείου σεναρίου κώδικα"

    # navigation.rpy:249
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "Δε βρέθηκε σχόλιο TODO.\n\nΓια να δημιουργήσετε ένα προσθέστε \"# TODO\" στον κώδικά σας."

    # navigation.rpy:256
    old "The list of names is empty."
    new "Η λίστα ονομάτων είναι άδεια."

    # new_project.rpy:38
    old "New GUI Interface"
    # Automatic translation.
    new "Νέα διεπαφή GUI"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    # Automatic translation.
    new "Και οι δύο διεπαφές έχουν μεταφραστεί στη γλώσσα σας."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    # Automatic translation.
    new "Μόνο το νέο GUI έχει μεταφραστεί στη γλώσσα σας."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    # Automatic translation.
    new "Μόνο η διεπαφή του παλαιού θέματος έχει μεταφραστεί στη γλώσσα σας."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    # Automatic translation.
    new "Καμία από τις δύο διεπαφές δεν έχει μεταφραστεί στη γλώσσα σας."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "Ήταν αδύνατον να οριστεί ο φάκελος του έργου. Ματαιώνεται η πράξη."

    # new_project.rpy:69
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    # Automatic translation.
    new "Ποια διεπαφή θα θέλατε να χρησιμοποιήσετε; Το νέο γραφικό περιβάλλον χρήστη έχει μοντέρνα εμφάνιση, υποστηρίζει ευρείες οθόνες και κινητές συσκευές και είναι ευκολότερο στην προσαρμογή. Τα παλαιότερα θέματα ενδέχεται να είναι απαραίτητα για να εργαστείτε με παλαιότερο κώδικα παραδείγματος.\n\n[language_support!t]\n\nΑν έχετε αμφιβολίες, επιλέξτε το νέο γραφικό περιβάλλον και, στη συνέχεια, κάντε κλικ στο κουμπί Συνέχεια κάτω δεξιά."

    # new_project.rpy:69
    old "Legacy Theme Interface"
    # Automatic translation.
    new "Διασύνδεση Legacy Theme"

    # new_project.rpy:90
    old "Choose Project Template"
    new "Επιλέξτε Μορτίβο Έργου"

    # new_project.rpy:108
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "Παρακαλώ επιλέξτε ένα μοτίβο, για να το εφαρμόσετε στο έργο σας. Το μοτίβο θέτει βασική γραμματοσειρά και τη γλώσσα του περιβάλλοντος χρήστη. Αν δεν υποστηρίζεται η γλώσσα σας, επιλέξτε 'english'."

    # preferences.rpy:64
    old "Launcher Preferences"
    new "Επιλογές Εκκινητή"

    # preferences.rpy:85
    old "Projects Directory:"
    new "Φάκελος έργων:"

    # preferences.rpy:92
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:94
    old "Projects directory: [text]"
    new "Φάκελος έργων: [text]"

    # preferences.rpy:96
    old "Not Set"
    new "Δεν έχει ορισθέι"

    # preferences.rpy:111
    old "Text Editor:"
    new "Επεξεργαστής κειμένου:"

    # preferences.rpy:117
    old "Text editor: [text]"
    new "Επεξεργαστής κειμένου: [text]"

    # preferences.rpy:133
    old "Update Channel:"
    new "Ενημέρωση καναλιού:"

    # preferences.rpy:153
    old "Navigation Options:"
    new "Επιλογές πλοήγησης:"

    # preferences.rpy:157
    old "Include private names"
    new "Συμπερίληψη ιδιωτικών ονομάτων"

    # preferences.rpy:158
    old "Include library names"
    new "Συμπερίληψη ονομάτων βιβλιοθηκών"

    # preferences.rpy:168
    old "Launcher Options:"
    new "Επιλογές Εκκινητή:"

    # preferences.rpy:172
    old "Hardware rendering"
    new "Κατασκευή γραφικών από το hardware."

    # preferences.rpy:173
    old "Show templates"
    new "Εμφάνιση μοτίβων"

    # preferences.rpy:174
    old "Show edit file section"
    new "Εμφάνιση μέρους επεξεργασίας αρχείου"

    # preferences.rpy:175
    old "Large fonts"
    new "Μεγάλο μέγεθος γραμματοσειράς"

    # preferences.rpy:178
    old "Console output"
    new "Έξοδος κονσόλας"

    # preferences.rpy:199
    old "Open launcher project"
    new "Άνοιξε το έργο Εκκινητής"

    # preferences.rpy:213
    old "Language:"
    new "Γλώσσα:"

    # project.rpy:47
    old "After making changes to the script, press shift+R to reload your game."
    new "Μετά τις αλλαγές στον κώδικα του σεναρίου, πατήστε shift+R για να φορτώσετε εκ νέου το παιχνίδι."

    # project.rpy:47
    old "Press shift+O (the letter) to access the console."
    new "Πατήστε shift+O (το γράμμα) για να ανοίξετε την κονσόλα."

    # project.rpy:47
    old "Press shift+D to access the developer menu."
    new "Πατήστε shift+D για να ανοίξετε το Μενού Δημιουργού."

    # project.rpy:47
    old "Have you backed up your projects recently?"
    new "Κάνατε αντίγραφο ασφαλείας των έργων σας πρόσφατα;"

    # project.rpy:229
    old "Launching the project failed."
    new "Αποτυχία εκκίνησης του έργου."

    # project.rpy:229
    old "Please ensure that your project launches normally before running this command."
    new "Παρακαλούμε σιγουρευτείτε πως το έργο εκκινείται φυσιολογικά, προτού εκτελέσετε αυτή την εντολή."

    # project.rpy:242
    old "Ren'Py is scanning the project..."
    new "Η Ren'Py αναζητάει έργα..."

    # project.rpy:568
    old "Launching"
    new "Εκκίνηση"

    # project.rpy:597
    old "PROJECTS DIRECTORY"
    new "ΦΑΚΕΛΟΣ ΕΡΓΩΝ"

    # project.rpy:597
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Παρακαλώ επιλέξτε το φάκελο έργων, χρησιμοποιώντας τον επιλογέα φακέλου.\n{b}Ο επιλογέας φακέλου ίσως έχει ανοίξει πίσω από αυτό το παράθυρο.{/b}"

    # project.rpy:597
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "Αυτός ο εκκινητής θα ψάξει για έργα σε αυτό το φάκελο, θα δημιουργεί νέα έργα σε αυτό τον φάκελο και θα τοποθετεί χτισμένα έργα σε αυτό το φάκελο."

    # project.rpy:602
    old "Ren'Py has set the projects directory to:"
    new "Η Ren'Py όρισε τον φάκελο έργων το φάκελο:"

    # translations.rpy:63
    old "Translations: [project.current.name!q]"
    # Automatic translation.
    new "Μεταφράσεις: [project.current.name!q]"

    # translations.rpy:104
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    # Automatic translation.
    new "Η γλώσσα με την οποία θα εργαστείτε. Θα πρέπει να περιέχει μόνο πεζούς χαρακτήρες ASCII και υπογράμμιση."

    # translations.rpy:130
    old "Generate empty strings for translations"
    new "Δημιουργία κενής συμβολοσειράς για μεταφράσεις"

    # translations.rpy:148
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    # Automatic translation.
    new "Δημιουργεί ή ενημερώνει αρχεία μετάφρασης. Τα αρχεία τοποθετούνται στο game/tl/[persistent.translate_language!q]."

    # translations.rpy:168
    old "Extract String Translations"
    # Automatic translation.
    new "Απόσπασμα μεταφράσεων συμβολοσειράς"

    # translations.rpy:170
    old "Merge String Translations"
    # Automatic translation.
    new "Συγχώνευση μεταφράσεων συμβολοσειρών"

    # translations.rpy:175
    old "Replace existing translations"
    # Automatic translation.
    new "Αντικατάσταση υφιστάμενων μεταφράσεων"

    # translations.rpy:176
    old "Reverse languages"
    # Automatic translation.
    new "Αντίστροφες γλώσσες"

    # translations.rpy:180
    old "Update Default Interface Translations"
    # Automatic translation.
    new "Ενημέρωση προεπιλεγμένων μεταφράσεων διασύνδεσης"

    # translations.rpy:200
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    # Automatic translation.
    new "Η εντολή extract σας επιτρέπει να εξαγάγετε μεταφράσεις συμβολοσειρών από ένα υπάρχον έργο σε ένα προσωρινό αρχείο.\n\nΗ εντολή merge συγχωνεύει τις μεταφράσεις που έχουν εξαχθεί σε ένα άλλο έργο."

    # translations.rpy:224
    old "Ren'Py is generating translations...."
    new "Η Ren'Py δημιουργεί αρχεία μεταγλωττίσεων..."

    # translations.rpy:235
    old "Ren'Py has finished generating [language] translations."
    new "Η Ren'Py ολοκλήρωσε τη δημιουργία αρχείων μεταγλώττισης για τη γλώσσα [language]."

    # translations.rpy:248
    old "Ren'Py is extracting string translations..."
    # Automatic translation.
    new "Η Ren'Py εξάγει μεταφράσεις συμβολοσειρών..."

    # translations.rpy:251
    old "Ren'Py has finished extracting [language] string translations."
    # Automatic translation.
    new "Η Ren'Py ολοκλήρωσε την εξαγωγή των μεταφράσεων των συμβολοσειρών [language]."

    # translations.rpy:271
    old "Ren'Py is merging string translations..."
    # Automatic translation.
    new "Το Ren'Py συγχωνεύει μεταφράσεις συμβολοσειρών..."

    # translations.rpy:274
    old "Ren'Py has finished merging [language] string translations."
    # Automatic translation.
    new "Ο Ren'Py ολοκλήρωσε τη συγχώνευση των μεταφράσεων του [language]."

    # translations.rpy:282
    old "Updating default interface translations..."
    # Automatic translation.
    new "Ενημέρωση προεπιλεγμένων μεταφράσεων διεπαφής..."

    # translations.rpy:306
    old "Extract Dialogue: [project.current.name!q]"
    new "Εξαγωγή διαλόγου: [project.current.name!q]"

    # translations.rpy:322
    old "Format:"
    new "Μορφή:"

    # translations.rpy:330
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Χωρισμένο με Tab φύλλο εργασίας (dialogue.tab)"

    # translations.rpy:331
    old "Dialogue Text Only (dialogue.txt)"
    new "Διάλογος σε απλή μορφή κειμένου (dialogue.txt)"

    # translations.rpy:344
    old "Strip text tags from the dialogue."
    new "Αφαίρεση tags από το κείμενο διαλόγου."

    # translations.rpy:345
    old "Escape quotes and other special characters."
    new "Ειδικοί χαρακτήρες."

    # translations.rpy:346
    old "Extract all translatable strings, not just dialogue."
    new "Εξαγωγή όλων των μεταφράσιμων συμβολοσειρών, όχι μόνο το διάλογο."

    # translations.rpy:374
    old "Ren'Py is extracting dialogue...."
    new "Η Ren'Py εξάγει το διάλογο...."

    # translations.rpy:378
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Η Ren'Py ολοκλήρωσε την εξαγωγή του διλόγου. Ο διάλογος μπορεί να βρεθεί στο: dialogue.[persistent.dialogue_format] εντός του κεντρικού φακέλου του παιχνιδιού."

    # updater.rpy:75
    old "Select Update Channel"
    new "Επιλέξτε κανάλι ενημέρωσης:"

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "Το κανάλι ενημέρωσης ελέγχει την έκδοση της Ren'Py που ο ενημερωτής θα κατεβάσει. Παρακαλώ επιλέξτε ένα κανάλι ενημέρωσης:"

    # updater.rpy:91
    old "Release"
    new "Κύρια Έκδοση"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}Αυτή που συνιστάται.{/b} Η έκδοση της Ren'Py που θα έπρεπε να χρησιμοποιούν όλα τα νέα παιχνίδια που δημιουργούνται."

    # updater.rpy:102
    old "Prerelease"
    new "Ακυκλοφόρητη"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Μια εικόνα της επόμενης έκδοσης της Ren'Py η οποία μπορεί να χρησιμοποιηθεί για ελέγχους και για το πλεονέκτημα χρήσης των νέων λειτουργιών. Δε συνιστάται για τελικές εκδόσεις παιχνιδιών."

    # updater.rpy:114
    old "Experimental"
    new "Πειραματική"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Η Πειραματική έκδοση της Ren'Py. Μην επιλέξετε το κανάλι αυτό, εκτός κι αν κάποιος εκ των δημιουργών της σας το ζητήσει."

    # updater.rpy:126
    old "Nightly"
    new "Καθεβραδυνή"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Η απόλυτη νεώτερη έκδοση της Ren'Py. Μπορεί να έχει τα πιο νέα χαρακτηριστικά, αλλά να μη μπορέι καν να φορτώσει."

    # updater.rpy:152
    old "An error has occured:"
    new "Ένα σφάλμα συνέβη:"

    # updater.rpy:154
    old "Checking for updates."
    new "Έλεγχος για διαθέσιμες ενημερώσεις"

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "Η Ren'Py είναι ενημερωμένη."

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new " Η έκδοση [u.version] είναι διαθέσιμη. Θέλετε να την εγκαταστήσετε;"

    # updater.rpy:160
    old "Preparing to download the update."
    new "Ετοιμάζεται το κατέβασμα της ενημέρωσης."

    # updater.rpy:162
    old "Downloading the update."
    new "Η ενημέρωση κατεβαίνει."

    # updater.rpy:164
    old "Unpacking the update."
    new "Ξεπακετάρεται η ενημέρωση."

    # updater.rpy:166
    old "Finishing up."
    new "Ολοκληρώνεται η ενημέρωση."

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "Η ενημέρωση εγκαταστήθηκε επιτυχώς. Η Ren'Py θα επανεκκινηθεί."

    # updater.rpy:170
    old "The update has been installed."
    new "Η ενημέρωση εγκαταστήθηκε."

    # updater.rpy:172
    old "The update was cancelled."
    new "Η ενημέρωση ματαιώθηκε."

    # updater.rpy:189
    old "Ren'Py Update"
    new "Ενημέρωση Ren'Py"

    # updater.rpy:195
    old "Proceed"
    new "Συνέχισε"

translate greek strings:

    # game/add_file.rpy:37
    old "The file name may not be empty."
    # Automatic translation.
    new "Το όνομα του αρχείου δεν πρέπει να είναι κενό."

    # game/android.rpy:37
    old "A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher."
    # Automatic translation.
    new "Για τη δημιουργία πακέτων Android στα Windows απαιτείται ένα 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit. Το JDK είναι διαφορετικό από το JRE, οπότε είναι πιθανό να έχετε Java χωρίς να έχετε το JDK.\n\nΠαρακαλούμε {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}κατεβάστε και εγκαταστήστε το JDK{/a}, στη συνέχεια επανεκκινήστε τον εκτοξευτή Ren'Py."

    # game/android.rpy:39
    old "RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory."
    # Automatic translation.
    new "Το RAPT έχει εγκατασταθεί, αλλά δεν έχει ρυθμιστεί ένα κλειδί. Παρακαλούμε δημιουργήστε νέα κλειδιά ή αντιγράψτε τα αρχεία android.keystore και bundle.keystore στον βασικό κατάλογο."

    # game/android.rpy:41
    old "Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores)."
    # Automatic translation.
    new "Παρακαλούμε επιλέξτε αν θέλετε ένα Play Bundle (για το Google Play) ή ένα Universal APK (για Sideloading και άλλα καταστήματα εφαρμογών)."

    # game/android.rpy:46
    old "Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    # Automatic translation.
    new "Προσπαθεί να μιμηθεί μια τηλεοπτική κονσόλα Android.\n\nΗ είσοδος του ελεγκτή αντιστοιχίζεται στα πλήκτρα βέλους, το Enter αντιστοιχίζεται στο κουμπί επιλογής, το Escape αντιστοιχίζεται στο κουμπί μενού και το PageUp αντιστοιχίζεται στο κουμπί επιστροφής."

    # game/android.rpy:48
    old "Downloads and installs the Android SDK and supporting packages."
    # Automatic translation.
    new "Λήψη και εγκατάσταση του Android SDK και των υποστηρικτικών πακέτων."

    # game/android.rpy:49
    old "Generates the keys required to sign the package."
    # Automatic translation.
    new "Δημιουργεί τα κλειδιά που απαιτούνται για την υπογραφή του πακέτου."

    # game/android.rpy:56
    old "Lists the connected devices."
    # Automatic translation.
    new "Εμφανίζει τις συνδεδεμένες συσκευές."

    # game/android.rpy:57
    old "Pairs with a device over Wi-Fi, on Android 11+."
    # Automatic translation.
    new "Συνδυάζεται με μια συσκευή μέσω Wi-Fi, σε Android 11+."

    # game/android.rpy:58
    old "Connects to a device over Wi-Fi, on Android 11+."
    # Automatic translation.
    new "Συνδέεται σε μια συσκευή μέσω Wi-Fi, σε Android 11+."

    # game/android.rpy:59
    old "Disconnects a device connected over Wi-Fi."
    # Automatic translation.
    new "Αποσυνδέει μια συσκευή που είναι συνδεδεμένη μέσω Wi-Fi."

    # game/android.rpy:61
    old "Removes Android temporary files."
    # Automatic translation.
    new "Αφαιρεί τα προσωρινά αρχεία του Android."

    # game/android.rpy:63
    old "Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data."
    # Automatic translation.
    new "Κατασκευάζει ένα πακέτο εφαρμογών Android (ABB), το οποίο προορίζεται να μεταφορτωθεί στο Google Play. Αυτό μπορεί να περιλαμβάνει έως και 2 GB δεδομένων."

    # game/android.rpy:64
    old "Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data."
    # Automatic translation.
    new "Κατασκευάζει ένα πακέτο APK γενικής χρήσης, που προορίζεται για παράλληλη φόρτωση και για καταστήματα εκτός του Google Play. Αυτό μπορεί να περιλαμβάνει έως και 2 GB δεδομένων."

    # game/android.rpy:327
    old "Android: [project.current.display_name!q]"
    new "Android: [project.current.display_name!q]"

    # game/android.rpy:383
    old "Install SDK"
    # Automatic translation.
    new "Εγκαταστήστε το SDK"

    # game/android.rpy:387
    old "Generate Keys"
    # Automatic translation.
    new "Δημιουργία κλειδιών"

    # game/android.rpy:397
    old "Play Bundle"
    new "Play Bundle"

    # game/android.rpy:402
    old "Universal APK"
    new "Universal APK"

    # game/android.rpy:452
    old "List Devices"
    # Automatic translation.
    new "Λίστα συσκευών"

    # game/android.rpy:456
    old "Wi-Fi Debugging Pair"
    # Automatic translation.
    new "Ζεύγος αποσφαλμάτωσης Wi-Fi"

    # game/android.rpy:460
    old "Wi-Fi Debugging Connect"
    # Automatic translation.
    new "Αποσφαλμάτωση Wi-Fi Connect"

    # game/android.rpy:464
    old "Wi-Fi Debugging Disconnect"
    # Automatic translation.
    new "Αποσύνδεση εντοπισμού σφαλμάτων Wi-Fi"

    # game/android.rpy:468
    old "Clean"
    # Automatic translation.
    new "Καθαρό"

    # game/android.rpy:573
    old "Wi-Fi Pairing Code"
    # Automatic translation.
    new "Κωδικός σύζευξης Wi-Fi"

    # game/android.rpy:573
    old "If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."
    # Automatic translation.
    new "Εάν υποστηρίζεται, μπορείτε να το βρείτε στις επιλογές \"Επιλογές προγραμματιστή\", \"Ασύρματη αποσφαλμάτωση\", \"Ζεύξη συσκευής με κωδικό ζεύξης\"."

    # game/android.rpy:580
    old "Pairing Host & Port"
    # Automatic translation.
    new "Σύζευξη κεντρικού υπολογιστή & θύρας"

    # game/android.rpy:596
    old "IP Address & Port"
    # Automatic translation.
    new "Διεύθυνση IP & θύρα"

    # game/android.rpy:596
    old "If supported, this can be found in 'Developer options', 'Wireless debugging'."
    # Automatic translation.
    new "Εάν υποστηρίζεται, μπορείτε να το βρείτε στις επιλογές \"Επιλογές προγραμματιστή\", \"Ασύρματη αποσφαλμάτωση\"."

    # game/android.rpy:612
    old "This can be found in 'List Devices'."
    # Automatic translation.
    new "Αυτό μπορείτε να το βρείτε στην ενότητα 'Λίστα συσκευών'."

    # game/android.rpy:632
    old "Cleaning up Android project."
    # Automatic translation.
    new "Καθαρισμός του έργου Android."

    # game/androidstrings.rpy:7
    old "{} is not a directory."
    # Automatic translation.
    new "{} δεν είναι κατάλογος."

    # game/androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    # Automatic translation.
    new "{} δεν περιέχει παιχνίδι Ren'Py."

    # game/androidstrings.rpy:10
    old "Run configure before attempting to build the app."
    # Automatic translation.
    new "Εκτελέστε το configure πριν προσπαθήσετε να δημιουργήσετε την εφαρμογή."

    # game/androidstrings.rpy:11
    old "Updating project."
    # Automatic translation.
    new "Ενημέρωση έργου."

    # game/androidstrings.rpy:12
    old "Creating assets directory."
    # Automatic translation.
    new "Δημιουργία καταλόγου περιουσιακών στοιχείων."

    # game/androidstrings.rpy:13
    old "Packaging internal data."
    # Automatic translation.
    new "Συσκευασία εσωτερικών δεδομένων."

    # game/androidstrings.rpy:14
    old "I'm using Gradle to build the package."
    # Automatic translation.
    new "Χρησιμοποιώ το Gradle για την κατασκευή του πακέτου."

    # game/androidstrings.rpy:15
    old "The build seems to have failed."
    # Automatic translation.
    new "Η κατασκευή φαίνεται να έχει αποτύχει."

    # game/androidstrings.rpy:16
    old "I'm installing the bundle."
    # Automatic translation.
    new "Εγκαθιστώ το πακέτο."

    # game/androidstrings.rpy:17
    old "Installing the bundle appears to have failed."
    # Automatic translation.
    new "Η εγκατάσταση του πακέτου φαίνεται να απέτυχε."

    # game/androidstrings.rpy:18
    old "Launching app."
    # Automatic translation.
    new "Εκκίνηση της εφαρμογής."

    # game/androidstrings.rpy:19
    old "Launching the app appears to have failed."
    # Automatic translation.
    new "Η εκκίνηση της εφαρμογής φαίνεται να έχει αποτύχει."

    # game/androidstrings.rpy:20
    old "The build seems to have succeeded."
    # Automatic translation.
    new "Η κατασκευή φαίνεται να έχει πετύχει."

    # game/androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    # Automatic translation.
    new "Ποιο είναι το πλήρες όνομα της αίτησής σας; Αυτό το όνομα θα εμφανίζεται στη λίστα των εγκατεστημένων εφαρμογών."

    # game/androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    # Automatic translation.
    new "Ποιο είναι το σύντομο όνομα της εφαρμογής σας; Αυτό το όνομα θα χρησιμοποιείται στον εκκινητή και για συντομεύσεις εφαρμογών."

    # game/androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    # Automatic translation.
    new "Ποιο είναι το όνομα του πακέτου;\n\nΣυνήθως έχει τη μορφή com.domain.program ή com.domain.email.program. Μπορεί να περιέχει μόνο γράμματα ASCII και τελείες. Πρέπει να περιέχει τουλάχιστον μία τελεία."

    # game/androidstrings.rpy:24
    old "The package name may not be empty."
    # Automatic translation.
    new "Το όνομα του πακέτου δεν πρέπει να είναι κενό."

    # game/androidstrings.rpy:25
    old "The package name may not contain spaces."
    # Automatic translation.
    new "Το όνομα του πακέτου δεν πρέπει να περιέχει κενά."

    # game/androidstrings.rpy:26
    old "The package name must contain at least one dot."
    # Automatic translation.
    new "Το όνομα του πακέτου πρέπει να περιέχει τουλάχιστον μία τελεία."

    # game/androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    # Automatic translation.
    new "Το όνομα του πακέτου δεν μπορεί να περιέχει δύο τελείες στη σειρά ή να αρχίζει ή να τελειώνει με τελεία."

    # game/androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    # Automatic translation.
    new "Κάθε μέρος του ονόματος του πακέτου πρέπει να αρχίζει με ένα γράμμα και να περιέχει μόνο γράμματα, αριθμούς και υπογράμμιση."

    # game/androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    # Automatic translation.
    new "{} είναι μια λέξη-κλειδί της Java και δεν μπορεί να χρησιμοποιηθεί ως μέρος ενός ονόματος πακέτου."

    # game/androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    # Automatic translation.
    new "Ποια είναι η έκδοση της εφαρμογής;\n\nΑυτή θα πρέπει να είναι η αναγνώσιμη από τον άνθρωπο εκδοχή που θα παρουσιάζατε σε ένα άτομο. Πρέπει να περιέχει μόνο αριθμούς και τελείες."

    # game/androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    # Automatic translation.
    new "Ο αριθμός έκδοσης πρέπει να περιέχει μόνο αριθμούς και τελείες."

    # game/androidstrings.rpy:32
    old "How much RAM (in GB) do you want to allocate to Gradle?\nThis must be a positive integer number."
    # Automatic translation.
    new "Πόση μνήμη RAM (σε GB) θέλετε να διαθέσετε στο Gradle;\nΠρέπει να είναι θετικός ακέραιος αριθμός."

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers and be positive."
    # Automatic translation.
    new "Το μέγεθος RAM πρέπει να περιέχει μόνο αριθμούς και να είναι θετικό."

    # game/androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    # Automatic translation.
    new "Πώς θα θέλατε να εμφανίζεται η αίτησή σας;"

    # game/androidstrings.rpy:35
    old "In landscape orientation."
    # Automatic translation.
    new "Σε οριζόντιο προσανατολισμό."

    # game/androidstrings.rpy:36
    old "In portrait orientation."
    # Automatic translation.
    new "Σε κατακόρυφο προσανατολισμό."

    # game/androidstrings.rpy:37
    old "In the user's preferred orientation."
    # Automatic translation.
    new "Στον προτιμώμενο προσανατολισμό του χρήστη."

    # game/androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    # Automatic translation.
    new "Από ποιο κατάστημα εφαρμογών θα θέλατε να υποστηρίζετε τις αγορές εντός εφαρμογής;"

    # game/androidstrings.rpy:39
    old "Google Play."
    new "Google Play."

    # game/androidstrings.rpy:40
    old "Amazon App Store."
    new "Amazon App Store."

    # game/androidstrings.rpy:41
    old "Both, in one app."
    # Automatic translation.
    new "Και τα δύο, σε μία εφαρμογή."

    # game/androidstrings.rpy:42
    old "Neither."
    # Automatic translation.
    new "Ούτε."

    # game/androidstrings.rpy:43
    old "Do you want to automatically update the Java source code?"
    # Automatic translation.
    new "Θέλετε να ενημερώνετε αυτόματα τον πηγαίο κώδικα Java;"

    # game/androidstrings.rpy:44
    old "Yes. This is the best choice for most projects."
    # Automatic translation.
    new "Ναι. Αυτή είναι η καλύτερη επιλογή για τα περισσότερα έργα."

    # game/androidstrings.rpy:45
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    # Automatic translation.
    new "Όχι. Αυτό μπορεί να απαιτεί χειροκίνητες ενημερώσεις όταν αλλάζει η Ren'Py ή η διαμόρφωση του έργου."

    # game/androidstrings.rpy:46
    old "Unknown configuration variable: {}"
    # Automatic translation.
    new "Άγνωστη μεταβλητή διαμόρφωσης: {}"

    # game/androidstrings.rpy:47
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    # Automatic translation.
    new "Μεταγλωττίζω ένα σύντομο δοκιμαστικό πρόγραμμα, για να δω αν έχετε ένα λειτουργικό JDK στο σύστημά σας."

    # game/androidstrings.rpy:48
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please make sure you installed the 'JavaSoft (Oracle) registry keys'.\n\nWithout a working JDK, I can't continue."
    # Automatic translation.
    new "Δεν μπόρεσα να χρησιμοποιήσω το javac για τη μεταγλώττιση ενός δοκιμαστικού αρχείου. Αν δεν έχετε εγκαταστήσει ακόμα το Java Development Kit, παρακαλούμε κατεβάστε το από τη διεύθυνση:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nΤο JDK είναι διαφορετικό από το JRE, οπότε είναι πιθανό να έχετε Java χωρίς να έχετε το JDK. Βεβαιωθείτε ότι έχετε εγκαταστήσει τα \"κλειδιά μητρώου της JavaSoft (Oracle)\".\n\nΧωρίς ένα λειτουργικό JDK, δεν μπορώ να συνεχίσω."

    # game/androidstrings.rpy:49
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    # Automatic translation.
    new "Η έκδοση της Java στον υπολογιστή σας δεν φαίνεται να είναι η JDK 8, η οποία είναι η μόνη έκδοση που υποστηρίζεται από το Android SDK. Εάν πρέπει να εγκαταστήσετε το JDK 8, μπορείτε να το κατεβάσετε από τη διεύθυνση:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nΜπορείτε επίσης να ορίσετε τη μεταβλητή περιβάλλοντος JAVA_HOME για να χρησιμοποιήσετε μια διαφορετική έκδοση της Java."

    # game/androidstrings.rpy:50
    old "The JDK is present and working. Good!"
    # Automatic translation.
    new "Το JDK είναι παρόν και λειτουργεί. Ωραία!"

    # game/androidstrings.rpy:51
    old "The Android SDK has already been unpacked."
    # Automatic translation.
    new "Το Android SDK έχει ήδη αποσυμπιεστεί."

    # game/androidstrings.rpy:52
    old "Do you accept the Android SDK Terms and Conditions?"
    # Automatic translation.
    new "Αποδέχεστε τους Όρους και Προϋποθέσεις του Android SDK;"

    # game/androidstrings.rpy:53
    old "I'm downloading the Android SDK. This might take a while."
    # Automatic translation.
    new "Κατεβάζω το Android SDK. Αυτό μπορεί να πάρει λίγο χρόνο."

    # game/androidstrings.rpy:54
    old "I'm extracting the Android SDK."
    # Automatic translation.
    new "Εξαγάγω το Android SDK."

    # game/androidstrings.rpy:55
    old "I've finished unpacking the Android SDK."
    # Automatic translation.
    new "Τελείωσα την αποσυσκευασία του Android SDK."

    # game/androidstrings.rpy:56
    old "I'm about to download and install the required Android packages. This might take a while."
    # Automatic translation.
    new "Είμαι έτοιμος να κατεβάσω και να εγκαταστήσω τα απαιτούμενα πακέτα Android. Αυτό μπορεί να πάρει λίγο χρόνο."

    # game/androidstrings.rpy:57
    old "I was unable to accept the Android licenses."
    # Automatic translation.
    new "Δεν μπόρεσα να αποδεχτώ τις άδειες Android."

    # game/androidstrings.rpy:59
    old "I was unable to install the required Android packages."
    # Automatic translation.
    new "Δεν μπόρεσα να εγκαταστήσω τα απαιτούμενα πακέτα Android."

    # game/androidstrings.rpy:60
    old "I've finished installing the required Android packages."
    # Automatic translation.
    new "Έχω ολοκληρώσει την εγκατάσταση των απαιτούμενων πακέτων Android."

    # game/androidstrings.rpy:61
    old "It looks like you're ready to start packaging games."
    # Automatic translation.
    new "Φαίνεται ότι είστε έτοιμοι να αρχίσετε να πακετάρετε παιχνίδια."

    # game/androidstrings.rpy:62
    old "Please enter your name or the name of your organization."
    # Automatic translation.
    new "Παρακαλώ εισάγετε το όνομά σας ή το όνομα του οργανισμού σας."

    # game/androidstrings.rpy:63
    old "I found an android.keystore file in the rapt directory. Do you want to use this file?"
    # Automatic translation.
    new "Βρήκα ένα αρχείο android.keystore στον κατάλογο rapt. Θέλετε να χρησιμοποιήσετε αυτό το αρχείο;"

    # game/androidstrings.rpy:64
    old "I can create an application signing key for you. This key is required to create Universal APK for sideloading and stores other than Google Play.\n\nDo you want to create a key?"
    # Automatic translation.
    new "Μπορώ να δημιουργήσω ένα κλειδί υπογραφής εφαρμογής για εσάς. Αυτό το κλειδί είναι απαραίτητο για τη δημιουργία του Universal APK για sideloading και καταστήματα εκτός του Google Play.\n\nΘέλετε να δημιουργήσετε ένα κλειδί;"

    # game/androidstrings.rpy:65
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    # Automatic translation.
    new "Θα δημιουργήσω το κλειδί στο αρχείο android.keystore.\n\nΠρέπει να δημιουργήσετε αντίγραφα ασφαλείας αυτού του αρχείου. Αν το χάσετε, δεν θα μπορέσετε να αναβαθμίσετε την εφαρμογή σας.\n\nΠρέπει επίσης να φυλάξετε το κλειδί. Εάν κακόβουλοι άνθρωποι αποκτήσουν αυτό το αρχείο, θα μπορούσαν να δημιουργήσουν ψεύτικες εκδόσεις της εφαρμογής σας και ενδεχομένως να κλέψουν τα δεδομένα των χρηστών σας.\n\nΘα δημιουργήσετε αντίγραφο ασφαλείας του android.keystore και θα το φυλάξετε σε ασφαλές μέρος;"

    # game/androidstrings.rpy:66
    old "\n\nSaying 'No' will prevent key creation."
    # Automatic translation.
    new "\n\nΗ απάντηση \"Όχι\" θα αποτρέψει τη δημιουργία κλειδιού."

    # game/androidstrings.rpy:67
    old "Could not create android.keystore. Is keytool in your path?"
    # Automatic translation.
    new "Δεν μπόρεσε να δημιουργήσει το android.keystore. Είναι το keytool στη διαδρομή σας;"

    # game/androidstrings.rpy:68
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    # Automatic translation.
    new "Έχω ολοκληρώσει τη δημιουργία του android.keystore. Παρακαλούμε δημιουργήστε αντίγραφα ασφαλείας και φυλάξτε το σε ασφαλές μέρος."

    # game/androidstrings.rpy:69
    old "I found a bundle.keystore file in the rapt directory. Do you want to use this file?"
    # Automatic translation.
    new "Βρήκα ένα αρχείο bundle.keystore στον κατάλογο rapt. Θέλετε να χρησιμοποιήσετε αυτό το αρχείο;"

    # game/androidstrings.rpy:70
    old "I can create a bundle signing key for you. This key is required to build an Android App Bundle (AAB) for upload to Google Play.\n\nDo you want to create a key?"
    # Automatic translation.
    new "Μπορώ να δημιουργήσω ένα κλειδί υπογραφής δέσμης για εσάς. Αυτό το κλειδί απαιτείται για τη δημιουργία ενός Android App Bundle (AAB) για μεταφόρτωση στο Google Play.\n\nΘέλετε να δημιουργήσετε ένα κλειδί;"

    # game/androidstrings.rpy:71
    old "I will create the key in the bundle.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of bundle.keystore, and keep it in a safe place?"
    # Automatic translation.
    new "Θα δημιουργήσω το κλειδί στο αρχείο bundle.keystore.\n\nΠρέπει να δημιουργήσετε αντίγραφα ασφαλείας αυτού του αρχείου. Αν το χάσετε, δεν θα μπορέσετε να αναβαθμίσετε την εφαρμογή σας.\n\nΠρέπει επίσης να φυλάξετε το κλειδί. Εάν κακόβουλοι άνθρωποι αποκτήσουν αυτό το αρχείο, θα μπορούσαν να δημιουργήσουν ψεύτικες εκδόσεις της εφαρμογής σας και ενδεχομένως να κλέψουν τα δεδομένα των χρηστών σας.\n\nΘα δημιουργήσετε αντίγραφο ασφαλείας του bundle.keystore και θα το φυλάξετε σε ασφαλές μέρος;"

    # game/androidstrings.rpy:73
    old "Could not create bundle.keystore. Is keytool in your path?"
    # Automatic translation.
    new "Δεν μπόρεσε να δημιουργήσει το bundle.keystore. Είναι το keytool στη διαδρομή σας;"

    # game/androidstrings.rpy:74
    old "I've opened the directory containing android.keystore and bundle.keystore. Please back them up, and keep them in a safe place."
    # Automatic translation.
    new "Άνοιξα τον κατάλογο που περιέχει το android.keystore και το bundle.keystore. Παρακαλούμε δημιουργήστε αντίγραφα ασφαλείας και φυλάξτε τα σε ασφαλές μέρος."

    # game/choose_directory.rpy:67
    old "Select Projects Directory"
    # Automatic translation.
    new "Επιλέξτε Κατάλογος Έργων"

    # game/choose_directory.rpy:79
    old "The selected projects directory is not writable."
    # Automatic translation.
    new "Ο επιλεγμένος κατάλογος έργων δεν είναι εγγράψιμος."

    # game/choose_theme.rpy:508
    old "changing the theme"
    # Automatic translation.
    new "αλλαγή του θέματος"

    # game/distribute.rpy:1278
    old "Signing the Macintosh application...\n(This may take a long time.)"
    # Automatic translation.
    new "Υπογραφή της εφαρμογής Macintosh...\n(Αυτό μπορεί να πάρει πολύ χρόνο.)"

    # game/distribute.rpy:1745
    old "Copying files..."
    # Automatic translation.
    new "Αντιγραφή αρχείων..."

    # game/distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    # Automatic translation.
    new "Κατασκευάστε διανομές: [project.current.display_name!q]"

    # game/distribute_gui.rpy:195
    old "Update old-game"
    # Automatic translation.
    new "Ενημέρωση παλαιού παιχνιδιού"

    # game/distribute_gui.rpy:231
    old "(DLC)"
    new "(DLC)"

    # game/dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    # Automatic translation.
    new "Το Ren'Py εκτελείται από έναν φάκελο που επιτρέπεται μόνο για ανάγνωση. Ορισμένες λειτουργίες δεν θα λειτουργούν."

    # game/dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    # Automatic translation.
    new "Αυτό οφείλεται πιθανώς στο γεγονός ότι το Ren'Py εκτελείται απευθείας από εικόνα δίσκου Macintosh. Για να το διορθώσετε αυτό, τερματίστε αυτόν τον εκκινητή, αντιγράψτε ολόκληρο το φάκελο %s κάπου αλλού στον υπολογιστή σας και εκτελέστε ξανά το Ren'Py."

    # game/editor.rpy:152
    old "A modern editor with many extensions including advanced Ren'Py integration."
    # Automatic translation.
    new "Ένας σύγχρονος επεξεργαστής με πολλές επεκτάσεις, συμπεριλαμβανομένης της προηγμένης ενσωμάτωσης του Ren'Py."

    # game/editor.rpy:153
    old "A modern editor with many extensions including advanced Ren'Py integration.\n{a=jump:reinstall_vscode}Upgrade Visual Studio Code to the latest version.{/a}"
    # Automatic translation.
    new "Ένας σύγχρονος επεξεργαστής με πολλές επεκτάσεις, συμπεριλαμβανομένης της προηγμένης ενσωμάτωσης του Ren'Py.\n{a=jump:reinstall_vscode}Αναβαθμίστε το Visual Studio Code στην τελευταία έκδοση.{/a}"

    # game/editor.rpy:169
    old "Visual Studio Code"
    new "Visual Studio Code"

    # game/editor.rpy:169
    old "Up to 110 MB download required."
    # Automatic translation.
    new "Απαιτείται λήψη έως 110 MB."

    # game/editor.rpy:182
    old "A modern and approachable text editor."
    # Automatic translation.
    new "Ένας σύγχρονος και προσιτός επεξεργαστής κειμένου."

    # game/editor.rpy:196
    old "Atom"
    new "Atom"

    # game/editor.rpy:196
    old "Up to 150 MB download required."
    # Automatic translation.
    new "Απαιτείται λήψη έως 150 MB."

    # game/editor.rpy:211
    old "jEdit"
    new "jEdit"

    # game/editor.rpy:220
    old "Visual Studio Code (System)"
    # Automatic translation.
    new "Visual Studio Code (σύστημα)"

    # game/editor.rpy:220
    old "Uses a copy of Visual Studio Code that you have installed outside of Ren'Py. It's recommended you install the language-renpy extension to add support for Ren'Py files."
    # Automatic translation.
    new "Χρησιμοποιεί ένα αντίγραφο του Visual Studio Code που έχετε εγκαταστήσει εκτός του Ren'Py. Συνιστάται να εγκαταστήσετε την επέκταση language-renpy για να προσθέσετε υποστήριξη για αρχεία Ren'Py."

    # game/editor.rpy:226
    old "System Editor"
    # Automatic translation.
    new "Επεξεργαστής συστήματος"

    # game/editor.rpy:245
    old "None"
    # Automatic translation.
    new "Κανένα"

    # game/editor.rpy:352
    old "Edit [text]."
    # Automatic translation.
    new "Επεξεργασία [text]."

    # game/front_page.rpy:58
    old "PROJECTS:"
    # Automatic translation.
    new "ΕΡΓΑ:"

    # game/front_page.rpy:165
    old "audio"
    new "audio"

    # game/front_page.rpy:182
    old "Open project"
    # Automatic translation.
    new "Ανοιχτό έργο"

    # game/front_page.rpy:188
    old "Actions"
    # Automatic translation.
    new "Δράσεις"

    # game/front_page.rpy:219
    old "Web"
    # Automatic translation.
    new "Ιστοσελίδα"

    # game/front_page.rpy:219
    old "(Beta)"
    new "(Beta)"

    # game/gui7.rpy:302
    old "{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"
    # Automatic translation.
    new "{size=-4}\n\nΑυτό δεν θα αντικαταστήσει τα gui/main_menu.png, gui/game_menu.png και gui/window_icon.png, αλλά θα δημιουργήσει αρχεία που δεν υπάρχουν.{/size}"

    # game/gui7.rpy:333
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    # Automatic translation.
    new "Προσαρμοσμένο. Το γραφικό περιβάλλον είναι βελτιστοποιημένο για αναλογία διαστάσεων 16:9."

    # game/gui7.rpy:350
    old "WIDTH"
    # Automatic translation.
    new "ΠΛΑΤΟΣ"

    # game/gui7.rpy:350
    old "Please enter the width of your game, in pixels."
    # Automatic translation.
    new "Εισάγετε το πλάτος του παιχνιδιού σας, σε pixels."

    # game/gui7.rpy:360
    old "The width must be a number."
    # Automatic translation.
    new "Το πλάτος πρέπει να είναι ένας αριθμός."

    # game/gui7.rpy:366
    old "HEIGHT"
    # Automatic translation.
    new "ΥΨΟΣ"

    # game/gui7.rpy:366
    old "Please enter the height of your game, in pixels."
    # Automatic translation.
    new "Εισάγετε το ύψος του παιχνιδιού σας, σε pixels."

    # game/gui7.rpy:376
    old "The height must be a number."
    # Automatic translation.
    new "Το ύψος πρέπει να είναι ένας αριθμός."

    # game/gui7.rpy:424
    old "creating a new project"
    # Automatic translation.
    new "δημιουργία ενός νέου έργου"

    # game/gui7.rpy:428
    old "activating the new project"
    # Automatic translation.
    new "ενεργοποίηση του νέου έργου"

    # game/install.rpy:33
    old "Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."
    # Automatic translation.
    new "Δεν ήταν δυνατή η εγκατάσταση του [name!t], καθώς δεν βρέθηκε ένα αρχείο που να ταιριάζει με το [zipglob] στον κατάλογο του SDK Ren'Py."

    # game/install.rpy:79
    old "Successfully installed [name!t]."
    # Automatic translation.
    new "Εγκαταστάθηκε επιτυχώς το [name!t]."

    # game/install.rpy:111
    old "This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed."
    # Automatic translation.
    new "Αυτή η οθόνη σας επιτρέπει να εγκαταστήσετε βιβλιοθήκες που δεν μπορούν να διανεμηθούν με το Ren'Py. Ορισμένες από αυτές τις βιβλιοθήκες μπορεί να απαιτούν να συμφωνήσετε με μια άδεια τρίτου μέρους πριν χρησιμοποιηθούν ή διανεμηθούν."

    # game/install.rpy:117
    old "Install Steam Support"
    # Automatic translation.
    new "Εγκαταστήστε την υποστήριξη Steam"

    # game/install.rpy:126
    old "Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}."
    # Automatic translation.
    new "Πριν εγκαταστήσετε την υποστήριξη του Steam, βεβαιωθείτε ότι είστε συνεργάτης του Steam {a=https://partner.steamgames.com/}{/a} ."

    # game/install.rpy:138
    old "Steam support has already been installed."
    # Automatic translation.
    new "Η υποστήριξη Steam έχει ήδη εγκατασταθεί."

    # game/install.rpy:142
    old "Install Live2D Cubism SDK for Native"
    # Automatic translation.
    new "Εγκαταστήστε το Live2D Cubism SDK for Native"

    # game/install.rpy:156
    old "Install Libraries"
    # Automatic translation.
    new "Εγκατάσταση βιβλιοθηκών"

    # game/install.rpy:182
    old "The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc."
    # Automatic translation.
    new "Το {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} προσθέτει υποστήριξη για την εμφάνιση μοντέλων Live2D. Τοποθετήστε το CubismSdkForNative-4-{i}έκδοση{/i}.zip στον κατάλογο Ren'Py SDK και, στη συνέχεια, κάντε κλικ στην επιλογή Install. Η διανομή ενός παιχνιδιού με το Live2D απαιτεί την αποδοχή μιας άδειας χρήσης από τη Live2D, Inc."

    # game/install.rpy:186
    old "Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support."
    # Automatic translation.
    new "Το Live2D στο Ren'Py δεν υποστηρίζει το Web, το Android x86_64 (συμπεριλαμβανομένων των εξομοιωτών και του Chrome OS) και πρέπει να προστεθεί χειροκίνητα στα έργα iOS. Το Live2D πρέπει να επανεγκατασταθεί μετά την αναβάθμιση του Ren'Py ή την εγκατάσταση υποστήριξης Android."

    # game/install.rpy:191
    old "Open Ren'Py SDK Directory"
    # Automatic translation.
    new "Ανοίξτε τον κατάλογο του Ren'Py SDK"

    # game/installer.rpy:10
    old "Downloading [extension.download_file]."
    # Automatic translation.
    new "Λήψη [extension.download_file]."

    # game/installer.rpy:11
    old "Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]"
    # Automatic translation.
    new "Δεν ήταν δυνατή η λήψη του [extension.download_file] από το [extension.download_url]:\n{b}[extension.download_error]"

    # game/installer.rpy:12
    old "The downloaded file [extension.download_file] from [extension.download_url] is not correct."
    # Automatic translation.
    new "Το αρχείο [extension.download_file] που κατεβάσατε από το [extension.download_url] δεν είναι σωστό."

    # game/interface.rpy:124
    old "[interface.version]"
    new "[interface.version]"

    # game/interface.rpy:141
    old "Ren'Py Sponsor Information"
    # Automatic translation.
    new "Πληροφορίες χορηγού Ren'Py"

    # game/interface.rpy:385
    old "opening the log file"
    # Automatic translation.
    new "ανοίγοντας το αρχείο καταγραφής"

    # game/ios.rpy:269
    old "iOS: [project.current.display_name!q]"
    new "iOS: [project.current.display_name!q]"

    # game/ios.rpy:379
    old "There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices."
    # Automatic translation.
    new "Υπάρχουν γνωστά προβλήματα με τον προσομοιωτή iOS στην Apple Silicon. Παρακαλούμε δοκιμάστε σε συσκευές x86_64 ή iOS."

    # game/itch.rpy:45
    old "Downloading the itch.io butler."
    # Automatic translation.
    new "Κατεβάζοντας τον μπάτλερ του itch.io."

    # game/navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    # Automatic translation.
    new "Πλοήγηση: [project.current.display_name!q]"

    # game/new_project.rpy:81
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    # Automatic translation.
    new "Θα δημιουργήσετε ένα γλωσσικό έργο [new_project_language]{#this substitution may be localized}. Αλλάξτε τη γλώσσα εκκίνησης στις προτιμήσεις για να δημιουργήσετε ένα έργο σε άλλη γλώσσα."

    # game/preferences.rpy:106
    old "General"
    # Automatic translation.
    new "Γενικά"

    # game/preferences.rpy:107
    old "Options"
    # Automatic translation.
    new "Επιλογές"

    # game/preferences.rpy:224
    old "Sponsor message"
    # Automatic translation.
    new "Μήνυμα χορηγού"

    # game/preferences.rpy:227
    old "Daily check for update"
    # Automatic translation.
    new "Καθημερινός έλεγχος για ενημέρωση"

    # game/preferences.rpy:246
    old "Launcher Theme:"
    # Automatic translation.
    new "Θέμα εκτοξευτή:"

    # game/preferences.rpy:250
    old "Default theme"
    # Automatic translation.
    new "Προεπιλεγμένο θέμα"

    # game/preferences.rpy:251
    old "Dark theme"
    # Automatic translation.
    new "Σκοτεινό θέμα"

    # game/preferences.rpy:252
    old "Custom theme"
    # Automatic translation.
    new "Προσαρμοσμένο θέμα"

    # game/preferences.rpy:256
    old "Information about creating a custom theme can be found {a=https://www.renpy.org/doc/html/skins.html}in the Ren'Py Documentation{/a}."
    # Automatic translation.
    new "Πληροφορίες σχετικά με τη δημιουργία ενός προσαρμοσμένου θέματος μπορείτε να βρείτε στη διεύθυνση {a=https://www.renpy.org/doc/html/skins.html}στην Τεκμηρίωση Ren'Py{/a}."

    # game/preferences.rpy:273
    old "Install Libraries:"
    # Automatic translation.
    new "Εγκατάσταση βιβλιοθηκών:"

    # game/preferences.rpy:300
    old "Reset window size"
    # Automatic translation.
    new "Επαναφορά μεγέθους παραθύρου"

    # game/preferences.rpy:301
    old "Clean temporary files"
    # Automatic translation.
    new "Καθαρισμός προσωρινών αρχείων"

    # game/preferences.rpy:308
    old "Cleaning temporary files..."
    # Automatic translation.
    new "Καθαρισμός προσωρινών αρχείων..."

    # game/preferences.rpy:338
    old "{#in language font}Welcome! Please choose a language"
    # Automatic translation.
    new "{#in language font}Καλώς ήρθατε! Παρακαλώ επιλέξτε μια γλώσσα"

    # game/preferences.rpy:373
    old "{#in language font}Start using Ren'Py in [lang_name]"
    # Automatic translation.
    new "{#in language font}Ξεκινήστε να χρησιμοποιείτε το Ren'Py στο [lang_name]"

    # game/project.rpy:46
    old "Lint checks your game for potential mistakes, and gives you statistics."
    # Automatic translation.
    new "Το Lint ελέγχει το παιχνίδι σας για πιθανά λάθη και σας παρέχει στατιστικά στοιχεία."

    # game/project.rpy:283
    old "This may be because the project is not writeable."
    # Automatic translation.
    new "Αυτό μπορεί να οφείλεται στο γεγονός ότι το έργο δεν είναι εγγράψιμο."

    # game/translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    # Automatic translation.
    new "Μεταφράσεις: [project.current.display_name!q]"

    # game/translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    # Automatic translation.
    new "Απόσπασμα διαλόγου: [project.current.display_name!q]"

    # game/translations.rpy:391
    old "Language (or None for the default language):"
    # Automatic translation.
    new "Γλώσσα (ή Καμία για την προεπιλεγμένη γλώσσα):"

    # game/updater.rpy:64
    old "Release (Ren'Py 8, Python 3)"
    # Automatic translation.
    new "Έκδοση (Ren'Py 8, Python 3)"

    # game/updater.rpy:65
    old "Release (Ren'Py 7, Python 2)"
    # Automatic translation.
    new "Έκδοση (Ren'Py 7, Python 2)"

    # game/updater.rpy:69
    old "Prerelease (Ren'Py 8, Python 3)"
    new "Prerelease (Ren'Py 8, Python 3)"

    # game/updater.rpy:70
    old "Prerelease (Ren'Py 7, Python 2)"
    new "Prerelease (Ren'Py 7, Python 2)"

    # game/updater.rpy:77
    old "Nightly (Ren'Py 8, Python 3)"
    # Automatic translation.
    new "Κάθε βράδυ (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly (Ren'Py 7, Python 2)"
    # Automatic translation.
    new "Νυχτερινή (Ren'Py 7, Python 2)"

    # game/updater.rpy:108
    old "The update channel controls the version of Ren'Py the updater will download."
    # Automatic translation.
    new "Το κανάλι ενημέρωσης ελέγχει την έκδοση του Ren'Py που θα κατεβάσει το πρόγραμμα ενημέρωσης."

    # game/updater.rpy:116
    old "• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}"
    # Automatic translation.
    new "- {a=https://www.renpy.org/doc/html/changelog.html}Προβολή αρχείου καταγραφής αλλαγών{/a}"

    # game/updater.rpy:118
    old "• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}"
    # Automatic translation.
    new "- {a=https://www.renpy.org/dev-doc/html/changelog.html}Προβολή αρχείου καταγραφής αλλαγών{/a}"

    # game/updater.rpy:124
    old "• This version is installed and up-to-date."
    # Automatic translation.
    new "- Αυτή η έκδοση είναι εγκατεστημένη και ενημερωμένη."

    # game/updater.rpy:136
    old "%B %d, %Y"
    new "%B %d, %Y"

    # game/updater.rpy:215
    old "Fetching the list of update channels"
    # Automatic translation.
    new "Λήψη της λίστας των καναλιών ενημέρωσης"

    # game/updater.rpy:220
    old "downloading the list of update channels"
    # Automatic translation.
    new "Λήψη του καταλόγου των καναλιών ενημέρωσης"

    # game/web.rpy:428
    old "Preparing progressive download"
    # Automatic translation.
    new "Προετοιμασία προοδευτικής λήψης"

    # game/web.rpy:485
    old "Creating package..."
    # Automatic translation.
    new "Δημιουργία πακέτου..."

    # game/web.rpy:505
    old "Web: [project.current.display_name!q]"
    new "Web: [project.current.display_name!q]"

    # game/web.rpy:535
    old "Build Web Application"
    # Automatic translation.
    new "Κατασκευάστε εφαρμογή Web"

    # game/web.rpy:536
    old "Build and Open in Browser"
    # Automatic translation.
    new "Κατασκευή και άνοιγμα σε πρόγραμμα περιήγησης"

    # game/web.rpy:537
    old "Open in Browser"
    # Automatic translation.
    new "Άνοιγμα σε πρόγραμμα περιήγησης"

    # game/web.rpy:538
    old "Open build directory"
    # Automatic translation.
    new "Άνοιγμα καταλόγου κατασκευής"

    # game/web.rpy:560
    old "Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    # Automatic translation.
    new "Εικόνες και μουσική μπορούν να μεταφορτωθούν κατά την αναπαραγωγή. Θα δημιουργηθεί ένα αρχείο 'progressive_download.txt' ώστε να μπορείτε να ρυθμίσετε αυτή τη συμπεριφορά."

    # game/web.rpy:568
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    # Automatic translation.
    new "Πριν συσκευάσετε εφαρμογές ιστού, θα πρέπει να κατεβάσετε το RenPyWeb, την υποστήριξη ιστού της Ren'Py. Θα θέλατε να κατεβάσετε το RenPyWeb τώρα;"


translate greek strings:

    # game/updater.rpy:79
    old "A nightly build of fixes to the release version of Ren'Py."
    # Automatic translation.
    new "Ένα νυχτερινό build με διορθώσεις στην έκδοση κυκλοφορίας του Ren'Py."

