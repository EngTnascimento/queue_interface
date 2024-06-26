# Message Queue Library

A Python library to abstract the behavior of message queues, supporting both RabbitMQ and Apache Kafka. This library provides a common interface for sending and receiving messages, making it easier to switch between different message brokers.

## Features

- Abstract `Queue` class for a unified interface
- RabbitMQ support with `RabbitMQQueue` implementation
- Kafka support (future implementation)
- Easy configuration using Pydantic
- Simple worker pattern for consuming messages

## Requirements

- Python 3.7+

## Install

- pip install git+https://github.com/EngTnascimento/queue_interface@main
