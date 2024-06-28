from typing import Callable, Generator, Type

import pika as pk
from pydantic import BaseModel, ValidationError

from .queue import Queue
from .queue_setup import RabbitMQConfig, RabbitMQSetup


class RabbitMQ(Queue):
    def __init__(
        self,
        queue: str,
        consumer: bool,
        MessageModel: Type[BaseModel],
        config: RabbitMQConfig = RabbitMQConfig(),
        exchange="",
    ) -> None:
        setup = RabbitMQSetup(config)
        super().__init__(setup)
        self.queue = queue
        self.MessageModel = MessageModel
        self.exchange = exchange
        self.consumer = consumer

        try:
            self.setup.channel.queue_declare(queue=self.queue, passive=consumer)
        except pk.exceptions.ChannelClosedByBroker as e:  # pyright: ignore
            print(f"Queue {self.queue} does not exists!: {e}")
            self.setup.connection.close()

    def send(self, message: BaseModel):
        try:
            self.MessageModel(**message.model_dump())
        except ValidationError as e:
            raise ValueError(f"Invalid message: {e}")

        self.setup.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=message.model_dump_json(),
        )

    def receive(self) -> Generator:
        if not self.consumer:
            raise ValueError("Not consumer instance cannot consume.")

        for method_frame, _, body in self.setup.channel.consume(self.queue):
            self.setup.channel.basic_ack(method_frame.delivery_tag)
            yield self.MessageModel.model_validate_json(body)

    def consume(self, process_message: Callable):
        if not self.consumer:
            raise ValueError("Not consumer instance cannot consume.")

        def callback(ch, method, properties, body):
            message = self.MessageModel.model_validate_json(body)
            process_message(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.setup.channel.basic_consume(queue=self.queue, on_message_callback=callback)

        try:
            print("Waiting for messages. To exit press CTRL+C")
            self.setup.channel.start_consuming()
        except KeyboardInterrupt:
            self.setup.channel.stop_consuming()
        finally:
            self.close()

    def close(self):
        self.setup.connection.close()

    def __del__(self):
        if self.setup and self.setup.connection.is_open:
            self.setup.connection.close()
