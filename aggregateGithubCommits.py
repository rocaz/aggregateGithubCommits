# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
import argparse
import json
import csv
import sys
import os
from github import Github

p = argparse.ArgumentParser()
p.add_argument("-r","--repo", default="Covid-19Radar/Covid19Radar")
p.add_argument("-a","--author", default=None)

github_token=os.environ['GITHUBTOKEN']
periods = [
  {"since": datetime.fromisoformat("2020-03-01T00:00:00+09:00"), "until": datetime.fromisoformat("2020-03-31T23:59:59+09:00")},
  {"since": datetime.fromisoformat("2020-04-01T00:00:00+09:00"), "until": datetime.fromisoformat("2020-04-30T23:59:59+09:00")},
  {"since": datetime.fromisoformat("2020-05-01T00:00:00+09:00"), "until": datetime.fromisoformat("2020-05-31T23:59:59+09:00")},
  {"since": datetime.fromisoformat("2020-06-01T00:00:00+09:00"), "until": datetime.fromisoformat("2020-06-30T23:59:59+09:00")}
]

def main(repo="Covid-19Radar/Covid19Radar", author=None):
  commit_count = {}
  g = Github(login_or_token=github_token)

  params = {"since": periods[0]["since"], "until": periods[-1]["until"]}
  if author is not None:
    u = g.get_user(login=author)
    params["author"] = u

  r = g.get_repo(repo)
  commits = r.get_commits(**params)

  for c in commits:
    ar = c.author.login if c.author is not None else c.commit.author.name
    dt = c.commit.author.date.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Tokyo'))
    hr = dt.strftime("%H")
    for p in periods:
      if dt <= p["until"] and dt >= p["since"]: 
        pd = "{0:%Y-%m-%d} - {1:%Y-%m-%d}".format(p["since"], p["until"])
    if ar in commit_count:
      if pd in commit_count[ar]:
        if hr in commit_count[ar][pd]:
          commit_count[ar][pd][hr] += 1
        else:
          commit_count[ar][pd][hr] = 1
      else:
        commit_count[ar][pd] = {}
        commit_count[ar][pd][hr] = 1
    else:
      commit_count[ar] = {}
      commit_count[ar][pd] = {}
      commit_count[ar][pd][hr] = 1

  print("Repository: {0}".format(r.git_url))
  print("Total:      {0}".format(commits.totalCount))

  csv_output = []
  hours = [format(x, '02d') for x in range(24)]
  csv_line = []
  csv_line.append("Author")
  csv_line.append("Period")
  for h in hours:
    csv_line.append(h)
  csv_output.append(csv_line)

  for k1,v1 in commit_count.items(): 
    author_total = 0
    print("  Author:     {0}".format(k1))
    for k2,v2 in v1.items():
      csv_line = []
      csv_line.append(k1)
      csv_line.append(k2)
      print("    Period:     {0}".format(k2))
      v_sorted = sorted(v2.items(), key=lambda x:x[0])
      v_dict = dict(v_sorted)
      sub_total = 0
      print("       Hour", end="")
      for h in hours:
        print("      {0:4s}".format(h), end="")
      print("")
      print("      Count", end="")
      for h in hours:
        if h in v_dict.keys():
          print("      {0:4d}".format(v_dict[h]), end="")
          sub_total += v_dict[h]
          author_total += v_dict[h]
          csv_line.append(v_dict[h])
        else:
          print("      {0:4s}".format(" " * 4), end="")
          csv_line.append("")
      print("")
      print("      SubTotal:  {0:4d}".format(sub_total))
      csv_output.append(csv_line)
    print("   AuthorTotal:  {0:4d}".format(author_total))

  print("JSON:")
  print("{0}".format(json.dumps(commit_count)))
  print("CSV:")
  csv_writer = csv.writer(sys.stdout, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator=os.linesep)
  print("{0}".format(csv_writer.writerows(csv_output)))
 

if __name__ == '__main__':
  args = p.parse_args()
  main(args.repo, args.author)
