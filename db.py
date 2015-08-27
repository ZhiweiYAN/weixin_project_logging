#!/usr/bin/env python
#-*- coding:utf-8 -*

"""Provide the interface functions about the database.

Here we define the table structures, connect the database
through a proxy. The PostgreSQL database is choosen in the
project.
"""

__author__ = "Zhe Yan, Zhiwei Yan"
__copyright__ = "Copyright 2015, The Workflow&Weixin Project"
__credits__ = ["Weiming Guo"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Zhiwei YAN"
__email__ = "jerod.yan@gmail.com"
__status__ = "Production"

import datetime 
from peewee import *
import logging
import logmsg

#dynamically defining a database through a proxy
database_proxy = Proxy()

#definition of tables
class BaseModel(Model):
    class Meta:
        database = database_proxy

#work flow
class Work_Flow(BaseModel):
    creator_id = CharField(default='N/A')
    creator_name = CharField(default='N/A')

    flow_title = TextField(default='N/A')
    flow_description = TextField(default='N/A')

    flow_created_timestamp = DateTimeField(default=datetime.datetime.now)
    flow_last_updated_timestamp = DateTimeField(default=datetime.datetime.now)

    flow_participant_id_list = TextField(default='N/A')

# workflow state: open or close.
    flow_state = TextField(default='close')
    flow_timeline_table_name = TextField(default='N/A')

    tinyurl = CharField(default='N/A')
    bookmark_color = CharField(default='#FFFFFF');

# staff list table for the department.
class Staff_List(BaseModel):
    staff_id = CharField(default='N/A')
    participanting_workflow_id_list = TextField(default='N/A')
    following_workflow_id_list = TextField(default='N/A')

# work flow timeline table for one project.
class Work_Flow_Timeline(BaseModel):
    work_flow_id = IntegerField(default=0)
    staff_id = CharField(default='N/A')
    staff_name = CharField(default='N/A')
    update_time = DateTimeField(default=datetime.datetime.now)
    details = TextField(default='N/A')
    child_work_flow_id = IntegerField(default=0)
    following_staff_list = TextField(default='N/A')
    item_state = TextField(default='N/A')
    bookmark_color = CharField(default='N/A');
    pic_url = TextField(default='N/A');

# Initialize the database tables
def InitDBTables(db_name, db_user, db_pw, db_host, db_port):

    db_conn = PostgresqlDatabase(db_name, user=db_user, \
                 password=db_pw, host=db_host, port=db_port)

    database_proxy.initialize(db_conn)

    if (not Work_Flow.table_exists()):
        Work_Flow.create_table()
        logging.info("Create table [Work_Flow]")
    else:
        logging.info("Table has existed.")

    if (not Staff_List.table_exists()):
        Staff_List.create_table()
        logging.info("Create table Staff_List")
    else:
        logging.info("Table has existed.")
    if (not Work_Flow_Timeline.table_exists()):
        Work_Flow_Timeline.create_table()
        logging.info("Create table Work_Flow_Timeline")
    else:
        logging.info("Table has existed.")

    return True
# end of the source file
