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

static void _bb_data_destroy_element(gpointer data)
{
    g_free(data);
}

gpointer bb_data_new(void)
{
    struct bb_data *data;

    data = g_new0(struct bb_data, 1);
    data->data = g_hash_table_new_full(g_str_hash, g_str_equal, _bb_data_destroy_element, _bb_data_destroy_element);

    return data;
}

gchar *bb_data_lookup(gconstpointer ptr, gchar *var)
{
    const struct bb_data *data = ptr;

    g_return_val_if_fail(G_LIKELY(data != NULL), FALSE);
    g_return_val_if_fail(G_LIKELY(data->data != NULL), FALSE);
    g_return_val_if_fail(G_LIKELY(var != NULL), FALSE);

    return g_hash_table_lookup(data->data, var);
}

gboolean bb_data_insert(gpointer ptr, gchar *var, gchar *val)
{
    struct bb_data *data = ptr;

    g_return_val_if_fail(G_LIKELY(data != NULL), FALSE);
    g_return_val_if_fail(G_LIKELY(data->data != NULL), FALSE);
    g_return_val_if_fail(G_LIKELY(var != NULL), FALSE);

    g_hash_table_insert(data->data, var, val);

    return TRUE;
}

gboolean bb_data_remove(gpointer ptr, gchar *var)
{
    struct bb_data *data = ptr;
    g_return_val_if_fail(G_LIKELY(data != NULL), FALSE);
    g_return_val_if_fail(G_LIKELY(data->data != NULL), FALSE);
    g_return_val_if_fail(G_LIKELY(var != NULL), FALSE);

    g_hash_table_remove(data->data, var);
    return TRUE;
}

gchar *bb_data_lookup_attr(gconstpointer ptr, gchar *var, gchar *attr);
gboolean bb_data_insert_attr(gpointer ptr, gchar *var, gchar *attr, gchar *val);
gboolean bb_data_remove_attr(gpointer ptr, gchar *var, gchar *attr);

void bb_data_destroy(gpointer ptr)
{
    struct bb_data *data = ptr;

    g_return_if_fail(G_LIKELY(data != NULL));

    g_hash_table_destroy(data->data);
    g_free(ptr);
}
