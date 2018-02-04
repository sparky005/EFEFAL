import pytest

def test_timestamp_sort(client, dummy_hits):
    sorted_hits = client.timestamp_sort(dummy_hits)
    assert sorted_hits != dummy_hits, "Sorted list is probably different than unsorted list"
    assert len(sorted_hits) == len(dummy_hits), "Sorted list should have the same length"

