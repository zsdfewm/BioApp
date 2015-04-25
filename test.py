import urllib
import urllib2

url = 'http://localhost:8080/sign'
values = {'id': 2,
          'first_name': 'X',
          'last_name': 'Y',
          'phone': 234}
#values = {'name' : 'Michael Foord',
#          'location' : 'Northampton',
#          'language' : 'Python' }

data = urllib.urlencode(values)
print data
req = urllib2.Request(url, data)
#req = urllib2.Request(url)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
