#ifndef _FOO_H
# define _FOO_H

# ifdef __cplusplus
#  define FOO_HDR_BEGIN extern "C" {
# else
#  define FOO_HDR_BEGIN
# endif /* __cplusplus */

# ifdef __cplusplus
#  define FOO_HDR_END }
# else
#  define FOO_HDR_END
# endif

FOO_HDR_BEGIN

/* Shared library support */
#ifdef WIN32
  #define FOOIMPORT __declspec(dllimport)
  #define FOOEXPORT __declspec(dllexport)
  #define FOODLLLOCAL
  #define FOODLLPUBLIC
#else
  #define FOOIMPORT
  #ifdef GCC_HASCLASSVISIBILITY
    #define FOOEXPORT __attribute__ ((visibility("default")))
    #define FOODLLLOCAL __attribute__ ((visibility("hidden")))
    #define FOODLLPUBLIC __attribute__ ((visibility("default")))
  #else
    #define FOOEXPORT
    #define FOODLLLOCAL
    #define FOODLLPUBLIC
  #endif
#endif

/* Define FOOAPI for DLL builds */
#ifdef FOXDLL
  #ifdef FOXDLL_EXPORTS
    #define FOOAPI FOOEXPORT
  #else
    #define FOOAPI FOOIMPORT
  #endif // FOXDLL_EXPORTS
#else
  #define FOOAPI
#endif // FOXDLL

/* Throwable classes must always be visible on GCC in all binaries */
#ifdef WIN32
  #define FOOEXCEPTIONAPI(api) api
#elif defined(GCC_HASCLASSVISIBILITY)
  #define FOOEXCEPTIONAPI(api) FOOEXPORT
#else
  #define FOOEXCEPTIONAPI(api)
#endif

FOO_HDR_END

#endif /* _FOO_H */
