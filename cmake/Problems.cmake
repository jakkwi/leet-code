# One test executable per problem: problems/<pattern>/<NNNN_slug>/cpp/test.cpp.
# Each target sees only its own folder and lc_common, which is how the
# "problems are isolated" rule is enforced for C++.

function(lc_add_problem test_src)
  cmake_path(GET test_src PARENT_PATH cpp_dir)
  cmake_path(GET cpp_dir PARENT_PATH problem_dir)
  cmake_path(GET problem_dir FILENAME slug)
  cmake_path(GET problem_dir PARENT_PATH pattern_dir)
  cmake_path(GET pattern_dir FILENAME pattern)

  set(target "p${slug}")
  add_executable(${target} ${test_src})
  target_link_libraries(${target} PRIVATE lc_common lc_warnings GTest::gtest_main)
  target_compile_definitions(${target} PRIVATE LC_CASES_PATH="${problem_dir}/cases.json")
  set_target_properties(${target} PROPERTIES FOLDER "problems/${pattern}")
  gtest_discover_tests(${target} DISCOVERY_MODE PRE_TEST TEST_PREFIX "${pattern}/${slug}/")

  if(LC_BENCHMARK AND EXISTS "${cpp_dir}/bench.cpp")
    add_executable(${target}_bench ${cpp_dir}/bench.cpp)
    target_link_libraries(${target}_bench PRIVATE lc_common lc_warnings benchmark::benchmark_main)
  endif()
endfunction()

function(lc_add_all_problems)
  file(GLOB test_sources CONFIGURE_DEPENDS "${PROJECT_SOURCE_DIR}/problems/*/*/cpp/test.cpp")
  list(LENGTH test_sources count)
  message(STATUS "Problems found: ${count}")
  foreach(test_src IN LISTS test_sources)
    lc_add_problem(${test_src})
  endforeach()
endfunction()
