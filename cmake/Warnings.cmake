# Strict warnings for our own code only (third-party headers are SYSTEM).

add_library(lc_warnings INTERFACE)

if(MSVC)
  target_compile_options(lc_warnings INTERFACE /W4 /permissive- /utf-8 /EHsc
                                               /external:anglebrackets /external:W0)
  if(LC_WARNINGS_AS_ERRORS)
    target_compile_options(lc_warnings INTERFACE /WX)
  endif()
else()
  target_compile_options(
    lc_warnings
    INTERFACE -Wall
              -Wextra
              -Wpedantic
              -Wshadow
              -Wconversion
              -Wsign-conversion
              -Wold-style-cast
              -Wnon-virtual-dtor)
  if(LC_WARNINGS_AS_ERRORS)
    target_compile_options(lc_warnings INTERFACE -Werror)
  endif()
endif()
