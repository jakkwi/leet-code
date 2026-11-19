"""LeetCode's singly linked list node plus conversions to and from Python lists."""

from __future__ import annotations


class ListNode:
    __slots__ = ("next", "val")

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({to_list(self)})"


def from_list(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: ListNode | None, max_nodes: int = 100_000) -> list[int]:
    """Raises instead of looping forever if a solution leaves a cycle."""
    out: list[int] = []
    while head is not None:
        if len(out) == max_nodes:
            msg = "list longer than max_nodes, cycle?"
            raise ValueError(msg)
        out.append(head.val)
        head = head.next
    return out
