# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:

    class __GalleryAllPriorCondition(object):

        def check(self, all_prior):
            return all_prior


    class __GalleryArbitraryCondition(object):
        def __init__(self, condition):
            self.condition = condition

        def check(self, all_prior):
            return eval(self.condition)


    class __GalleryUnlockCondition(object):
        def __init__(self, images):
            self.images = images

        def check(self, all_prior):
            for i in self.images:
                if not renpy.seen_image(i):
                    return False

            return True


    class __GalleryImage(object):
        def __init__(self, gallery, displayables):

            # The gallery object we belong to.
            self.gallery = gallery

            # A list of conditions for this image to be displayed.
            self.conditions = [ ]

            # A list of displayables to show.
            self.displayables = displayables

            # A list of transforms to apply to those displayables, or None
            # to not apply a transform.
            self.transforms = [ None ] * len(displayables)


        def check_unlock(self, all_prior):
            """
            Returns True if the image is unlocked.
            """

            for i in self.conditions:
                if not i.check(all_prior):
                    return False

            return True

        def show(self, locked, index, count):
            """
            Shows this image when it's unlocked.
            """

            renpy.transition(self.gallery.transition)
            ui.saybehavior()

            displayables = [ ]

            for d, transform in zip(self.displayables, self.transforms):

                if transform is not None:
                    d = transform(d)
                else:
                    d = config.default_transform(d)

                displayables.append(d)

            if renpy.has_screen("gallery"):
                gallery = "gallery"
            else:
                gallery = "_gallery"
            renpy.show_screen(gallery, locked=locked, index=index + 1, count=count, displayables=displayables, gallery=self.gallery)
            return ui.interact()

    class __GalleryButton(object):
        def __init__(self, gallery):
            self.gallery = gallery
            self.images = [ ]
            self.conditions = [ ]

        def check_unlock(self):
            for i in self.conditions:
                if not i.check(True):
                    return False

            for i in self.images:
                if i.check_unlock(False):
                    return True

            return False

        def show(self):

            all_prior = True
            diff = False

            for i, img in enumerate(self.images):
                locked = not img.check_unlock(all_prior)
                rv = img.show(locked, i, len(self.images))
                if rv == "next" or rv == "previous" or rv == "close":
                    return rv

            if rv == "diff_next":
                return "next"

            renpy.transition(self.gallery.transition)

    class Gallery(object):
        """
        :doc: gallery class

        This class supports the creation of an image gallery by handling the
        locking of images, providing an action that can show one or more images,
        and a providing method that creates buttons that use that action.

        .. attribute:: transition

            The transition that is used when changing images.

        .. attribute:: locked_button

            The default displayable used by make_button for a locked button.

        .. attribute:: hover_border

            The default hover border used by make_button.

        .. attribute:: idle_border

            The default idle border used by make_button.
        """

        transition = None

        hover_border = None
        idle_border = None

        locked_button = None

        def __init__(self):

            # A map from button name (or image) to __GalleryButton object.
            self.buttons = { }
            self.button_list = []

            self.button_ = None
            self.image_ = None
            self.unlockable = None
            self.slideshow = False
            self.start_time = None

        def button(self, name):
            """
            :doc: gallery method

            Creates a new button, named `name`.

            `name`
                The name of the button being created.
            """

            self.button_ = __GalleryButton(self)
            self.unlockable = self.button_
            self.buttons[name] = self.button_
            self.button_list.append(name)

        def image(self, *displayables):
            """
            :doc: gallery method

            Adds a new image to the current button, where an image consists
            of one or more displayables.
            """

            self.image_ = __GalleryImage(self, displayables)
            self.button_.images.append(self.image_)
            self.unlockable = self.image_

        display = image

        def transform(self, *transforms):
            """
            :doc: gallery method

            Applies transforms to the last image registered. This should be
            called with the same number of transforms as the image has
            displayables. The transforms are applied to the corresponding
            displayables.

            If a transform is None, the default transform is used.
            """

            self.image_.transforms = transforms

        def unlock(self, *images):
            """
            :doc: gallery method

            A condition that takes one or more image names as argument, and
            is satisfied when all the named images have been seen by the
            player. The image names should be given as strings.
            """

            self.unlockable.conditions.append(__GalleryUnlockCondition(images))

        def condition(self, expression):
            """
            :doc: gallery method

            A condition that is satisfied when an expression evaluates to true.

            `expression`
                A string giving a python expression.
            """

            if not isinstance(expression, basestring):
                raise Exception("Gallery condition must be a string containing an expression.")

            self.unlockable.conditions.append(__GalleryArbitraryCondition(expression))

        def allprior(self):
            """
            :doc: gallery method

            A condition that is true if all prior images associated with the
            current button have been unlocked.
            """

            self.unlockable.conditions.append(__GalleryAllPriorCondition())

        def unlock_image(self, *images):
            """
            :doc: gallery method

            A convenience method that is equivalent to calling image and unlock
            with the same parameters. This will cause an image to be displayed
            if it has been seen before.

            The images should be specified as strings giving image names.
            """

            self.image(*images)
            self.unlock(*images)

        def Action(self, name):
            """
            :doc: gallery method

            An action that displays the images associated with the given button
            name.
            """

            if name not in self.buttons:
                raise Exception("{0!r} is not a button defined in this gallery.".format(name))

            b = self.buttons[name]

            if b.check_unlock():
                return ui.invokesinnewcontext(self.show, b, name)
            else:
                return None

        def make_button(self, name, unlocked, locked=None, hover_border=None, idle_border=None, **properties):
            """
            :doc: gallery method

            This creates a button that displays the images associated with the given
            button name.

            `name`
                The name of the button that will be created.

            `unlocked`
                A displayable that is displayed for this button when it is
                unlocked.

            `locked`
                A displayable that is displayed for this button when it is
                locked. If None, the locked_button field of the gallery
                object is used instead.

            `hover_border`
                A displayable that is used to overlay this button when
                it is unlocked and has focus. If None, the hover_border
                field of the gallery object is used.

            `idle_border`
                A displayable that is used to overlay this button when
                it is unlocked but unfocused. If None, the idle_border
                field of the gallery object is used.

            Additional keyword arguments become style properties of the
            created button object.
            """

            action = self.Action(name)

            if locked is None:
                locked = self.locked_button

            if hover_border is None:
                hover_border = self.hover_border

            if idle_border is None:
                idle_border = self.idle_border

            return Button(action=action, child=unlocked, insensitive_child=locked, hover_foreground=hover_border, idle_foreground=idle_border, **properties)

        def get_fraction(self, name, format="{seen}/{total}"):
            """
            :doc: gallery method

            Returns a text string giving the number of unlocked images and total number of images in the button
            named `name`.

            `format`
                A python format string that's used to format the numbers. This has three values that
                can be substituted in:

                {seen}
                    The number of images that have been seen.
                {total}
                    The total number of images in the button.
                {locked}
                    The number of images that are still locked.
            """

            seen = 0
            total = 0

            all_prior = True

            for i in self.buttons[name].images:
                total += 1
                if i.check_unlock(all_prior):
                    seen += 1
                else:
                    all_prior = False

            return format.format(seen=seen, total=total, locked=total - seen)

        def show(self, button, name):
            while True:
                rv = button.show()
                if rv == "close":
                    return
                elif rv == "next":
                    idx = self.button_list.index(name) + 1
                    try:
                        while not self.buttons[self.button_list[idx]].check_unlock():
                            idx += 1
                    except IndexError:
                        return
                    name = self.button_list[idx]
                    button = self.buttons[name]
                    continue
                elif rv == "previous":
                    idx = self.button_list.index(name) - 1
                    while not self.buttons[self.button_list[idx]].check_unlock():
                        idx -= 1
                    if idx >= 0:
                        name = self.button_list[idx]
                        button = self.buttons[name]
                        continue
                    else:
                        return
                else:
                    return

        def close(self):
            return "close"

        def Close(self):
            """
            :doc: gallery method
            
            Close the current image.
            """
            return self.close

        def next(self):
            return "next"

        def diff_next(self):
            return "diff_next"

        def Next(self, diff=False):
            """
            :doc: gallery method
            
            This is the action to advance to the next unlocked image.
            When the last image is showing, close it.

            `diff`
                If True, advance to the next image in the button, otherwise
                advance to the image in the next button.
            """
            if diff:
                return self.diff_next
            else:
                return self.next

        def previous(self):
            return "previous"

        def Previous(self):
            """
            :doc: gallery method
            
            This is the action to return to the previous unlocked image.
            When the first image is showing, close it.
            """
            return self.previous

        def ToggleSlideshow(self):
            """
            :doc: gallery method
            
            This is the action to toggle slideshow.
            
            """
            return __GalleryToggleSlideShow(self)
        
        def SlideShow(self, time=10):
            """
            :doc: gallery method
            
            This is the action to be set to timer for slideshow.
            
            `time`
                This is a number in second, defaults to 10. advance to the next unlocked image
                when this time is elapsed if slideshow is enable.
            """
            return __GallerySlideShow(self, time)

    class __GalleryToggleSlideShow(Action):

        def __init__(self, gallery):
            self.gallery = gallery
            self.selected = self.get_selected()

        def __call__(self):
            if self.gallery.slideshow:
                self.gallery.slideshow = False
            else:
                self.gallery.slideshow = True
                self.gallery.start_time = renpy.display.core.get_time()

        def get_selected(self):
            return self.gallery.slideshow

        def periodic(self, st):
            if self.selected != self.get_selected():
                renpy.restart_interaction()

    class __GallerySlideShow(Action):
            
        def __init__(self, gallery, time):
            self.gallery = gallery
            self.time = time
            if self.gallery.slideshow:
                self.gallery.start_time = renpy.display.core.get_time()

        def __call__(self):
            if self.gallery.start_time is not None:
                if renpy.display.core.get_time() > self.gallery.start_time + self.time and self.gallery.slideshow:
                    return self.gallery.diff_next()


