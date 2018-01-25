import sqlite3
import csv

# open database
con = sqlite3.connect('db.sqlite')
cur = con.cursor()


# Step 1.1 - import nodes

# Creating table for nodes
cur.execute('DROP TABLE IF EXISTS "nodes"')  # clear previous table if it exists
cur.execute('CREATE TABLE "nodes" ('
            'id INTEGER,'
            'lat REAL,'
            'lon REAL,'
            'user TEXT,'
            'uid INTEGER,'
            'version INTEGER,'
            'changeset INTEGER,'
            'timestamp DATE )')

# reading "nodes.csv" and put every row in database
with open('nodes.csv') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        if len(row) == 0:  # skipping empty rows
            continue
        cur.execute('INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?)', row) # put in database

# saving database
con.commit()


# Step 1.2 - import nodes_tags

# Creating table for nodes_tags
cur.execute('DROP TABLE IF EXISTS "nodes_tags"')
cur.execute('CREATE TABLE "nodes_tags" ('
            'id INTEGER,'
            'key TEXT,'
            'value TEXT,'
            'type TEXT)')

# reading "nodes_tags.csv" and put every row in database
with open('nodes_tags.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 0:
            continue
        cur.execute('INSERT INTO nodes_tags VALUES (?, ?, ?, ?)', row)

# saving
con.commit()


# Step 1.3 - import ways

# Creating table for ways
cur.execute('DROP TABLE IF EXISTS "ways"')
cur.execute('CREATE TABLE "ways" ('
            'id INTEGER,'
            'user TEXT,'
            'uid INTEGER,'
            'version INTEGER,'
            'changeset INTEGER,'
            'timestamp DATE )')

# reading "ways.csv" and put every row in database
with open('ways.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 0:
            continue
        cur.execute('INSERT INTO ways VALUES (?, ?, ?, ?, ?, ?)', row)

# saving
con.commit()


# Step 1.4 - import ways_nodes

# Creating table for ways_nodes
cur.execute('DROP TABLE IF EXISTS "ways_nodes"')
cur.execute('CREATE TABLE "ways_nodes" ('
            'id INTEGER,'
            'node_id INTEGER,'
            'position INTEGER )')

# reading "ways_nodes.csv" and put every row in database
with open('ways_nodes.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 0:
            continue
        cur.execute('INSERT INTO ways_nodes VALUES (?, ?, ?)', row)

# saving
con.commit()


# Step 1.5 - import ways_tags

# Creating table for ways_tags
cur.execute('DROP TABLE IF EXISTS "ways_tags"')
cur.execute('CREATE TABLE "ways_tags" ('
            'id INTEGER,'
            'key TEXT,'
            'value TEXT,'
            'type TEXT)')

# reading "ways_tags.csv" and put every row in database
with open('ways_tags.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 0:
            continue
        cur.execute('INSERT INTO ways_tags VALUES (?, ?, ?, ?)', row)

# saving
con.commit()


# Step 2.1 computing number of nodes
cur.execute('SELECT COUNT(id) FROM nodes')
amount = cur.fetchone()[0]  # extract first element from row
print(u'Number of nodes: {}'.format(amount))


# Step 2.2 computing number of nodes_tags
cur.execute('SELECT COUNT(id) FROM nodes_tags')
amount = cur.fetchone()[0]
print(u'Number of nodes_tags: {}'.format(amount))


# Step 2.3 computing number of ways
cur.execute('SELECT COUNT(id) FROM ways')
amount = cur.fetchone()[0]
print(u'Number of ways: {}'.format(amount))


# Step 2.4 computing number of ways_nodes
cur.execute('SELECT COUNT(id) FROM ways_nodes')
amount = cur.fetchone()[0]
print(u'Number of ways_nodes: {}'.format(amount))


# Step 2.5 computing number of ways_tags
cur.execute('SELECT COUNT(id) FROM ways_tags')
amount = cur.fetchone()[0]
print(u'Number of ways_tags: {}'.format(amount))


# Step 2.6 computing number of unique users
cur.execute('SELECT COUNT(DISTINCT "user") FROM nodes')  # at this point I use "DISTINCT" keyword, in order to compute number of unique users
amount = cur.fetchone()[0]
print(u'Number of unique users: {}'.format(amount))


# Step 2.7 computing number of cafes
cur.execute('SELECT COUNT(id) FROM nodes_tags WHERE value="cafe"')  # skips everything not a cafe
amount = cur.fetchone()[0]
print(u'Number of cafes: {}'.format(amount))


# Step 2.8 computing number of restaurants
cur.execute('SELECT COUNT(id) FROM nodes_tags WHERE value="restaurant"')  # skips everything not a restaurant
amount = cur.fetchone()[0]
print(u'Number of restaurants: {}'.format(amount))
