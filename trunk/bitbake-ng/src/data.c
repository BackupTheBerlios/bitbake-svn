/* ex:ts=4:sw=4:sts=4:et
 * -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*- */

/** @file data.c
 *  @brief Bitbake Metadata Handling Code
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

# include <bitbake/common.h>
# include <bitbake/data.h>
# include <bitbake/data-private.h>
# include <glib.h>

gpointer bb_data_new(void)
{
    struct bb_data *data;
    data = g_new0(struct bb_data, 1);
    data->data = g_hash_table_new(g_str_hash, g_str_equal);
    return data;
}

gchar *bb_data_lookup(gconstpointer data, gchar *key);
gchar *bb_data_get_var(gconstpointer data, gchar *var);
gboolean bb_data_set_var(gpointer data, gchar *var, gchar *val);
gboolean bb_data_del_var(gpointer data, gchar *var);
gchar *bb_data_get_var_attr(gconstpointer data, gchar *var, gchar *attr);
gboolean bb_data_set_var_attr(gpointer data, gchar *var, gchar *attr, gchar *val);
gboolean bb_data_del_var_attr(gpointer data, gchar *var, gchar *attr);

void bb_data_destroy(gpointer ptr)
{
    struct bb_data *data = ptr;
    g_hash_table_destroy(data->data);
    g_free(ptr);
}
