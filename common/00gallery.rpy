# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1135 python:

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
            ui.interact()

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

            for i, img in enumerate(self.images):
                locked = not img.check_unlock(all_prior)
                img.show(locked, i, len(self.images))

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

            self.button_ = None
            self.image_ = None
            self.unlockable = None
            
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
                return ui.invokesinnewcontext(b.show)
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
                A displayable that is used to overlay this button when when 
                it is unlocked and has focus. If None, the hover_border
                field of the gallery object is used. 
 
            `idle_border`
                A displayable that is used to overlay this button when when 
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


init -1135:

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
            text "Image [index] of [count] locked." align (0.5, 0.5)          
        else:
            for d in displayables:
                add d
                        
