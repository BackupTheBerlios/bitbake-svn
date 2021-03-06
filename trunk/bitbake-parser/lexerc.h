
#ifndef LEXERC_H
#define LEXERC_H

#include <stdio.h>

extern int lineError;
extern int errorParse;

typedef struct {
    void *parser;
    void *scanner;
    FILE *file;
    char *name;
    PyObject *tree;
    int config;
    int error;
    int lineno;
} lex_t;

#endif
