#!/bin/env python

import psycopg2


DBNAME = "news"


def connect_to_db():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    return db, c


def print_result(result, cursor):
    widths = []
    columns = []
    tavnit = '|'
    separator = '+'

    for cd in cursor.description:
        widths.append(33)
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in result:
        print(tavnit % row)
    print(separator)


def query_three_most_popular_articles():
    db, c = connect_to_db()
    query = """SELECT articles.title AS title, count(path) AS views
                FROM articles, log
                WHERE articles.slug = substring(path, 10)
                GROUP BY articles.title
                ORDER BY Views DESC
                LIMIT 3;"""
    c.execute(query)
    result = c.fetchall()
    print("\nHere are the three most popular articles of all time: \n")
    print_result(result, c)
    db.close()


def query_most_popular_authors():
    db, c = connect_to_db()
    query = """SELECT authors.name, count(path) AS views
                FROM authors, log, articles
                WHERE articles.slug = substring(path, 10)
                AND articles.author = authors.id
                GROUP BY authors.name
                ORDER BY views DESC;"""
    c.execute(query)
    result = c.fetchall()
    print("\nHere are the most popular authors of all time: \n")
    print_result(result, c)
    db.close


def query_high_error_days():
    db, c = connect_to_db()
    query = """SELECT TO_CHAR(errors.date, 'Mon DD, YYYY'),
                ROUND(100.0 * errors.errors / requests.requests, 2)
                    AS errors
                FROM errors, requests
                WHERE errors.date = requests.date
                    AND (errors.errors > requests.requests / 100)
                ORDER BY errors DESC;"""
    c.execute(query)
    result = c.fetchall()
    print("\nOn these days the error percentage was higher than 1%: \n")
    print_result(result, c)
    db.close


if __name__ == '__main__':
    query_three_most_popular_articles()
    query_most_popular_authors()
    query_high_error_days()
