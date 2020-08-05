#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import os
from datetime import datetime, timedelta, date
from github import Github, PaginatedList

from aggregateGithubCommits.aggregateGithubCommits import *


class TestExtractCommits(object):
    def setup_method(self, method):
        #
        # Causion: Please set your GitHub Personal access token as envionment variable 'GITHUBTOKEN'
        #
        assert 'GITHUBTOKEN' in os.environ
        self.github_token = os.environ['GITHUBTOKEN']
        self.repo = "github/covid-19-repo-data"

    def test_notset_author_normal(self):
        result, _ = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        commits = extract_commits(result)
        assert type(commits) is dict
        assert len(commits) == sum(1 for x in commits)
    def test_set_author_normal(self):
        result, _ = get_commits(self.github_token, self.repo, "hamelsmu", "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        commits = extract_commits(result)
        assert type(commits) is dict
        assert len(commits) == sum(1 for x in commits)
    def test_nodata_normal(self):
        result, _ = get_commits(self.github_token, self.repo, "hamelsmu", "2020-05-16 23:59:59", "2020-01-31 00:00:00")
        commits = extract_commits(result)
        assert type(commits) is dict
        assert len(commits) == sum(1 for x in commits)
        assert len(commits) == 0
    # TODO: How should change Commit object data?
    ''' 
    def test_no_authorid_normal(self):
        result, _ = get_commits(self.github_token, self.repo, None, "2020-01-31 00:00:00", "2020-05-16 23:59:59")
        print(type(result))
        assert result.totalCount == sum(1 for x in result)
        i=0
        for item in result:
            print(item.author.login)
            print(item.commit.author.name)
            if item.author.login == "hamelsmu":
                print(result[i].author.login)
                del result[i]["author"]
                break
            else:
                i += 1
        commits = extract_commits(result)
        assert "hamelsmu" not in commits.keys()
        assert "Hamel Husain" in commits.keys()
    '''
