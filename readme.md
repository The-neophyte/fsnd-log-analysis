# Logs Analysis Project Submission
## About
This is a Logs Analysis project submission for Udacity's full stack nanodegree program.
## Python Version
Python 3.
## Views Used
1. stats
```SQL
CREATE VIEW stats AS
SELECT title, count(*) as VIEWS
FROM log JOIN articles
ON concat('/article/', articles.slug) = log.path
GROUP BY title ORDER BY views DESC;
```
2. errcount
```SQL
CREATE VIEW errcount AS
SELECT time::date as errdate, count(*) as errors
FROM log WHERE status!='200 OK'
GROUP BY errdate ORDER BY errors DESC;
```
3. viewcount
```SQL
CREATE VIEW viewcount AS
SELECT time::date as l_date, count(*) as views
FROM log GROUP BY l_date;
```
4. errtoviewratio
```SQL
CREATE VIEW errtoviewratio AS
SELECT l_date, views, errors
FROM viewcount JOIN errcount
ON errcount.errdate = viewcount.l_date;
```
5. errpercentage
```SQL
CREATE VIEW errpercentage AS
SELECT l_date, round(((errors*100)::decimal / views), 1) AS percentage
FROM errtoviewratio ORDER BY percentage DESC;
```  

## Files Included
- `readme.md`: This file you're reading
- `news.py`: The file containing the source code
- `output.txt`: A plain text file that contains the code's output
- `tables.txt`: A plain text file that contains the table representation of every view or query I used in this project so It's easier to understand my thought process.
