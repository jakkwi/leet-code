# Third-party code, each pinned to an exact commit and verified by SHA-256.
# To bump: change the commit, download the archive, update URL_HASH.

include(FetchContent)

# GoogleTest v1.18.0
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/063de7e9578f82b369302001269680b4b1553359.tar.gz
  URL_HASH SHA256=623fe05d283020f37a579a8985ba338091ac7229da62b5591ff40acdf05b95e2
  SYSTEM
  EXCLUDE_FROM_ALL)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)

# nlohmann/json v3.12.0 (reads cases.json)
FetchContent_Declare(
  nlohmann_json
  URL https://github.com/nlohmann/json/archive/55f93686c01528224f448c19128836e7df245f72.tar.gz
  URL_HASH SHA256=67f4cdd9ca930c9c1e130af4a437c7fc98fab77a2846fc2d2a14b4943831f8ef
  SYSTEM
  EXCLUDE_FROM_ALL)
set(JSON_BuildTests OFF CACHE INTERNAL "")

FetchContent_MakeAvailable(googletest nlohmann_json)

if(LC_BENCHMARK)
  # Google Benchmark v1.10.0
  FetchContent_Declare(
    benchmark
    URL https://github.com/google/benchmark/archive/a6b4a9f00b36c19af9997d68a1cf6e0b5b3d032c.tar.gz
    URL_HASH SHA256=1e34f52437882bfe010f955580e77a19b4fb0a702ef678609b509a834296075c
    SYSTEM
    EXCLUDE_FROM_ALL)
  set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)
  set(BENCHMARK_ENABLE_GTEST_TESTS OFF CACHE BOOL "" FORCE)
  set(BENCHMARK_ENABLE_INSTALL OFF CACHE BOOL "" FORCE)
  FetchContent_MakeAvailable(benchmark)
endif()
