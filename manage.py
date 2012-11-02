#!/usr/bin/env python
import os
import sys


def fix_mssql():
    from sqlserver_ado import creation
    creation.DatabaseCreation.data_types["TextField"] = "nvarchar(4000)"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aike.settings")

    from django.core.management import execute_from_command_line
    fix_mssql()
    execute_from_command_line(sys.argv)
