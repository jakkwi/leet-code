// Self-test of the shared test harness: loader, variant x case product, naming.

#include <filesystem>
#include <stdexcept>
#include <vector>

#include <gtest/gtest.h>

#include "lc/cases.hpp"
#include "lc/variant.hpp"

namespace {

int add(int a, int b) { return a + b; }
int add_reversed(int a, int b) { return b + a; }

using Solver = int (*)(int, int);

const std::vector<lc::Variant<Solver>>& variants() {
    static const std::vector<lc::Variant<Solver>> kVariants{
        {.name = "add", .fn = &add},
        {.name = "add_reversed", .fn = &add_reversed},
    };
    return kVariants;
}

TEST(LoadCases, ReadsAllFields) {
    const auto cases = lc::load_cases(LC_SAMPLE_CASES_PATH);
    ASSERT_EQ(cases.size(), 2U);
    EXPECT_EQ(cases[0].name, "sum_basic");
    EXPECT_EQ(cases[0].input.at("a").get<int>(), 2);
    EXPECT_EQ(cases[0].expected.get<int>(), 5);
    EXPECT_TRUE(cases[0].note.empty());
    EXPECT_FALSE(cases[1].note.empty());
}

TEST(LoadCases, MissingFileThrows) {
    EXPECT_THROW((void)lc::load_cases("does/not/exist.json"), std::runtime_error);
}

TEST(SanitizeTestName, ReplacesNonAlnum) {
    EXPECT_EQ(lc::sanitize_test_name("a b-c.d_1"), "a_b_c_d_1");
}

TEST(Combine, IsCartesianProduct) {
    const auto product = lc::combine(variants(), lc::load_cases(LC_SAMPLE_CASES_PATH));
    EXPECT_EQ(product.size(), 4U);
}

class SampleTest : public ::testing::TestWithParam<lc::VariantCase<Solver>> {};

TEST_P(SampleTest, MatchesExpected) {
    const auto& [variant, tc] = GetParam();
    const int got = variant.fn(tc.input.at("a").get<int>(), tc.input.at("b").get<int>());
    EXPECT_EQ(got, tc.expected.get<int>()) << tc.note;
}

INSTANTIATE_TEST_SUITE_P(AllVariants, SampleTest,
                         ::testing::ValuesIn(lc::combine(variants(),
                                                         lc::load_cases(LC_SAMPLE_CASES_PATH))),
                         lc::VariantCaseName{});

}  // namespace
