cdef extern from "steam/steam_api.h":
    bint SteamAPI_Init()
    void SteamAPI_RunCallbacks()

    cdef cppclass ISteamUserStats:
        bint RequestCurrentStats()

    ISteamUserStats *SteamUserStats()

    ctypedef struct UserStatsReceived_t

cdef extern from "steamcallbacks.h":
    cdef cppclass OnUserStatsReceivedCallback:
        OnUserStatsReceivedCallback(void (*)(UserStatsReceived_t *))


print SteamAPI_Init()


stats_done = False

cdef void stats_received_callback(UserStatsReceived_t *s):
    global stats_done
    stats_done = True

cdef OnUserStatsReceivedCallback *on_stats_received = new OnUserStatsReceivedCallback(stats_received_callback)

import time

def update_stats():
    print SteamUserStats().RequestCurrentStats()

    start = time.time()
    while not stats_done:
        SteamAPI_RunCallbacks()
        time.sleep(.01)
    print time.time() - start

update_stats()
