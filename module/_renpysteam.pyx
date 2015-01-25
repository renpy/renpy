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

    cdef enum ENotificationPosition:
        k_EPositionTopLeft
        k_EPositionTopRight
        k_EPositionBottomLeft
        k_EPositionBottomRight

    cdef cppclass ISteamUtils:
        bint IsOverlayEnabled()
        void SetOverlayNotificationPosition(ENotificationPosition eNotificationPosition)

    ISteamUtils *SteamUtils()

    # Apps.

    ctypedef int AppId_t

    cdef cppclass ISteamApps:
        bool BIsSubscribedApp(AppId_t appID)
        const char *GetCurrentGameLanguage()
        bool GetCurrentBetaName( char *pchName, int cchNameBufferSize );

        bool BIsDlcInstalled(AppId_t nAppID)
        void InstallDLC(AppId_t nAppID)
        void UninstallDLC(AppId_t nAppID)

    ctypedef struct DlcInstalled_t:
        AppId_t m_nAppID

    ISteamApps *SteamApps()

    # Friends.

    cdef enum EOverlayToStoreFlag:
        k_EOverlayToStoreFlag_None
        k_EOverlayToStoreFlag_AddToCart
        k_EOverlayToStoreFlag_AddToCartAndShow

    cdef cppclass ISteamFriends:
        void ActivateGameOverlay(const char *pchDialog)
        void ActivateGameOverlayToWebPage(const char *pchURL)
        void ActivateGameOverlayToStore(AppId_t nAppID, EOverlayToStoreFlag eFlag)

    ISteamFriends *SteamFriends()


cdef extern from "steamcallbacks.h":
    cdef cppclass SteamCallback[T]:
        SteamCallback(void (*)(T *))

import renpy

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

########################################################################### Apps

def is_subscribed_app(appid):
    """
    :doc: steam_apps

    Returns true if the user owns the app with `appid`, and false otherwise.
    """

    return SteamApps().BIsSubscribedApp(appid)

def get_current_game_language():
    """
    :doc: steam_apps

    Return the name of the language the user has selected.
    """

    cdef const char *s = SteamApps().GetCurrentGameLanguage()
    return str(s)

def get_current_beta_name():
    """
    :doc: steam_apps

    Returns the name of the current beta, or None if it can't.
    """

    cdef char rv[256]

    if not SteamApps().GetCurrentBetaName(rv, 256):
        return None

    return str(rv)

def dlc_installed(appid):
    """
    :doc: steam_apps

    Returns True if `dlc` is installed, or False otherwise.
    """

    return SteamApps().BIsDlcInstalled(appid)

# A callable that is called when the stats are available.
got_dlc = None

cdef void call_got_dlc(DlcInstalled_t *s):
    if got_dlc is not None:
        got_dlc(s.m_nAppID)

cdef SteamCallback[DlcInstalled_t] *dlc_callback = \
    new SteamCallback[DlcInstalled_t](call_got_dlc)

def install_dlc(appid, callback):
    """
    :doc: steam_apps

    Requests the DLC with `appid` be installed. If not None, `callback`
    will be called with `appid` when the install finishes. Only one
    callback can be registered at a time.
    """

    global got_dlc
    got_dlc = callback

    SteamApps().InstallDLC(appid)

def uninstall_dlc(appid):
    """
    :doc: steam_apps

    Requests that the DLC with `appid` be uninstalled.
    """

    SteamApps().UninstallDLC(appid)

######################################################################## Overlay

def is_overlay_enabled():
    """
    :doc: steam_overlay

    Returns true if the steam overlay is enabled. (This might take a while to
    return true once the game starts.)
    """

    return SteamUtils().IsOverlayEnabled()

POSITION_TOP_LEFT = k_EPositionTopLeft
POSITION_TOP_RIGHT = k_EPositionTopRight
POSITION_BOTTOM_LEFT = k_EPositionBottomLeft
POSITION_BOTTOM_RIGHT = k_EPositionBottomRight

def set_overlay_notification_position(position):
    """
    :doc: steam_overlay

    Sets the position of the steam overlay. `Position` should be one of
    _renpysteam.POSTION_TOP_LEFT, .POSITION_TOP_RIGHT, .POSITION_BOTTOM_LEFT,
    or .POSITION_BOTTOM_RIGHT.
    """

    SteamUtils().SetOverlayNotificationPosition(position)

def activate_overlay(dialog):
    """
    :doc: steam_overlay

    Activates the Steam overlay.

    `dialog`
        The dialog to open the overlay to. One of "Friends", "Community",
        "Players", "Settings", "OfficialGameGroup", "Stats", "Achievements"
    """

    SteamFriends().ActivateGameOverlay(dialog)

def activate_overlay_to_web_page(url):
    """
    :doc: steam_overlay

    Activates the Steam overlay, and opens the web page at `url`.
    """

    SteamFriends().ActivateGameOverlayToWebPage(url)

STORE_NONE = k_EOverlayToStoreFlag_None
STORE_ADD_TO_CART = k_EOverlayToStoreFlag_AddToCart
STORE_ADD_TO_CART_AND_SHOW = k_EOverlayToStoreFlag_AddToCartAndShow

def activate_overlay_to_store(appid, flag=STORE_NONE):
    """
    :doc: steam_overlay

    Opens the steam overlay to the store.

    `appid`
        The appid to open.

    `flag`
        One of _renpysteam.STORE_NONE, .STORE_ADD_TO_CART, or .STORE_ADD_TO_CART_AND_SHOW.
    """

    SteamFriends().ActivateGameOverlayToStore(appid, flag)


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
            set_overlay_notification_position(POSITION_TOP_RIGHT)

    return initialized
