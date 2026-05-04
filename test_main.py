import pytest
from collections import OrderedDict
from main import LRUCache   # assuming the code above is saved as main.py

class TestLRUCache:
    def test_put_and_get(self):
        cache = LRUCache(2)
        cache.put("a", 100)
        cache.put("b", 200)
        assert cache.get("a") == 100
        assert cache.get("b") == 200
        assert cache.get("c") is None

    def test_eviction_when_full(self):
        cache = LRUCache(2)
        cache.put(1, "one")
        cache.put(2, "two")
        # access 1 to make 2 the LRU
        cache.get(1)
        cache.put(3, "three")
        assert 2 not in cache
        assert cache.get(2) is None
        assert cache.get(3) == "three"
        assert cache.get(1) == "one"
        assert len(cache) == 2

    def test_update_existing_key(self):
        cache = LRUCache(2)
        cache.put("x", 10)
        cache.put("y", 20)
        cache.put("x", 11)  # update
        # should be still 2 items, x updated
        assert cache.size == 2
        assert cache.get("x") == 11
        # LRU should be y still
        cache.put("z", 30)
        assert cache.get("y") is None
        assert cache.get("z") == 30

    def test_hit_miss_counting(self):
        cache = LRUCache(3)
        cache.put(1, "a")
        assert cache.hits == 0
        assert cache.misses == 0

        cache.get(1)  # hit
        assert cache.hits == 1
        assert cache.misses == 0

        cache.get(2)  # miss
        assert cache.hits == 1
        assert cache.misses == 1

        cache.get(1)  # hit again
        assert cache.hits == 2
        assert cache.misses == 1

    def test_stats(self):
        cache = LRUCache(2)
        # no accesses yet -> ratio 0.0
        stats = cache.stats()
        assert stats == {"hits": 0, "misses": 0, "ratio": 0.0}

        cache.get(1)  # miss
        stats = cache.stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 1
        assert stats["ratio"] == 0.0

        cache.put(1, "one")
        cache.get(1)  # hit
        stats = cache.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["ratio"] == 0.5

    def test_capacity_validation(self):
        with pytest.raises(ValueError, match="Capacity must be at least 1"):
            LRUCache(0)
        with pytest.raises(ValueError):
            LRUCache(-5)

    def test_contains(self):
        cache = LRUCache(3)
        cache.put(1, "one")
        assert 1 in cache
        assert 2 not in cache

    def test_len_and_size(self):
        cache = LRUCache(5)
        assert len(cache) == 0
        assert cache.size == 0
        cache.put("k1", "v1")
        cache.put("k2", "v2")
        assert len(cache) == 2
        assert cache.size == 2

    def test_edge_case_capacity_one(self):
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.size == 1
        cache.put("b", 2)  # evicts a
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert len(cache) == 1

        # update b
        cache.put("b", 3)
        assert cache.size == 1
        assert cache.get("b") == 3

        # stats after operations
        assert cache.hits == 1   # get("b") was a hit after put
        assert cache.misses == 1 # get("a") was a miss