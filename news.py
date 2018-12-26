#!/usr/bin/env python3

"""This is a program that extract important info from a database and
rolls it into a handy report"""

import psycopg2


news_db = psycopg2.connect("dbname=news")

news_cursor = news_db.cursor()


# 1. What are the most popular three articles of all time?
# The "stats" view is needed to execute the following query:
"""
CREATE VIEW stats AS
SELECT title, count(*) as VIEWS
FROM log JOIN articles
ON concat('/article/', articles.slug) = log.path
GROUP BY title ORDER BY views DESC;
"""
news_cursor.execute("SELECT * FROM stats LIMIT 3;")
most_popular_3_articles = news_cursor.fetchall()
print("### 1. What are the most popular three articles of all time? ###")
for article in most_popular_3_articles:
    print('* "{}" - {} views'.format(article[0], str(article[1])))


# 2. Who are the most popular article authors of all time?
# The "stats" view from the previous query is needed:
news_cursor.execute("""
SELECT authors.name , sum(stats.views)
FROM stats, articles, authors
WHERE articles.title= stats.title
AND articles.author = authors.id
GROUP BY authors.name
ORDER BY sum DESC;
""")
most_popular_authors = news_cursor.fetchall()
print("### 2. Who are the most popular article authors of all time? ###")
for author in most_popular_authors:
    print('* "{}" - {} views'.format(author[0], str(author[1])))


# 3. On which days did more than 1% of requests lead to errors?
# This uses many views for the sake of simplicity
# and to break the problem down into multiple chunks
# and also because of some stupid error relating to GROUP BY
# Here they are in order:
# 1:
"""
CREATE VIEW errcount AS
SELECT time::date as errdate, count(*) as errors
FROM log WHERE status!='200 OK'
GROUP BY errdate ORDER BY errors DESC;
"""
# 2:
"""
CREATE VIEW viewcount AS
SELECT time::date as l_date, count(*) as views
FROM log GROUP BY l_date;
"""
# 3:
"""
CREATE VIEW errtoviewratio AS
SELECT l_date, views, errors
FROM viewcount JOIN errcount
ON errcount.errdate = viewcount.l_date;
"""
# 4:
"""
CREATE VIEW errpercentage AS
SELECT l_date, round(((errors*100)::decimal / views), 1) AS percentage
FROM errtoviewratio ORDER BY percentage DESC;
"""
# P.S. : Really sorry but it's your fault
# because you wanted the database to do all the hard work.
# This would have been way easier and cleaner
# if I was allowed to do it in an actual programming language.
news_cursor.execute("SELECT * FROM errpercentage WHERE percentage > 1;")
days_with_more_than_1_percent_errors = news_cursor.fetchall()
print("### 3. On which days did more than 1% of requests lead to errors? ###")
for day in days_with_more_than_1_percent_errors:
    print('* "{}" - {} %  errors'.format(day[0], str(day[1])))
