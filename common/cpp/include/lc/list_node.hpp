#pragma once

// LeetCode's singly linked list node plus helpers that build lists from JSON
// arrays and read them back. Solutions get raw pointers exactly like on
// LeetCode; ListArena owns the nodes, so tests never leak under ASan.

#include <cstddef>
#include <deque>
#include <stdexcept>
#include <vector>

namespace lc {

struct ListNode {
    int val = 0;
    ListNode* next = nullptr;

    ListNode() = default;
    explicit ListNode(int x) : val(x) {}
    ListNode(int x, ListNode* n) : val(x), next(n) {}
};

class ListArena {
public:
    // std::deque never moves existing elements on push_back, so the pointers
    // handed out stay valid for the arena's lifetime.
    ListNode* make(int val) { return &nodes_.emplace_back(val); }

    ListNode* from_vector(const std::vector<int>& values) {
        ListNode dummy;
        ListNode* tail = &dummy;
        for (const int v : values) {
            tail->next = make(v);
            tail = tail->next;
        }
        return dummy.next;
    }

    [[nodiscard]] std::size_t size() const noexcept { return nodes_.size(); }

private:
    std::deque<ListNode> nodes_;
};

// Throws instead of looping forever if a buggy solution leaves a cycle.
[[nodiscard]] inline std::vector<int> to_vector(const ListNode* head,
                                                std::size_t max_nodes = 100'000) {
    std::vector<int> out;
    for (; head != nullptr; head = head->next) {
        if (out.size() == max_nodes) {
            throw std::runtime_error("list longer than max_nodes, cycle?");
        }
        out.push_back(head->val);
    }
    return out;
}

}  // namespace lc
