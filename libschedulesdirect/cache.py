#!/usr/bin/python
# coding=utf-8

import sqlite3
import json
import logging

class SchedulesDirectCache:

    def __init__(self, path):
        self._path = path
        self._logger = logging.getLogger(__name__)
        self._db = sqlite3.connect(self._path)
        self._cursor = self._db.cursor()

    def __enter__(self):
        self._logger.debug('__enter__()')
        self._open()
        return self

    def __exit__(self, type, value, traceback):
        self._logger.debug('__exit__()')
        self._commit()
        self._close()

    def _open(self):
        self._logger.debug('_open()')
        self._db = sqlite3.connect(self._path)
        self._cursor = self._db.cursor()

    def _commit(self):
        self._logger.debug('_commit()')
        if self._cursor is not None:
            self._db.commit()

    def _close(self):
        self._logger.debug('_close()')
        if self._db is not None:
            self._db.close()

    def init_database(self):
        self._logger.debug('init_database()')
        self._db.execute('''CREATE TABLE IF NOT EXISTS lineups
                (lineup_id TEXT PRIMARY KEY ON CONFLICT REPLACE, lineup_json TEXT, modified TEXT)''')
        self._db.execute('''CREATE TABLE IF NOT EXISTS programs
                (program_id TEXT PRIMARY KEY ON CONFLICT REPLACE, program_json TEXT, program_hash TEXT)''')
        self._db.execute('VACUUM')
        self._db.commit()

    def get_lineup(self, lineup_id, modified):
        self._logger.debug('get_lineup("%s", "%s")' % (lineup_id, modified))
        self._cursor.execute('SELECT lineup_json FROM lineups WHERE lineup_id = ? AND modified = ?', (lineup_id, modified))
        result = self._cursor.fetchone()
        if result is None:
            return None
        result = json.loads(result[0])
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('result:\n' + json.dumps(result, indent=4))
        return result

    def add_lineup(self, lineup_id, modified, lineup):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('add_lineup("%s", "%s", "%s")' % (lineup_id, modified, lineup))
        lineup_json = json.dumps(lineup)
        self._cursor.execute('''INSERT INTO lineups (lineup_id, lineup_json, modified)
            VALUES (?, ?, ?)''', (lineup_id, lineup_json, modified))
        self._db.commit()

    def get_program(self, program_id, program_hash=None):
        self._logger.debug('get_program("%s", "%s")' % (program_id, program_hash))
        if program_hash is None:
            self._cursor.execute('SELECT program_json FROM programs WHERE program_id = ?', (program_id,))
        else:
            self._cursor.execute('SELECT program_json FROM programs WHERE program_id = ? AND program_hash = ?', (program_id, program_hash))
        result = self._cursor.fetchone()
        if result is None:
            return None
        result = json.loads(result[0])
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('result:\n' + json.dumps(result, indent=4))
        return result

    def program_exists(self, program_id, program_hash):
        self._logger.debug('program_exists("%s", "%s")' % (program_id, program_hash))
        self._cursor.execute('SELECT 1 FROM programs WHERE program_id = ? AND program_hash = ?', (program_id, program_hash))
        result = self._cursor.fetchone()
        return result is not None

    def add_programs(self, programs):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('add_programs("%s")' % (programs))
        to_insert = [(program['programID'], json.dumps(program), program['md5']) for program in programs]
        self._db.executemany('''INSERT INTO programs (program_id, program_json, program_hash)
            VALUES (?, ?, ?)''', to_insert)
        self._db.commit()

if __name__ == "__main__":
    pass