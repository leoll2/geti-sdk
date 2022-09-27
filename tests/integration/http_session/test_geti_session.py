# Copyright (C) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
import pytest

from geti_sdk.http_session import GetiSession
from geti_sdk.http_session.geti_session import INITIAL_HEADERS
from geti_sdk.platform_versions import SC11_VERSION, SC12_VERSION


class TestGetiSession:
    def test_authenticate(self, fxt_geti_session: GetiSession):
        """
        Test that the authenticated GetiSession instance contains authentication cookies
        """
        fxt_geti_session.authenticate(verbose=False)

    def test_product_version(self, fxt_geti_session: GetiSession):
        """
        Test that the 'version' attribute of the session is assigned a valid product
        version
        """
        known_versions = [SC11_VERSION, SC12_VERSION]
        version_matches = [
            fxt_geti_session.version >= version for version in known_versions
        ]
        assert sum(version_matches) >= 1

    @pytest.mark.vcr()
    def test_logout(self, fxt_geti_session: GetiSession):
        """
        Test that logging out of the platform works, and clears all cookies and headers
        """
        fxt_geti_session.logout()
        assert len(fxt_geti_session.cookies) == 0
        assert len(fxt_geti_session.headers) == len(INITIAL_HEADERS)
        for key, value in fxt_geti_session._cookies.items():
            assert value is None