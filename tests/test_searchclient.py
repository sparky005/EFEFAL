import pytest

def test_timestamp_sort(client, dummy_hits):
    sorted_hits = client.timestamp_sort(dummy_hits)
    assert isinstance(sorted_hits, list)
    assert sorted_hits != dummy_hits, "Sorted list is probably different than unsorted list"
    assert len(sorted_hits) == len(dummy_hits), "Sorted list should have the same length"
    assert len(sorted_hits) == 14, "Length of sorted hits should be 14"

def test_remove_tasklist_duplicates(client, dummy_hits):
    deduped_hits = client.remove_tasklist_duplicates(dummy_hits)
    assert isinstance(deduped_hits, list), "taskslist removal should return list"
    assert deduped_hits != dummy_hits, "Tasklist removal should alter list"
    assert len(deduped_hits) <= len(dummy_hits), "Deduped list should be <= original"
    assert len(deduped_hits) == 7, "Here, list should be half the size of original"

def test_calculate_totals(client, dummy_hits, dummy_finish):
    pass
