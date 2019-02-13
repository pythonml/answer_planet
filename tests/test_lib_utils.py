from django.test import TestCase
import lib.utils

class Test(TestCase):
    def test_generate_invite_code(self):
        result = lib.utils.generate_invite_code("hello")
        print(result)
        result = lib.utils.generate_invite_code("hellp")
        print(result)

