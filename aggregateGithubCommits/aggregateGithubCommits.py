#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from datetime import datetime, timedelta, date
from pytz import timezone
from tzlocal import get_localzone
from dateutil.relativedelta import relativedelta
import calendar
from io import StringIO
import argparse
import re
import json
import csv
import sys
import os
import pandas as pd
from github import Github, GithubException

import aggregateGithubCommits

__version__ = '3.20200806'


class Error(Exception):
  pass
class GitHubTokenError(Error):
  def __init__(self, message):
        self.message = message
class AugumentError(Error):
  def __init__(self, message):
        self.message = message
class ValueCleansingError(Error):
  def __init__(self, message):
        self.message = message
class NoneValueError(Error):
  def __init__(self, message):
        self.message = message


def check_datetime(dt):
    try:
        return date.fromisoformat(dt)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e) + " since and until must be in ISO format. ex) '2020-07-12'")

def check_args(params):
  if 'GITHUBTOKEN' in os.environ and os.environ['GITHUBTOKEN'] != '':
    github_token=os.environ['GITHUBTOKEN']
  else:
    raise GitHubTokenError("Plese set 'GITHUBTOKEN' environment variable for access to GitHub.")

  parser = argparse.ArgumentParser(description='Aggregate Github commits by author and time.', prefix_chars='-/')
  parser.add_argument("-r", "--repo", required=True, help="[Required] GitHub owner and repositry name. ex) 'github/covid-19-repo-data'")
  parser.add_argument("-a", "--author", default=None, help="GitHub author name, default is all authors. ex) 'github'")
  parser.add_argument("-s", "--since", default=None, type=check_datetime, help="since date in ISO format. ex) '2020-07-12'")
  parser.add_argument("-u", "--until", default=datetime.today().strftime('%Y-%m-%d'), type=check_datetime, help="until date in ISO format, default is today. ex) '2020-07-12'")
  parser.add_argument("-p", "--period", choices=("h","d","m","w"), default="h", help="Aggregating period, default is 'h'. 'h': per hour, 'd': per day, 'm': per month, 'w': per day of week")
  parser.add_argument("-t", "--term", default=None, help="Aggregating term from until, default is '3m'. '3m' means '3months', '100d' means '100days'")
  parser.add_argument("-f", "--format", choices=("text","json","csv"), default="text", dest="format_type", help="Output format type, default is 'text'. ")
  parser.add_argument("-v", "--version", action="version", version=__version__)

  args = parser.parse_args(params)

  if args.repo == None:
    raise AugumentError("Repository is required.")

  if args.term != None:
    if args.since != None:
      raise AugumentError("-s/--since and -t/--term are mutually exclusive.")
    m = re.match(r"^(\d+)(m|d)$", args.term)
    if not m:
      raise AugumentError("-t/--term format is invalid.")
  elif args.since == None:
    # default term is "3m"
    args.term = "3m"

  return github_token, args

def parse_args(args):
  if args.since == None:
    if args.term == None:
      raise AugumentError("Either -s/--since or -t/--term is required.")
    else:
      m = re.search(r"^(\d+)(m|d)$", args.term)
      term_num = int(m.group(1))
      term_unit = m.group(2)
      if term_unit == "m":
        return (datetime.strptime(args.until.strftime("%Y-%m-%d 23:59:59"), "%Y-%m-%d %H:%M:%S") - relativedelta(months=term_num)).strftime("%Y-%m-%d 00:00:00")
      elif term_unit == "d":
        return (datetime.strptime(args.until.strftime("%Y-%m-%d 23:59:59"), "%Y-%m-%d %H:%M:%S") - timedelta(days=term_num)).strftime("%Y-%m-%d 00:00:00")
      else:
        raise AugumentError("-t/--term format is invalid.")
  else:
    return args.since.strftime("%Y-%m-%d 00:00:00")

      
