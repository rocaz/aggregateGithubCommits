#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import copy
from github import Github, PaginatedList

from aggregateGithubCommits.aggregateGithubCommits import *


class TestConvertToText(object):
    def setup_method(self, method):
        self.git_url = "git://github.com/github/covid-19-repo-data.git"
        self.dataframe_hour_normal =    {'AggregatedCommits':
                                        {'gregce': {'00': 1, '01': 3, '02': 1, '05': 1, '06': 0, '08': 1, '09': 0, '10': 0, '12': 0, '13': 0, '15': 0},
                                        'hamelsmu': {'00': 1, '01': 3, '02': 1, '05': 0, '06': 0, '08': 0, '09': 3, '10': 0, '12': 2, '13': 6, '15': 6},
                                        'github-actions[bot]': {'00': 0, '01': 0, '02': 0, '05': 0, '06': 0, '08': 0, '09': 0, '10': 1, '12': 0, '13': 0, '15': 0},
                                        'DJedamski': {'00': 0, '01': 0, '02': 0, '05': 0, '06': 1, '08': 0, '09': 0, '10': 0, '12': 0, '13': 0, '15': 0}},
                                        'Period': 'h', 'CommitCount': 31, 'Authors': ['gregce', 'hamelsmu', 'github-actions[bot]', 'DJedamski'],
                                        'Indexes': ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']}
        self.dataframe_day_normal =     {'AggregatedCommits':
                                        {'gregce': {'2020-03-31': 0, '2020-04-01': 1, '2020-04-02': 0, '2020-04-03': 0, '2020-04-08': 1, '2020-04-15': 1, '2020-04-22': 1, '2020-04-29': 1, '2020-05-06': 1, '2020-05-13': 1},
                                        'hamelsmu': {'2020-03-31': 0, '2020-04-01': 0, '2020-04-02': 17, '2020-04-03': 5, '2020-04-08': 0, '2020-04-15': 0, '2020-04-22': 0, '2020-04-29': 0, '2020-05-06': 0, '2020-05-13': 0},
                                        'github-actions[bot]': {'2020-03-31': 0, '2020-04-01': 0, '2020-04-02': 1, '2020-04-03': 0, '2020-04-08': 0, '2020-04-15': 0, '2020-04-22': 0, '2020-04-29': 0, '2020-05-06': 0, '2020-05-13': 0},
                                        'DJedamski': {'2020-03-31': 1, '2020-04-01': 0, '2020-04-02': 0, '2020-04-03': 0, '2020-04-08': 0, '2020-04-15': 0, '2020-04-22': 0, '2020-04-29': 0, '2020-05-06': 0, '2020-05-13': 0}},
                                        'Period': 'd', 'CommitCount': 31, 'Authors': ['gregce', 'hamelsmu', 'github-actions[bot]', 'DJedamski'],
                                        'Indexes': ['2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-08', '2020-04-15', '2020-04-22', '2020-04-29', '2020-05-06', '2020-05-13']}
        self.dataframe_month_normal =   {'AggregatedCommits':
                                        {'gregce': {'2020-03': 0, '2020-04': 5, '2020-05': 2},
                                        'hamelsmu': {'2020-03': 0, '2020-04': 22, '2020-05': 0},
                                        'github-actions[bot]': {'2020-03': 0, '2020-04': 1, '2020-05': 0},
                                        'DJedamski': {'2020-03': 1, '2020-04': 0, '2020-05': 0}},
                                        'Period': 'm', 'CommitCount': 31, 'Authors': ['gregce', 'hamelsmu', 'github-actions[bot]', 'DJedamski'],
                                        'Indexes': ['2020-03', '2020-04', '2020-05']}
        self.dataframe_weekday_normal = {'AggregatedCommits':
                                        {'gregce': {'Tue': 0, 'Wed': 7, 'Thu': 0, 'Fri': 0},
                                        'hamelsmu': {'Tue': 0, 'Wed': 0, 'Thu': 17, 'Fri': 5},
                                        'github-actions[bot]': {'Tue': 0, 'Wed': 0, 'Thu': 1, 'Fri': 0},
                                        'DJedamski': {'Tue': 1, 'Wed': 0, 'Thu': 0, 'Fri': 0}},
                                        'Period': 'w', 'CommitCount': 31, 'Authors': ['gregce', 'hamelsmu', 'github-actions[bot]', 'DJedamski'],
                                        'Indexes': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']}
        

    def test_period_hour_normal(self):
        dataframe = self.dataframe_hour_normal
        text_lines = convert_to_text(dataframe, self.git_url)
        assert type(text_lines) is list
        assert self.git_url == text_lines[0].replace("Repository:","").replace(" ","")
        assert str(dataframe["CommitCount"]) == text_lines[1].replace("Total:","").replace(" ","")
        line_cnt=0
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            assert k in text_lines[2 + i + line_cnt]
            d = dict(zip([h for h in text_lines[2 + i + line_cnt + 1].replace("Hour","").split(" ") if h != ""], [v for v in text_lines[2 + i + line_cnt + 2].replace("Count","").split(" ") if v != ""]))
            for k1 in dataframe["AggregatedCommits"][k].keys():
                assert int(d[k1]) == dataframe["AggregatedCommits"][k][k1]
            assert str(sum([int(v) for v in d.values()])) == text_lines[2 + i + line_cnt + 3].replace("AuthorTotal:","").replace(" ","")
            line_cnt += 3
    def test_period_day_normal(self):
        dataframe = self.dataframe_day_normal
        text_lines = convert_to_text(dataframe, self.git_url)
        assert type(text_lines) is list
        assert self.git_url == text_lines[0].replace("Repository:","").replace(" ","")
        assert str(dataframe["CommitCount"]) == text_lines[1].replace("Total:","").replace(" ","")
        line_cnt=0
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            assert k in text_lines[2 + i + line_cnt]
            d = dict(zip([h for h in text_lines[2 + i + line_cnt + 1].replace("Day","").split(" ") if h != ""], [v for v in text_lines[2 + i + line_cnt + 2].replace("Count","").split(" ") if v != ""]))
            for k1 in dataframe["AggregatedCommits"][k].keys():
                assert int(d[k1]) == dataframe["AggregatedCommits"][k][k1]
            assert str(sum([int(v) for v in d.values()])) == text_lines[2 + i + line_cnt + 3].replace("AuthorTotal:","").replace(" ","")
            line_cnt += 3
    def test_period_month_normal(self):
        dataframe = self.dataframe_month_normal
        text_lines = convert_to_text(dataframe, self.git_url)
        assert type(text_lines) is list
        assert self.git_url == text_lines[0].replace("Repository:","").replace(" ","")
        assert str(dataframe["CommitCount"]) == text_lines[1].replace("Total:","").replace(" ","")
        line_cnt=0
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            assert k in text_lines[2 + i + line_cnt]
            d = dict(zip([h for h in text_lines[2 + i + line_cnt + 1].replace("Month","").split(" ") if h != ""], [v for v in text_lines[2 + i + line_cnt + 2].replace("Count","").split(" ") if v != ""]))
            for k1 in dataframe["AggregatedCommits"][k].keys():
                assert int(d[k1]) == dataframe["AggregatedCommits"][k][k1]
            assert str(sum([int(v) for v in d.values()])) == text_lines[2 + i + line_cnt + 3].replace("AuthorTotal:","").replace(" ","")
            line_cnt += 3
    def test_period_weekday_normal(self):
        dataframe = self.dataframe_weekday_normal
        text_lines = convert_to_text(dataframe, self.git_url)
        assert type(text_lines) is list
        assert self.git_url == text_lines[0].replace("Repository:","").replace(" ","")
        assert str(dataframe["CommitCount"]) == text_lines[1].replace("Total:","").replace(" ","")
        line_cnt=0
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            assert k in text_lines[2 + i + line_cnt]
            d = dict(zip([h for h in text_lines[2 + i + line_cnt + 1].replace("Weekday","").split(" ") if h != ""], [v for v in text_lines[2 + i + line_cnt + 2].replace("Count","").split(" ") if v != ""]))
            for k1 in dataframe["AggregatedCommits"][k].keys():
                assert int(d[k1]) == dataframe["AggregatedCommits"][k][k1]
            assert str(sum([int(v) for v in d.values()])) == text_lines[2 + i + line_cnt + 3].replace("AuthorTotal:","").replace(" ","")
            line_cnt += 3
    def test_nodata_aggregatecommits_normal(self):
        dataframe = self.dataframe_day_normal
        temp_dataframe = copy.copy(dataframe)
        temp_dataframe["AggregatedCommits"] = {}
        text_lines = convert_to_text(temp_dataframe, self.git_url)
        assert type(text_lines) is list
        assert self.git_url == text_lines[0].replace("Repository:","").replace(" ","")
        assert str(temp_dataframe["CommitCount"]) == text_lines[1].replace("Total:","").replace(" ","")
        line_cnt=0
        for i,k in enumerate(temp_dataframe["AggregatedCommits"]):
            assert k in text_lines[2 + i + line_cnt]
            d = dict(zip([h for h in text_lines[2 + i + line_cnt + 1].replace("Day","").split(" ") if h != ""], [v for v in text_lines[2 + i + line_cnt + 2].replace("Count","").split(" ") if v != ""]))
            for k1 in temp_dataframe["AggregatedCommits"][k].keys():
                assert int(d[k1]) == temp_dataframe["AggregatedCommits"][k][k1]
            assert str(sum([int(v) for v in d.values()])) == text_lines[2 + i + line_cnt + 3].replace("AuthorTotal:","").replace(" ","")
            line_cnt += 3
    def test_nodata_indexes_normal(self):                           # It seems like no data
        dataframe = self.dataframe_day_normal
        temp_dataframe = copy.copy(dataframe)
        temp_dataframe["Indexes"] = {}
        text_lines = convert_to_text(temp_dataframe, self.git_url)
        assert type(text_lines) is list
        assert self.git_url == text_lines[0].replace("Repository:","").replace(" ","")
        assert str(temp_dataframe["CommitCount"]) == text_lines[1].replace("Total:","").replace(" ","")
        line_cnt=0
        for i,k in enumerate(temp_dataframe["AggregatedCommits"]):
            assert k in text_lines[2 + i + line_cnt]
            d = dict(zip([h for h in text_lines[2 + i + line_cnt + 1].replace("Day","").split(" ") if h != ""], [v for v in text_lines[2 + i + line_cnt + 2].replace("Count","").split(" ") if v != ""]))
            for k1 in temp_dataframe["AggregatedCommits"][k].keys():
                if k1 in d:
                    assert int(d[k1]) == temp_dataframe["AggregatedCommits"][k][k1]
            assert str(sum([int(v) for v in d.values()])) == text_lines[2 + i + line_cnt + 3].replace("AuthorTotal:","").replace(" ","")
            line_cnt += 3
    def test_none_commitcount_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            temp_dataframe["CommitCount"] = None
            text_lines = convert_to_text(temp_dataframe, self.git_url)
    def test_none_period_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            temp_dataframe["Period"] = None
            text_lines = convert_to_text(temp_dataframe, self.git_url)
    def test_none_giturl_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_hour_normal
            text_lines = convert_to_text(dataframe, None)
    def test_none_dataframe_error(self):
        with pytest.raises(NoneValueError) as e:
            text_lines = convert_to_text(None, self.git_url)
    def test_no_aggregatecommits_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["AggregatedCommits"]
            text_lines = convert_to_text(temp_dataframe, self.git_url)
    def test_no_commitcount_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["CommitCount"]
            text_lines = convert_to_text(temp_dataframe, self.git_url)
    def test_no_period_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["Period"]
            text_lines = convert_to_text(temp_dataframe, self.git_url)
    def test_no_indexes_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["Indexes"]
            text_lines = convert_to_text(temp_dataframe, self.git_url)
    def test_no_authors_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["Authors"]
            text_lines = convert_to_text(temp_dataframe, self.git_url)
