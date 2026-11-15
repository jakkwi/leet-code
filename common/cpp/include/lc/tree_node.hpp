#pragma once

// LeetCode's binary tree node plus level-order (BFS) conversion, the format
// LeetCode uses in examples: [3, 9, 20, null, null, 15, 7].

#include <cstddef>
#include <deque>
#include <optional>
#include <queue>
#include <vector>

#include <nlohmann/json.hpp>

namespace lc {

struct TreeNode {
    int val = 0;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;

    TreeNode() = default;
    explicit TreeNode(int x) : val(x) {}
    TreeNode(int x, TreeNode* l, TreeNode* r) : val(x), left(l), right(r) {}
};

using LevelOrder = std::vector<std::optional<int>>;

// JSON array with nulls, e.g. [1, null, 2], to LevelOrder.
[[nodiscard]] inline LevelOrder level_order_from_json(const nlohmann::json& arr) {
    LevelOrder out;
    out.reserve(arr.size());
    for (const auto& item : arr) {
        out.push_back(item.is_null() ? std::nullopt : std::optional<int>(item.get<int>()));
    }
    return out;
}

class TreeArena {
public:
    TreeNode* make(int val) { return &nodes_.emplace_back(val); }

    TreeNode* from_level_order(const LevelOrder& values) {
        if (values.empty()) {
            return nullptr;
        }
        // Bind to a reference so the has_value() check and the dereference are
        // visibly on the same object (bugprone-unchecked-optional-access).
        const std::optional<int>& first = values.front();
        if (!first.has_value()) {
            return nullptr;
        }
        TreeNode* root = make(*first);
        std::queue<TreeNode*> parents;
        parents.push(root);
        std::size_t i = 1;
        while (!parents.empty() && i < values.size()) {
            TreeNode* parent = parents.front();
            parents.pop();
            for (TreeNode** child : {&parent->left, &parent->right}) {
                if (i >= values.size()) {
                    break;
                }
                if (const std::optional<int>& value = values[i]; value.has_value()) {
                    *child = make(*value);
                    parents.push(*child);
                }
                ++i;
            }
        }
        return root;
    }

private:
    std::deque<TreeNode> nodes_;
};

// Inverse of from_level_order, trailing nulls trimmed like LeetCode prints it.
[[nodiscard]] inline LevelOrder to_level_order(const TreeNode* root) {
    LevelOrder out;
    std::queue<const TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        const TreeNode* node = q.front();
        q.pop();
        if (node == nullptr) {
            out.emplace_back(std::nullopt);
            continue;
        }
        out.emplace_back(node->val);
        q.push(node->left);
        q.push(node->right);
    }
    while (!out.empty() && !out.back().has_value()) {
        out.pop_back();
    }
    return out;
}

}  // namespace lc
