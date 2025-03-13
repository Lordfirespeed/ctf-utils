from pathlib import Path

project_source_dirname = Path(__file__).parent
project_dirname = project_source_dirname.parent
project_tests_dirname = Path(project_dirname, "tests")
project_cache_dirname = Path(project_dirname, "cache")

__all__ = (
    "project_dirname",
    "project_source_dirname",
    "project_tests_dirname",
    "project_cache_dirname",
)
