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

"""This script list groups in a Google Cloud identitysource using 
the Cloud Identity API.


Prerequisites:
 - Google Cloud Identity enable on the gSuite organization
 - Created a Google Cloud Third-party identity sources ID
 - GCP project
 - Google Cloud Identity API enabled in the project
 - GCS bucket (Publicly readable)
 - GCP service account

To run this script, you will need Python3 packages listed in REQUIREMENTS.txt.

You can easily install them with virtualenv and pip by running these commands:
    virtualenv -p python3 env
    source ./env/bin/activate
    pip install -r REQUIREMENTS.txt

You can than run the script as follow:
    python item_list.py \
    --service_account_file /PATH/TO/service.json \
    --identitysources YOUR_IDENTITYSOURCES_ID 
"""

import argparse
import base64
import cloudidentity
import google.oauth2.credentials
import googleapiclient.http
import logging
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('cloudidentity.group_list')

# Scope grants [CLOUD SEARCH]
IDENTITY_SCOPES = ['https://www.googleapis.com/auth/cloud-identity']
IDENTITY_API_SERVICE_NAME = 'cloudidentity'
IDENTITY_API_VERSION = 'v1'


def get_authenticated_service(service_account_file, scope, service_name, version):
  # Create credentials from Service Account File
  credentials = service_account.Credentials.from_service_account_file(
      service_account_file, scopes=scope)
  return build(service_name, version, credentials=credentials, cache_discovery=False)


def main(service_account_file,
         identitysources):
  LOGGER.info('List groups - START')

  service_identity = get_authenticated_service(service_account_file,
                                             IDENTITY_SCOPES,
                                             IDENTITY_API_SERVICE_NAME,
                                             IDENTITY_API_VERSION)

  groupService = cloudidentity.GroupService(service_identity, identitysources)

  groups = groupService.list() or []
  for group in groups:
    LOGGER.info('\n******\n Group: %s \n DisplayName: %s \n******\n' %
                (group.get("name"), group.get("displayName")))
  LOGGER.info('List groups - END')
  return


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description='Example to parse HTML and send to CloudIdentity.')
  parser.add_argument('--service_account_file', dest='service_account_file',
                      help='File name for the service account.')
  parser.add_argument('--identitysources', dest='identitysources',
                      help='Identity source to list.')

  args = parser.parse_args()

  main(args.service_account_file,
       args.identitysources)
