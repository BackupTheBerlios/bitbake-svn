/* ex:ts=4:sw=4:sts=4:et
 * -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
 *
 * Copyright (C) 2004, 2005 Chris Larson <kergoth@handhelds.org>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

#include <bitbake-data.h>
#include <glib.h>
#include <sqlite3.h>

#include "config.h"

/**
 * Static structure to hold process wide information associated with
 * our bitbake data.  In this case, this holds our pointer to our open
 * sqlite3 database, its path, and so on.  Protected by a GStaticMutex.
 */
static struct {
    gboolean initialized;
    GStaticMutex mutex;
    gchar *datapath;
    sqlite3 *db;
    guint users;
} bbdata_setup = {
    .initialized = FALSE,
    .mutex = G_STATIC_MUTEX_INIT,
    .users = 0,
};

BBDATA_IMPORT static gboolean bb_data_init(void)
{
    gboolean ret = TRUE;
    const gchar *datapath = g_getenv("BBDATAPATH");

    if (datapath)
        bbdata_setup.datapath = g_filename_to_utf8(datapath, -1, NULL, NULL, NULL);

    if (!bbdata_setup.datapath)
        bbdata_setup.datapath = g_build_path(LOCALSTATEDIR, "lib", "bitbake-data", NULL);

    bbdata_setup.initialized = TRUE;
    return ret;
}

BBDATA_IMPORT static void bb_data_shutdown(void)
{
    bbdata_setup.initialized = FALSE;
    g_free(bbdata_setup.datapath);
}

#if 0
#include <stdio.h>
#include <sqlite3.h>

static int callback(void *NotUsed, int argc, char **argv, char **azColName){
  int i;
  for(i=0; i<argc; i++){
    printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
  }
  printf("\n");
  return 0;
}

int main(int argc, char **argv){
  sqlite3 *db;
  char *zErrMsg = 0;
  int rc;

  if( argc!=3 ){
    fprintf(stderr, "Usage: %s DATABASE SQL-STATEMENT\n", argv[0]);
    exit(1);
  }
  rc = sqlite3_open(argv[1], &db);
  if( rc ){
    fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    exit(1);
  }
  rc = sqlite3_exec(db, argv[2], callback, 0, &zErrMsg);
  if( rc!=SQLITE_OK ){
    fprintf(stderr, "SQL error: %s\n", zErrMsg);
  }
  sqlite3_close(db);
  return 0;
}
#endif

struct bb_data {
    gchar *recipe;
};

BBDATA_API gpointer bb_data_new(const gchar *recipe)
{
    gpointer ret = NULL; /* FIXME: return something useful :) */

    g_static_mutex_lock(&bbdata_setup.mutex);

    if (!bbdata_setup.initialized) {
        if (!bb_data_init())
            ret = NULL;
    }

    if (bbdata_setup.initialized)
        bbdata_setup.users += 1;

    g_static_mutex_unlock(&bbdata_setup.mutex);

    if (ret == NULL)
        return ret;

//    rc = sqlite3_open(argv[1], &db);

    return ret;
}

BBDATA_API GTimeVal bb_data_get_modif_date(gpointer data);
BBDATA_API gchar *bb_data_lookup(gconstpointer data, const gchar *var);
BBDATA_API gboolean bb_data_insert(gpointer data, const gchar *var, const gchar *val);
BBDATA_API gboolean bb_data_remove(gpointer data, const gchar *var);
BBDATA_API gchar *bb_data_lookup_attr(gconstpointer data, const gchar *var, const gchar *attr);
BBDATA_API gboolean bb_data_insert_attr(gpointer data, const gchar *var, const gchar *attr, const gchar *val);
BBDATA_API gboolean bb_data_remove_attr(gpointer data, const gchar *var, const gchar *attr);

BBDATA_API void bb_data_destroy(gpointer data)
{
    g_static_mutex_lock(&bbdata_setup.mutex);

    if (bbdata_setup.initialized) {
        bbdata_setup.users -= 1;

        if (bbdata_setup.users < 1) {
            bb_data_shutdown();
        }
    }

    g_static_mutex_unlock(&bbdata_setup.mutex);
}
