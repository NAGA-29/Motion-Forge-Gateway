import os
import unittest
import logging
from importlib import reload
from unittest.mock import patch

from app.utils import logger as logger_module

class TestAppLogger(unittest.TestCase):
    """AppLoggerの設定反映とレベル設定を確認するテスト。"""

    def tearDown(self):
        # reset configuration after each test
        logger_module.AppLogger._configured = False

    @patch.dict(os.environ, {"LOG_LEVEL": "DEBUG", "APP_ENV": "local"})
    def test_log_level_env(self):
        """環境変数によってログレベルが設定されることを検証する。"""
        logger_module.AppLogger._configured = False
        logger = logger_module.AppLogger.get_logger('test')
        self.assertEqual(logger.getEffectiveLevel(), logging.DEBUG)

if __name__ == '__main__':
    unittest.main()
