#pragma once

// {{NUMBER}}. {{TITLE}}
// {{URL}}

#include <vector>

#include <lc/variant.hpp>

namespace lc::{{NAMESPACE}} {

// TODO: set the signature every variant shares (and the call in test.cpp).
using Solver = int (*)(const std::vector<int>& nums);

// Variants go here, one function each.

// Every variant listed here is run against every case in cases.json.
inline const std::vector<Variant<Solver>>& variants() {
    static const std::vector<Variant<Solver>> kVariants{
        // {.name = "brute_force", .fn = &brute_force},
    };
    return kVariants;
}

}  // namespace lc::{{NAMESPACE}}
