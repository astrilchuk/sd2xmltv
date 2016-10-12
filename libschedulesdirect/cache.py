#!/usr/bin/python
# coding=utf-8

import sqlite3
import json
import logging
from . import jsonify, parse_date, result_iterator, batched
from common import Program, Schedule, ProgramArtwork
from contextlib import closing

class SchedulesDirectCache:
    def __init__(self, path):
        self._logger = logging.getLogger(__name__)
        self._path = path
        self._db = sqlite3.connect(self._path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self._db.row_factory = sqlite3.Row
        self._in_context = False

    def __enter__(self):
        self._logger.debug(u"__enter__()")
        self._in_context = True
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._logger.debug(u"__exit__()")
        try:
            if exception_type is None:
                self._commit()
            else:
                self._rollback()
        finally:
            self._in_context = False
        return False  # re-raise exception (if any)

    def _open(self):
        self._logger.debug(u"_open()")
        self._db = sqlite3.connect(self._path)

    def _commit(self):
        self._logger.debug(u"_commit()")
        self._db.commit()

    def _rollback(self):
        self._logger.debug(u"_rollback()")
        self._db.rollback()

    def _close(self):
        self._logger.debug(u"_close()")
        if self._db is not None:
            self._db.close()

    def init_database(self):
        self._logger.debug(u"init_database()")

        # sqlite 3.12.0+ uses default page_size of 4096 so set it for earlier versions
        self._db.execute("""PRAGMA page_size = 4096""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS lineups
                (lineup_id TEXT, lineup_json TEXT, modified DATE,
                PRIMARY KEY (lineup_id) ON CONFLICT REPLACE)""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS programs
                (program_id TEXT, program_json TEXT, program_hash TEXT, max_schedule_date DATE, artwork_id TEXT,
                PRIMARY KEY (program_id) ON CONFLICT REPLACE)""")

        self._db.execute("""CREATE INDEX IF NOT EXISTS programs_artwork_id_index ON programs (artwork_id)""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS schedules
                (station_id TEXT, schedule_date DATE, schedule_hash TEXT, schedule_json TEXT,
                PRIMARY KEY (station_id, schedule_date) ON CONFLICT REPLACE)""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS artwork
                (artwork_id TEXT, artwork_json TEXT,
                PRIMARY KEY (artwork_id) ON CONFLICT REPLACE)""")

        self._db.execute("""CREATE TEMP TABLE IF NOT EXISTS schedule_hashes
                (station_id TEXT, schedule_date DATE, schedule_hash TEXT,
                PRIMARY KEY (station_id, schedule_date) ON CONFLICT REPLACE)""")

        self._db.execute("""CREATE TEMP TABLE IF NOT EXISTS program_hashes
                (program_id TEXT, program_hash TEXT,
                PRIMARY KEY (program_id) ON CONFLICT REPLACE)""")

        self._db.commit()

    def compress_database(self):
        total_pages = self.get_total_pages()
        free_pages = self.get_free_pages()

        if free_pages / total_pages >= 0.2:
            self._logger.info(u"Free pages (%s) greater than 20%% of total pages (%s), executing vacuum.", free_pages, total_pages)
            self._db.execute("VACUUM")
        else:
            self._logger.info(u"Free pages (%s) less than 20%% of total pages (%s), skipping vacuum.", free_pages, total_pages)

        if not self._in_context:
            self._db.commit()

    def select_many(self, sql, parameters=(), fetch_size=250):
        with closing(self._db.cursor()) as cursor:
            cursor.execute(sql, parameters)
            for item in result_iterator(cursor, fetch_size):
                yield item

    def select_one(self, sql, parameters=()):
        with closing(self._db.cursor()) as cursor:
            cursor.execute(sql, parameters)
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None

    def get_free_pages(self):
        return self.select_one("PRAGMA freelist_count")[0]

    def get_total_pages(self):
        return self.select_one("PRAGMA page_count")[0]

    def get_lineup(self, lineup_id, modified=None):
        self._logger.debug(u"get_lineup('%s', '%s')", lineup_id, modified)
        if modified is None:
            sql = u"SELECT lineup_json FROM lineups WHERE lineup_id = ? LIMIT 1"
            result = self.select_one(sql, (lineup_id,))
        else:
            sql = u"SELECT lineup_json FROM lineups WHERE lineup_id = ? AND modified = ? LIMIT 1"
            result = self.select_one(sql, (lineup_id, modified))
        if result is None:
            return None
        return json.loads(result["lineup_json"])

    def add_lineup(self, lineup_id, modified, lineup):
        self._logger.debug(u"add_lineup('%s', '%s', %s)", lineup_id, modified, lineup)
        sql = u"INSERT INTO lineups (lineup_id, lineup_json, modified) VALUES (?, ?, ?)"
        cursor = self._db.execute(sql, (lineup_id, jsonify(lineup), modified))
        self._logger.debug(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def get_programs(self, program_ids):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(u"get_programs(%s)", program_ids)
        for batch in batched(program_ids, 999):
            sql = u"SELECT program_json FROM programs WHERE program_id IN ({0})".format(u",".join(u"?" * len(batch)))
            for item in self.select_many(sql, batch):
                yield json.loads(item["program_json"], object_hook=Program.from_dict)

    def get_artwork(self, artwork_ids):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(u"get_artwork(%s)", artwork_ids)
        for batch in batched(artwork_ids, 999):
            sql = u"SELECT artwork_json FROM artwork WHERE artwork_id IN ({0})".format(u",".join(u"?" * len(batch)))
            for item in self.select_many(sql, batch):
                yield json.loads(item['artwork_json'], object_hook=ProgramArtwork.from_dict)

    def add_programs(self, programs):
        self._logger.debug(u"add_programs()")
        to_insert = [(program["programID"], jsonify(program), program["md5"], program["programID"][0:10] if program.get("hasImageArtwork", False) else None) for program in programs]
        sql = u"INSERT INTO programs (program_id, program_json, program_hash, artwork_id) VALUES (?, ?, ?, ?)"
        cursor = self._db.executemany(sql, to_insert)
        self._logger.debug(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def add_artwork(self, artwork):
        self._logger.debug(u"add_artwork()")
        to_insert = [(art["programID"], jsonify(art)) for art in artwork]
        sql = u"INSERT INTO artwork (artwork_id, artwork_json) VALUES (?, ?)"
        cursor = self._db.executemany(sql, to_insert)
        self._logger.debug(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def add_program_hashes(self, program_hashes):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(u"add_program_hashes(%s)", program_hashes)
        sql = u"INSERT INTO program_hashes (program_id, program_hash) VALUES (?, ?)"
        cursor = self._db.executemany(sql, program_hashes)
        self._logger.debug(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def get_program_delta(self):
        self._logger.debug(u"get_program_delta()")
        sql = u"SELECT program_id FROM program_hashes LEFT JOIN programs USING (program_id, program_hash) WHERE programs.program_id IS NULL"
        for item in self.select_many(sql):
            yield item["program_id"]

    def get_artwork_delta(self):
        self._logger.debug(u"get_artwork_delta()")
        sql = u"SELECT DISTINCT artwork_id FROM programs LEFT JOIN artwork USING (artwork_id) WHERE programs.artwork_id IS NOT NULL AND artwork.artwork_id IS NULL"
        for item in self.select_many(sql):
            yield item["artwork_id"]

    def get_schedule_delta(self):
        self._logger.debug(u"get_schedule_delta()")
        sql = u"SELECT station_id, schedule_date FROM schedule_hashes LEFT JOIN schedules USING (station_id, schedule_date, schedule_hash) WHERE schedules.station_id IS NULL"
        for item in self.select_many(sql):
            yield (item["station_id"], item["schedule_date"])

    def add_schedule_hashes(self, schedule_hashes):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(u"add_schedule_hashes(%s)", schedule_hashes)
        sql = u"INSERT INTO schedule_hashes (station_id, schedule_date, schedule_hash) VALUES (?, ?, ?)"
        cursor = self._db.executemany(sql, schedule_hashes)
        self._logger.info(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def get_schedules(self, schedule_keys):
        self._logger.debug(u"get_schedules()")
        for (station_id, schedule_date) in schedule_keys:
            sql = u"SELECT schedule_json FROM schedules WHERE (:station_id IS NULL OR station_id = :station_id) AND (:schedule_date IS NULL OR schedule_date = :schedule_date)"
            result = self.select_many(sql, {"station_id": station_id, "schedule_date": schedule_date})
            for item in result:
                yield json.loads(item["schedule_json"], object_hook=Schedule.from_dict)

    def add_schedules(self, schedules):
        self._logger.debug(u"add_schedules()")
        to_insert = [(schedule["stationID"], parse_date(schedule["metadata"]["startDate"]), jsonify(schedule), schedule["metadata"]["md5"]) for schedule in schedules]
        sql = u"INSERT INTO schedules (station_id, schedule_date, schedule_json, schedule_hash) VALUES (?, ?, ?, ?)"
        cursor = self._db.executemany(sql, to_insert)
        self._logger.debug(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def update_program_max_schedule_dates(self, programs):
        self._logger.info(u"update_program_max_schedule_dates()")
        to_update = [{"program_id": program_id, "max_schedule_date": max_schedule_date} for (program_id, max_schedule_date) in programs]
        sql = u"UPDATE programs SET max_schedule_date = :max_schedule_date WHERE program_id = :program_id AND (max_schedule_date IS NULL OR max_schedule_date < :max_schedule_date)"
        cursor = self._db.executemany(sql, to_update)
        self._logger.info(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def delete_expired_programs(self):
        self._logger.info(u"delete_expired_programs()")
        sql = u"DELETE FROM programs WHERE max_schedule_date IS NULL OR max_schedule_date NOT IN (SELECT DISTINCT schedule_date FROM schedule_hashes)"
        cursor = self._db.execute(sql)
        self._logger.info(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def delete_expired_schedules(self):
        self._logger.info(u"delete_expired_schedules()")
        sql = u"DELETE FROM schedules WHERE station_id NOT IN (SELECT DISTINCT station_id FROM schedule_hashes) OR schedule_date NOT IN (SELECT DISTINCT schedule_date FROM schedule_hashes)"
        cursor = self._db.execute(sql)
        self._logger.info(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()

    def delete_expired_artwork(self):
        self._logger.info(u"delete_expired_artwork")
        sql = u"DELETE FROM artwork WHERE artwork_id NOT IN (SELECT DISTINCT artwork_id FROM programs)"
        cursor = self._db.execute(sql)
        self._logger.info(u"%s rows affected.", cursor.rowcount)
        if not self._in_context:
            self._db.commit()


if __name__ == "__main__":
    pass
