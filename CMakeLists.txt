cmake_minimum_required(VERSION 3.28)

project(leetcode_cpp_python LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

option(LC_SANITIZE "Build with AddressSanitizer (plus UBSan on GCC/Clang)" OFF)
option(LC_BENCHMARK "Fetch Google Benchmark and build problems' bench.cpp" OFF)
option(LC_WARNINGS_AS_ERRORS "Treat compiler warnings as errors" ON)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

# Sanitizer flags are global so GoogleTest is instrumented the same way as our code.
include(Sanitizers)
include(Dependencies)
include(Warnings)

enable_testing()
include(GoogleTest)

add_subdirectory(common/cpp)

include(Problems)
lc_add_all_problems()
