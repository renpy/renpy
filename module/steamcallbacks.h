#ifndef STEAMCALLBACKS_H
#define STEAMCALLBACKS_H
#include "steam/steam_api.h"

class OnUserStatsReceivedCallback {
public:
	STEAM_CALLBACK( OnUserStatsReceivedCallback, OnUserStatsReceived, UserStatsReceived_t, steam_callback);

	void (*callback)(UserStatsReceived_t *stats);

	void callback_method(UserStatsReceived_t *stats) {
		callback(stats);
	}

	OnUserStatsReceivedCallback(void (*callback)(UserStatsReceived_t *))
		: steam_callback(this, &OnUserStatsReceivedCallback::callback_method) {
		this->callback = callback;
	}
};


#endif
