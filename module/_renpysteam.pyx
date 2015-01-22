cdef extern from "steam/steam_api.h":
    bint SteamAPI_Init()

print SteamAPI_Init()
