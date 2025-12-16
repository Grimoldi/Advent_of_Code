import day_01

FIRST_EXAMPLE = "01_first_example"


def test_load_data() -> None:
    numbers = day_01._build_data(FIRST_EXAMPLE)
    expected_result = ([1, 2, 3, 3, 3, 4], [3, 3, 3, 4, 5, 9])
    assert numbers == expected_result


def test_first_question() -> None:
    """Test the first question."""
    total_distance = day_01._find_total_distance(FIRST_EXAMPLE)
    assert total_distance == 11


def test_second_question() -> None:
    """Test the second question."""
    total_similarity = day_01._find_total_similarity_score(FIRST_EXAMPLE)
    assert total_similarity == 31
