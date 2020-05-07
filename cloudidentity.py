# Copyright 2020 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""In this package you have 1 classes:
 - GroupService: Simple to handle Cloud Identity APIs.
"""

import os
import copy
import json



class GroupService(object):
  def __init__(self, service, identitysources, tmp_path=None):
    self.service = service
    self.identitysources = identitysources
    self._tmp_path = tmp_path or 'tmp'

  @property
  def tmp_path(self):
    return self._tmp_path

  def _get_identitysource_name(self):
    return "identitysources/%s" % (self.identitysources)

  def _get_group_name(self, group_id):
    return "groups/%s" % (group_id,)

  

  def get(self, group_id):
    return self.service.groups().get(
        name=self._get_group_name(group_id)).execute()

  def memberships_list(self, group_id):
    results = self.service.groups().memberships().list(
        parent=self._get_group_name(group_id),
        pageSize=50).execute()

    output = []
    while results:
      for result in results.get('memberships', []):
        output.append(result)
      if results.get('nextPageToken'):
        results = self.service.groups().memberships().list(
        parent=self._get_group_name(group_id),
        pageToken=results.get('nextPageToken'),
        pageSize=50).execute()
      else:
        results = False
    return output
  def list(self):
    results = self.service.groups().list(
        parent=self._get_identitysource_name(),
        pageSize=50).execute()

    output = []
    while results:
      for result in results.get('groups', []):
        output.append(result)
      if results.get('nextPageToken'):
        results = self.service.groups().list(
            parent=self._get_identitysource_name(),
            pageToken=results.get('nextPageToken'),
            pageSize=50).execute()
      else:
        results = False
    return output
