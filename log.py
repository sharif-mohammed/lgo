#!/usr/bin/env python

# import Postgresql library
import psycopg2


dbname = 'news'


def ashish(q):
    """ashish takes a string as a parameter.  It executes the q
    and returns the output as a list of tuples."""
    try:
        db = psycopg2.connect('dbname=' + dbname)
        c = db.cursor()
        c.execute(q)
        rows = c.fetchall()
        db.close()
        return rows
    except BaseException:
        print("Unable to connect to the database")


# Query 1: What are the most popular three articles of all time?
def top_articles():
    """Return the top three articles by most views"""
    q = """SELECT title, COUNT(log.id) AS views
            FROM articles, log
            WHERE log.path = CONCAT('/article/', articles.slug)
            GROUP BY articles.title ORDER BY views desc LIMIT 3;"""
    top_three = ashish(q)
    # Display header and output for Problem 1
    print('**** Top Three Articles by Page View ****')
    for s in top_three:
        print('"' + s[0] + '" -- ' + str(s[1]) + " views")


# Problem 2: Who are the most popular article authors of all time?
def famous_authors():

    # query 2: Who are the most popular article authors of all time?

    q = """
        select authors.name, count(*) as num
        from authors
        join articles
        on authors.id = articles.author
        join log
        on log.path like concat('/article/%', articles.slug)
        group by authors.name
        order by num desc
        limit 3;
    """

# executing q for top authors.
    output = ashish(q)

# printing outputs.
    print('\ntop three authors:')
    d = 1
    for z in output:
        print('' + str(z) + '. ' + z[0] + ' with ' + str(z[1]) + " views")
        d += 1


# query 3: On which days did more than 1% of requests lead to errors?
def day_errors():
    """Return the days where errors exceeded 1%"""
    q = """
        select total.day,
          round(((errors.error_requests*1.0) / total.requests), 3) as percent
        from (
          select date_trunc('day', time) "day", count(*) as error_requests
          from log
          where status like '404%'
          group by day
        ) as errors
        join (
          select date_trunc('day', time) "day", count(*) as requests
          from log
          group by day
          ) as total
        on total.day = errors.day
        where (round(((errors.error_requests*1.0) / total.requests), 3) > 0.01)
        order by percent desc;
    """
    output = ashish(q)
    # Display header and output for Problem 3
    print('\ndays with more than 1% errors:')
    for y in output:
        print(y[0].strftime('%B %d, %Y') + " -- " +
              str(round(y[1]*100, 1)) + "%" + " errors")

if __name__ == '__main__':
    top_articles()
    famous_authors()
    day_errors()

