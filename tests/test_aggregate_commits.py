#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from datetime import datetime, timedelta, date
import collections
from github import Github, PaginatedList

from aggregateGithubCommits.aggregateGithubCommits import *


class TestAggregateCommits(object):
    def setup_method(self, method):
        self.commits_normal =       {'gregce': {'2020-05-13T08:58:46+0900': 1, '2020-05-06T02:17:27+0900': 1, '2020-04-29T05:27:18+0900': 1, '2020-04-22T01:16:31+0900': 1, '2020-04-15T01:43:41+0900': 1, '2020-04-08T01:35:51+0900': 1, '2020-04-01T00:56:34+0900': 1},\
                                     'hamelsmu': {'2020-04-03T02:23:19+0900': 1, '2020-04-03T01:42:23+0900': 1, '2020-04-03T01:41:41+0900': 1, '2020-04-03T01:20:21+0900': 1, '2020-04-03T00:18:38+0900': 1, '2020-04-02T15:29:27+0900': 1, '2020-04-02T15:29:15+0900': 1, '2020-04-02T15:26:21+0900': 1, '2020-04-02T15:24:02+0900': 1, '2020-04-02T15:23:35+0900': 1, '2020-04-02T15:22:40+0900': 1, '2020-04-02T13:50:02+0900': 1, '2020-04-02T13:49:36+0900': 1, '2020-04-02T13:46:52+0900': 1, '2020-04-02T13:45:26+0900': 1, '2020-04-02T13:20:51+0900': 1, '2020-04-02T13:04:18+0900': 1, '2020-04-02T12:59:07+0900': 1, '2020-04-02T12:57:48+0900': 1, '2020-04-02T09:59:37+0900': 1, '2020-04-02T09:53:49+0900': 1, '2020-04-02T09:50:51+0900': 1},\
                                     'github-actions[bot]': {'2020-04-02T10:00:19+0900': 1},\
                                     'DJedamski': {'2020-03-31T06:35:41+0900': 1}}
        self.commits_1author =       {'DJedamski': {'2020-03-31T06:35:41+0900': 1}}
        self.commits_invalid_date = {'gregce': {'2020-05-13T08:58:46+0900': 1, '2020-05-06T02:17:27+0900': 1, '2020-04-29T05:27:18+0900': 1, '2020-04-22T01:16:31+0900': 1, '2020-04-15T01:43:41+0900': 1, '2020-04-08T01:35:51+0900': 1, '2020-04-01T00:56:34+0900': 1},\
                                     'hamelsmu': {'2020-04-03T02:23:19+0900': 1, '2020-04-03T01:42:23+0900': 1, '2020-04-03T01:41:41+0900': 1, '2020-04-03T01:20:21+0900': 1, '2020-04-03T00:18:38+0900': 1, '2020-04-02T15:29:27+0900': 1, '2020-04-02T15:29:15+0900': 1, '2020-04-02T15:26:21+0900': 1, '2020-04-02T15:24:02+0900': 1, '2020-04-02T15:23:35+0900': 1, '2020-04-02T15:22:40+0900': 1, '2020-04-02T13:50:02+0900': 1, '2020-04-02T13:49:36+0900': 1, '2020-04-02T13:46:52+0900': 1, '2020-04-02T13:45:26+0900': 1, '2020-04-02T13:20:51+0900': 1, '2020-04-02T13:04:18+0900': 1, '2020-04-02T12:59:07+0900': 1, '2020-04-02T12:57:48+0900': 1, '2020-04-02T09:59:37+0900': 1, '2020-04-02T09:53:49+0900': 1, '2020-04-02T09:50:51+0900': 1},\
                                     'github-actions[bot]': {'2020-04-02T10:00:19+0900': 1},\
                                     'DJedamski': {'2020-02-30T06:35:41+0900': 1}}
        self.commits_invalid_num =  {'gregce': {'2020-05-13T08:58:46+0900': 1, '2020-05-06T02:17:27+0900': 1, '2020-04-29T05:27:18+0900': 1, '2020-04-22T01:16:31+0900': 1, '2020-04-15T01:43:41+0900': 1, '2020-04-08T01:35:51+0900': 1, '2020-04-01T00:56:34+0900': 1},\
                                     'hamelsmu': {'2020-04-03T02:23:19+0900': 1, '2020-04-03T01:42:23+0900': 1, '2020-04-03T01:41:41+0900': 1, '2020-04-03T01:20:21+0900': 1, '2020-04-03T00:18:38+0900': 1, '2020-04-02T15:29:27+0900': 1, '2020-04-02T15:29:15+0900': 1, '2020-04-02T15:26:21+0900': 1, '2020-04-02T15:24:02+0900': 1, '2020-04-02T15:23:35+0900': 1, '2020-04-02T15:22:40+0900': 1, '2020-04-02T13:50:02+0900': 1, '2020-04-02T13:49:36+0900': 1, '2020-04-02T13:46:52+0900': 1, '2020-04-02T13:45:26+0900': 1, '2020-04-02T13:20:51+0900': 1, '2020-04-02T13:04:18+0900': 1, '2020-04-02T12:59:07+0900': 1, '2020-04-02T12:57:48+0900': 1, '2020-04-02T09:59:37+0900': 1, '2020-04-02T09:53:49+0900': 1, '2020-04-02T09:50:51+0900': 1},\
                                     'github-actions[bot]': {'2020-04-02T10:00:19+0900': 1},\
                                     'DJedamski': {'2020-03-31T06:35:41+0900': 'x'}}
        self.commits_negative_num =  {'gregce': {'2020-05-13T08:58:46+0900': 1, '2020-05-06T02:17:27+0900': 1, '2020-04-29T05:27:18+0900': 1, '2020-04-22T01:16:31+0900': 1, '2020-04-15T01:43:41+0900': 1, '2020-04-08T01:35:51+0900': 1, '2020-04-01T00:56:34+0900': 1},\
                                     'hamelsmu': {'2020-04-03T02:23:19+0900': 1, '2020-04-03T01:42:23+0900': 1, '2020-04-03T01:41:41+0900': 1, '2020-04-03T01:20:21+0900': 1, '2020-04-03T00:18:38+0900': 1, '2020-04-02T15:29:27+0900': 1, '2020-04-02T15:29:15+0900': 1, '2020-04-02T15:26:21+0900': 1, '2020-04-02T15:24:02+0900': 1, '2020-04-02T15:23:35+0900': 1, '2020-04-02T15:22:40+0900': 1, '2020-04-02T13:50:02+0900': 1, '2020-04-02T13:49:36+0900': 1, '2020-04-02T13:46:52+0900': 1, '2020-04-02T13:45:26+0900': 1, '2020-04-02T13:20:51+0900': 1, '2020-04-02T13:04:18+0900': 1, '2020-04-02T12:59:07+0900': 1, '2020-04-02T12:57:48+0900': 1, '2020-04-02T09:59:37+0900': 1, '2020-04-02T09:53:49+0900': 1, '2020-04-02T09:50:51+0900': 1},\
                                     'github-actions[bot]': {'2020-04-02T10:00:19+0900': 1},\
                                     'DJedamski': {'2020-03-31T06:35:41+0900': -1}}

    def test_period_hour_normal(self):
        dataframe = aggregate_commits(self.commits_normal, "h")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").hour for v1 in self.commits_normal.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_normal.keys())
        assert set(dataframe["Indexes"]) == set(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])
    def test_period_day_normal(self):
        dataframe = aggregate_commits(self.commits_normal, "d")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d") for v1 in self.commits_normal.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_normal.keys())
        assert set(dataframe["Indexes"]) == set([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d") for v1 in self.commits_normal.values() for k2,v2 in v1.items()])
    def test_period_month_normal(self):
        dataframe = aggregate_commits(self.commits_normal, "m")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m") for v1 in self.commits_normal.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_normal.keys())
        assert set(dataframe["Indexes"]) == set([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m") for v1 in self.commits_normal.values() for k2,v2 in v1.items()])
    def test_period_weekday_normal(self):
        dataframe = aggregate_commits(self.commits_normal, "w")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").weekday() for v1 in self.commits_normal.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_normal.keys())
        assert set(dataframe["Indexes"]) == set(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    def test_1author_period_hour_normal(self):
        dataframe = aggregate_commits(self.commits_1author, "h")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").hour for v1 in self.commits_1author.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_1author.keys())
        assert set(dataframe["Indexes"]) == set(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])
    def test_1author_period_day_normal(self):
        dataframe = aggregate_commits(self.commits_1author, "d")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d") for v1 in self.commits_1author.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_1author.keys())
        assert set(dataframe["Indexes"]) == set([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d") for v1 in self.commits_1author.values() for k2,v2 in v1.items()])
    def test_p1author_eriod_month_normal(self):
        dataframe = aggregate_commits(self.commits_1author, "m")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m") for v1 in self.commits_1author.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_1author.keys())
        assert set(dataframe["Indexes"]) == set([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m") for v1 in self.commits_1author.values() for k2,v2 in v1.items()])
    def test_1author_period_weekday_normal(self):
        dataframe = aggregate_commits(self.commits_1author, "w")
        assert type(dataframe) is dict
        assert type(dataframe["AggregatedCommits"]) is dict
        assert type(dataframe["CommitCount"]) is int
        assert type(dataframe["Authors"]) is list
        assert type(dataframe["Indexes"]) is list
        assert dataframe["CommitCount"] == sum(collections.Counter([datetime.strptime(k2, "%Y-%m-%dT%H:%M:%S%z").weekday() for v1 in self.commits_1author.values() for k2,v2 in v1.items()]).values())
        assert set(dataframe["Authors"]) == set(self.commits_1author.keys())
        assert set(dataframe["Indexes"]) == set(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    def test_no_author_error(self):
        with pytest.raises(ValueCleansingError) as e:
            dataframe = aggregate_commits({}, "m")
    def test_period_invalid_error(self):
        with pytest.raises(AugumentError) as e:
            dataframe = aggregate_commits(self.commits_normal, "x")
    def test_none_period_error(self):
        with pytest.raises(AugumentError) as e:
            dataframe = aggregate_commits(self.commits_normal, None)
    def test_invalid_date_error(self):
        with pytest.raises(ValueError) as e:
            dataframe = aggregate_commits(self.commits_invalid_date, "d")
    def test_invalid_num_error(self):
        with pytest.raises(ValueCleansingError) as e:
            dataframe = aggregate_commits(self.commits_invalid_num, "m")
    def test_negative_number_error(self):
        with pytest.raises(ValueCleansingError) as e:
            dataframe = aggregate_commits(self.commits_negative_num, "m")
    def test_none_data_error(self):
        with pytest.raises(ValueCleansingError) as e:
            dataframe = aggregate_commits(None, "m")