def get_commits(github_token, repo, author, since, until):
  g = Github(login_or_token=github_token)

  params = {
    "since": datetime.strptime(since, "%Y-%m-%d %H:%M:%S").astimezone(), 
    "until": datetime.strptime(until, "%Y-%m-%d %H:%M:%S").astimezone() }
  if author is not None:
    u = g.get_user(login=author)
    params["author"] = u

  r = g.get_repo(repo)
  result = r.get_commits(**params)

  return result, r.git_url


def extract_commits(result):
  commits = {}

  for c in result:
    ar = c.author.login if c.author is not None else c.commit.author.name
    dt = c.commit.author.date.replace(tzinfo=timezone('UTC')).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    if ar in commits:
      if dt in commits[ar]:
        commits[ar][dt] += 1
      else:
        commits[ar][dt] = 1
    else:
      commits[ar] = {}
      commits[ar][dt] = 1

  return commits


def aggregate_commits(commits, period):
  dataframe = {}
  dataframe["AggregatedCommits"] = {}
  dataframe["Period"] = period

  df = pd.DataFrame(commits)
  df.index.name = "datetime"
  df.index = pd.to_datetime(df.index)
  try:
    df.values.astype('uint64')
  except ValueError as e:
    raise ValueCleansingError("Commit count seems not Unsigned Number.")

  period_type = {
    "h":{"indexes": [df.index.hour],                               "names": ["hour"]                         },
    "d":{"indexes": [df.index.year, df.index.month, df.index.day], "names": ["year", "month", "day"]         },
    "m":{"indexes": [df.index.year, df.index.month],               "names": ["year", "month"]                },
    "w":{"indexes": [df.index.weekday],                            "names": ["weekday"]                      },
  }
  if period not in period_type.keys():
    raise AugumentError("-p/--period is out of range.")

  df_temp = df.set_index(period_type[period]["indexes"]).sort_index()
  df_temp.index.names = period_type[period]["names"]
  try:
    df_sum = df_temp.sum(level=period_type[period]["names"]).convert_dtypes()
  except ValueError as e:
    raise ValueCleansingError("Commit data is invalid.")
  dataframe["CommitCount"] = df_temp.index.size
  if dataframe["CommitCount"] != (df_temp >= 0).values.sum():
    raise ValueCleansingError("Commit count seems not Unsigned Number.")
  dataframe["Authors"] = list(df_sum.columns)
  if period == "h":
    dataframe["Indexes"] = ["{:02d}".format(x) for x in range(24)]
  elif period == "w":
    dataframe["Indexes"] = [calendar.day_abbr[x] for x in range(7)]
  else:
    dataframe["Indexes"] = ["-".join(map("{:02d}".format, x)) for x in list(df_sum.index)]

  for k1,v1 in df_sum.to_dict().items():
    dataframe["AggregatedCommits"][k1] = {}
    for k2,v2 in v1.items():
      if period == "h":
        dataframe["AggregatedCommits"][k1]["{:02d}".format(int(k2))] = int(v2)
      elif period == "d":
        dataframe["AggregatedCommits"][k1]["{:04d}".format(int(k2[0])) + "-" + "{:02d}".format(int(k2[1])) + "-" + "{:02d}".format(int(k2[2]))] = int(v2)
      elif period == "m":
        dataframe["AggregatedCommits"][k1]["{:04d}".format(int(k2[0])) + "-" + "{:02d}".format(int(k2[1]))] = int(v2)
      elif period == "w":
        dataframe["AggregatedCommits"][k1][calendar.day_abbr[int(k2)]] = int(v2)

  return dataframe


