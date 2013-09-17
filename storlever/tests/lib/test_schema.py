import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.schema = Schema({
            "key1": str,       # key1 should be string
            "key2": int,       # key2 should be int
            "key3": Use(int),  # key3 should be in or int in string
            "key4": IntVal(1, 99),   # key4 should be int between 1-99
            # key5 is optional,
            # should be str and default value is "value 5"
            Optional("key5"): Default(str, default="value5"),
            DoNotCare(str): object  # for all those key we don't care
        })

    def test_int_value(self):
        schema = Schema(IntVal())
        self.assertEquals(10, schema.validate(10))
        self.assertEquals(10, schema.validate('10'))
        with self.assertRaises(SchemaError):
            schema.validate('abc')

        schema = Schema(IntVal(values=(0, 1)))
        self.assertEqual(1, schema.validate(1))
        self.assertEqual(1, schema.validate("1"))
        with self.assertRaises(SchemaError):
            schema.validate(2)
        with self.assertRaises(SchemaError):
            schema.validate("2")

        schema = Schema(IntVal(min=10, max=100))
        self.assertEqual(10, schema.validate(10))
        self.assertEqual(100, schema.validate('100'))
        self.assertEqual(50, schema.validate(50))
        with self.assertRaises(SchemaError):
            schema.validate(200)
        with self.assertRaises(SchemaError):
            schema.validate(0)

        schema = Schema(IntVal(min=10, max=100, values=(0, 1)))
        self.assertEqual(0, schema.validate(0))
        self.assertEqual(100, schema.validate(100))
        self.assertEqual(50, schema.validate('50'))
        with self.assertRaises(SchemaError):
            schema.validate(2)
        with self.assertRaises(SchemaError):
            schema.validate(200)

        schema = Schema(IntVal(min=10, values=(0, 1)))
        self.assertEqual(200, schema.validate(200))
        self.assertEqual(1, schema.validate(1))
        with self.assertRaises(SchemaError):
            schema.validate(3)

    def test_optional_value(self):
        schema = Schema({
            "key": str,
            Optional("op_key"): IntVal()
        })
        data = schema.validate({"key": "abc"})
        self.assertEqual({"key": "abc"}, data)
        data = schema.validate({'key': 'abc', 'opt_key': 123})
        self.assertEqual({'key':'abc', 'op_key': 123}, data)
        with self.assertRaises(SchemaError):
            data = schema.validate({'key': 'abc', 'op_key': 'bcd'})

    def test_dict(self):
        data = self.schema.validate({
            "key1": "abc",
            "key2": 123,
            "key3": "223",
            "key4": 88,
        })
        self.assertDictEqual(data, {
            "key1": "abc",
            "key2": 123,
            "key3": 223,
            "key4": 88,
            "key5": "value5"
        })
