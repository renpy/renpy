#include <ft2build.h>
#include FT_CONFIG_CONFIG_H
#include FT_TYPES_H
#include FT_FREETYPE_H
#include FT_IMAGE_H
#include FT_GLYPH_H
#include FT_OUTLINE_H
#include FT_BITMAP_H
#include FT_STROKER_H
#include FT_MULTIPLE_MASTERS_H

#define FT_FLOOR(X)     ((X & -64) >> 6)
#define FT_CEIL(X)      (((X + 63) & -64) >> 6)
#define FT_ROUND(X)      (((X + 32) & -64) >> 6)
