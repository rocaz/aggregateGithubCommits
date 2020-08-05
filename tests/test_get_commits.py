#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import os
from datetime import datetime, timedelta, date
from github import Github, PaginatedList

from aggregateGithubCommits.aggregateGithubCommits import *


class TestGetCommits(object):
    def setup_method(self, method):
        #
        # Causion: Please set your GitHub Personal access token as envionment variable 'GITHUBTOKEN'
        #
        assert 'GITHUBTOKEN' in os.environ
        self.github_token = os.environ['GITHUBTOKEN']
        self.repo = "github/covid-19-repo-data"
        self.git_url = "git://github.com/github/covid-19-repo-data.git"

    def test_notset_author_normal(self):
        result, url = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        assert type(result) is PaginatedList.PaginatedList
        assert result.totalCount == sum(1 for x in result)
        assert url == self.git_url
    def test_set_author_normal(self):
        result, url  = get_commits(self.github_token, self.repo, "hamelsmu", "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        assert type(result) is PaginatedList.PaginatedList
        assert result.totalCount == sum(1 for x in result)
        assert url == self.git_url
    def test_invalid_token_error(self):
        with pytest.raises(GithubException) as e:
            result, _ = get_commits("dummy_token", self.repo, None, "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        assert e.value.status == 401
    def test_invalid_repo_error(self):
        with pytest.raises(GithubException) as e:
            result, _ = get_commits(self.github_token, "invalid_repo", None, "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        assert e.value.status == 404
    def test_invalid_author_error(self):
        with pytest.raises(GithubException) as e:
            result, _ = get_commits(self.github_token, self.repo, "invalid_author", "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        assert e.value.status == 404
    def test_no_since_error(self):
        with pytest.raises(TypeError) as e:
            result, _ = get_commits(self.github_token, self.repo, None, None, "2020-05-16 23:59:59")
    def test_no_until_error(self):
        with pytest.raises(TypeError) as e:
            result, _ = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:00", None)
    def test_invalid_since_1_error(self):
        with pytest.raises(ValueError) as e:
            result, _ = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:61", "2020-05-16 23:59:59")
    def test_invalid_since_2_error(self):
        with pytest.raises(ValueError) as e:
            result, _ = get_commits(self.github_token, self.repo, None, "dummy_since", "2020-05-16 23:59:59")
    def test_invalid_until_1_error(self):
        with pytest.raises(ValueError) as e:
            result, _ = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:00", "2019-02-29 23:59:59")
    def test_invalid_until_2_error(self):
        with pytest.raises(ValueError) as e:
            result, _ = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:00", "dummy_until")
    def test_reverse_since_and_until_error(self):
        result, url = get_commits(self.github_token, self.repo, None, "2020-05-16 23:59:59", "2020-01-31 00:00:00")
        assert 0 == result.totalCount
        assert result.totalCount == sum(1 for x in result)
        assert url == self.git_url
