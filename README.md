# aggregateGithubCommits

Aggregate Github commit count by author and time.

[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-4584b6.svg?style=popout&logo=python)](https://www.python.org/) ![PyPI](https://img.shields.io/pypi/v/aggregateGithubCommits)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

![GitHub Actions](https://github.com/rocaz/aggregateGithubCommits/workflows/GitHub%20Actions/badge.svg) [![codecov](https://codecov.io/gh/rocaz/aggregateGithubCommits/branch/master/graph/badge.svg)](https://codecov.io/gh/rocaz/aggregateGithubCommits)

## Requirement

- Python 3.7+
- Your own GitHub account

## Install

```
pip install aggregateGithubCommits
```

or

```
pip install git+https://github.com/rocaz/aggregateGithubCommits
```

## Usage

aggregateGithubCommits [-h] -r|--repo REPO [-a|--author AUTHOR] [-s|since SINCE]
                                 [-u|until UNTIL] [-p|--period {h,d,m,w}] [-t|--term TERM]
                                 [-f|--format {text,json,csv}] [-v]

-h, --help:                   show this help message and exit

-r REPO, --repo REPO:         [Required] GitHub owner and repositry name. ex)'github/covid-19-repo-data'

-a AUTHOR, --author AUTHOR:   GitHub author name, default is all authors. ex)'github'

-s SINCE, --since SINCE:    since date in ISO format. ex) '2020-07-12'

-u UNTIL, --until UNTIL:    until date in ISO format, default is today. ex)'2020-07-12'

-p {h,d,m,w}, --period {h,d,m,w}:
                              Aggregating period, default is 'h'.
                              'h': per hour,'d': per day, 'm': per month, 'w': per day of week

-t TERM, --term TERM:       Aggregating term from until, default is '3m'. '3m' means '3months', '100d' means '100days'

-f {text,json,csv}, --format {text,json,csv}:
                              Output format type, default is 'text'.

-v, --version:              show program's version number and exit

## Example

(1) Specified author. Default term is from now to 3months ago.

```python ./aggregateGithubCommits.py -r "github/covid-19-repo-data" -a gregce```

Output:

```
Repository: git://github.com/github/covid-19-repo-data.git
Total:      15
   Author:    gregce
        Hour    00    01    02    03    04    05    06    07    08    09    10    11    12    13    14    15    16    17    18    19    20    21    22    23
       Count       2     1     2     1     1     0     2     0     1     2     0     1     1     1     0     0     0     0     0     0     0     0     0     0
        AuthorTotal:        15
```

(2) The term is specified from '2020-02-29' to '2020-08-02', Aggregation period is 'per month'.

```python ./aggregateGithubCommits.py -r "github/covid-19-repo-data" -p m -u '2020-08-02' -s '2020-02-29'```

Output:

```
Repository: git://github.com/github/covid-19-repo-data.git
Total:      49
   Author:    gregce
       Month    2020-03  2020-04  2020-05  2020-06  2020-07
       Count          0        5        4        4        7
        AuthorTotal:        20
   Author:    Ashikpaul
       Month    2020-03  2020-04  2020-05  2020-06  2020-07
       Count          0        0        0        0        1
        AuthorTotal:         1
   Author:    hamelsmu
       Month    2020-03  2020-04  2020-05  2020-06  2020-07
       Count          0       22        0        4        0
        AuthorTotal:        26
   Author:    github-actions[bot]
       Month    2020-03  2020-04  2020-05  2020-06  2020-07
       Count          0        1        0        0        0
        AuthorTotal:         1
   Author:    DJedamski
       Month    2020-03  2020-04  2020-05  2020-06  2020-07
       Count          1        0        0        0        0
        AuthorTotal:         1
```

(3) Output format is setted to JSON.

```python ./aggregateGithubCommits.py -r "github/covid-19-repo-data" -f json```

```
{"AggregatedCommits": {"gregce": {"00": 2, "01": 1, "02": 2, "03": 1, "04": 1, "06": 2, "08": 1, "09": 2, "11": 1, "12": 1, "13": 1}, "Ashikpaul": {"00": 0, "01": 0, "02": 1, "03": 0, "04": 0, "06": 0, "08": 0, "09": 0, "11": 0, "12": 0, "13": 0}, "hamelsmu": {"00": 0, "01": 0, "02": 4, "03": 0, "04": 0, "06": 0, "08": 0, "09": 0, "11": 0, "12": 0, "13": 0}}, "Period": "h", "CommitCount": 20, "Authors": ["gregce", "Ashikpaul", "hamelsmu"], "Indexes": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]}
```

(4) Output format is setted to CSV.

```python ./aggregateGithubCommits.py -r "github/covid-19-repo-data" -f csv```

```
"","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"
"gregce","2","1","2","1","1","0","2","0","1","2","0","1","1","1","0","0","0","0","0","0","0","0","0","0"
"Ashikpaul","0","0","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
"hamelsmu","0","0","4","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
```

## Environment Variable

'GITHUBTOKEN'

Plase set your Github Token

## License

CC BY-NC-SA 4.0

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

non-commercial use only.
