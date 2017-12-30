import osmium as osm
import pandas as pd


class Reader(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.elements = []

    def node(self, n):
        self.elements.append(["node",
                             n.id,
                             n.version,
                             n.location.lat,
                             n.location.lon,
                             pd.Timestamp(n.timestamp),
                             n.uid,
                             n.changeset,
                             n.user,
                             len(n.tags),
                             n.tags])

reader = Reader()
reader.apply_file('denver-boulder_colorado.osm')

colnames = ['type', 'id', 'version', 'lat', 'lon',  'ts', 'uid', 'chgset', 'user', 'ntags', 'tags']

elements = pd.DataFrame(reader.elements, columns=colnames)

print elements.head(10)

elements.to_csv("denver-boulder_colorado.csv", date_format='%Y-%m-%d %H:%M:%S')
