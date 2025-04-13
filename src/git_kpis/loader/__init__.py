"""A source loading player profiles and games from chess.com api"""

from typing import Iterator, List, Sequence

import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
import git


# TODO: add branch argument (default is main)
@dlt.source(name="git")
def source(repos: List[str]) -> Sequence[DltResource]:
    """ """
    Repos = [git.Repo(repo_path) for repo_path in repos]
    return (
        git_commit_info(Repos),
        git_commit_total_stats(Repos),
        git_commit_file_stats(Repos),
    )


@dlt.resource(
    write_disposition="replace",
    columns={
        "binsha": {"data_type": "text"},
        "repo_dir": {"data_type": "text"},
        "date": {"data_type": "timestamp"},
        "message": {"data_type": "text"},
        "author": {"data_type": "text"},
    },
)
def git_commit_info(repos: List[git.Repo]) -> Iterator[TDataItem]:
    """
    Yields player profiles for a list of player usernames.
    Args:
        repos (List[str]): List of directories to retrieve stats for.
    Yields:
        Iterator[TDataItem]: An iterator over commits.
    """
    for repo in repos:
        for commit in repo.iter_commits():
            yield {
                "binsha": str(commit.binsha),
                "repo_dir": commit.repo.git_dir,
                "date": commit.committed_date,
                "message": commit.message,
                "author": commit.author.name,
            }


@dlt.resource(
    write_disposition="replace",
    columns={
        "binsha": {"data_type": "text"},
        "repo_dir": {"data_type": "text"},
        "total_insertions": {"data_type": "bigint"},
        "total_deletions": {"data_type": "bigint"},
        "total_lines": {"data_type": "bigint"},
        "total_files": {"data_type": "bigint"},
    },
)
def git_commit_total_stats(repos: List[git.Repo]) -> Iterator[TDataItem]:
    """
    Yields commit info from a list of git directories.
    Args:
        repos (List[str]): List of directories to retrieve stats for.
    Yields:
        Iterator[TDataItem]: An iterator over commits.
    """
    for repo in repos:
        for commit in repo.iter_commits():
            yield {
                "binsha": str(commit.binsha),
                "repo_dir": commit.repo.git_dir,
            } | {f"total_{k}": v for (k, v) in commit.stats.total.items()}


@dlt.resource(
    write_disposition="replace",
    columns={
        "binsha": {"data_type": "text"},
        "repo_dir": {"data_type": "text"},
        "file": {"data_type": "text"},
        "insertions": {"data_type": "bigint"},
        "deletions": {"data_type": "bigint"},
        "lines": {"data_type": "bigint"},
        "change_type": {"data_type": "text"},
    },
)
def git_commit_file_stats(repos: List[git.Repo]) -> Iterator[TDataItem]:
    """
    Yields commit info from a list of git directories.
    Args:
        repos (List[str]): List of directories to retrieve stats for.
    Yields:
        Iterator[TDataItem]: An iterator over commits.
    """
    for repo in repos:
        for commit in repo.iter_commits():
            for file, stats in commit.stats.files.items():
                yield (
                    {
                        "binsha": str(commit.binsha),
                        "repo_dir": commit.repo.git_dir,
                    }
                    | {"file": file}
                    | stats
                )
