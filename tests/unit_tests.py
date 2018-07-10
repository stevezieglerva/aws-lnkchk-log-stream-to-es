import unittest
from lambda_function import *
import time


class TestMethods(unittest.TestCase):
	def test_logging(self):
		# Arrange
		payload = ""
		with open("test_payload_logs_zip.json", "r") as f:
			payload = f.read()
			f.close()
		event = json.loads(payload)

		print(json.dumps(event, indent=True))

		# Act
		
		# Assert


if __name__ == '__main__':
	unittest.main()		


