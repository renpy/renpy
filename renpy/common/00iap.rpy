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

    from store import persistent, Action
    import time

    background = "black"

    class Product(object):
        """
        A data object representing a product.
        """

        def __init__(self, product, identifier, google, amazon):
            self.product = product
            self.identifier = identifier
            self.google = google
            self.amazon = amazon

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

    class AndroidBackend(object):
        """
        The IAP backend that is used when IAP is supported.
        """

        def __init__(self, devicePurchase, store_name):
            self.devicePurchase = devicePurchase
            self.store_name = store_name

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

            while True:
                rv = self.devicePurchase.checkPurchaseResult()

                if rv:
                    break

                if interact:
                    renpy.pause(.1)
                else:
                    time.sleep(.1)

            if rv == 1:
                return True
            else:
                return False


        def purchase(self, p, interact=True):
            identifier = self.identifier(p)
            self.devicePurchase.beginPurchase(identifier)
            return self.wait_for_result(interact=interact)

        def restore_purchases(self, interact=True):
            self.devicePurchase.restorePurchases()
            self.wait_for_result(interact)

        def has_purchased(self, p):
            identifier = self.identifier(p)
            return self.devicePurchase.isPurchaseOwned(identifier)

    # The backend we're using.
    backend = NoneBackend()

    # A map from product identifier to the product object.
    products = { }

    def register(product, identifier=None, amazon=None, google=None):
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
        """

        if product in products:
            raise Exception('Product %r has already been registered.' % product)

        identifier = identifier or product
        amazon = amazon or identifier
        google = google or identifier

        p = Product(product, identifier, google, amazon)
        products[product] = p

    def with_background(f, *args, **kwargs):
        """
        Displays the background, then invokes `f`.
        """

        renpy.scene()
        renpy.show(background)
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

        rv = backend.purchase(p, interact)

        if rv:
            persistent._iap_purchases[p.identifier] = True

        return rv

    class Purchase(Action):
        """
        :doc: iap_actions

        An action that attempts the purchase of `product`. This action is
        sensitive iff and only if the product is purchasable (a store is
        enabled, and the product has not already been purchased.)
        """

        def __init__(self, product):
            self.product = product

        def __call__(self):
            renpy.invoke_in_new_context(with_background, purchase, self.product)
            renpy.restart_interaction()

        def get_sensitive(self):
            return get_store_name() and not has_purchased(self.product)

    def has_purchased(product):
        """
        :doc: iap

        Returns True if the user has purchased `product` in the past, and
        False otherwise.
        """

        p = get_product(product)

        return persistent._iap_purchases[p.identifier]

    def get_store_name():
        """
        :doc: iap

        Returns the name of the enabled store for in-app purchase. This
        currently returns one of "amazon", "google", or None if no store
        is configured.
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

        # Restore purchases.
        if products:
            restore(False)

init 1500 python in iap:
    init()
