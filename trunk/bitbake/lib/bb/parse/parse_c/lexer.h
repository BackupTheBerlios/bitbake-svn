/*
Copyright (C) 2005 Holger Hans Peter Freyther

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/

#ifndef LEXER_H
#define LEXER_H

/*
 * The PyObject Token. Likely to be
 * a bb.data implementation
 */
struct PyObject;


/**
 * This is used by the Parser and Scanner
 * of BitBake.
 * The implementation and creation is done
 * in the scanner.
 */
struct lex_t {
    void *parser;
    void *scanner;
    FILE *file;
    PyObject *data;
    void* (*parse)(void*, int, token_t, lex_t*);

    void accept(int token, const char* string = 0);
    void input(char *buf, int *result, int max_size);
    int  line()const;
};


#endif
