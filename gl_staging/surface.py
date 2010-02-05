class Texture(object):
    """
    This object stores information about an OpenGL texture.
    """

    def __init__(self):

        # The number of the OpenGL texture this texture object
        # represents.
        self.texture

        # These are used to map an index into texture coordinates.
        self.xmul
        self.xadd
        self.ymul
        self.yadd

        # The width and height of the texture, in pixels. Note that
        # this is the amount of usable data, and that the texture
        # includes a 1 pixel border on each side. So this will be
        # 2 pixels smaller than the actual texture size.
        self.width
        self.height

        # A reference count giving the number of TextureGrids that
        # refer to this texture. When this falls to 0, the texture
        # can be deallocated.
        self.reference_count = 0


class TextureGrid(object):
    """
    This represents one or more textures that cover a rectangular
    area.   
    """

    def __init__(self):

        # The width and height of this TextureGrid
        self.width
        self.height

        # For each row of tiles, a tuple giving:
        # - The y offset within the texture.
        # - The height of the row.
        self.rows

        # For each column of tiles, a tuple giving.
        # - The x offset within the texture.
        # - The width of the column.
        self.columns

        # The actual grid of texture titles, a list of lists of
        # textures. The outer list represents the rows, the inner
        # lists columns.
        self.tiles

        
    
    
        
        
        
