#pragma once

// Glue for parameterized tests: every solution variant runs against every case.

#include <cctype>
#include <ostream>
#include <string>
#include <string_view>
#include <vector>

#include <gtest/gtest.h>

#include "lc/cases.hpp"

namespace lc {

// One implementation of a problem, e.g. {"brute_force", &brute_force}.
template <class Fn>
struct Variant {
    std::string_view name;
    Fn fn;
};

template <class Fn>
struct VariantCase {
    Variant<Fn> variant;
    TestCase test_case;

    // Keeps GoogleTest from dumping raw bytes when a test fails.
    friend void PrintTo(const VariantCase& vc, std::ostream* os) {
        *os << vc.variant.name << " / " << vc.test_case.name;
    }
};

// Cartesian product: variants x cases.
template <class Fn>
[[nodiscard]] std::vector<VariantCase<Fn>> combine(const std::vector<Variant<Fn>>& variants,
                                                   const std::vector<TestCase>& cases) {
    std::vector<VariantCase<Fn>> out;
    out.reserve(variants.size() * cases.size());
    for (const auto& variant : variants) {
        for (const auto& test_case : cases) {
            out.push_back({variant, test_case});
        }
    }
    return out;
}

// GoogleTest parameter names may only contain [A-Za-z0-9_].
[[nodiscard]] inline std::string sanitize_test_name(std::string_view raw) {
    std::string out;
    out.reserve(raw.size());
    for (const char c : raw) {
        out.push_back(std::isalnum(static_cast<unsigned char>(c)) != 0 ? c : '_');
    }
    return out;
}

struct VariantCaseName {
    template <class Fn>
    std::string operator()(const ::testing::TestParamInfo<VariantCase<Fn>>& info) const {
        return sanitize_test_name(std::string(info.param.variant.name) + "__" +
                                  info.param.test_case.name);
    }
};

}  // namespace lc
