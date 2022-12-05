from base import do
from base.enums import RoleType
from typing import Sequence
import exceptions as exc

import asyncpg

from .util import pyformat2psql
from . import pool_handler


async def add(username: str, pass_hash: str) -> int:
    sql, params = pyformat2psql(
        sql=fr'INSERT INTO account'
            fr'            (username, pass_hash, role, real_name, student_id)'
            fr'     VALUES (%(username)s, %(pass_hash)s, %(role)s, %(real_name)s, LOWER(%(student_id)s))'
            fr'  RETURNING id',
        username=username, pass_hash=pass_hash,
    )
    try:
        id_, = await pool_handler.pool.fetchrow(sql, *params)
    except asyncpg.exceptions.UniqueViolationError:
        raise exc.UniqueViolationError
    return id_


async def read(account_id: int) -> do.Account:
    sql, params = pyformat2psql(
        sql=fr"SELECT id, username, role, student_id, real_name"
            fr"  FROM account"
            fr" WHERE id = %(account_id)s",
        account_id=account_id
    )
    try:
        id_, username, role, student_id, real_name = await pool_handler.pool.fetchrow(sql, *params)
    except TypeError:
        raise exc.NotFound
    return do.Account(id=id_, username=username, role=RoleType(role),
                      student_id=student_id, real_name=real_name)


async def read_by_username(username: str) -> tuple[int, str, RoleType]:
    sql, params = pyformat2psql(
        sql=fr"SELECT id, pass_hash, role"
            fr"  FROM account"
            fr" WHERE username = %(username)s",
        username=username,
    )
    id_, pass_hash, role = await pool_handler.pool.fetchrow(sql, *params)
    return id_, pass_hash, RoleType(role)


async def is_duplicate_student_id(student_id: str) -> bool:
    sql, params = pyformat2psql(
        sql=fr"SELECT COUNT(*) FROM account"
            fr" WHERE student_id = LOWER(%(student_id)s)",
        student_id=student_id
    )
    count, = await pool_handler.pool.fetchrow(sql, *params)
    return count > 0


async def delete(account_id: int) -> None:
    sql, params = pyformat2psql(
        sql=fr"DELETE FROM account"
            fr" WHERE id = %(account_id)s",
        account_id=account_id
    )
    return await pool_handler.pool.execute(sql, *params)


async def browse_by_role(role: RoleType) -> Sequence[do.Account]:
    sql, params = pyformat2psql(
        sql=fr"SELECT id, username, role, student_id, real_name"
            fr"  FROM account"
            fr" WHERE role = %(role)s"
            fr" ORDER BY id ASC",
        role=role.value,
    )
    records = await pool_handler.pool.fetch(sql, *params)
    return [do.Account(id=id_, username=username, role=RoleType(role), real_name=real_name, student_id=student_id)
            for id_, username, role, real_name, student_id in records]
