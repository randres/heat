# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from heat.common import exception


class Timestamp(object):
    '''
    A descriptor for fetching an up-to-date timestamp from the database.
    '''

    def __init__(self, db_fetch, attribute):
        '''
        Initialise with a function to fetch the database representation of an
        object (given a context and ID) and the name of the attribute to
        retrieve.
        '''
        self.db_fetch = db_fetch
        self.attribute = attribute

    def __get__(self, obj, obj_class):
        '''
        Get the latest data from the database for the given object and class.
        '''
        if obj is None or obj.id is None:
            return None

        o = self.db_fetch(obj.context, obj.id)
        o.refresh(attrs=[self.attribute])
        return getattr(o, self.attribute)

    def __set__(self, obj, timestamp):
        '''Update the timestamp for the given object.'''
        if obj.id is None:
            raise exception.ResourceNotAvailable(resource_name=obj.name)
        o = self.db_fetch(obj.context, obj.id)
        o.update_and_save({self.attribute: timestamp})
