import dlt
from git_kpis.loader import source
from typing import List
import sys


def load_git_commit_info(repo_dir: List[str]) -> None:
    """Constructs a pipeline that will load chess games of specific players for a range of months."""

    # configure the pipeline: provide the destination and dataset name to which the data should go
    pipeline = dlt.pipeline(
        pipeline_name="git_kpis_pipeline", dataset_name="git_commit_data"
    )
    data = source(repo_dir)
    info = pipeline.run(
        data.with_resources(
            "git_commit_info", "git_commit_total_stats", "git_commit_file_stats"
        )
    )
    print(info)


# could make a few tables:
# files changed over time - both total and by repo (window function?)
# lines changed over time - both total and by repo (window function?)
# Focus by commit type/topic (conventional commits) (over time) - both total and by repo (window function?)
# total no. of commits

if __name__ == "__main__":
    load_git_commit_info(sys.argv[1:])
