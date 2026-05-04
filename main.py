#!/usr/bin/env python3
"""Simple LRU cache with hit/miss statistics using collections.OrderedDict."""

from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """Least Recently Used (LRU) cache with access statistics."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self._store: OrderedDict[Any, Any] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: Any) -> Optional[Any]:
        """Return value for key, or None if not present. Counts hit/miss."""
        if key in self._store:
            self._store.move_to_end(key)
            self._hits += 1
            return self._store[key]
        self._misses += 1
        return None

    def put(self, key: Any, value: Any) -> None:
        """Insert or update key-value pair. Evicts LRU item if at capacity."""
        if key in self._store:
            self._store[key] = value
            self._store.move_to_end(key)
        else:
            if len(self._store) >= self.capacity:
                self._store.popitem(last=False)  # remove oldest (LRU)
            self._store[key] = value

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    @property
    def size(self) -> int:
        return len(self._store)

    def stats(self) -> dict:
        """Return a dict with hits, misses, and hit ratio."""
        total = self._hits + self._misses
        ratio = self._hits / total if total > 0 else 0.0
        return {"hits": self._hits, "misses": self._misses, "ratio": ratio}

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: Any) -> bool:
        return key in self._store


def main() -> None:
    # Create a cache with capacity 2
    cache = LRUCache(2)

    # Add some entries
    cache.put(1, "one")
    cache.put(2, "two")
    print(f"After putting 1,2 -> size={cache.size}, hits={cache.hits}, misses={cache.misses}")

    # Access an existing key -> hit
    val = cache.get(1)
    print(f"get(1) returned: {val} -> hits={cache.hits}, misses={cache.misses}")

    # Add a third entry -> should evict key 2 (LRU)
    cache.put(3, "three")
    print(f"put(3) -> size={cache.size}")

    # Now get(2) should be a miss
    val = cache.get(2)
    print(f"get(2) returned: {val} -> misses={cache.misses}")

    # get(3) should be a hit
    val = cache.get(3)
    print(f"get(3) returned: {val} -> hits={cache.hits}, misses={cache.misses}")

    # Print overall statistics
    print("Cache stats:", cache.stats())

    # Demonstrate updating an existing key
    cache.put(3, "THREE")
    print(f"Updated key 3, size still {cache.size}")

    # Check membership
    print(f"1 in cache? {1 in cache}")
    print(f"2 in cache? {2 in cache}")
    print(f"3 in cache? {3 in cache}")


if __name__ == "__main__":
    main()