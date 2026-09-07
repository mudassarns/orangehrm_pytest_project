import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    environment = "qa"

    @classmethod
    def get(cls, name):
        env_name = f"{cls.environment.upper()}_{name}"
        value = os.getenv(env_name)

        if not value:
            raise ValueError(f"{env_name} is not configured")

        return value