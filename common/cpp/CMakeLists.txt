add_library(lc_common INTERFACE)
target_include_directories(lc_common INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lc_common INTERFACE nlohmann_json::nlohmann_json)
target_compile_features(lc_common INTERFACE cxx_std_20)

add_executable(lc_common_tests tests/test_cases.cpp tests/test_nodes.cpp)
target_link_libraries(lc_common_tests PRIVATE lc_common lc_warnings GTest::gtest_main)
target_compile_definitions(
  lc_common_tests PRIVATE LC_SAMPLE_CASES_PATH="${PROJECT_SOURCE_DIR}/common/testdata/sample_cases.json")
gtest_discover_tests(lc_common_tests DISCOVERY_MODE PRE_TEST TEST_PREFIX "common/")
