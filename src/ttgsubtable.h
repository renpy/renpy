#ifndef TTGSUBTable_H
#define TTGSUBTable_H

#include <stdint.h>
#include <ft2build.h>
#include FT_OPENTYPE_VALIDATE_H

typedef struct
{
    uint32_t Version;
    uint16_t ScriptList;
    uint16_t FeatureList;
    uint16_t LookupList;
} tt_gsub_header;

typedef struct
{
    uint16_t LookupOrder;
    uint16_t ReqFeatureIndex;
    uint16_t FeatureCount;
    uint16_t *FeatureIndex;
} TLangSys;

typedef struct
{
    uint32_t LangSysTag;
    TLangSys LangSys;
} TLangSysRecord;

typedef struct
{
    uint16_t DefaultLangSys;
    uint16_t LangSysCount;
    TLangSysRecord *LangSysRecord;
} TScript;

typedef struct
{
    uint32_t ScriptTag;
    TScript Script;
} TScriptRecord;

typedef struct
{
    uint16_t ScriptCount;
    TScriptRecord *ScriptRecord;
} TScriptList;

typedef struct
{
    uint16_t FeatureParams;
    int LookupCount;
    uint16_t *LookupListIndex;
} TFeature;

typedef struct
{
    uint32_t FeatureTag;
    TFeature Feature;
} TFeatureRecord;

typedef struct
{
    int FeatureCount;
    TFeatureRecord *FeatureRecord;
} TFeatureList;

typedef struct
{
    uint16_t Start;
    uint16_t End;
    uint16_t StartCoverageIndex;
} TRangeRecord;

typedef struct
{
    uint16_t CoverageFormat;
    uint16_t GlyphCount;
    uint16_t *GlyphArray;
    uint16_t RangeCount;
    TRangeRecord *RangeRecord;
} TCoverageFormat;

typedef struct
{
    uint16_t SubstFormat;
    TCoverageFormat Coverage;
    int16_t DeltaGlyphID;
    uint16_t GlyphCount;
    uint16_t *Substitute;
} TSingleSubstFormat;

typedef struct
{
    uint16_t LookupType;
    uint16_t LookupFlag;
    uint16_t SubTableCount;
    TSingleSubstFormat *SubTable;
} TLookup;

typedef struct
{
    int LookupCount;
    TLookup *Lookup;
} TLookupList;

typedef struct
{
    int loaded;
    tt_gsub_header header;
    TScriptList ScriptList;
    TFeatureList FeatureList;
    TLookupList LookupList;
} TTGSUBTable;

void LoadGSUBTable(TTGSUBTable *table, FT_Face face);
int LoadGSUBTable2(TTGSUBTable *table, FT_Bytes gsub);
int GetVerticalGlyph(TTGSUBTable *table, uint32_t glyphnum, uint32_t *vglyphnum);

int Parse(TTGSUBTable *table, FT_Bytes scriptlist, FT_Bytes featurelist, FT_Bytes lookuplist);
void ParseScriptList(TTGSUBTable *table, FT_Bytes raw, TScriptList *rec);
void ParseScript(TTGSUBTable *table, FT_Bytes raw, TScript *rec);
void ParseLangSys(TTGSUBTable *table, FT_Bytes raw, TLangSys *rec);

void ParseFeatureList(TTGSUBTable *table, FT_Bytes raw, TFeatureList *rec);
void ParseFeature(TTGSUBTable *table, FT_Bytes raw, TFeature *rec);

void ParseLookupList(TTGSUBTable *table, FT_Bytes raw, TLookupList *rec);
void ParseLookup(TTGSUBTable *table, FT_Bytes raw, TLookup *rec);

void ParseCoverage(TTGSUBTable *table, FT_Bytes raw, TCoverageFormat *rec);
void ParseCoverageFormat1(TTGSUBTable *table, FT_Bytes raw, TCoverageFormat *rec);
void ParseCoverageFormat2(TTGSUBTable *table, FT_Bytes raw, TCoverageFormat *rec);

void ParseSingleSubst(TTGSUBTable *table, FT_Bytes raw, TSingleSubstFormat *rec);
void ParseSingleSubstFormat1(TTGSUBTable *table, FT_Bytes raw, TSingleSubstFormat *rec);
void ParseSingleSubstFormat2(TTGSUBTable *table, FT_Bytes raw, TSingleSubstFormat *rec);

int GetVerticalGlyphSub(TTGSUBTable *table, uint32_t glyphnum, uint32_t *vglyphnum, TFeature *Feature);
int GetVerticalGlyphSub2(TTGSUBTable *table, uint32_t glyphnum, uint32_t *vglyphnum, TLookup *Lookup);

int GetCoverageIndex(TTGSUBTable *table, TCoverageFormat *Coverage, uint32_t g);

void init_gsubtable(TTGSUBTable *table);
void free_gsubtable(TTGSUBTable *table);
#endif
