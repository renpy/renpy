# This extra implements an image gallery, complete with automatic
# unlocking of the images that have been shown to the user. The images
# are divided into pages, with a fixed number of images on each page.

# Right now, this is configured to used the images found in the demo.
# The images are repeated quite a bit, so that we can get four pages
# of them. You probably wouldn't do that if you were using this in a
# real game.

# To see this in action, drop it into the game directory of the
# demo.

# Configuration.
init:

    python hide:


        # The number of columns and rows of images to show in the
        # gallery.
        store.gallery_cols = 3
        store.gallery_rows = 4

        # The size that each image should be scaled to, and that
        # thumbnails should be.
        store.gallery_width = 160
        store.gallery_height = 120

        # The contents of each of the page. Each of these is a list of
        # tuples with the first element of the tuple being the image
        # filename and the second element being the name of the image
        # that will unlock the image with this filename. (That is,
        # the name that is used in show or scene statements, as a
        # string.)
        #
        # When displaying an image as a thumbnail, this code first
        # looks for the file thumbnail_<filename>. If that file
        # exists, it should be a gallery_width x gallery_height
        # thumbnail. Otherwise, a thumbnail is automatically
        # generated, but it may screw up the aspect ratio of the
        # image.
        #
        # You probably want to create thumbnails for most images, to
        # limit memory consumption.
        page1 = [
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ]

        page2 = [
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ( "carillon.jpg", "carillon" ),
            ]

        page3 = [
            ( "whitehouse.jpg", "whitehouse" ),
            ( "washington.jpg", "washington" ),
            ]        

        page4 = [
            ( "9a_happy.png", "eileen happy" ),
            ( "9a_vhappy.png", "eileen vhappy" ),
            ( "9a_concerned.png", "eileen concerned" ),
            ]

        # This is the actual list of gallery pages. It's a list
        # of tuples, with the first element being the name of the
        # page, the second being the contents of the page (one of
        # the lists created above), and the third image being the
        # image used as the background of the page.
        store.gallery_pages = [
            ("Backgrounds 1", page1, "washington.jpg"),
            ("Backgrounds 2", page2, "whitehouse.jpg"),
            ("Backgrounds 3", page3, "carillon.jpg"),
            ("Character Art", page4, "washington.jpg"),
            ]

        # A window containing the gallery page buttons.
        style.create('gallery_pages', 'default')
        style.gallery_pages.xpos = 0.99
        style.gallery_pages.xanchor='right'
        style.gallery_pages.ypos = 0.02
        style.gallery_pages.yanchor = 'top'

        # A button that links to a gallery page.
        style.create('gallery_page_button', 'button')
        style.create('gallery_page_button_text', 'button_text')

        # A button that returns us to from whence we came.
        style.create('gallery_return_button', 'button')
        style.create('gallery_return_button_text', 'button_text')

        style.gallery_return_button.xpos = 0.99
        style.gallery_return_button.xanchor='right'
        style.gallery_return_button.ypos = 0.98
        style.gallery_return_button.yanchor = 'bottom'


        # The grid containing the gallery image buttons.
        style.create('gallery_grid', 'default')

        # The style of the buttons in the gallery.
        style.create('gallery_button', 'default')

        # Right now, the backgrounds are all solids, but in a more
        # professional version, the insensitive background would
        # probably be a placeholder image that indicates that a
        # picture has yet to be unlocked.        
        style.gallery_button.insensitive_background = Solid((192, 192, 192, 255))
        style.gallery_button.idle_background = Solid((255, 255, 255, 255))
        style.gallery_button.hover_background = Solid((255, 255, 192, 255))

        style.gallery_button.left_margin = 5
        style.gallery_button.right_margin = 5
        style.gallery_button.top_margin = 5
        style.gallery_button.bottom_margin = 5

        style.gallery_button.left_padding = 5
        style.gallery_button.right_padding = 5
        style.gallery_button.top_padding = 5
        style.gallery_button.bottom_padding = 5

        # The style of the images in the buttons in the gallery.
        style.create('gallery_button_image', 'default')

        # The style of the images that are being shown to the user.
        style.create('gallery_image', 'image_placement')

        # The transition used when switching gallery pages.
        store.gallery_transition = Dissolve(0.5)
              
    python:

        # The function that actually manages the display of the image
        # gallery.
        def gallery():

            page = 0

            while True:

                images = gallery_pages[page][1]
                ui.image(gallery_pages[page][2])

                # Show the names of the various gallery pages.

                ui.window(style='gallery_pages')
                ui.vbox(focus="gallery_pages")

                for i in range(0, len(gallery_pages)):
                    if i == page:
                        clicked = None
                    else:
                        clicked = ui.returns(("page", i))

                    ui.textbutton(gallery_pages[i][0],
                              style='gallery_page_button',
                              text_style='gallery_page_button_text',
                              clicked=clicked)
                ui.close()

                # Show the return button.
                ui.textbutton('Return',
                              style='gallery_return_button',
                              text_style='gallery_return_button_text',
                              clicked=ui.returns(("return", None)))

                # Show the grid for this page.
                ui.grid(gallery_cols, gallery_rows, style='gallery_grid')

                # For each grid cell.
                for i in range(0, gallery_cols * gallery_rows):

                    # Fill empty space with nulls.
                    if i >= len(images):
                        ui.null()
                        continue

                    # Otherwise, get the filename and spec and see if
                    # we've unlocked it.
                    filename, spec = images[i]

                    if spec:
                        spec = spec.split()
                        
                    if spec and tuple(spec) not in persistent._seen_images:
                        filename = None
                        clicked = None
                    else:
                        clicked = ui.returns(('show', filename))

                    # Create the button, containing the appropriate
                    # image or a null if we haven't unlocked it yet.
                    
                    ui.button(style='gallery_button', clicked=clicked)

                    if not filename:
                        ui.null(width=gallery_width, height=gallery_height)
                    else:
                        
                        if renpy.loadable("thumbnail_" + filename):
                            ui.image("thumbnail_" + filename,
                                     style="gallery_button_image")
                        else:
                            ui.add(im.Scale(filename,
                                            gallery_width,
                                            gallery_height))
                            
                ui.close()

                # Interact with the user.
                renpy.transition(gallery_transition)
                cmd, arg = ui.interact(suppress_overlay=True, suppress_underlay=True)

                # Process the user's commands.
                if cmd == "show":
                    ui.add(Solid((0, 0, 0, 255)))
                    ui.image(arg)
                    ui.saybehavior()
                    renpy.transition(gallery_transition)
                    ui.interact(suppress_overlay=True, suppress_underlay=True)

                if cmd == "page":
                    page = arg

                if cmd == "return":
                    renpy.transition(gallery_transition)
                    return


        library.main_menu.insert(2, ("CG Gallery", ui.jumps("gallery")))


label gallery:

    $ gallery()

    jump _main_menu
                    
                    
                    
                
