#ifndef STEAMCALLBACKS_H
#define STEAMCALLBACKS_H
#include "steam/steam_api.h"

template <class P>
class SteamCallback : CCallbackBase {
	void (*callback)(P*);

public:

	SteamCallback(void (*func)(P *)) : callback(func) {
		m_iCallback = P::k_iCallback;
		SteamAPI_RegisterCallback(this, P::k_iCallback);
	}

	~SteamCallback() {
		SteamAPI_UnregisterCallback(this);
	}

protected:

	virtual void Run(void *param) {
		callback((P *) param);
	}

	virtual void Run( void *param, bool, SteamAPICall_t ) {
		callback((P *) param);
	}

	int GetCallbackSizeBytes() {
		return sizeof(P);
	}
};

#endif
