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

import sys
from apache.aurora.client.cli import CommandLine, ConfigurationPlugin
from apache.aurora.client.cli.client import AuroraCommandLine
from apache.aurora.common.auth.auth_module_manager import register_auth_module
from apache.aurora.common.cookie_auth_module import CookieAuthModule

class AuroraAuthConfigurationPlugin(ConfigurationPlugin):
  """Plugin for configuring aurora client authentication."""

  def get_options(self):
    return []

  def before_dispatch(self, raw_args):
    return raw_args

  def before_execution(self, context):
    try:
      from apache.aurora.kerberos.auth_module import KerberosAuthModule
      register_auth_module(KerberosAuthModule())
    except ImportError:
      # Use default auth implementation if kerberos is not available.
      pass
    register_auth_module(CookieAuthModule())

  def after_execution(self, context, result_code):
    pass

class CustomAuroraCommandLine(AuroraCommandLine):
  """ALICE Aurora Client"""

  @property
  def name(self):
    return "alice-aurora"

  @classmethod
  def get_description(cls):
    return 'ALICE Aurora client'

  def __init__(self):
    super(CustomAuroraCommandLine, self).__init__()
    self.register_plugin(AuroraAuthConfigurationPlugin())

  def register_nouns(self):
    super(CustomAuroraCommandLine, self).register_nouns()
    # You can even add new commands / sub-commands!
    # FIXME: this is actually potentially very useful
    #self.register_noun(YourStartUpdateProxy())
    #self.register_noun(YourDeployWorkflowCommand())

def proxy_main():
  client = CustomAuroraCommandLine()
  if len(sys.argv) == 1:
    sys.argv.append("-h")
  sys.exit(client.execute(sys.argv[1:]))
