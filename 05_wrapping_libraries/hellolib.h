#ifndef _HELLOLIB_H_
#define _HELLOLIB_H_

// This part is necessary only for MSVC to create .lib and .dll files
// and for GCC >= 4 to show the symbols at all

// explicit custom argument for MSVC
#if defined(MSVC_LIB)
#   define HELLOLIBCALL __cdecl
#   define HELLOLIBEXPORT __declspec(dllexport)
// otherwise check automatically
#else
#   define HELLOLIBCALL
#   if defined(__GNUC__) && __GNUC__ >= 4
#       define HELLOLIBEXPORT __attribute__ ((visibility("default")))
#   else
#       define HELLOLIBEXPORT
#   endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

HELLOLIBEXPORT char * HELLOLIBCALL hello(void);

#ifdef __cplusplus
}
#endif

// header endif
#endif
