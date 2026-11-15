# Global sanitizer flags. Applied before dependencies are fetched so every
# translation unit (ours and GoogleTest's) is built with the same settings;
# MSVC refuses to link ASan and non-ASan objects that use std::vector together.

if(NOT LC_SANITIZE)
  return()
endif()

if(MSVC)
  # MSVC supports ASan only (no UBSan). /RTC and incremental linking conflict with it.
  foreach(flag_var CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELWITHDEBINFO)
    string(REGEX REPLACE "/RTC[1csu]*" "" ${flag_var} "${${flag_var}}")
  endforeach()
  foreach(flag_var CMAKE_EXE_LINKER_FLAGS_DEBUG CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO)
    string(REGEX REPLACE "/INCREMENTAL(:YES)?" "" ${flag_var} "${${flag_var}}")
  endforeach()
  add_compile_options(/fsanitize=address /Zi)
  add_link_options(/INCREMENTAL:NO /DEBUG)

  # Tests run outside a Developer shell too, so ship the ASan runtime next to them.
  cmake_path(GET CMAKE_CXX_COMPILER PARENT_PATH _lc_cl_dir)
  file(GLOB _lc_asan_dlls "${_lc_cl_dir}/clang_rt.asan_dynamic-x86_64.dll"
       "${_lc_cl_dir}/clang_rt.asan_dbg_dynamic-x86_64.dll")
  file(COPY ${_lc_asan_dlls} DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
else()
  add_compile_options(-fsanitize=address,undefined -fno-sanitize-recover=all
                      -fno-omit-frame-pointer)
  add_link_options(-fsanitize=address,undefined)
endif()

message(STATUS "Sanitizers enabled")
