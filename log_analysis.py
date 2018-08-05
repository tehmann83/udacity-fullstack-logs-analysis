#!/bin/env python2.7

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
    query = """select articles.title as title, count(path) as views
                from articles, log
                where articles.slug = substring(path, 10)
                group by articles.title
                order by Views desc
                limit 3;"""
    c.execute(query)
    result = c.fetchall()
    print("\nHere are the three most popular articles of all time: \n")
    print_result(result, c)
    db.close()


def query_most_popular_authors():
    db, c = connect_to_db()
    query = """select authors.name, count(path) as views
                from authors, log, articles
                where articles.slug = substring(path, 10)
                and articles.author = authors.id
                group by authors.name
                order by views desc;"""
    c.execute(query)
    result = c.fetchall()
    print("\nHere are the most popular authors of all time: \n")
    print_result(result, c)
    db.close


def query_high_error_days():
    db, c = connect_to_db()
    query = """select errors.date,
                round(100.0 * errors.errors / requests.requests, 2)
                    as errors
                from errors, requests
                where errors.date = requests.date
                    and (errors.errors > requests.requests / 100)
                order by errors desc;"""
    c.execute(query)
    result = c.fetchall()
    print("\nOn these days the error percentage was higher than 1%: \n")
    print_result(result, c)
    db.close


if __name__ == '__main__':
    query_three_most_popular_articles()
    query_most_popular_authors()
    query_high_error_days()
