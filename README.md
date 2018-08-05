# Logs Analysis Project - Udacity Fullstack Nanodegree
---

## About

This project is about creating a reporting tool for a fictional news website in
Python. The connection to the PostgreSQL database is established via the
`psycopg2` module.

The final report answers these questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## How to run the program

1. `Cd` into `vagrant` directory
2. Run `$ vagrant up`
3. Run `$ vagrant ssh` to connect to the VM.
4. Connect to database via `psql -d news -f newsdata.sql`


## Views

To answer question 3, two views were created:

``` sql
create view requests as
  select date(time) as date, count(status) as requests
  from log
  group by date;
```

``` sql
create view errors as
  select date(time) as date, count(status) as errors
  from log
  where status = '404 NOT FOUND'
  group by date;
```

## Output
``` terminal

Here are the three most popular articles of all time:

+-----------------------------------+-----------------------------------+
| title                             | views                             |
+-----------------------------------+-----------------------------------+
| Candidate is jerk, alleges rival  | 338647                            |
| Bears love berries, alleges bear  | 253801                            |
| Bad things gone, say good people  | 170098                            |
+-----------------------------------+-----------------------------------+

Here are the most popular authors of all time:

+-----------------------------------+-----------------------------------+
| name                              | views                             |
+-----------------------------------+-----------------------------------+
| Ursula La Multa                   | 507594                            |
| Rudolf von Treppenwitz            | 423457                            |
| Anonymous Contributor             | 170098                            |
| Markoff Chaney                    | 84557                             |
+-----------------------------------+-----------------------------------+

On these days the error percentage was higher than 1%:

+-----------------------------------+-----------------------------------+
| date                              | errors                            |
+-----------------------------------+-----------------------------------+
| 2016-07-17                        | 2.26                              |
+-----------------------------------+-----------------------------------+

```
