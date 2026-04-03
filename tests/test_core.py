from pyxa_integration.controller.core import ExecutionController
from pyxa_integration.perception.delta import hamming_distance, screen_changed
from pyxa_integration.research.compatible_repos import recommend_for_windows_i5_16gb


def test_hamming_distance():
    assert hamming_distance("aaaa", "aaab") == 1


def test_screen_changed_threshold():
    assert screen_changed("abcd", "abcf", threshold=1)


def test_controller_sets_completed_state():
    controller = ExecutionController()
    ran = []

    def step():
        ran.append(True)

    controller.run_plan([step])
    assert ran == [True]
    assert controller.active_step == "completed"


def test_recommendations_non_empty():
    repos = recommend_for_windows_i5_16gb()
    assert len(repos) >= 5
