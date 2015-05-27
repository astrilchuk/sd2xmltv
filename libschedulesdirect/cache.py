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
        self._cursor.execute(
            '''CREATE TABLE IF NOT EXISTS lineups
                (lineup_id TEXT PRIMARY KEY ON CONFLICT REPLACE, lineup_json TEXT, modified TEXT)''')
        self._cursor.execute(
            '''CREATE TABLE IF NOT EXISTS programs
                (program_id TEXT PRIMARY KEY ON CONFLICT REPLACE, program_json TEXT, program_hash TEXT)''')
        self._cursor.execute(
            '''CREATE TABLE IF NOT EXISTS schedules
                (station_id TEXT, schedule_date TEXT, schedule_json TEXT, schedule_hash TEXT, PRIMARY KEY (station_id, schedule_date) ON CONFLICT REPLACE)''')
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

    def get_schedule(self, station_id, schedule_hash):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('get_schedule("%s","%s")' % (station_id, schedule_hash))
        self._cursor.execute('SELECT schedule_json FROM schedules WHERE station_id = ? AND schedule_hash = ?', (station_id, schedule_hash))
        result = self._cursor.fetchone()
        if result is None:
            self._logger.debug('result: cache miss')
            return None
        result = json.loads(result[0])
        self._logger.debug('result: cache hit')
        return result

    def add_schedule(self, station_id, schedule_date, schedule_hash, schedule):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('add_schedule("%s", "%s", "%s", "%s")' % (station_id, schedule_date, schedule_hash, schedule))
        schedule_json = json.dumps(schedule)
        self._cursor.execute('''INSERT INTO schedules (station_id, schedule_date, schedule_json, schedule_hash)
            VALUES (?, ?, ?, ?)''', (station_id, schedule_date, schedule_json, schedule_hash))
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

    def add_program(self, program):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('add_program("%s")' % (program))
        program_json = json.dumps(program)
        self._cursor.execute('''INSERT INTO programs (program_id, program_json, program_hash)
            VALUES (?, ?, ?)''', (program['programID'], program_json, program['md5']))
        self._db.commit()

if __name__ == "__main__":
    pass