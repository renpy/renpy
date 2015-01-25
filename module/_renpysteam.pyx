cdef extern from "steam/steam_api.h":
    ctypedef bint bool

    # Init.

    bool SteamAPI_Init()
    void SteamAPI_RunCallbacks()
    bool SteamAPI_RestartAppIfNecessary(unsigned int)

    # Stats & Achievements.

    cdef cppclass ISteamUserStats:
        bool RequestCurrentStats()
        bool StoreStats()

        bool GetAchievement(const char *pchName, bool *pbAchieved);
        bool SetAchievement(const char *pchName);
        bool ClearAchievement(const char *pchName);

        int GetNumAchievements()
        char *GetAchievementName(int)

        bool GetStat(const char *pchName, float *pData)
        bool SetStat(const char *pchName, float fData)

    ctypedef struct UserStatsReceived_t
    ISteamUserStats *SteamUserStats()

    # Utils.

    cdef cppclass ISteamUtils:
        bint IsOverlayEnabled()

    ISteamUtils *SteamUtils()




cdef extern from "steamcallbacks.h":
    cdef cppclass SteamCallback[T]:
        SteamCallback(void (*)(T *))

import renpy

################################################################# Initialization

# Have we been initialized?
initialized = None

# Called periodically to run callbacks.
def periodic():
    SteamAPI_RunCallbacks()

# Initialize the Steam API.
def init():
    """
    :doc: steam

    Initializes the Steam API. Returns true for success, false for failure.
    If a failure has occurred, no other steam functions should be called.

    This may be called multiple times, but only attempts initialization the
    first time it's been called.
    """

    global initialized

    if initialized is None:
        initialized = SteamAPI_Init()

        if initialized:
            renpy.config.periodic_callbacks.append(periodic)

    return initialized


######################################################### Stats and Achievements

# A callable that is called when the stats are available.
got_stats = None

cdef void call_got_stats(UserStatsReceived_t *s):
    if got_stats is not None:
        got_stats()

cdef SteamCallback[UserStatsReceived_t] *stats_received_callback = \
    new SteamCallback[UserStatsReceived_t](call_got_stats)

def retrieve_stats(callback):
    """
    :doc: steam_stats

    Retrieves achievements and statistics from Steam. `callback` will be
    called with no parameters if and when the statistics become available.
    """

    global got_stats
    got_stats = callback

    print SteamUserStats().RequestCurrentStats()

def store_stats():
    """
    :doc: steam_stats

    Stores statistics and achievements on the Steam server.
    """

    SteamUserStats().StoreStats()

def list_achievements():
    """
    :doc: steam_stats

    Returns a list of achievement names.
    """

    rv = [ ]

    cdef int na = SteamUserStats().GetNumAchievements()
    cdef char *s
    cdef int i

    for 0 <= i < na:
        s = <char *> SteamUserStats().GetAchievementName(i)
        rv.append(s)

    return rv

def get_achievement(name):
    """
    :doc: steam_stats

    Gets the state of the achievements with `name`. This returns True if the
    achievement has been granted, False if it hasn't, and None if the achievement
    is unknown or an error occurs.
    """

    cdef bool rv

    if not SteamUserStats().GetAchievement(name, &rv):
        return None

    return rv

def grant_achievement(name):
    """
    :doc: steam_stats

    Grants the achievement with `name`. Call :func:`_renpysteam.store_stats` to
    push this change to the server.
    """

    return SteamUserStats().SetAchievement(name)

def clear_achievement(name):
    """
    :doc: steam_stats

    Clears the achievement with `name`. Call :func:`_renpysteam.store_stats` to
    push this change to the server.
    """

    return SteamUserStats().ClearAchievement(name)

def get_stat(name):
    """
    :doc: steam_stats

    Returns the value of the stat with `name`, or None if no such stat
    exits.
    """

    cdef float rv

    if not SteamUserStats().GetStat(name, &rv):
        return None

    return rv

def set_stat(name, value):
    """
    :doc: steam_stats

    Sets the value of the stat with `name`, which must have the type of
    FLOAT. Call :func:`_renpysteam.store_stats` to push this change to the
    server.
    """

    return SteamUserStats().SetStat(name, <float> value)
