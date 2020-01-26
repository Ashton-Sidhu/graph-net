Kafka
---

This uses the docker installation of Kafka from https://github.com/wurstmeister/kafka-docker.

## Installation

`start-kafka.sh`

To add more brokers:

  - `docker-compose scale kafka=$NUM_BROKERS`
