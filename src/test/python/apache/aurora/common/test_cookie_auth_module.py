import cookielib
import os
import unittest

import mock
import requests
from twitter.common.contextutil import temporary_dir

from apache.aurora.common.cookie_auth_module import CookieAuth, CookieAuthModule


def check_cookie(arg):
  assert arg.__class__ is cookielib.MozillaCookieJar
  for x in arg:
    assert x.domain is "www.foo.bar"
  return


class TestCookieAuthModule(unittest.TestCase):
  def test_cookie_auth(self):
    with self.assertRaises(IOError):
      CookieAuth(["/non-existing-path"])

    with temporary_dir() as dp:
      # Test the case in which the cookie is not there

      # Create a dummy cookie in a temporary directory and verify
      # Requests.prepare_cookies is correctly invoked with the cookie.
      jar = cookielib.MozillaCookieJar(os.path.join(dp, "auth-token"))
      cookie = cookielib.Cookie(None, 'asdf', None, '80', '80', 'www.foo.bar',
             None, None, '/', None, False, False, 'TestCookie', None, None, None)
      jar.set_cookie(cookie)
      jar.save()

      c = CookieAuth((dp,))
      req = requests.PreparedRequest()
      req.prepare_cookies = mock.Mock(side_effect=check_cookie)
      c(req)

  def test_cookie_auth_module(self):
    cam = CookieAuthModule()
    assert cam.mechanism is "COOKIE"
    assert cam.failed_auth_message == "Unable to authenticate using COOKIE method."
