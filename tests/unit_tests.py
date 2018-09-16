import unittest
from lambda_function import *
import time


class TestMethods(unittest.TestCase):
	def test_extract_json_from_message_line__regular_line__no_json(self):
		# Arrange
		message = "END RequestId: 85d5df48-b9e7-11e8-bed1-f900f13a12fd\n"

		# Act
		result = extract_json_from_message_line(message)

		# Assert
		self.assertEqual(result, "")

	def test_extract_json_from_message_line__multiple_lines_without_json__no_json(self):
		# Arrange
		message = "test\nline 1\nline 2"

		# Act
		result = extract_json_from_message_line(message)

		# Assert
		self.assertEqual(result, "")

if __name__ == '__main__':
	unittest.main()		


