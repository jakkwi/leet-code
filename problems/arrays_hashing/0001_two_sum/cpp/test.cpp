#include <algorithm>
#include <vector>

#include <gtest/gtest.h>
#include <lc/cases.hpp>
#include <lc/variant.hpp>

#include "solution.hpp"

namespace {

namespace sol = lc::p0001_two_sum;
using Param = lc::VariantCase<sol::Solver>;

class TwoSumTest : public ::testing::TestWithParam<Param> {};

TEST_P(TwoSumTest, MatchesExpected) {
    const auto& [variant, tc] = GetParam();
    const auto nums = tc.input.at("nums").get<std::vector<int>>();
    const int target = tc.input.at("target").get<int>();

    // Any order is accepted, so compare sorted index pairs.
    auto got = variant.fn(nums, target);
    auto expected = tc.expected.get<std::vector<int>>();
    std::ranges::sort(got);
    std::ranges::sort(expected);
    EXPECT_EQ(got, expected) << tc.note;
}

INSTANTIATE_TEST_SUITE_P(AllVariants, TwoSumTest,
                         ::testing::ValuesIn(lc::combine(sol::variants(),
                                                         lc::load_cases(LC_CASES_PATH))),
                         lc::VariantCaseName{});

// No variants or no cases yet is a valid state while working on a problem.
GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST(TwoSumTest);

}  // namespace
