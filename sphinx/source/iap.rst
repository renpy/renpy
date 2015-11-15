=================
In-App Purchasing
=================

Ren'Py includes a high-level in-app purchasing framework. This framework
currently only supports unlock-style purchases from the Apple App Store,
Google Play, and the Amazon App Store.

Using this framework is fairly simple, and consists of the following
functions.

* In the init phase of your game, register available purchases using the
  :func:`iap.register` function.
* Once the game has started, check to see if a purchase has been purchased
  using the :func:`iap.has_purchased` function.
* Allow the user to purchase an item using the :func:`iap.purchase` function
  or the :func:`iap.Purchase` action.
* Allow the user to restore purchases bought on other devices using the
  :func:`iap.restore` function or the :func:`iap.Restore` action.

To offer in-app purchases, the purchases (including an associated price)
must be set up on the various marketplaces. When building for android,
Ren'Py will ask for the marketplace in use when configuring the package.

Apple App Store
    The Apple App Store is based on the package name, and does not require
    special configuration.

Google Play
    Before Google Play can be used, you must add the google play key and
    a salt to your project. See the :ref:`Expansion APK <expansion-apk>`
    section for information on how to do this.

Amazon App Store
    The Amazon app store is based on the package name, and does not
    require special configuration.


IAP Functions
-------------

.. include:: inc/iap

IAP Actions
-----------

.. include:: inc/iap_actions
