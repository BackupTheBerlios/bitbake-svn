# BB_CXX_SUPPORTS_HIDDEN_VISIBILITY_INLINES
# ----------
# Check the C++ compiler for support for -fvisibility-inlines-hidden.
AC_DEFUN([BB_CXX_SUPPORTS_HIDDEN_VISIBILITY_INLINES],
[AC_REQUIRE([AC_PROG_CXX])
  bb_save_CXXFLAGS="$CXXFLAGS"
  CXXFLAGS="-fvisibility-inlines-hidden $bb_save_CXXFLAGS"
  AC_CACHE_CHECK([whether the C++ compiler supports -fvisibility-inlines-hidden],
                 [bb_cv_cc_supports_hidden_visibility_inlines], [
    AC_LANG_PUSH(C++)
    AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[]], [[]])], [bb_cv_cc_supports_hidden_visibility_inlines=yes], [bb_cv_cc_supports_hidden_visibility_inlines=no])
    AC_LANG_POP(C++)
  ])
  CXXFLAGS="$bb_save_CXXFLAGS"
]) # BB_CXX_SUPPORTS_HIDDEN_VISIBILITY_INLINES


# BB_CXX_HIDDEN_VISIBILITY_INLINES
# ----------
# Decide whether or not to use -fvisibility-inlines-hidden for c++ applications.
AC_DEFUN([BB_CXX_HIDDEN_VISIBILITY_INLINES],
[AC_REQUIRE([BB_CXX_SUPPORTS_HIDDEN_VISIBILITY_INLINES])
  AC_MSG_CHECKING([whether to use -fvisibility-inlines-hidden])
  AC_ARG_WITH([hidden_visibility_inlines],
              AC_HELP_STRING([--with-hidden_visibility_inlines=VAL],
                             [use -fvisibility-inlines-hidden (default VAL is 'auto')]),
              [bb_with_hidden_visibility_inlines=$withval], [bb_with_hidden_visibility_inlines=auto])

  if test "x$bb_with_hidden_visibility_inlines" != "xno" && \
     test "x$bb_cv_cc_supports_hidden_visibility_inlines" != "xno"; then
     AC_MSG_RESULT([yes])
     CXXFLAGS="-fvisibility-inlines-hidden $CXXFLAGS"
     AC_MSG_NOTICE([prepending -fvisibility-inlines-hidden to CXXFLAGS])
  else
     AC_MSG_RESULT([no])
  fi
]) # BB_CXX_HIDDEN_VISIBILITY_INLINES


# BB_CC_SUPPORTS_HIDDEN_VISIBILITY
# ----------
# Check the C compiler for support for -fvisibility=hidden.
AC_DEFUN([BB_CC_SUPPORTS_HIDDEN_VISIBILITY],
[AC_REQUIRE([AC_PROG_CC])
  bb_save_CFLAGS="$CFLAGS"
  CFLAGS="-fvisibility=hidden $bb_save_CFLAGS"
  AC_CACHE_CHECK([whether the C compiler supports -fvisibility=hidden],
                 [bb_cv_cc_supports_hidden_visibility], [
    AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[]], [[]])], [bb_cv_cc_supports_hidden_visibility=yes], [bb_cv_cc_supports_hidden_visibility=no])
  ])
  CFLAGS="$bb_save_CFLAGS"
]) # BB_CC_SUPPORTS_HIDDEN_VISIBILITY


# BB_CC_HIDDEN_VISIBILITY
# ----------
# Decide whether or not to use -fvisibility=hidden.
AC_DEFUN([BB_CC_HIDDEN_VISIBILITY],
[AC_REQUIRE([BB_CC_SUPPORTS_HIDDEN_VISIBILITY])
  AC_MSG_CHECKING([whether to use -fvisibility=hidden])
  AC_ARG_WITH([hidden_visibility],
              AC_HELP_STRING([--with-hidden_visibility=VAL],
                             [use -fvisibility=hidden (default VAL is 'auto')]),
              [bb_with_hidden_visibility=$withval], [bb_with_hidden_visibility=auto])

  if test "x$bb_with_hidden_visibility" != "xno" && \
     test "x$bb_cv_cc_supports_hidden_visibility" != "xno"; then
     AC_MSG_RESULT([yes])
     CFLAGS="-DGCC_HASCLASSVISIBILITY -fvisibility=hidden $CFLAGS"
     AC_MSG_NOTICE([prepending -DGCC_HASCLASSVISIBILITY -fvisibility=hidden to CFLAGS])
  else
     AC_MSG_RESULT([no])
  fi
]) # BB_CC_HIDDEN_VISIBILITY


# BB_DEFAULT_FLAGS
# ----------
# Set our default FLAGS variables.
# Remember to call before the AC_PROG_ variables, otherwise those
# defaults will be used instead of ours.
AC_DEFUN([BB_DEFAULT_FLAGS],
[
  if test x"$CFLAGS" = "x"; then
    CFLAGS="-O2 -Wall -W"
  fi
]) # BB_DEFAULT_FLAGS
