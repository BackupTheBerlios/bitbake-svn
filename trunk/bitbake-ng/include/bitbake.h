#ifndef _BITBAKE_H
# define _BITBAKE_H

# ifdef __cplusplus
#  define BITBAKE_HDR_BEGIN extern "C" {
# else
#  define BITBAKE_HDR_BEGIN
# endif /* __cplusplus */

# ifdef __cplusplus
#  define BITBAKE_HDR_END }
# else
#  define BITBAKE_HDR_END
# endif

BITBAKE_HDR_BEGIN

/* Shared library support */
#ifdef WIN32
  #define BBIMPORT __declspec(dllimport)
  #define BBEXPORT __declspec(dllexport)
  #define BBDLLLOCAL
  #define BBDLLPUBLIC
#else
  #define BBIMPORT
  #ifdef GCC_HASCLASSVISIBILITY
    #define BBEXPORT __attribute__ ((visibility("default")))
    #define BBDLLLOCAL __attribute__ ((visibility("hidden")))
    #define BBDLLPUBLIC __attribute__ ((visibility("default")))
  #else
    #define BBEXPORT
    #define BBDLLLOCAL
    #define BBDLLPUBLIC
  #endif
#endif

/* Define BBAPI for DLL builds */
#ifdef FOXDLL
  #ifdef FOXDLL_EXPORTS
    #define BBAPI BBEXPORT
  #else
    #define BBAPI BBIMPORT
  #endif // FOXDLL_EXPORTS
#else
  #define BBAPI
#endif // FOXDLL

/* Throwable classes must always be visible on GCC in all binaries */
#ifdef WIN32
  #define BBEXCEPTIONAPI(api) api
#elif defined(GCC_HASCLASSVISIBILITY)
  #define BBEXCEPTIONAPI(api) BBEXPORT
#else
  #define BBEXCEPTIONAPI(api)
#endif

BITBAKE_HDR_END

#endif /* _BITBAKE_H */
