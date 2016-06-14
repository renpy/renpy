Chrome OS / Chrome Browser
==========================

Ren'Py supports being run under Chrome OS and as an application inside the
Chrome web browser. This consists of the ability to run Ren'Py
Android apps under the Android Runtime for Chrome (ARC).

To port a Ren'Py Android app to Chrome, the following steps are required:

1. Install the ARC Welder app from the chrome web store:
   https://chrome.google.com/webstore/detail/arc-welder/emfinbmielocnlhgmfkkmkngdoccbadn

2. Package the game for android, as described in the :ref:`android documentation <android>`.

3. Launch ARC Welder from the apps menu inside chrome.

4. Find the path to the .apk file containin your app.

5. Choose the following options:

   * Orientation: Landscape
   * Form factor: Tablet
   * Resize: Disabled
   * Clipboard access: unchecked

   Resizing does not currently work, so it's best to leave it disabled.


6. Choose "Test". The game will load and run in the Chrome web browser.

7. Choose "Download Zip". Chrome will generate a Zip file suitable for
   uploading to the chrome web store.
