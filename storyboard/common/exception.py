# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from wsme.exc import ClientSideError

from storyboard.openstack.common.gettextutils import _  # noqa


class StoryboardException(ClientSideError):
    """Base Exception for the project

    To correctly use this class, inherit from it and define
    the 'message' property.
    """

    message = _("An unknown exception occurred")

    def __str__(self):
        return self.message

    def __init__(self, message=None, status_code=None):
        super(StoryboardException, self).__init__(msg=message,
                                                  status_code=status_code)


class NotFound(StoryboardException):
    message = _("Object not found")

    def __init__(self, message=None):
        super(NotFound, self).__init__(message, 404)


class NotEmpty(StoryboardException):
    message = _("Database object must be empty")

    def __init__(self, message=None):
        if message:
            self.message = message


class DBException(StoryboardException):
    # Base exception for database errors

    message = _("Database Exception")

    def __init__(self, message=None, status_code=None):
        """Constructor for base exception class

        :param: message: exception message.
        :param: status_code: code of exception.
        """
        if not status_code:
            status_code = 400

        super(DBException, self).__init__(message=message,
                                          status_code=status_code)


class DBDuplicateEntry(DBException):
    """Duplicate entry exception

    This exception wraps the same exception from database.
    """

    message = _("Database object already exists.")

    def __init__(self, message=None, object_name=None, value=None,
                 status_code=None):
        """Constructor for duplicate entry exception

        :param : message: This message will be shown after exception raised.
        :param : object_name: This parameter is name of object, in which
        exception was raised.
        :param: value: Invalid value.
        :param: status_code: code of exception.

        If object_name or value is not 'None', to message will be appended with
        new message with information about object name or invalid value
        """

        super(DBDuplicateEntry, self).__init__(message=message,
                                               status_code=status_code)
        db_message = None

        if object_name or value:
            db_message_list = [_("Database object")]

            if object_name:
                db_message_list.append(_("\'%s\'") % object_name)

            if value:
                db_message_list.append(_("with field value \'%s\'") % value)
            else:
                db_message_list.append(_("with some of unique fields"))

            db_message_list.append(_("already exists."))
            db_message = _(" ").join(db_message_list)

        if db_message:
            message_list = []

            if message:
                message_list.append(message)

            message_list.append(db_message)
            self.msg = " ".join(message_list)


class DBConnectionError(DBException):
    """Connection error exception

    This exception wraps the same exception from database.
    """

    message = _("Connection to database failed.")


class ColumnError(DBException):
    """Column error exception

    This exception wraps the same exception from database.
    """

    message = _("Column is invalid or not found")


class DBDeadLock(DBException):
    """Deadlock exception

    This exception wraps the same exception from database.
    """

    message = _("Database in dead lock")


class DBInvalidUnicodeParameter(DBException):
    """Invalid unicode parameter exception

    This exception wraps the same exception from database.
    """

    message = _("Unicode parameter is passed to "
                "a database without encoding directive")


class DBMigrationError(DBException):
    """Migration error exception

    This exception wraps the same exception from database.
    """

    message = _("migrations could not be completed successfully")


class DBReferenceError(DBException):
    """Reference error exception

    This exception wraps the same exception from database.
    """

    message = _("Foreign key error.")

    def __init__(self, message=None, object_name=None, value=None,
                 key=None, status_code=None):
        """Constructor for duplicate entry exception

        :param : message: This message will be shown after exception raised.
        :param : object_name: This parameter is name of object, in which
        exception was raised.
        :param: value: Invalid value.
        :param : key: Field with invalid value.
        :param : status_code: code of exception.

        If object_name or value or key is not 'None', to message will be
        appended with new message with information about object name or
        invalid value or field with invalid value.
        """

        super(DBReferenceError, self).__init__(message=message,
                                               status_code=status_code)
        db_message = None

        if object_name or value or key:
            db_message_list = []

            if object_name:
                db_message_list.append(
                    _("Error in object"))
                db_message_list.append(_("\'%s\'.") % object_name)

            if value or key:
                db_message_list.append(_("Field"))

                if key:
                    db_message_list.append(_("\'%s\'") % key)

                if value:
                    db_message_list.append(_("value"))
                    db_message_list.append(_("\'%s\'") % value)

                db_message_list.append(_("is invalid."))

            db_message = " ".join(db_message_list)

        if db_message:
            message_list = []

            if message:
                message_list.append(message)
            else:
                message_list.append(self.message)

            message_list.append(db_message)
            self.msg = " ".join(message_list)


class DBInvalidSortKey(DBException):
    """Invalid sortkey error exception

    This exception wraps the same exception from database.
    """

    message = _("Invalid sort field")
