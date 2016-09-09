from cassandra.cluster import Cluster
cluster = Cluster(
    contact_points=['192.168.99.100'], port=9042
)

session = cluster.connect()
session.set_keyspace("test")
results = session.execute("select * from test_table")


for result in results:
    print result.id, result.test_value

result = session.execute("CREATE keyspace SHOP2 WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 2};")[0];

print result;


