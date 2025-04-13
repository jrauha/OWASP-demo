from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare


class PlainTextPasswordHasher(BasePasswordHasher):
    algorithm = "plain"

    def encode(self, password, salt=None, iterations=None):
        return f"{self.algorithm}${password}"

    def verify(self, password, encoded):
        _, hash = encoded.split("$", 1)
        return constant_time_compare(password, hash)

    def safe_summary(self, encoded):
        algorithm, _ = encoded.split("$", 1)
        return {
            "algorithm": algorithm,
            "hash": hash,
        }

    def harden_runtime(self, password, encoded):
        pass
