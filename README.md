United States of America Education budget to GDP analysis

## Data

Data comes from Office of Management and Budget, President’s Budget from white house official website on  https://www.whitehouse.gov/sites/whitehouse.gov/files/omb/budget/fy2018/hist05z2.xls

It consists of useful information about BUDGET AUTHORITY BY AGENCY in the range 1976–2022.

Gross Domestic Value(GDP) comes from DataHub http://datahub.io/core/gdp/r/gdp.csv since it is regularly updated and includes all country codes.

## Preparation 

There are several steps have been done to get final data.

* We extracted budget and gdp data separately
* We merged and added new column `RATIO` which is calculated by `education expenditure / GDP`

Process is recorded and automated in python script:

```
# to get final data.csv
scripts/process.py
```

## License

Public Domain Dedication and License (PDDL)