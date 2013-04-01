/*
Copyright 2012 Koichi Akabe <vbkaisetsu@gmail.com>

The original C++ source is distributed under the PD-like license.
For more details, see:
     http://higambana.ashigaru.jp/

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <stdlib.h>
#include "ttgsubtable.h"

uint8_t GetUInt8(FT_Bytes *p)
{
    uint8_t ret = (*p)[0];
    *p += 1;
    return ret;
}

int16_t GetInt16(FT_Bytes *p)
{
    uint16_t ret = (*p)[0] << 8 | (*p)[1];
    *p += 2;
    return *(int16_t*)&ret;
}

uint16_t GetUInt16(FT_Bytes *p)
{
    uint16_t ret = (*p)[0] << 8 | (*p)[1];
    *p += 2;
    return ret;
}

int32_t GetInt32(FT_Bytes *p)
{
    uint32_t ret = (*p)[0] << 24 | (*p)[1] << 16 | (*p)[2] << 8 | (*p)[3];
    *p += 4;
    return *(int32_t*)&ret;
}

uint32_t GetUInt32(FT_Bytes *p)
{
    uint32_t ret = (*p)[0] << 24 | (*p)[1] << 16 | (*p)[2] << 8 | (*p)[3];
    *p += 4;
    return ret;
}

void init_gsubtable(TTGSUBTable *table)
{
    table->loaded = 0;
    table->ScriptList.ScriptCount = 0;
    table->ScriptList.ScriptRecord = NULL;
    table->FeatureList.FeatureCount = 0;
    table->FeatureList.FeatureRecord = NULL;
    table->LookupList.LookupCount = 0;
    table->LookupList.Lookup = NULL;
}

void free_gsubtable(TTGSUBTable *table)
{
    if(table->loaded == 0)
    {
        return;
    }
    int i, j;
    int scr_cnt = table->ScriptList.ScriptCount;
    TScriptRecord *scr_rcd = table->ScriptList.ScriptRecord;
    for(i = 0; i < scr_cnt; i++)
    {
        int ls_cnt = scr_rcd[i].Script.LangSysCount;
        TLangSysRecord *ls_rcd = scr_rcd[i].Script.LangSysRecord;
        for(j = 0; j < ls_cnt; j++)
        {
            free(ls_rcd[j].LangSys.FeatureIndex);
        }
        free(ls_rcd);
    }
    free(scr_rcd);
    int ftr_cnt = table->FeatureList.FeatureCount;
    TFeatureRecord *ftr_rcd = table->FeatureList.FeatureRecord;
    for(i = 0; i < ftr_cnt; i++)
    {
        free(ftr_rcd[i].Feature.LookupListIndex);
    }
    free(ftr_rcd);
    int lup_cnt = table->LookupList.LookupCount;
    TLookup *lup = table->LookupList.Lookup;
    for(i = 0; i < lup_cnt; i++)
    {
        int ls_cnt = lup[i].SubTableCount;
        TSingleSubstFormat *subt = lup[i].SubTable;
        for(j = 0; j < ls_cnt; j++)
        {
            if(subt[j].Coverage.CoverageFormat == 1) {
                free(subt[j].Coverage.GlyphArray);
            } else if(subt[j].Coverage.CoverageFormat == 2) {
            	free(subt[j].Coverage.RangeRecord);
            }
            if(subt[j].SubstFormat == 2)
                free(subt[j].Substitute);
        }
        free(subt);
    }
    free(lup);
}
    
int LoadGSUBTable2(TTGSUBTable *table, FT_Bytes gsub)
{
    table->header.Version = gsub[0] << 24 | gsub[1] << 16 | gsub[2] << 8 | gsub[3];
    if(table->header.Version != 0x00010000)
    {
        return -1;
    }
    table->header.ScriptList  = gsub[4] << 8 | gsub[5];
    table->header.FeatureList = gsub[6] << 8 | gsub[7];
    table->header.LookupList  = gsub[8] << 8 | gsub[9];
    return Parse(table, &gsub[table->header.ScriptList], &gsub[table->header.FeatureList], &gsub[table->header.LookupList]);
}

int GetVerticalGlyph(TTGSUBTable *table, uint32_t glyphnum, uint32_t *vglyphnum)
{
    int i, j;
    uint32_t tag[] = {
        (uint8_t)'v' << 24 |
        (uint8_t)'r' << 16 |
        (uint8_t)'t' <<  8 |
        (uint8_t)'2',

        (uint8_t)'v' << 24 |
        (uint8_t)'e' << 16 |
        (uint8_t)'r' <<  8 |
        (uint8_t)'t',
    };
    if(!table->loaded)
    {
        return -1;
    }
    for(i = 0; i < 2; i++)
    {
        for(j = 0; j < table->FeatureList.FeatureCount; j++)
        {
            if(table->FeatureList.FeatureRecord[j].FeatureTag == tag[i])
            {
                if(GetVerticalGlyphSub(table, glyphnum, vglyphnum, &table->FeatureList.FeatureRecord[j].Feature) == 0)
                {
                    return 0;
                }
            }
        }
    }
    return -1;
}

int GetVerticalGlyphSub(TTGSUBTable *table, uint32_t glyphnum, uint32_t *vglyphnum, TFeature *Feature)
{
    int i, index;
    for(i = 0; i < Feature->LookupCount; i++)
    {
        index = Feature->LookupListIndex[i];
        if(index < 0 || table->LookupList.LookupCount < index)
        {
            continue;
        }
        if(table->LookupList.Lookup[index].LookupType == 1)
        {
            if(GetVerticalGlyphSub2(table, glyphnum, vglyphnum, &table->LookupList.Lookup[index]) == 0)
            {
                return 0;
            }
        }
    }
    return -1;
}

int GetVerticalGlyphSub2(TTGSUBTable *table, uint32_t glyphnum, uint32_t *vglyphnum, TLookup *Lookup)
{
    int i, index;
    TSingleSubstFormat *tbl;
    for(i = 0; i < Lookup->SubTableCount; i++)
    {
        switch(Lookup->SubTable[i].SubstFormat)
        {
        case 1:
            tbl = &Lookup->SubTable[i];
            if(GetCoverageIndex(table, &tbl->Coverage, glyphnum) >= 0)
            {
                *vglyphnum = glyphnum + tbl->DeltaGlyphID;
                return 0;
            }
            break;
        case 2:
            tbl = &Lookup->SubTable[i];
            index = GetCoverageIndex(table, &tbl->Coverage, glyphnum);
            if(0 <= index && index < tbl->GlyphCount)
            {
                *vglyphnum = tbl->Substitute[index];
                return 0;
            }
            break;
        }
    }
    return -1;
}

int GetCoverageIndex(TTGSUBTable *table, TCoverageFormat *Coverage, uint32_t g)
{
    int i;
    switch(Coverage->CoverageFormat)
    {
    case 1:
        for(i = 0; i < Coverage->GlyphCount; i++)
        {
            if((uint32_t)Coverage->GlyphArray[i] == g)
            {
                return i;
            }
        }
        return -1;
    case 2:
        for(i = 0; i < Coverage->RangeCount; i++)
        {
            uint32_t s = Coverage->RangeRecord[i].Start;
            uint32_t e = Coverage->RangeRecord[i].End;
            uint32_t si = Coverage->RangeRecord[i].StartCoverageIndex;
            if(si + s <= g && g <= si + e)
            {
                return si + g - s;
            }
        }
        return -1;
    }
    return -1;
}

int Parse(TTGSUBTable *table, FT_Bytes scriptlist, FT_Bytes featurelist, FT_Bytes lookuplist)
{
    ParseScriptList(table, scriptlist, &table->ScriptList);
    ParseFeatureList(table, featurelist, &table->FeatureList);
    ParseLookupList(table, lookuplist, &table->LookupList);
    return 0;
}

void ParseScriptList(TTGSUBTable *table, FT_Bytes raw, TScriptList *rec)
{
    int i;
    FT_Bytes sp = raw;
    rec->ScriptCount = GetUInt16(&sp);
    if(rec->ScriptCount <= 0)
    {
        rec->ScriptRecord = NULL;
        return;    
    }
    rec->ScriptRecord = calloc(rec->ScriptCount, sizeof(TScriptRecord));
    for(i = 0; i < rec->ScriptCount; i++)
    {
        rec->ScriptRecord[i].ScriptTag = GetUInt32(&sp);
        uint16_t offset = GetUInt16(&sp);
        ParseScript(table, &raw[offset], &rec->ScriptRecord[i].Script);
    }
}

void ParseScript(TTGSUBTable *table, FT_Bytes raw, TScript *rec)
{
    int i;
    FT_Bytes sp = raw;
    rec->DefaultLangSys = GetUInt16(&sp);
    rec->LangSysCount = GetUInt16(&sp);
    if(rec->LangSysCount <= 0)
    {
        rec->LangSysRecord = NULL;
        return;
    }
    rec->LangSysRecord = calloc(rec->LangSysCount, sizeof(TLangSysRecord));
    for(i = 0; i < rec->LangSysCount; i++)
    {
        rec->LangSysRecord[i].LangSysTag = GetUInt32(&sp);
        uint16_t offset = GetUInt16(&sp);
        ParseLangSys(table, &raw[offset], &rec->LangSysRecord[i].LangSys);
    }
}

void ParseLangSys(TTGSUBTable *table, FT_Bytes raw, TLangSys *rec)
{
    FT_Bytes sp = raw;
    rec->LookupOrder = GetUInt16(&sp);
    rec->ReqFeatureIndex = GetUInt16(&sp);
    rec->FeatureCount = GetUInt16(&sp);
    if(rec->FeatureCount <= 0)
        return;
    rec->FeatureIndex = calloc(rec->FeatureCount, sizeof(uint16_t));
}

void ParseFeatureList(TTGSUBTable *table, FT_Bytes raw, TFeatureList *rec)
{
    int i;
    FT_Bytes sp = raw;
    rec->FeatureCount = GetUInt16(&sp);
    if(rec->FeatureCount <= 0)
    {
        rec->FeatureRecord = NULL;
        return;
    }
    rec->FeatureRecord = calloc(rec->FeatureCount, sizeof(TFeatureRecord));
    for(i = 0; i < rec->FeatureCount; i++)
    {
        rec->FeatureRecord[i].FeatureTag = GetUInt32(&sp);
        uint16_t offset = GetUInt16(&sp);
        ParseFeature(table, &raw[offset], &rec->FeatureRecord[i].Feature);
    }
}

void ParseFeature(TTGSUBTable *table, FT_Bytes raw, TFeature *rec)
{
    int i;
    FT_Bytes sp = raw;
    rec->FeatureParams = GetUInt16(&sp);
    rec->LookupCount = GetUInt16(&sp);
    if(rec->LookupCount <= 0)
    {
        return;
    }
    rec->LookupListIndex = calloc(rec->LookupCount, sizeof(uint16_t));
    for(i = 0;i < rec->LookupCount; i++)
    {
        rec->LookupListIndex[i] = GetUInt16(&sp);
    }
}

void ParseLookupList(TTGSUBTable *table, FT_Bytes raw, TLookupList *rec)
{
    int i;
    FT_Bytes sp = raw;
    rec->LookupCount = GetUInt16(&sp);
    if(rec->LookupCount <= 0)
    {
        rec->Lookup = NULL;
        return;
    }
    rec->Lookup = calloc(rec->LookupCount, sizeof(TLookup));
    for(i = 0; i < rec->LookupCount; i++)
    {
        uint16_t offset = GetUInt16(&sp);
        ParseLookup(table, &raw[offset], &rec->Lookup[i]);
    }
}

void ParseLookup(TTGSUBTable *table, FT_Bytes raw, TLookup *rec)
{
    int i;
    FT_Bytes sp = raw;
    rec->LookupType = GetUInt16(&sp);
    rec->LookupFlag = GetUInt16(&sp);
    rec->SubTableCount = GetUInt16(&sp);
    if(rec->SubTableCount <= 0)
    {
        rec->SubTable = NULL;
        return;
    }
    rec->SubTable = calloc(rec->SubTableCount, sizeof(TSingleSubstFormat));
    if(rec->LookupType != 1)
        return;
    for(i = 0; i < rec->SubTableCount; i++)
    {
        uint16_t offset = GetUInt16(&sp);
        ParseSingleSubst(table, &raw[offset], &rec->SubTable[i]);
    }
}

void ParseCoverage(TTGSUBTable *table, FT_Bytes raw, TCoverageFormat *rec)
{
    FT_Bytes sp = raw;
    uint16_t Format = GetUInt16(&sp);
    switch(Format)
    {
    case 1:
        rec->CoverageFormat = 1;
        ParseCoverageFormat1(table, raw, rec);
        break;
    case 2:
        rec->CoverageFormat = 2;
        ParseCoverageFormat2(table, raw, rec);
        break;
    default:
        rec->CoverageFormat = 0;
    }
}

void ParseCoverageFormat1(TTGSUBTable *table, FT_Bytes raw, TCoverageFormat *rec)
{
    int i;
    FT_Bytes sp = raw;
    GetUInt16(&sp);
    rec->GlyphCount = GetUInt16(&sp);
    if(rec->GlyphCount <= 0)
    {
        rec->GlyphArray = NULL;
        return;
    }
    rec->GlyphArray = calloc(rec->GlyphCount, sizeof(uint16_t));
    for(i = 0; i < rec->GlyphCount; i++)
    {
        rec->GlyphArray[i] = GetUInt16(&sp);
    }
}

void ParseCoverageFormat2(TTGSUBTable *table, FT_Bytes raw, TCoverageFormat *rec)
{
    int i;
    FT_Bytes sp = raw;
    GetUInt16(&sp);
    rec->RangeCount = GetUInt16(&sp);
    if(rec->RangeCount <= 0)
    {
        rec->RangeRecord = NULL;
        return;
    }
    rec->RangeRecord = calloc(rec->RangeCount, sizeof(TRangeRecord));
    for(i = 0; i < rec->RangeCount; i++)
    {
        rec->RangeRecord[i].Start = GetUInt16(&sp);
        rec->RangeRecord[i].End = GetUInt16(&sp);
        rec->RangeRecord[i].StartCoverageIndex = GetUInt16(&sp);
    }
}

void ParseSingleSubst(TTGSUBTable *table, FT_Bytes raw, TSingleSubstFormat *rec)
{
    FT_Bytes sp = raw;
    uint16_t Format = GetUInt16(&sp);
    switch(Format)
    {
    case 1:
        rec->SubstFormat = 1;
        ParseSingleSubstFormat1(table, raw, rec);
        break;
    case 2:
        rec->SubstFormat = 2;
        ParseSingleSubstFormat2(table, raw, rec);
        break;
    default:
        rec->SubstFormat = 0;
    }
}

void ParseSingleSubstFormat1(TTGSUBTable *table, FT_Bytes raw, TSingleSubstFormat *rec)
{
    FT_Bytes sp = raw;
    GetUInt16(&sp);
    uint16_t offset = GetUInt16(&sp);
    ParseCoverage(table, &raw[offset], &rec->Coverage);
    rec->DeltaGlyphID = GetInt16(&sp);
}

void ParseSingleSubstFormat2(TTGSUBTable *table, FT_Bytes raw, TSingleSubstFormat *rec)
{
    int i;
    FT_Bytes sp = raw;
    GetUInt16(&sp);
    uint16_t offset = GetUInt16(&sp);
    ParseCoverage(table, &raw[offset], &rec->Coverage);
    rec->GlyphCount = GetUInt16(&sp);
    if(rec->GlyphCount <= 0)
    {
        rec->Substitute = NULL;
        return;
    }
    rec->Substitute = calloc(rec->GlyphCount, sizeof(uint16_t));
    for(i = 0; i < rec->GlyphCount; i++)
    {
        rec->Substitute[i] = GetUInt16(&sp);
    }
}

void LoadGSUBTable(TTGSUBTable *table, FT_Face face)
{
    FT_Bytes base = NULL;
    FT_Bytes gdef = NULL;
    FT_Bytes gpos = NULL;
    FT_Bytes gsub = NULL;
    FT_Bytes jstf = NULL;
    FT_OpenType_Validate(face, FT_VALIDATE_GSUB, &base, &gdef, &gpos, &gsub, &jstf);
    if(gsub == NULL)
    {
        table->loaded = 0;
        return;
    }
    int ret = LoadGSUBTable2(table, gsub);
    FT_OpenType_Free(face, gsub);
    if(ret != 0)
    {
        table->loaded = 0;
        return;
    }
    table->loaded = 1;
}
