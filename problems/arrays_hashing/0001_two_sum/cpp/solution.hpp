#pragma once

// 0001. Two Sum
// https://leetcode.com/problems/two-sum/

#include <vector>

#include <lc/variant.hpp>

namespace lc::p0001_two_sum {

// Returns the indices of the two numbers that add up to target, in any order.
// LeetCode passes vector<int>& (non-const); nothing here needs to mutate the input.
using Solver = std::vector<int> (*)(const std::vector<int>& nums, int target);

// Variants go here, one function each.

// Every variant listed here is run against every case in cases.json.
inline const std::vector<Variant<Solver>>& variants() {
    static const std::vector<Variant<Solver>> kVariants{
        // {.name = "brute_force", .fn = &brute_force},
    };
    return kVariants;
}

}  // namespace lc::p0001_two_sum
