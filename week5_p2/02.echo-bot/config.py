#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 1878
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "")

    OPENAI_ENDPOINT = os.environ.get("OPENAI_ENDPOINT", "https://w6languageservice.cognitiveservices.azure.com/")
    print(OPENAI_ENDPOINT)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")