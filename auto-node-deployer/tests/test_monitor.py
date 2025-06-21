import pytest
from utils.monitor import is_process_running

def test_is_process_running_false():
    # Should not find a nonsense process
    assert not is_process_running("definitelynotarealprocess") 