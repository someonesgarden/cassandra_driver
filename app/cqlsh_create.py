from cassandra.cluster import Cluster
cluster = Cluster(
    contact_points=['192.168.99.100'], port=9042
)
session = cluster.connect()



result = session.execute("CREATE keyspace firsttable WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 2};");
session.set_keyspace("firsttable")

print result;


