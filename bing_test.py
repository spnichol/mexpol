# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:02:30 2017

@author: spnichol
"""

import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '38c942ee95b14176a6b85053e445bda2',
}

params = urllib.urlencode({
"locale":"en-us"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, "locale:en-us", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


