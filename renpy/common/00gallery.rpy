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

            renpy.show_screen("_gallery", locked=locked, index=index + 1, count=count, displayables=displayables, gallery=self.gallery)

            return ui.interact()


    class __GalleryButton(object):
        def __init__(self, gallery, index):
            self.gallery = gallery
            self.images = [ ]
            self.conditions = [ ]
            self.index = index

        def check_unlock(self):
            for i in self.conditions:
                if not i.check(True):
                    return False

            for i in self.images:
                if i.check_unlock(False):
                    return True

            return False


    class __GalleryToggleSlideshow(Action):

        def __init__(self, gallery):
            self.gallery = gallery

        def __call__(self):
            self.gallery.slideshow = not self.gallery.slideshow
            renpy.restart_interaction()

        def get_selected(self):
            return self.gallery.slideshow


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

        .. attribute:: navigation

            If true, the gallery will display navigation and slideshow
            buttons on top of the images.

        .. attribute:: span_buttons

            If true, the gallery will advance between buttons.

        .. attribute:: locked

            If true, the gallery will advance through locked images.

        .. attribute:: slideshow_delay

            The time it will take for the gallery to advance between images
            in slideshow mode.
        """

        transition = None

        hover_border = None
        idle_border = None

        locked_button = None

        def __init__(self):

            # A map from button name (or image) to __GalleryButton object.
            self.buttons = { }

            # A list of buttons.
            self.button_list = [ ]

            self.button_ = None
            self.image_ = None

            self.unlockable = None

            self.navigation = False
            self.span_buttons = False
            self.locked = True

            self.slideshow_delay = 5

        def button(self, name):
            """
            :doc: gallery method

            Creates a new button, named `name`.

            `name`
                The name of the button being created.
            """

            button = __GalleryButton(self, len(self.button_list))

            self.unlockable = button
            self.buttons[name] = button
            self.button_list.append(button)
            self.button_ = button

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
                return ui.invokesinnewcontext(self.show, b.index)
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

        def show(self, button=0, image=0):
            """
            Starts showing gallery images.

            `button`
                The index of the button to start showing.
            """

            # A list of (button, image) index pairs for all of the images we know
            # about.
            all_images = [ ]

            # A list of (button, image) index pairs for all of the unlocked
            # images.
            unlocked_images = [ ]

            for bi, b in enumerate(self.button_list):

                all_unlocked = True

                for ii, i in enumerate(b.images):

                    all_images.append((bi, ii))

                    unlocked = i.check_unlock(all_unlocked)

                    if unlocked:
                        unlocked_images.append((bi, ii))
                    else:
                        all_unlocked = False

            self.slideshow = False

            # Loop, displaying the images.
            while True:

                b = self.button_list[button]
                i = b.images[image]

                result = i.show((button, image) not in all_images, image, len(b.images))

                # Default action for click.

                if result is True:
                    result = "next"

                if result == 'return':
                    break

                # At this point, result is either 'next', "next_unlocked", "previous", or "previous_unlocked"
                # Go through the common advance code.

                if self.locked and result.endswith("_unlocked"):
                    images = all_images
                else:
                    images = unlocked_images

                index = images.index((button, image))

                if result.startswith('previous'):
                    index -= 1
                else:
                    index += 1

                if index < 0 or index >= len(images):
                    break

                new_button, new_image = images[index]

                if not self.span_buttons:
                    if new_button != button:
                        break

                button = new_button
                image = new_image

            renpy.transition(self.transition)

        def Return(self):
            """
            :doc: gallery method

            Stops displaying gallery images.
            """

            return ui.returns("return")

        def Next(self, unlocked=False):
            """
            :doc: gallery method

            Advances to the next image in the gallery.

            `unlocked`
                If true, only considers unlocked images.
            """

            if unlocked:
                return ui.returns("next_unlocked")
            else:
                return ui.returns("next")

        def Previous(self, unlocked=False):
            """
            :doc: gallery method

            Goes to the previous image in the gallery.

            `unlocked`
                If true, only considers unlocked images.
            """

            if unlocked:
                return ui.returns("previous_unlocked")
            else:
                return ui.returns("previous")

        def ToggleSlideshow(self):
            """
            :doc: gallery method

            Toggles slideshow mode.
            """
            return __GalleryToggleSlideshow(self)

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
    screen _gallery:

        if locked:
            add "#000"
            text _("Image [index] of [count] locked.") align (0.5, 0.5)
        else:
            for d in displayables:
                add d

        if gallery.slideshow:
            timer gallery.slideshow_delay action Return("next")

        key "game_menu" action gallery.Return()

        if gallery.navigation:

            hbox:
                spacing 20

                style_group "gallery"
                align (.98, .98)

                textbutton _("prev") action gallery.Previous()
                textbutton _("next") action gallery.Next()
                textbutton _("slideshow") action gallery.ToggleSlideshow()
                textbutton _("return") action gallery.Return()

    python:
        style.gallery = Style(style.default)
        style.gallery_button.background = None
        style.gallery_button_text.color = "#666"
        style.gallery_button_text.hover_color = "#fff"
        style.gallery_button_text.selected_color = "#fff"
        style.gallery_button_text.size = 16