def convert_to_text(dataframe, git_url):
  if dataframe is None or git_url is None:
    raise NoneValueError("Display Data is none.")
  if "AggregatedCommits" not in dataframe or "CommitCount" not in dataframe or \
    "Period" not in dataframe or "Indexes" not in dataframe or "Authors" not in dataframe:
    raise NoneValueError("Display Data is none.")
  if dataframe["CommitCount"] is None:
    raise NoneValueError("Total Data is none.")
  if dataframe["Period"] is None:
    raise NoneValueError("Period Data is none.")

  text_lines = []

  period_names         = {"h":"Hour",   "d":"Day",    "m":"Month",  "w":"Weekday"}
  period_header_format = {"h":"{:4}",   "d":"{:10}",  "m":"{:7}",  "w":"{:4}"   }
  period_value_format  = {"h":"{:>4}",  "d":"{:>10}", "m":"{:>7}", "w":"{:>4}"  }

  text_lines.append("Repository: {0}".format(git_url))
  text_lines.append("Total:      {0}".format(dataframe["CommitCount"]))

  for k1,v1 in dataframe["AggregatedCommits"].items():
    author_total = 0
    text_lines.append("{0:>10}    {1}".format("Author:", k1))
    tmp_line = []
    tmp_line.append("{:>12}    ".format(period_names[dataframe["Period"]]))
    for idx in dataframe["Indexes"]:
      tmp_line.append((period_header_format[dataframe["Period"]] + "  ").format(idx))
    text_lines.append("".join(tmp_line))

    tmp_line = []
    tmp_line.append("{:>12}    ".format("Count"))
    for idx in dataframe["Indexes"]:
      if idx in v1.keys():
        tmp_line.append((period_value_format[dataframe["Period"]] + "  ").format(str(v1[idx])))
        author_total += v1[idx]
      else:
        tmp_line.append((period_value_format[dataframe["Period"]] + "  ").format("0"))
    text_lines.append("".join(tmp_line))
    text_lines.append("{0:>20}{1:10d}".format("AuthorTotal:", author_total))

  return text_lines


def convert_to_json(dataframe):
  return "{0}".format(json.dumps(dataframe))


def convert_to_csv(dataframe):
  if dataframe is None:
    raise NoneValueError("Display Data is none.")
  if "AggregatedCommits" not in dataframe or "Indexes" not in dataframe:
    raise NoneValueError("Display Data is none.")

  csv_lines = []

  tmp_line = []
  tmp_line.append("")
  for idx in dataframe["Indexes"]:
    tmp_line.append(idx)
  csv_lines.append(tmp_line)

  for k1,v1 in dataframe["AggregatedCommits"].items():
    tmp_line = []
    tmp_line.append(k1)
    for idx in dataframe["Indexes"]:
      if idx in v1.keys():
        tmp_line.append(int(v1[idx]))
      else:
        tmp_line.append(0)
    csv_lines.append(tmp_line)

  csv_buf = StringIO()
  csv.writer(csv_buf, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator=os.linesep).writerows(csv_lines)
  return csv_buf.getvalue()
 

def main():
  try:
    github_token, args = check_args(sys.argv[1:])
    repo = args.repo
    author = args.author
    period = args.period
    until = args.until.strftime('%Y-%m-%d 23:59:59')
    since = parse_args(args)
    format_type = args.format_type

    result, git_url = get_commits(github_token, repo, author, since, until)
    commits = extract_commits(result)
    dataframe = aggregate_commits(commits, period)

    if format_type == "text":
      text_lines = convert_to_text(dataframe, git_url)
      print(os.linesep.join(text_lines))
    elif format_type == "json":
      print(convert_to_json(dataframe))
    elif format_type == "csv":
      print(convert_to_csv(dataframe))
    else:
      raise AugumentError("-f/--format format type is invalid.")

  except GitHubTokenError as e:
    print(e)
    sys.exit(101)
  except AugumentError as e:
    print(e)
    sys.exit(102)
  except GithubException as e:
    print("GitHub access error. Status:[{}], Message:[{}]".format(e.status, e.data["message"]))
    sys.exit(103)
  except ValueCleansingError as e:
    print(e)
    sys.exit(104)
  except Exception as e:
    print("Other error happens.")
    tb = sys.exc_info()[2]
    print(e.with_traceback(tb))
    sys.exit(1)

if __name__ == '__main__':
  main()
  
