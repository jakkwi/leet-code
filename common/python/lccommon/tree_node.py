"""LeetCode's binary tree node plus level-order conversion: [3, 9, 20, None, None, 15, 7]."""

from __future__ import annotations

from collections import deque


class TreeNode:
    __slots__ = ("left", "right", "val")

    def __init__(
        self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({to_level_order(self)})"


def from_level_order(values: list[int | None]) -> TreeNode | None:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    parents: deque[TreeNode] = deque([root])
    i = 1
    while parents and i < len(values):
        parent = parents.popleft()
        left = values[i]
        if left is not None:
            parent.left = TreeNode(left)
            parents.append(parent.left)
        i += 1
        if i < len(values):
            right = values[i]
            if right is not None:
                parent.right = TreeNode(right)
                parents.append(parent.right)
            i += 1
    return root


def to_level_order(root: TreeNode | None) -> list[int | None]:
    out: list[int | None] = []
    q: deque[TreeNode | None] = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        q.extend((node.left, node.right))
    while out and out[-1] is None:
        out.pop()
    return out
