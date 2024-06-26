import base64
import subprocess

import pika as pk
from pydantic import Field
from pydantic_settings import BaseSettings


class RabbitMQConfig(BaseSettings):
    username: str = Field(default="user")
    password: str = Field(default_factory=lambda: RabbitMQSetup.get_secret())
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=5672)


class RabbitMQSetup:
    def __init__(self):
        self.config = RabbitMQConfig()
        self.credentials = pk.PlainCredentials(
            self.config.username, self.config.password
        )
        self.parameters = pk.ConnectionParameters(
            host=self.config.host, port=self.config.port, credentials=self.credentials
        )
        self.connection = pk.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    @staticmethod
    def get_secret() -> str:
        try:
            # Define the kubectl command
            command = [
                "kubectl",
                "get",
                "secret",
                "--namespace",
                "default",
                "rabbitmq",
                "-o",
                "jsonpath={.data.rabbitmq-password}",
            ]

            # Run the command and capture the output
            result = subprocess.check_output(command).strip()

            # Decode the base64 output
            password = base64.b64decode(result).decode("utf-8")

            return password
        except subprocess.CalledProcessError as e:
            raise e


QueueSetup = RabbitMQSetup
