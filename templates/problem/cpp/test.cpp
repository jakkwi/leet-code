#include <vector>

#include <gtest/gtest.h>
#include <lc/cases.hpp>
#include <lc/variant.hpp>

#include "solution.hpp"

namespace {

namespace sol = lc::{{NAMESPACE}};
using Param = lc::VariantCase<sol::Solver>;

class {{SUITE}}Test : public ::testing::TestWithParam<Param> {};

TEST_P({{SUITE}}Test, MatchesExpected) {
    const auto& [variant, tc] = GetParam();
    // TODO: adapt to the problem's signature.
    const auto nums = tc.input.at("nums").get<std::vector<int>>();
    EXPECT_EQ(variant.fn(nums), tc.expected.get<int>()) << tc.note;
}

INSTANTIATE_TEST_SUITE_P(AllVariants, {{SUITE}}Test,
                         ::testing::ValuesIn(lc::combine(sol::variants(),
                                                         lc::load_cases(LC_CASES_PATH))),
                         lc::VariantCaseName{});

// No variants or no cases yet is a valid state while working on a problem.
GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST({{SUITE}}Test);

}  // namespace
