#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import copy
from github import Github, PaginatedList

from aggregateGithubCommits.aggregateGithubCommits import *


class TestConvertToCSV(object):
    def setup_method(self, method):
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
        csv_data = convert_to_csv(dataframe)
        assert type(csv_data) is str
        csv_lines = [l for l in csv_data.rstrip().splitlines()]
        indexes = [v for v in csv_lines[0].replace("\"","").split(",") if v != ""]
        assert set(dataframe["Indexes"]) == set(indexes)
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            l = csv_lines[i + 1].replace("\"","").split(",")
            assert l[0] == k
            del l[0]
            csv_dict = dict(zip(indexes, l))
            for k1 in dataframe["AggregatedCommits"][k]:
                assert int(csv_dict[k1]) == dataframe["AggregatedCommits"][k][k1]
    def test_period_day_normal(self):
        dataframe = self.dataframe_day_normal
        csv_data = convert_to_csv(dataframe)
        assert type(csv_data) is str
        csv_lines = [l for l in csv_data.rstrip().splitlines()]
        indexes = [v for v in csv_lines[0].replace("\"","").split(",") if v != ""]
        assert set(dataframe["Indexes"]) == set(indexes)
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            l = csv_lines[i + 1].replace("\"","").split(",")
            assert l[0] == k
            del l[0]
            csv_dict = dict(zip(indexes, l))
            for k1 in dataframe["AggregatedCommits"][k]:
                assert int(csv_dict[k1]) == dataframe["AggregatedCommits"][k][k1]
    def test_period_month_normal(self):
        dataframe = self.dataframe_month_normal
        csv_data = convert_to_csv(dataframe)
        assert type(csv_data) is str
        csv_lines = [l for l in csv_data.rstrip().splitlines()]
        indexes = [v for v in csv_lines[0].replace("\"","").split(",") if v != ""]
        assert set(dataframe["Indexes"]) == set(indexes)
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            l = csv_lines[i + 1].replace("\"","").split(",")
            assert l[0] == k
            del l[0]
            csv_dict = dict(zip(indexes, l))
            for k1 in dataframe["AggregatedCommits"][k]:
                assert int(csv_dict[k1]) == dataframe["AggregatedCommits"][k][k1]
    def test_period_weekday_normal(self):
        dataframe = self.dataframe_weekday_normal
        csv_data = convert_to_csv(dataframe)
        assert type(csv_data) is str
        csv_lines = [l for l in csv_data.rstrip().splitlines()]
        indexes = [v for v in csv_lines[0].replace("\"","").split(",") if v != ""]
        assert set(dataframe["Indexes"]) == set(indexes)
        for i,k in enumerate(dataframe["AggregatedCommits"]):
            l = csv_lines[i + 1].replace("\"","").split(",")
            assert l[0] == k
            del l[0]
            csv_dict = dict(zip(indexes, l))
            for k1 in dataframe["AggregatedCommits"][k]:
                assert int(csv_dict[k1]) == dataframe["AggregatedCommits"][k][k1]
    def test_nodata_aggregatecommits_normal(self):
        dataframe = self.dataframe_day_normal
        temp_dataframe = copy.copy(dataframe)
        temp_dataframe["AggregatedCommits"] = {}
        csv_data = convert_to_csv(temp_dataframe)
        assert type(csv_data) is str
        csv_lines = [l for l in csv_data.rstrip().splitlines()]
        indexes = [v for v in csv_lines[0].replace("\"","").split(",") if v != ""]
        assert set(temp_dataframe["Indexes"]) == set(indexes)
        for i,k in enumerate(temp_dataframe["AggregatedCommits"]):
            l = csv_lines[i + 1].replace("\"","").split(",")
            assert l[0] == k
            del l[0]
            csv_dict = dict(zip(indexes, l))
            for k1 in temp_dataframe["AggregatedCommits"][k]:
                assert int(csv_dict[k1]) == temp_dataframe["AggregatedCommits"][k][k1]
    def test_nodata_indexes_normal(self):
        dataframe = self.dataframe_day_normal
        temp_dataframe = copy.copy(dataframe)
        temp_dataframe["Indexes"] = {}
        csv_data = convert_to_csv(temp_dataframe)
        assert type(csv_data) is str
        csv_lines = [l for l in csv_data.rstrip().splitlines()]
        indexes = [v for v in csv_lines[0].replace("\"","").split(",") if v != ""]
        assert set(temp_dataframe["Indexes"]) == set(indexes)
        for i,k in enumerate(temp_dataframe["AggregatedCommits"]):
            l = csv_lines[i + 1].replace("\"","").split(",")
            assert l[0] == k
            del l[0]
            csv_dict = dict(zip(indexes, l))
            for k1 in temp_dataframe["AggregatedCommits"][k]:
                if k1 in csv_dict:
                    assert int(csv_dict[k1]) == temp_dataframe["AggregatedCommits"][k][k1]
    def test_none_dataframe_error(self):
        with pytest.raises(NoneValueError) as e:
            csv_data = convert_to_csv(None)
    def test_no_aggregatecommits_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["AggregatedCommits"]
            csv_data = convert_to_csv(temp_dataframe)
    def test_no_indexes_error(self):
        with pytest.raises(NoneValueError) as e:
            dataframe = self.dataframe_day_normal
            temp_dataframe = copy.copy(dataframe)
            del temp_dataframe["Indexes"]
            csv_data = convert_to_csv(temp_dataframe)
    