init -1500:

    # Displays a set of images in the gallery, or indicates that the images
    # are locked. This is given the following arguments:
    #
    # locked
    #     True if the image is locked.
    # displayables
    #     A list of transformed displayables that should be shown to the user.
    # index
    #     A 1-based index of the image being shown.
    # count
    #     The number of images attached to the current button.
    # gallery
    #     The image gallery object.
    #
    # And if you use slideshow, set timer gallery.SlideShow().

    screen _gallery:
        key "game_menu" action gallery.Close()
        timer .1 repeat True action gallery.SlideShow()

        if locked:
            add "#000"
            text "Image [index] of [count] locked." align (0.5, 0.5)
        else:
            for d in displayables:
                add d

        hbox:
            style_group "gallery"
            align (.98, .98)

            textbutton _("prev") action gallery.Previous()
            textbutton _("next") action gallery.Next()
            textbutton _("slide show") action gallery.ToggleSlideshow()
            textbutton _("close") action gallery.Close()

    python:
        style.gallery = Style(style.default)
        style.gallery_button.background = None
        style.gallery_button_text.color = "#7779"
        style.gallery_button_text.hover_color = "#999"
        style.gallery_button_text.selected_color = "fff6"
        style.gallery_button_text.outlines = [(1, "#0006", 0, 0)]
