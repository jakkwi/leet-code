#pragma once

// Loader for a problem's cases.json, shared by every C++ test.
//
// File format (the same file is read by the Python tests):
//   {
//     "cases": [
//       {"name": "example_1", "input": {...}, "expected": ..., "note": "optional"}
//     ]
//   }

#include <cstddef>
#include <filesystem>
#include <fstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include <nlohmann/json.hpp>

namespace lc {

using Json = nlohmann::json;

struct TestCase {
    std::string name;
    Json input;
    Json expected;
    std::string note;
};

[[nodiscard]] inline std::vector<TestCase> load_cases(const std::filesystem::path& path) {
    std::ifstream file(path);
    if (!file) {
        throw std::runtime_error("cannot open cases file: " + path.string());
    }
    const Json root = Json::parse(file);
    const Json& items = root.at("cases");

    std::vector<TestCase> cases;
    cases.reserve(items.size());
    for (const Json& item : items) {
        cases.push_back(TestCase{
            .name = item.at("name").get<std::string>(),
            .input = item.at("input"),
            .expected = item.at("expected"),
            .note = item.value("note", std::string{}),
        });
    }
    return cases;
}

}  // namespace lc
