import os
import logging
import twitter
import unittest
import tempfile


class TwitterTestCase(unittest.TestCase):
    def list_user(self):
        self.list_user()
        rv = self.app.post('/users', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data



if __name__ == '__main__':
    unittest.main()
