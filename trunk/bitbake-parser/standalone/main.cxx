#include "bitbake_token.h"
#include "lexer.h"

#include <stdlib.h>
#include <stdio.h>
#include <glob.h>

extern "C" {
extern void parse (FILE* file, char* name);
    
void e_assign(lex_t*, const char*, const char*) {}
void e_export(lex_t*, const char*) {}
void e_immediate(lex_t*, const char*, const char*) {}
void e_cond(lex_t*, const char*, const char*) {}
void e_prepend(lex_t*, const char*, const char*) {}
void e_append(lex_t*, const char*, const char*) {}
void e_precat(lex_t*, const char*, const char*) {}
void e_postcat(lex_t*, const char*, const char*) {}

void e_addtask(lex_t*, const char*, const char*, const char*) {}
void e_addhandler(lex_t*,const char*) {}
void e_export_func(lex_t*, const char*) {}
void e_inherit(lex_t*, const char*) {}
void e_include(lex_t*, const char*) {}
void e_require(lex_t*, const char*) {}
void e_proc(lex_t*, const char*, const char*) {}
void e_proc_python(lex_t*, const char*, const char*) {}
void e_proc_fakeroot(lex_t*, const char*, const char*) {}
void e_def(lex_t*, const char*, const char*, const char*) {}
void e_parse_error(lex_t* lex) {
    fprintf(stderr, "ParseError: %s:%d \n", lex->name, lex->line());
}

}

int main(int argc, char* argv[]) {
    printf("%d arguments\n", argc);
    glob_t myglob;

    if( argc > 1 )
        glob( argv[1], GLOB_TILDE, NULL, &myglob);
        
    for( int i = 2; i < argc; ++i) {
        glob( argv[i], GLOB_APPEND|GLOB_TILDE, NULL, &myglob);
    }

    if( myglob.gl_pathc == 0 ) {
        printf("Nothing found\n");
        return EXIT_FAILURE;
    }

    int i = 0;
    fprintf(stderr, "Pathc: %p %d\n", myglob.gl_pathv[i], myglob.gl_pathc );
    while( myglob.gl_pathv[i] != NULL ) {
        FILE *f = fopen(myglob.gl_pathv[i], "r");
        parse(f, myglob.gl_pathv[i]);
        fclose(f);

        ++i;            
    }


    return EXIT_SUCCESS;
}

