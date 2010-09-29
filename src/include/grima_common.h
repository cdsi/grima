#ifndef GRIMA_COMMON_H
#define GRIMA_COMMON_H 1

#ifdef HAVE_CONFIG_H
#include "grima_config.h"
#endif                          /* HAVE_CONFIG_H */

#ifndef HAVE_AHEXTOI
#define ahextoi(x)	strtol(x, (char **)NULL, 16)
#endif                          /* ! HAVE_AHEXTOI */

#ifndef HAVE_ATOFF
#define atoff(x)	strtof(x, NULL)
#endif                          /* ! HAVE_ATOFF */

/* TODO: This could also be __FUNCTION__ which is a GCC extension...  */
#define __FUNC__ __func__

#endif                          /* ! GRIMA_COMMON_H */

/*
 * $Id:$
 *
 * Local Variables:
 * c-file-style: "linux"
 * indent-tabs-mode: nil
 * End:
 * vim: ai et si sw=8 ts=8
 */
