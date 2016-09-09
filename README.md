# Cassandra DB Cluster + Terminal Flask App

Dockerfile_DBを使ってCassandraのクラスターを作成し、Dockerfile_Terminalを使って、Cassandraを操作するFlaskウェブアプリケーションを作成する。
Flask側のサーバーは、brew、pip、cassandra driverそのほか、かなりのインストールが行われるのでDocker buildは時間がかかる。

## Dockerfile_Terminal_Centos、Dockerfile_Terminal_Debian
* cassandra_driver for pythonを利用して、Flaskアプリケーションから操作する
* Centos(yum)バージョンはuwsgiがうまく動いてないので、Debian版の方が調子がいい

### イメージを作成

`docker build -f ./Dockerfile_Terminal_Debian -t sog-cqlsh-term .`

### コンテナを作成
docker run --name cassandra_term -p 5000 -p 9090 -d sog-cqlsh-term



## Dockerfile
DockerでCassandraのクラスターを作成する

`docker build -f ./Dockerfile -t sog-cassandra .`

### cassandraイメージを取得し、コンテナcassandra1を作成
latest=3.0.4で動作確認

`docker run --name cassandra1 -m 2g -p 9042:9042 -d sog-cassandra`

### クラスター化するための、ネットワーク　IPを取得
`docker inspect --format='{{ .NetworkSettings.IPAddress }}' cassandra1`

### このネットワークアドレスに向けてcqlshコマンドで接続
`docker run -it --link cassandra1 --rm sog-cassandra sh -c 'exec cqlsh 172.17.0.2'`

### クラスターの形成 : cassandra2
`docker run --name cassandra2 -m 2g -p 9042 -d -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cassandra1)" sog-cassandra`

### ２インスタンスのクラスタが完成したので、nodetool statusで確認
* この時、statusがUP(U)でないと動作しないので注意
`docker exec -i -t cassandra1 sh -c 'nodetool status'`

### keyspaceとtableを作成してクラスタの動作確認
cassandra1ノード上で作業
`docker exec -it cassandra1 /bin/bash`

### ~/create_keyspace.cql を作成
`
    CREATE KEYSPACE test WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 2};
    USE test;
    CREATE TABLE test_table (
      id text,
      test_value text,
      PRIMARY KEY (id)
     );
    INSERT INTO test_table (id, test_value) VALUES ('1', 'one');
    INSERT INTO test_table (id, test_value) VALUES ('2', 'two');
    INSERT INTO test_table (id, test_value) VALUES ('3', 'three');
`

### CQLファイルを実行
`cqlsh -f create_keyspace.cql 172.17.0.2`

### クエリのテスト(cassandra1が172.17.0.2の場合）

`
    cqlsh 172.17.0.2
    cqlsh> use test;
    cqlsh:test> SELECT * FROM test_table;
`


### 今度は別のノード(cassandra2)からクエリのテスト

まずIPの確認

`docker inspect --format='{{ .NetworkSettings.IPAddress }}' cassandra2`


### cassandra2が172.17.0.3の場合

`
cqlsh 172.17.0.3
cqlsh> use test;
cqlsh:test> SELECT * FROM test_table;
`


### 同じデータが表示されればクラスタは成功。

#### 基本的なCQL

`
CREATE keyspace
CREATE KEYSPACE test WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 2};
DESCRIBE keyspaces;
DROP keyspace shop;
use shop;
`

古いCassandraではテーブルのことをcolumnfamilyと呼んでいる
`
create columnfamily GOODS (key text primary key, name text, price int);
describe columnfamily goods;
`

新しいCassandraではtableを使う。
`
create table PERSONS (key text primary key, name text, age int);
describe table persons;
`

### 参考
<http://yurisubach.com/2016/03/24/cassandra-docker-test-cluster/>
<http://qiita.com/masato/items/f0d924ef2854970a9391># cassandra_driver

### Auto Build
<https://hub.docker.com/r/someonesgarden/cassandra_driver>

