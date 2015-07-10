﻿# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init -1500 python in iap:

    from store import persistent, Action
    import time

    background = "black"

    class Product(object):
        """
        A data object representing a product.
        """

        def __init__(self, product, identifier, google, amazon, ios):
            self.product = product
            self.identifier = identifier
            self.google = google
            self.amazon = amazon
            self.ios = ios

            # None if the item is not purchasable. Otherwise, a string that
            # gives the price in the local language.
            self.price = None

    class NoneBackend(object):
        """
        The IAP backend that is used when IAP is not supported.
        """

        def get_store_name(self):
            """
            Returns the name of the app store in use, or None if there is
            no app store.
            """

            return None

        def purchase(self, p, interact=True):
            """
            Triggers an attempt to purchase the product `p`. Returns true if
            the purchase succeeds, and False otherwise.
            """

            return False

        def restore_purchases(self, interact=True):
            """
            Restores purchases found on the server.

            `interact`
                If true, Ren'Py will pause while waiting for the restore to
                occur.
            """

        def has_purchased(self, p):
            """
            Returns True if `p` has been purchased, and False otherwise.
            """

            return False

        def is_deferred(self, p):
            """
            Returns True if the purchase of `p` has been deferred, and False otherwise.
            """

            return False

        def get_price(self, p):
            """
            Returns the price of the item, or None if the item is not
            purchasable.
            """

            return None

        def init(self):
            """
            Called at init time to do any initialization required.
            """

            return

    class AndroidBackend(object):
        """
        The IAP backend that is used when IAP is supported.
        """

        def __init__(self, store, store_name):
            self.store = store
            self.store_name = store_name

            self.store.clearSKUs()

            for p in products.values():
                self.store.addSKU(self.identifier(p))

        def get_store_name(self):
            return self.store_name

        def identifier(self, p):
            """
            Returns the identifier for a store purchase.
            """

            if self.store_name == "amazon":
                return p.amazon
            else:
                return p.google

        def wait_for_result(self, interact=True):
            """
            Waits for a result.

            `interact`
                If true, waits interactively. If false, waits using
                renpy.pause.
            """

            while not self.store.getFinished():
                if interact:
                    renpy.pause(.1)
                else:
                    time.sleep(.1)

        def purchase(self, p, interact=True):
            identifier = self.identifier(p)
            self.store.beginPurchase(identifier)
            self.wait_for_result(interact=interact)

        def restore_purchases(self, interact=True):
            self.store.updatePrices();
            self.wait_for_result(interact)

            self.store.restorePurchases();
            self.wait_for_result(interact)

        def has_purchased(self, p):
            identifier = self.identifier(p)
            return self.store.hasPurchased(identifier)

        def is_deferred(self, p):
            return False

        def get_price(self, p):
            identifier = self.identifier(p)
            return self.store.getPrice(identifier)

        def init(self):
            restore(False)

    if renpy.ios:
        import pyobjus
        IAPHelper = pyobjus.autoclass("IAPHelper")
        NSMutableArray = pyobjus.autoclass("NSMutableArray")

        from pyobjus import objc_str, objc_arr

    class IOSBackend(object):

        def __init__(self):
            self.helper = IAPHelper.alloc().init()

            identifiers = NSMutableArray.alloc().init()

            for p in products.values():
                identifiers.addObject_(objc_str(p.ios))

            self.helper.productIdentifiers = identifiers

            self.validated_products = False

        def get_store_name(self):
            if renpy.predicting():
                return "ios"

            if self.helper.canMakePayments():
                return "ios"
            else:
                return None

        def identifier(self, p):
            """
            Returns the identifier for a store purchase.
            """

            return p.ios

        def wait_for_result(self, interact=True):
            """
            Waits for a result.

            `interact`
                If true, waits interactively. If false, waits using
                renpy.pause.
            """

            while not self.helper.finished:
                if interact:
                    renpy.pause(.1)
                else:
                    import pygame
                    pygame.event.pump()
                    time.sleep(.1)

        def validate_products(self, interact):
            if self.validated_products:
                return False

            self.helper.validateProductIdentifiers()
            self.wait_for_result(interact)

            self.validated_products = True


        def purchase(self, p, interact=True):
            self.validate_products(interact)

            identifier = objc_str(self.identifier(p))
            self.helper.beginPurchase_(identifier)
            self.wait_for_result(interact=interact)

        def restore_purchases(self, interact=True):
            self.validate_products(interact)

            self.helper.restorePurchases()
            self.wait_for_result(interact)

        def has_purchased(self, p):
            identifier = objc_str(self.identifier(p))
            return self.helper.hasPurchased_(identifier)

        def is_deferred(self, p):
            identifier = objc_str(self.identifier(p))
            return self.helper.isDeferred_(identifier)

        def get_price(self, p):

            if renpy.predicting():
                return None

            self.validate_products(False)

            identifier = objc_str(self.identifier(p))
            rv = self.helper.formatPrice_(identifier)

            if rv is not None:
                rv = rv.UTF8String().decode("utf-8")

            return rv

        def init(self):
            return


    # The backend we're using.
    backend = NoneBackend()

    # A map from product identifier to the product object.
    products = { }

    def register(product, identifier=None, amazon=None, google=None, ios=None):
        """
        :doc: iap

        Registers a product with the in-app purchase system.

        `product`
            A string giving the high-level name of the product. This is the
            string that will be passed to :func:`iap.purchase`, :func:`iap.Purchase`,
            and :func:`iap.has_purchased` to represent this product.

        `identifier`
            A string that's used to identify the product internally. Once used
            to represent a product, this must never change. These strings are
            generall of the form "com.domain.game.product".

            If None, defaults to `product`.

        `amazon`
            A string that identifies the product in the Amazon app store.
            If not given, defaults to `identifier`.

        `google`
            A string that identifies the product in the Google Play store.
            If not given, defaults to `identifier`.

        `ios`
            A string that identifies the product in the Apple App store for
            iOS. If not given, defaults to `identifier`.
        """

        if product in products:
            raise Exception('Product %r has already been registered.' % product)

        identifier = identifier or product
        amazon = amazon or identifier
        google = google or identifier
        ios = ios or identifier

        p = Product(product, identifier, google, amazon, ios)
        products[product] = p

    def with_background(f, *args, **kwargs):
        """
        Displays the background, then invokes `f`.
        """

        renpy.scene()
        renpy.show(background)
        renpy.pause(0)

        return f(*args, **kwargs)

    def restore(interact=True):
        """
        :doc: iap

        Contacts the app store and restores any missing purchases.

        `interact`
            If True, renpy.pause will be called while waiting for the app store
            to respond.
        """

        backend.restore_purchases(interact)

        for p in products.values():
            persistent._iap_purchases[p.identifier] = backend.has_purchased(p)

    class Restore(Action):
        """
        :doc: iap_actions

        An Action that contacts the app store and restores any missing purchases.
        """

        def __call__(self):
            renpy.invoke_in_new_context(with_background, restore)

        def get_sensitive(self):
            return get_store_name()

    def get_product(product):
        p = products.get(product, None)
        if p is None:
            raise Exception("Product %r is has not been registered.")

        return p

    def purchase(product, interact=True):
        """
        :doc: iap

        This function requests the purchase of `product`.

        It returns true if the purchase succeded, now or at any time in the past,
        and false otherwise.
        """

        p = get_product(product)

        if persistent._iap_purchases[p.identifier]:
            return True

        backend.purchase(p, interact)

        if backend.has_purchased(p):
            persistent._iap_purchases[p.identifier] = True
            return True
        else:
            return False

    class Purchase(Action):
        """
        :doc: iap_actions

        An action that attempts the purchase of `product`. This action is
        sensitive iff and only if the product is purchasable (a store is
        enabled, and the product has not already been purchased.)
        """

        def __init__(self, product):
            self.product = product
            self.sensitive = True

        def __call__(self):
            renpy.invoke_in_new_context(with_background, purchase, self.product)
            renpy.restart_interaction()

        def should_be_sensitive(self):

            if not get_store_name():
                return False

            if has_purchased(self.product):
                return False

            if is_deferred(self.product):
                return False

            return True

        def get_sensitive(self):
            self.sensitive = self.should_be_sensitive()
            return self.sensitive

        def periodic(self, st):
            if self.should_be_sensitive() != self.sensitive:
                renpy.restart_interaction()

            return 5.0

    def has_purchased(product):
        """
        :doc: iap

        Returns True if the user has purchased `product` in the past, and
        False otherwise.
        """

        p = get_product(product)

        # Check the cache first, since we might be off line.
        if persistent._iap_purchases.get(p.identifier, False):
            return True

        # Then ask the backend, in case we bought the product
        # recently.
        return backend.has_purchased(p)


    def is_deferred(product):
        """
        :doc: iap

        Returns True if the user has asked to purchase `product`, but that
        request has to be approved by a third party, such as a parent or
        guardian.
        """

        p = get_product(product)

        # Then ask the backend, in case we bought the product
        # recently.
        return backend.is_deferred(p)

    def get_price(product):
        """
        :doc: iap

        Returns a string giving the price of the `product` in the user's
        local currency. Returns None if the price of the product is unknown -
        which indicates the product cannot be purchased.
        """

        p = get_product(product)

        if p.price is None:
            p.price = backend.get_price(p)

        return p.price

    def get_store_name():
        """
        :doc: iap

        Returns the name of the enabled store for in-app purchase. This
        currently returns one of "amazon", "google", "ios" or None if no store
        is available.
        """

        return backend.get_store_name()

    def missing_products():
        """
        Determines if any products are missing from persistent._iap_purchases
        """

        for p in products.values():
            if p.identifier not in persistent._iap_purchases:
                return True

        return False

    def init_android():
        """
        Initialize IAP on Android.
        """

        from jnius import autoclass
        Store = autoclass('org.renpy.iap.Store')
        store = Store.getStore()

        store_name = store.getStoreName()

        if store_name == "none":
            return NoneBackend()

        return AndroidBackend(store, store_name)

    def init():
        """
        Called to initialize the IAP system.
        """

        global backend

        if persistent._iap_purchases is None:
            persistent._iap_purchases = { }

        # Do nothing if we have no products.
        if not products:
            return

        for p in products.values():
            if p.identifier not in persistent._iap_purchases:
                persistent._iap_purchases[p.identifier] = False

        # Set up the back end.
        if renpy.android:
            backend = init_android()
        elif renpy.ios:
            backend = IOSBackend()
        else:
            backend = NoneBackend()

        # Restore purchases.
        if products:
            backend.init()

init 1500 python in iap:
    init()
