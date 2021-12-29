=================
In-App Purchasing
=================

Ren'Py includes a high-level in-app purchasing framework. This framework
currently only supports unlock-style purchases from the Apple App Store,
Google Play, and the Amazon Appstore.

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
must be set up on the various marketplaces.

IAP Functions
-------------

.. include:: inc/iap

IAP Actions
-----------

.. include:: inc/iap_actions
