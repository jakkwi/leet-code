#include <optional>
#include <stdexcept>
#include <vector>

#include <gtest/gtest.h>
#include <nlohmann/json.hpp>

#include "lc/list_node.hpp"
#include "lc/tree_node.hpp"

namespace {

TEST(ListNode, RoundTrip) {
    lc::ListArena arena;
    const std::vector<int> values{1, 2, 3};
    EXPECT_EQ(lc::to_vector(arena.from_vector(values)), values);
    EXPECT_EQ(arena.size(), 3U);
}

TEST(ListNode, EmptyIsNullptr) {
    lc::ListArena arena;
    EXPECT_EQ(arena.from_vector({}), nullptr);
    EXPECT_TRUE(lc::to_vector(nullptr).empty());
}

TEST(ListNode, CycleIsDetected) {
    lc::ListArena arena;
    lc::ListNode* head = arena.from_vector({1, 2});
    head->next->next = head;
    EXPECT_THROW((void)lc::to_vector(head, 10), std::runtime_error);
}

TEST(TreeNode, RoundTripWithNulls) {
    const auto json = nlohmann::json::parse("[3, 9, 20, null, null, 15, 7]");
    const lc::LevelOrder values = lc::level_order_from_json(json);
    lc::TreeArena arena;
    const lc::TreeNode* root = arena.from_level_order(values);
    ASSERT_NE(root, nullptr);
    EXPECT_EQ(root->right->left->val, 15);
    EXPECT_EQ(lc::to_level_order(root), values);
}

TEST(TreeNode, EmptyIsNullptr) {
    lc::TreeArena arena;
    EXPECT_EQ(arena.from_level_order({}), nullptr);
    EXPECT_TRUE(lc::to_level_order(nullptr).empty());
}

TEST(TreeNode, TrailingNullsTrimmed) {
    lc::TreeArena arena;
    const lc::LevelOrder in{1, std::nullopt, 2, std::nullopt, std::nullopt};
    const lc::LevelOrder expected{1, std::nullopt, 2};
    EXPECT_EQ(lc::to_level_order(arena.from_level_order(in)), expected);
}

}  // namespace
