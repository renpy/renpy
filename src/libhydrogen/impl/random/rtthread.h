#include <rtthread.h>
#include <hw_rng.h>

#define DBG_TAG "libhydrogen"
#define DBG_LVL DBG_LOG
#include <rtdbg.h>

static int
hydrogen_init(void) {
    if (hydro_init() != 0) {
        abort();
    }
    LOG_I("libhydrogen initialized");
    return 0;
}
INIT_APP_EXPORT(hydrogen_init);

static int
hydro_random_init(void)
{
    const char       ctx[hydro_hash_CONTEXTBYTES] = { 'h', 'y', 'd', 'r', 'o', 'P', 'R', 'G' };
    hydro_hash_state st;
    uint16_t         ebits = 0;

    hydro_hash_init(&st, ctx, NULL);

    while (ebits < 256) {
        uint32_t r = rt_hwcrypto_rng_update();
        hydro_hash_update(&st, (const uint32_t *) &r, sizeof r);
        ebits += 32;
    }

    hydro_hash_final(&st, hydro_random_context.state, sizeof hydro_random_context.state);
    hydro_random_context.counter = ~LOAD64_LE(hydro_random_context.state);

    return 0;
}
