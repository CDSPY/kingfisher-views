"""select_collection_tables

Revision ID: 947ad833b815
Revises:
Create Date: 2019-02-18 12:31:24.495009

"""

import os

from alembic import op

dir_path = os.path.dirname(os.path.realpath(__file__))
sql_dir = os.path.join(dir_path, '../../sql/')

# revision identifiers, used by Alembic.
revision = '947ad833b815'
down_revision = None
branch_labels = None
depends_on = None


# This is duplicated in ocdskingfisherviews/migrations/versions/ef71f7dd7e45_no_default_views.py
def upgrade():
    sql_text = '''
    set search_path = views, public;
    create table extra_collections(collection_id integer primary key);


    create view selected_collections
    as
    select
       id
    from
       collection
    join
        (
        select
            source_id,
            data_version,
            row_number() over (partition by source_id order by data_version desc) date_order
        from (
            select
                source_id,
                data_version
            from
                collection
            where
                not sample
            group by
                source_id, data_version
            ) grouped
        ) with_date_order
        using
            (source_id, data_version)
    where
        date_order <= 2

    union

    select collection_id from extra_collections;
    '''
    op.execute(sql_text)


# This is duplicated in ocdskingfisherviews/migrations/versions/ef71f7dd7e45_no_default_views.py
def downgrade():

    sql_text = '''
    set search_path = views, public;
    drop view selected_collections;
    drop table extra_collections;
    '''
    op.execute(sql_text)
