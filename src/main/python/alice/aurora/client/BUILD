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
import os

python_binary(
  name='aurora',
  entry_point='alice.aurora.client.client:proxy_main',
  dependencies=[
    ':alice_client_lib'
  ]
)

python_library(
  name='alice_client_lib',
  sources = [
    'client.py',
  ],
  dependencies = [
    '3rdparty/python:pex',
    'src/main/python/apache/aurora/client',
    # The Apache Aurora client
    # Any other dependencies for your custom code
  ],
)

python_library(
  name = 'client',
  dependencies = [
    ':alice_client_lib',
  ],
  provides = setup_py(
    name = 'alice.aurora.client',
    version = open(os.path.join(get_buildroot(), '.auroraversion')).read().strip().upper(),
  ).with_binaries({
    'aurora': ':aurora',
  }),
)
