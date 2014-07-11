# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

    from store import persistent

    class Product(object):
        """
        A data object representing a product.
        """

        def __init__(self, identifier):
            self.identifier = identifier

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

        def purchase(self, p):
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

    class AndroidBackend(object):
        """
        The IAP backend that is used when IAP is supported.
        """

        def __init__(self, devicePurchase, store_name):
            self.devicePurchase = devicePurchase
            self.store_name = store_name

        def get_store_name(self):
            return self.store_name

        def wait_for_result(self, sleep):
            """
            Waits for a result.

            `sleep`
                The function used to sleep, which should have the signature
                of time.sleep.

            Returns True if the action succeded, or False otherwise.
            """

            while True:
                rv = self.devicePurchase.checkPurchaseResult()
                if rv:
                    break

                sleep(.1)

            if rv == 1:
                return True
            else:
                return False

        def purchase(self, p):
            self.devicePurchase.beginPurchase(p.identifier)
            return self.wait_for_result(renpy.pause)

        def restore_purchases(self, interact=True):
            import time

            self.devicePurchase.restorePurchases()

            if interact:
                self.wait_for_result(renpy.pause)
            else:
                self.wait_for_result(time.sleep)

        def has_purchased(self, p):
            return self.devicePurchase.isPurchaseOwned(p.identifier)

    # The backend we're using.
    backend = NoneBackend()

    # A map from product identifier to the product object.
    products = { }

    def register(product):
        """
        :doc: iap

        Registers a product with the in-app purchase system.

        `product`
            A string identifying the product to be purchased. This must match
            the product identifier in the various app stores.

            These strings are generally of the form "com.domain.app.product".
        """

        if product in prodicts:
            raise Exception('Product %r has already been registered.' % product)

        p = Product(product)
        products[product] = p

    def restore(interact=True):
        """
        :doc: iap

        Contacts the app store and restores any missing purchases.

        `interact`
            If True, renpy.pause will be cause while waiting for the app store
            to respond.
        """

        backend.restore_purchases(interact)

        for p in products.values():
            persistent._iap_purchases[p.identifier] = backend.has_purchased(p)


    def get_product(product):
        p = products.get(product, None)
        if p is None:
            raise Exception("Product %r is has not been registered.")

        return p

    def purchase(product):
        """
        :doc: iap

        This function requests the purchase of `product`.

        It returns true if the purchase succeded, now or at any time in the past,
        and false otherwise.
        """

        p = get_product(product)

        if persistent._iap_purchases[p.identifier]:
            return True

        rv = backend.purchase(p.identifier)

        if rv:
            persistent._iap_purchases[p.identifier] = True

        return rv

    def has_purchased(product):
        """
        :doc: iap

        Returns True if the user has purchased `product` in the past, and
        False otherwise.
        """

        p = get_product(product)

        return persistent._iap_purchases[p.identifier]

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
        devicePurchase = autoclass('com.puzzlebrothers.renpurchase.devicePurchase')

        store_name = devicePurchase.getStoreName()
        if store_name == "none":
            return NoneBackend()

        return AndroidBackend(devicePurchase, store_name)

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

        # Set up the back end.
        if renpy.android:
            backend = init_android()
        else:
            backend = NoneBackend()

        # If there are any missing products, restore purchases.
        if missing_products():
            restore(False)

init 1500 python in iap:
    init()
