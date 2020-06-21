from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available
        started execute (call_command)in the wait_for_db command
        we try to get database connection which try to execute
        (django.db.utils.ConnectionHandler.__getitem__) in rela time . but
        here , when  trying to execute this __getitem__, this does not execute,
        instead of this, just return the result (gi.return_value = True),
        that's how we can test database connecetion by unit testing without
        calling actual database
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
