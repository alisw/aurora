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
#
import cookielib
from os.path import join

from requests.auth import AuthBase

from apache.aurora.common.auth.auth_module import AuthModule
from apache.aurora.common.clusters import DEFAULT_SEARCH_PATHS


class CookieAuth(AuthBase):
  """Attaches a cookiejar containing the SSO cookie to the request."""

  def __init__(self, search_paths=DEFAULT_SEARCH_PATHS):
    # setup any auth-related data here
    for search_path in search_paths:
      filename = join(search_path, 'auth-token')
      try:
        self.jar = cookielib.MozillaCookieJar(filename)
        self.jar.load()
        return
      except IOError:
        pass
    prettySearchPath = ", ".join(search_paths)
    errorMsg = "Could not find file `auth-token` in search paths:\n%s" % prettySearchPath
    raise IOError(errorMsg)

  def __call__(self, r):
    # Pass the cookie to the request
    r.prepare_cookies(self.jar)
    return r


class CookieAuthModule(AuthModule):
  @property
  def mechanism(self):
    return 'COOKIE'

  def auth(self):
    return CookieAuth()

  @property
  def failed_auth_message(self):
    return 'Unable to authenticate using COOKIE method.'
