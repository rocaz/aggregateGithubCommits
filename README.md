# aggregateGithubCommits

Aggregate Github commits by author and time.

## using

usage: aggregateGithubCommits.py [-h] [-r REPO] [-a AUTHOR]

-r: Required. Github Repository name. i.e.) "github/covid-19-repo-data"

-a: Optional. Author login name that you want to specify.

Example:

python3 ./aggregateGithubCommits.py -r "github/covid-19-repo-data" -a gregce

Output:

```
Repository: git://github.com/github/covid-19-repo-data.git
Total:      37
  Author:     gregce
    Period:     2020-06-01 - 2020-06-30
       Hour      00        01        02        03        04        05        06        07        08        09        10        11        12        13        14        15        16        17        18        19        20        21        22        23
      Count                                       1         1                   1                                                                     1                                                                                     
      SubTotal:     4
    Period:     2020-05-01 - 2020-05-31
       Hour      00        01        02        03        04        05        06        07        08        09        10        11        12        13        14        15        16        17        18        19        20        21        22        23
      Count                   1         1                                       1                   1                                                                                                                                       
      SubTotal:     4
    Period:     2020-04-01 - 2020-04-30
       Hour      00        01        02        03        04        05        06        07        08        09        10        11        12        13        14        15        16        17        18        19        20        21        22        23
      Count         1         3                                       1                                                                                                                                                                     
      SubTotal:     5
   AuthorTotal:    13
JSON:
{"gregce": {"2020-06-01 - 2020-06-30": {"04": 1, "13": 1, "06": 1, "03": 1}, "2020-05-01 - 2020-05-31": {"06": 1, "01": 1, "08": 1, "02": 1}, "2020-04-01 - 2020-04-30": {"05": 1, "01": 3, "00": 1}}}
CSV:
"Author","Period","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"
"gregce","2020-06-01 - 2020-06-30","","","","1","1","","1","","","","","","","1","","","","","","","","","",""
"gregce","2020-05-01 - 2020-05-31","","1","1","","","","1","","1","","","","","","","","","","","","","","",""
"gregce","2020-04-01 - 2020-04-30","1","3","","","","1","","","","","","","","","","","","","","","","","",""
```

## Environment Variable

GITHUBTOKEN

Plase set your Github Token

## Limitation

Now, Period is setted between 1 May 2020 to 30 June 2020. Those are hard coding in this source code.
If you want to change period, change source code. 
