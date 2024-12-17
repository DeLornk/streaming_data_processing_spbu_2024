DROP TABLE IF EXISTS kafka_messages;
DROP TABLE IF EXISTS kafka_messages_local;
DROP TABLE IF EXISTS kafka_to_local;

CREATE TABLE kafka_messages (
  market String,
  country String,
  product String,
  color String,
  price Float,
  time DateTime,
) ENGINE = Kafka SETTINGS 
                  kafka_broker_list = 'kafka:29092', 
                  kafka_topic_list = 'my_topic', 
                  kafka_group_name = 'clickhouse', 
                  kafka_format = 'JSONEachRow';

CREATE TABLE IF NOT EXISTS kafka_messages_local (
  market String,
  country String,
  product String,
  color String,
  price Float,
  time DateTime,
  processed_dttm DateTime default now()
) ENGINE = MergeTree() 
ORDER BY processed_dttm;

CREATE MATERIALIZED VIEW IF NOT EXISTS kafka_to_local TO kafka_messages_local AS 
SELECT 
  *,
  now() as processed_dttm
FROM kafka_messages;