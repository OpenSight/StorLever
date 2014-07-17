import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, AutoDel


class TestSchema(unittest.TestCase):

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

    def test_bool_value(self):
        schema = Schema(BoolVal())
        self.assertEquals(True, schema.validate(True))
        self.assertEquals(True, schema.validate("True"))
        self.assertEquals(True, schema.validate("true"))

        self.assertEquals(False, schema.validate(False))
        self.assertEquals(False, schema.validate("False"))
        self.assertEquals(False, schema.validate("false"))

        with self.assertRaises(SchemaError):
            schema.validate(0)

        with self.assertRaises(SchemaError):
            schema.validate(1)

        with self.assertRaises(SchemaError):
            schema.validate("abc")

    def test_strre_value(self):
        schema = Schema(StrRe("^(abc|efg)$"))
        self.assertEquals("abc", schema.validate("abc"))
        self.assertEquals("efg", schema.validate("efg"))

        with self.assertRaises(SchemaError):
            schema.validate("ebc")

        with self.assertRaises(SchemaError):
            schema.validate("abcdefg")

        with self.assertRaises(SchemaError):
            schema.validate(0)

        with self.assertRaises(SchemaError):
            schema.validate(1)

    def test_optional_value(self):
        schema = Schema({
            "key": str,
            Optional("op_key"): IntVal()
        })
        data = schema.validate({"key": "abc"})
        self.assertEqual({"key": "abc"}, data)
        data = schema.validate({'key': 'abc', 'op_key': 123})
        self.assertEqual({'key': 'abc', 'op_key': 123}, data)
        with self.assertRaises(SchemaError):
            schema.validate({'key': 'abc', 'op_key': 'bcd'})

    def test_autodel(self):
        schema = Schema({
            'key': str,
            AutoDel(str): object
        })
        schema2 = Schema({
            'key': str
        })
        data = schema.validate({'key': 'abc', 'key2': 'bbb', 'key3': [1, 2, 3]})
        self.assertEqual({'key': 'abc'}, data)
        with self.assertRaises(SchemaError):
            schema2.validate({'key': 'abc', 'key2': 'bbb', 'key3': [1, 2, 3]})

        with self.assertRaises(SchemaError):
            schema.validate({'key2': 'bbb', 1: [1, 2, 3]})


    def test_default_value(self):
        schema = Schema({
            "key": str,
            Optional('op_key'): Default(IntVal(min=10), default=50)
        })
        data = schema.validate({'key': 'abc'})
        self.assertEqual({'key': 'abc', 'op_key': 50}, data)
        data = schema.validate({'key': 'abc', 'op_key': 20})
        self.assertEqual({'key': 'abc', 'op_key': 20}, data)
        with self.assertRaises(SchemaError):
            schema.validate({'key': 'abc', 'op_key': 0})

    def test_donot_care(self):
        schema = Schema({
            'key': str,
            DoNotCare(str): object
        })
        data = schema.validate({'key': 'abc', 'key2': 'bbb', 'key3': [1, 2, 3]})
        self.assertEqual({'key': 'abc', 'key2': 'bbb', 'key3': [1, 2, 3]}, data)
        with self.assertRaises(SchemaError):
            schema.validate({'key2': 'bbb', 'key3': [1, 2, 3]})

    def test_list(self):
        schema = Schema([str])
        self.assertEqual(schema.validate(['abc', 'bbc', 'ddc']),
                         ['abc', 'bbc', 'ddc'])
        with self.assertRaises(SchemaError):
            schema.validate(['abc', 123, 'bbc'])
        schema = Schema([IntVal(min=10, max=20)])
        self.assertEqual(schema.validate([10, 12, 19, 11]), [10, 12, 19, 11])
        with self.assertRaises(SchemaError):
            schema.validate([10, 12, 21])

    def test_dict(self):
        schema = Schema({
            "key1": str,       # key1 should be string
            "key2": Use(int),  # key3 should be in or int in string
            "key3": [IntVal(min=10, max=20)],
            # key4 is optional,
            Optional("key4"): str,
            Optional('key5'): Default(IntVal(min=100, max=200), default=100),
            DoNotCare(str): object  # for all those key we don't care
        })

        data = schema.validate({
            "key1": "abc",
            "key2": '123',
            "key3": [10, 15, 20],
            "key5": 199,
        })
        self.assertEqual(data, {
            "key1": "abc",
            "key2": 123,
            "key3": [10, 15, 20],
            "key5": 199
        })

        data = schema.validate({
            "key1": "abc",
            "key2": '123',
            "key3": [10, 15, 20],
        })
        self.assertEqual(data, {
            "key1": "abc",
            "key2": 123,
            "key3": [10, 15, 20],
            "key5": 100
        })

        data = schema.validate({
            "key1": "abc",
            "key2": '123',
            "key3": [10, 15, 20],
            "key4": 'abc'
        })
        self.assertEqual(data, {
            "key1": "abc",
            "key2": 123,
            "key3": [10, 15, 20],
            "key4": 'abc',
            "key5": 100
        })

        data = schema.validate({
            "key1": "abc",
            "key2": '123',
            "key3": [10, 15, 20],
            "key4": 'abc',
            "key100": 'bbc',
            'key200': [123, 23, 334]
        })
        self.assertEqual(data, {
            "key1": "abc",
            "key2": 123,
            "key3": [10, 15, 20],
            "key4": 'abc',
            "key5": 100,
            "key100": 'bbc',
            'key200': [123, 23, 334]
        })

        with self.assertRaises(SchemaError):
            schema.validate({
                'key1': 123,
                "key2": '123',
                "key3": [10, 15, 20],
                "key4": 223,
            })
        with self.assertRaises(SchemaError):
            schema.validate({
                'key1': 123,
                "key2": '123',
                "key3": [10, 15, 20],
                "key4": 'abc',
                "key100": 'bbc',
                'key200': [123, 23, 334]
            })
        with self.assertRaises(SchemaError):
            schema.validate({
                'key1': 'abc',
                "key2": '123',
                "key3": [10, 15, 20],
                "key4": 'abc',
                'key5': 0,
                "key100": 'bbc',
                'key200': [123, 23, 334]
            })

