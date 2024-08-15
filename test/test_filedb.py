from entangled.filedb import file_db, stat
from time import sleep
from pathlib import Path
import pytest
from contextlib import chdir


@pytest.fixture(scope="session")
def example_files(tmp_path_factory: pytest.TempPathFactory):
    tmp_path = tmp_path_factory.mktemp("test-filedb")
    with open(tmp_path / "a", "w") as f:
        f.write("hello")
    # modification times of b, c, and d need to be later than a
    sleep(0.02)
    with open(tmp_path / "b", "w") as f:
        f.write("hello")
    with open(tmp_path / "c", "w") as f:
        f.write("goodbye")
    with open(tmp_path / "d", "w") as f:
        f.write("earth")
    return tmp_path


def test_stat(example_files: Path):
    with chdir(example_files):
        stat_a = stat(example_files / "a")
        stat_b = stat(example_files / "b")
        stat_c = stat(example_files / "c")
        assert stat_a == stat_b
        assert stat_c != stat_b
        assert stat_a < stat_b


def test_filedb(example_files: Path):
    with chdir(example_files):
        with file_db() as db:
            for n in "abcd":
                db.update(Path(n))

        with open(example_files / "d", "w") as f:
            f.write("mars")

        with file_db() as db:
            assert db.changed() == [Path("d")]
            db.update(Path("d"))
            assert db.changed() == []
