
import pytest

from pathlib import Path
import os
import sys
import datetime
from dateutil.parser import parse as parse_datetime

import pypipe

from pypipe.core.task.base import Task


import logging
from importlib import reload


def copy_file_to_tmpdir(tmpdir, source_file, target_path):
    target_path = Path(target_path)
    source_path = Path(os.path.dirname(__file__)) / "test_files" / source_file

    fh = tmpdir.join(target_path.name)
    with open(source_path) as f:
        fh.write(f.read())
    return fh

@pytest.fixture
def script_files(tmpdir):
    for folder in Path("scripts").parts:
        tmpdir = tmpdir.mkdir(folder)
    
    copy_file_to_tmpdir(tmpdir, source_file="succeeding_script.py", target_path="scripts/succeeding_script.py")
    copy_file_to_tmpdir(tmpdir, source_file="failing_script.py", target_path="scripts/failing_script.py")
    copy_file_to_tmpdir(tmpdir, source_file="parameterized_script.py", target_path="scripts/parameterized_script.py")


@pytest.fixture(scope="session", autouse=True)
def reset_loggers():
    #reload(pypipe)
    # prepare something ahead of all tests
    # request.addfinalizer(finalizer_function)

    pypipe.session.reset()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(action)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    task_logger = logging.getLogger(Task._logger_basename)
    task_logger.addHandler(handler)
    #Task.add_logger_handler(handler)
    yield
    pypipe.session.reset()


class mockdatetime(datetime.datetime):
    _freezed_datetime = None
    @classmethod
    def now(cls):
        return cls._freezed_datetime

@pytest.fixture
def mock_datetime_now(monkeypatch):
    """Monkey patch datetime.datetime.now
    Returns a function that takes datetime as string as input
    and sets that to datetime.datetime.now()"""
    class mockdatetime(datetime.datetime):
        _freezed_datetime = None
        @classmethod
        def now(cls):
            return cls._freezed_datetime

    def wrapper(dt):
        mockdatetime._freezed_datetime = parse_datetime(dt)
        monkeypatch.setattr(datetime, 'datetime', mockdatetime)

    return wrapper