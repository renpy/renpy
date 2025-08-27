from sdl2 cimport *

# Acquire the GIL for callbacks.
cdef extern from "SDL_mixer.h":
    void Mix_ChannelFinished(void (*channel_finished)(int channel))
    void Mix_HookMusicFinished(void (*music_finished)())
    void Mix_SetPostMix(void (*mix_func)(void *udata, Uint8 *stream, int len), void *arg)
    void Mix_HookMusic(void (*mix_func)(void *udata, Uint8 *stream, int len), void *arg)

cdef extern from "SDL_mixer.h" nogil:
    cdef enum:
        SDL_MIXER_MAJOR_VERSION
        SDL_MIXER_MINOR_VERSION
        SDL_MIXER_PATCHLEVEL

    const SDL_version * Mix_Linked_Version()

    ctypedef enum MIX_InitFlags:
        MIX_INIT_FLAC
        MIX_INIT_MP3
        MIX_INIT_OGG

    int Mix_Init(int flags)
    void Mix_Quit()

    cdef enum:
        MIX_CHANNELS
        MIX_DEFAULT_FREQUENCY
        MIX_DEFAULT_FORMAT
        MIX_DEFAULT_CHANNELS
        MIX_MAX_VOLUME

    ctypedef struct Mix_Chunk:
        int allocated
        Uint8 *abuf
        Uint32 alen
        Uint8 volume

    ctypedef enum Mix_Fading:
        MIX_NO_FADING
        MIX_FADING_OUT
        MIX_FADING_IN

    ctypedef enum Mix_MusicType:
        MUS_NONE
        MUS_CMD
        MUS_WAV
        MUS_MOD
        MUS_MID
        MUS_OGG
        MUS_MP3
        MUS_MP3_MAD
        MUS_FLAC
        MUS_MODPLUG

    ctypedef struct _Mix_Music
    ctypedef _Mix_Music Mix_Music

    int Mix_OpenAudio(int frequency, Uint16 format, int channels, int chunksize)
    int Mix_AllocateChannels(int numchans)
    int Mix_QuerySpec(int *frequency,Uint16 *format,int *channels)
    Mix_Chunk * Mix_LoadWAV_RW(SDL_RWops *src, int freesrc)
    Mix_Music * Mix_LoadMUS(const char *file)
    Mix_Music * Mix_LoadMUS_RW(SDL_RWops *src, int freesrc)
    Mix_Music * Mix_LoadMUSType_RW(SDL_RWops *src, Mix_MusicType type, int freesrc)
    Mix_Chunk * Mix_QuickLoad_WAV(Uint8 *mem)
    Mix_Chunk * Mix_QuickLoad_RAW(Uint8 *mem, Uint32 len)
    void Mix_FreeChunk(Mix_Chunk *chunk)
    void Mix_FreeMusic(Mix_Music *music)

    int Mix_GetNumChunkDecoders()
    const char * Mix_GetChunkDecoder(int index)
    int Mix_GetNumMusicDecoders()
    const char * Mix_GetMusicDecoder(int index)
    Mix_MusicType Mix_GetMusicType(const Mix_Music *music)
    void * Mix_GetMusicHookData()

    cdef enum:
        MIX_CHANNEL_POST

    ctypedef void (*Mix_EffectFunc_t)(int chan, void *stream, int len, void *udata)
    ctypedef void (*Mix_EffectDone_t)(int chan, void *udata)

    int Mix_RegisterEffect(int chan, Mix_EffectFunc_t f, Mix_EffectDone_t d, void *arg)
    int Mix_UnregisterEffect(int channel, Mix_EffectFunc_t f)
    int Mix_UnregisterAllEffects(int channel)

    cdef enum:
        MIX_EFFECTSMAXSPEED

    int Mix_SetPanning(int channel, Uint8 left, Uint8 right)
    int Mix_SetPosition(int channel, Sint16 angle, Uint8 distance)
    int Mix_SetDistance(int channel, Uint8 distance)
    int Mix_SetReverseStereo(int channel, int flip)

    int Mix_ReserveChannels(int num)
    int Mix_GroupChannel(int which, int tag)
    int Mix_GroupChannels(int from_, int to, int tag)
    int Mix_GroupAvailable(int tag)
    int Mix_GroupCount(int tag)
    int Mix_GroupOldest(int tag)
    int Mix_GroupNewer(int tag)

    int Mix_PlayChannelTimed(int channel, Mix_Chunk *chunk, int loops, int ticks)
    int Mix_PlayMusic(Mix_Music *music, int loops)

    int Mix_FadeInMusic(Mix_Music *music, int loops, int ms)
    int Mix_FadeInMusicPos(Mix_Music *music, int loops, int ms, double position)
    int Mix_FadeInChannelTimed(int channel, Mix_Chunk *chunk, int loops, int ms, int ticks)

    int Mix_Volume(int channel, int volume)
    int Mix_VolumeChunk(Mix_Chunk *chunk, int volume)
    int Mix_VolumeMusic(int volume)

    int Mix_HaltChannel(int channel)
    int Mix_HaltGroup(int tag)
    int Mix_HaltMusic()

    int Mix_ExpireChannel(int channel, int ticks)

    int Mix_FadeOutChannel(int which, int ms)
    int Mix_FadeOutGroup(int tag, int ms)
    int Mix_FadeOutMusic(int ms)

    Mix_Fading Mix_FadingMusic()
    Mix_Fading Mix_FadingChannel(int which)

    void Mix_Pause(int channel)
    void Mix_Resume(int channel)
    int Mix_Paused(int channel)

    void Mix_PauseMusic()
    void Mix_ResumeMusic()
    void Mix_RewindMusic()
    int Mix_PausedMusic()

    int Mix_SetMusicPosition(double position)

    int Mix_Playing(int channel)
    int Mix_PlayingMusic()

    int Mix_SetMusicCMD(const char *command)

    int Mix_SetSynchroValue(int value)
    int Mix_GetSynchroValue()

    int Mix_SetSoundFonts(const char *paths)
    const char* Mix_GetSoundFonts()
    int Mix_EachSoundFont(int (*function)(const char*, void*), void *data)

    Mix_Chunk * Mix_GetChunk(int channel)

    void Mix_CloseAudio()
