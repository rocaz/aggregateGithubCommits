#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import os
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from aggregateGithubCommits.aggregateGithubCommits import *


class TestCheckArgs(object):
    def setup_method(self, method):
        #
        # Causion: Please set your GitHub Personal access token as envionment variable 'GITHUBTOKEN'
        #
        assert 'GITHUBTOKEN' in os.environ
        self.github_token = os.environ['GITHUBTOKEN']
        self.repo = "github/covid-19-repo-data"
 
    def test_GitHubToken_error(self):
        with pytest.raises(GitHubTokenError) as e:
            if 'GITHUBTOKEN' in os.environ:
                del os.environ['GITHUBTOKEN']
            github_token, args = check_args([])
        assert "Plese set 'GITHUBTOKEN' environment variable for access to GitHub." in str(e.value)
        os.environ['GITHUBTOKEN'] = self.github_token
    def test_no_repo_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args([])
        assert e.value.code == 2
    def test_exist_repo_1_normal(self):
        github_token, args = check_args(["--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_exist_repo_2_normal(self):
        github_token, args = check_args(["-r", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_author_1_normal(self):
        github_token, args = check_args(["--author", "dummy_author", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == "dummy_author"
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_author_2_normal(self):
        github_token, args = check_args(["-a", "dummy_author", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == "dummy_author"
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_since_1_normal(self):
        github_token, args = check_args(["--since", "2020-01-31", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since.strftime("%Y-%m-%d") == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d")
        assert args.term == None
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_since_2_normal(self):
        github_token, args = check_args(["-s", "2020-01-31", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since.strftime("%Y-%m-%d") == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d")
        assert args.term == None
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_since_3_normal(self):
        github_token, args = check_args(["-s", "2020-02-29", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since.strftime("%Y-%m-%d") == datetime.strptime("2020-02-29", "%Y-%m-%d").strftime("%Y-%m-%d")
        assert args.term == None
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_since_1_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["-s", "dummy_since", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_since_2_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["-s", "2019-02-29", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_until_1_normal(self):
        github_token, args = check_args(["--until", "2020-01-31", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d")
    def test_set_until_2_normal(self):
        github_token, args = check_args(["-u", "2020-01-31", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d")
    def test_set_until_3_normal(self):
        github_token, args = check_args(["-u", "2020-02-29", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.strptime("2020-02-29", "%Y-%m-%d").strftime("%Y-%m-%d")
    def test_set_until_1_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["-u", "dummy_since", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_until_2_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["-u", "2019-02-29", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_since_until_1_normal(self):
        github_token, args = check_args(["--since", "2020-01-31", "--until", "2020-05-16", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since.strftime("%Y-%m-%d") == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d")
        assert args.term == None
        assert args.until.strftime("%Y-%m-%d") == datetime.strptime("2020-05-16", "%Y-%m-%d").strftime("%Y-%m-%d")
    def test_set_since_until_2_normal(self):
        github_token, args = check_args(["-s", "2020-01-31", "-u", "2020-05-16", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since.strftime("%Y-%m-%d") == datetime.strptime("2020-01-31", "%Y-%m-%d").strftime("%Y-%m-%d")
        assert args.term == None
        assert args.until.strftime("%Y-%m-%d") == datetime.strptime("2020-05-16", "%Y-%m-%d").strftime("%Y-%m-%d")
    def test_set_term_1_normal(self):
        github_token, args = check_args(["--term", "1d", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "1d"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_term_2_normal(self):
        github_token, args = check_args(["-t", "1d", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "1d"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_term_3_normal(self):
        github_token, args = check_args(["--term", "123d", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "123d"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_term_4_normal(self):
        github_token, args = check_args(["--term", "5000m", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "5000m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_term_5_normal(self):
        github_token, args = check_args(["--term", "0050m", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "0050m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_term_1_error(self):
        with pytest.raises(AugumentError) as e:
            github_token, args = check_args(["--term", "9y", "--repo", self.repo])
    def test_set_term_2_error(self):
        with pytest.raises(AugumentError) as e:
            github_token, args = check_args(["--term", "79", "--repo", self.repo])
    def test_set_term_3_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["--term", "-68m", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_period_1_normal(self):
        github_token, args = check_args(["--period", "h", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_period_2_normal(self):
        github_token, args = check_args(["-p", "h", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_period_3_normal(self):
        github_token, args = check_args(["--period", "d", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "d"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_period_4_normal(self):
        github_token, args = check_args(["--period", "m", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "m"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_period_5_normal(self):
        github_token, args = check_args(["--period", "w", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "w"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_period_1_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["--period", "H", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_period_2_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["--period", "x", "--repo", self.repo])
        assert e.value.code == 2
    def test_set_formattype_1_normal(self):
        github_token, args = check_args(["--format", "text", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_formattype_2_normal(self):
        github_token, args = check_args(["-f", "text", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "text"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_formattype_3_normal(self):
        github_token, args = check_args(["--format", "json", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "json"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_formattype_4_normal(self):
        github_token, args = check_args(["--format", "csv", "--repo", self.repo])
        assert github_token == os.environ['GITHUBTOKEN']
        assert args.repo == self.repo
        assert args.author == None
        assert args.format_type == "csv"
        assert args.period == "h"
        assert args.since == None
        assert args.term == "3m"
        assert args.until.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")
    def test_set_formattype_1_error(self):
        with pytest.raises(SystemExit) as e:
            github_token, args = check_args(["--format", "dummy", "--repo", self.repo])
        assert e.value.code == 2
