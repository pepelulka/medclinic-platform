#include <stdio.h>
#include <stdlib.h>
#include <onion/onion.h>
#include <onion/response.h>
#include <onion/router.h>

int hello(onion_request *req, onion_response *res) {
    onion_response_printf(res, "Hello, World!\n");
    return OCS_PROCESSED;
}

int main() {
    onion *o = onion_new(O_THREADED, 8080);
    onion_router *router = onion_router_new(o);

    onion_router_add(router, "/", hello);

    onion_set_root(o, router);
    onion_listen(o);

    onion_free(o);
    return 0;
}
