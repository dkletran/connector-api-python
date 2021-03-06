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

"""This script create or update a schema in a Google Cloud Search datasource using 
the Cloud Search API.


Prerequisites:
 - Google Cloud Search enable on the gSuite organization
 - Created a Google Cloud Third-party data sources ID
 - GCP project
 - Google Cloud Search API enabled in the project
 - GCP service account

To run this script, you will need Python3 packages listed in REQUIREMENTS.txt.

You can easily install them with virtualenv and pip by running these commands:
    virtualenv -p python3 env
    source ./env/bin/activate
    pip install -r REQUIREMENTS.txt

You can than run the script as follow:
    python schema_create_or_update.py \
    --service_account_file /PATH/TO/service.json \
    --datasources YOUR_DATASOURCE_ID \
    --schema_json schema.json 
"""


import argparse
import base64
import json
import logging
import os

import google.oauth2.credentials
import googleapiclient.http

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('cloudsearch.schema')

# Scope grants [CLOUD SEARCH]
SEARCH_SCOPES = ['https://www.googleapis.com/auth/cloud_search']
SEARCH_API_SERVICE_NAME = 'cloudsearch'
SEARCH_API_VERSION = 'v1'


def get_authenticated_service(service_account_file, scope, service_name, version):
  # Create credentials from Service Account File
  credentials = service_account.Credentials.from_service_account_file(
      service_account_file, scopes=scope)
  return build(service_name, version, credentials=credentials, cache_discovery=False)


def cloud_search_get_schema_default(schema_json):
  with open(schema_json) as f:
    body = json.load(f)
  return body


def cloud_search_update_schema(service, datasources, schema):
  body = {"schema": schema}
  update = service.indexing().datasources().updateSchema(
      name="datasources/"+datasources, body=body).execute()
  return update


def cloud_search_get_schema(service, datasources):
  schema = service.indexing().datasources().getSchema(
      name="datasources/"+datasources).execute()
  return schema


def main(service_account_file, datasources, schema_json):
  # Create a service instance
  try:
    service_search = get_authenticated_service(
        service_account_file,
        SEARCH_SCOPES,
        SEARCH_API_SERVICE_NAME,
        SEARCH_API_VERSION)
    LOGGER.info("Updating schema - START")
    # Retireve Schema definition
    schema = cloud_search_get_schema_default(schema_json)
    # Upsert Schema in the Datasource
    update = cloud_search_update_schema(service_search, datasources, schema)
    LOGGER.info("Update: %s" % update)
    # Read Schema from the Datasource
    get = cloud_search_get_schema(service_search, datasources)
    LOGGER.info("Get: %s" % get)
    LOGGER.info("Updating schema - END")
  # Example code only. Add proper exception handling
  except Exception as e:
    LOGGER.error('Error %s' % e)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description='Example to handle CRUD for CloudSearch Schema.')
  parser.add_argument('--service_account_file', dest='service_account_file',
                      help='File name for the service account.')
  parser.add_argument('--datasources', dest='datasources',
                      help='DataSource to update.')
  parser.add_argument('--schema_json', dest='schema_json',
                      help='Schema JSON structure.')

  args = parser.parse_args()

  main(args.service_account_file, args.datasources, args.schema_json)
