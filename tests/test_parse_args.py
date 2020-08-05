#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import os
from datetime import datetime, timedelta, date

from aggregateGithubCommits.aggregateGithubCommits import *


class TestParseArgs(object):
    def setup_method(self, method):
        #
        # Causion: Please set your GitHub Personal access token as envionment variable 'GITHUBTOKEN'
        #
        assert 'GITHUBTOKEN' in os.environ
        self.github_token = os.environ['GITHUBTOKEN']
        self.repo = "github/covid-19-repo-data"

    def test_set_since_term_1_normal(self):
        github_token, args = check_args(["--since", "2020-01-31", "--repo", self.repo])
        since = parse_args(args)
        assert since == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")
    def test_set_since_term_2_normal(self):
        github_token, args = check_args(["--term", "6m", "--repo", self.repo])
        since = parse_args(args)
        assert since == (datetime.now() - relativedelta(months=6)).strftime("%Y-%m-%d 00:00:00")
    def test_set_since_term_3_normal(self):
        github_token, args = check_args(["--term", "30d", "--repo", self.repo])
        since = parse_args(args)
        assert since == (datetime.now() - relativedelta(days=30)).strftime("%Y-%m-%d 00:00:00")
    def test_set_since_term_4_normal(self):
        github_token, args = check_args(["--term", "30d", "--until", "2020-03-31", "--repo", self.repo])
        since = parse_args(args)
        assert since == "2020-03-01 00:00:00"
    def test_set_since_term_5_normal(self):
        github_token, args = check_args(["--term", "6m", "--until", "2020-03-31", "--repo", self.repo])
        since = parse_args(args)
        assert since == "2019-09-30 00:00:00"
    def test_set_since_term_6_normal(self):
        github_token, args = check_args(["--term", "6m", "--until", "2020-02-29", "--repo", self.repo])
        since = parse_args(args)
        assert since == "2019-08-29 00:00:00"
