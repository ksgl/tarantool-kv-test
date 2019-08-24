#!/usr/bin/env python

import re
import sys
import socket
import httplib
import json
import unittest

arg_host = "localhost"
arg_port = 8888
if len(sys.argv) > 1:
  arg_host = sys.argv[1]
if len(sys.argv) > 2:
  arg_port = int(sys.argv[2])

ctype = {'Content-type':'application/json'}

class HttpServer(unittest.TestCase):
  host = arg_host
  port = arg_port

  def setUp(self):
    self.conn = httplib.HTTPConnection(self.host, self.port, timeout=10)

  def tearDown(self):
    self.conn.close()

  def test_create_pair(self):
    body = {
            "key" : "1",
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.8,
            }
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    data = r.read()
    self.assertEqual(int(r.status), 200)
    self.assertDictEqual(json.loads(data), body)

  def test_create_pair_with_bad_key(self):
    body = {
            "key" : 1,
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.8,
            }
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 400)

  def test_create_pair_with_bad_value(self):
    body = {
            "key" : "1",
            "value" : "apple"
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 400)

  def test_create_pair_conflict(self):
    body = {
            "key" : "2",
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.8,
            }
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    data = r.read()
    self.assertEqual(int(r.status), 200)
    self.assertDictEqual(json.loads(data), body)

    body = {
            "key" : "2",
            "value" : {
                "fruit" : "orange",
                "calories" : 65,
                "protein" : 1,
                "fat" : 0.3,
                "carbs" : 16,
            }
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 409)

  def test_update_pair(self):
    body = {
            "key" : "3",
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.7,
            }
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    data = r.read()
    self.assertEqual(int(r.status), 200)
    self.assertDictEqual(json.loads(data), body)

    updatedBody =  {
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.8,
            }
        }

    self.conn.request("PUT", "/kv/3", body=json.dumps(updatedBody,indent=1),headers=ctype)
    r = self.conn.getresponse()
    data = r.read()
    self.assertEqual(int(r.status), 200)
    updatedBody["key"] = "3"
    self.assertDictEqual(json.loads(data), updatedBody)

  def test_update_pair_with_bad_value(self):
    body = {
            "key" : "4",
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.7,
            }
        }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    data = r.read()
    self.assertEqual(int(r.status), 200)
    self.assertDictEqual(json.loads(data), body)

    updatedBody =  {
            "value" : "apple"
        }

    self.conn.request("PUT", "/kv/4", body=json.dumps(updatedBody,indent=1),headers=ctype)
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 400)

  def test_update_nonexistent_pair(self):
    updatedBody =  {
            "value" : {
                "fruit" : "apple",
                "calories" : 52,
                "protein" : 0.3,
                "fat" : 0.2,
                "carbs" : 13.8,
            }
        }

    self.conn.request("PUT", "/kv/42", body=json.dumps(updatedBody,indent=1),headers=ctype)
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 404)

  def test_get_pair(self):
    body = {
        "key" : "5",
        "value" : {
            "fruit" : "apple",
            "calories" : 52,
            "protein" : 0.3,
            "fat" : 0.2,
            "carbs" : 13.8,
        }
    }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    r.read()
    self.assertEqual(int(r.status), 200)

    self.conn.request("GET", "/kv/5")
    r = self.conn.getresponse()
    data = r.read()
    self.assertEqual(int(r.status), 200)
    self.assertDictEqual(json.loads(data), body)

  def test_get_nonexistent_pair(self):
    self.conn.request("GET", "/kv/42")
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 404)

  def test_delete_pair(self):
    body = {
        "key" : "6",
        "value" : {
            "fruit" : "apple",
            "calories" : 52,
            "protein" : 0.3,
            "fat" : 0.2,
            "carbs" : 13.8,
        }
    }

    self.conn.request("POST", "/kv", body=json.dumps(body,indent=1),headers=ctype)
    r = self.conn.getresponse()
    r.read()
    self.assertEqual(int(r.status), 200)

    self.conn.request("DELETE", "/kv/6")
    r = self.conn.getresponse()
    r.read()
    self.assertEqual(int(r.status), 200)

  def test_delete_nonexistent_pair(self):
    self.conn.request("DELETE", "/kv/42")
    r = self.conn.getresponse()
    self.assertEqual(int(r.status), 404)

loader = unittest.TestLoader()
suite = unittest.TestSuite()
a = loader.loadTestsFromTestCase(HttpServer)
suite.addTest(a)

class NewResult(unittest.TextTestResult):
  def getDescription(self, test):
    doc_first_line = test.shortDescription()
    return doc_first_line or ""

class NewRunner(unittest.TextTestRunner):
  resultclass = NewResult

runner = NewRunner(verbosity=2)
runner.run(suite)
