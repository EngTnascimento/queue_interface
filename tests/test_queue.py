import threading

import pytest
from pydantic import BaseModel

from queue_interface.rabbitMQ import RabbitMQ


class HelloMessage(BaseModel):
    content: str


sended_message = HelloMessage(content="Hello, RabbitMQ!")
num_messages = 10


def process_message(received_message):
    assert received_message == sended_message


def producer_task():
    producer_queue = RabbitMQ(queue="test", consumer=False, MessageModel=HelloMessage)
    for _ in range(num_messages):
        producer_queue.send(sended_message)
        print(f"Message sent: {sended_message.model_dump()}")


def consumer_task(stop_event):
    consumer_queue = RabbitMQ(queue="test", consumer=True, MessageModel=HelloMessage)
    count = 0
    for message in consumer_queue.receive():
        print(f"Received message: {message.content}")
        process_message(message)
        count += 1
        if count >= num_messages:
            stop_event.set()
            break


def bad_consumer_task(stop_event):
    bad_consumer_queue = RabbitMQ(
        queue="test", consumer=False, MessageModel=HelloMessage
    )
    count = 0
    try:
        for message in bad_consumer_queue.receive():
            print(f"Received bad message: {message.content}")
            count += 1
            if count >= num_messages:
                stop_event.set()
                break
        raise
    except Exception as e:
        assert "Not consumer instance cannot consume." in str(e)


def test_queue_behaviour():
    stop_event = threading.Event()

    consumer_thread = threading.Thread(target=consumer_task, args=(stop_event,))
    bad_consumer_thread = threading.Thread(target=bad_consumer_task, args=(stop_event,))

    producer_thread = threading.Thread(target=producer_task)

    bad_consumer_thread.start()
    consumer_thread.start()
    producer_thread.start()

    producer_thread.join()
    stop_event.wait()
    bad_consumer_thread.join()
    consumer_thread.join()


if __name__ == "__main__":
    pytest.main()
