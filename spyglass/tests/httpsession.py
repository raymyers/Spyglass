
import datetime

from django.test import TestCase
from spyglass.models import HttpSession


class HttpSessionTest(TestCase):

    def test_simple_unicode(self):

        s = HttpSession(http_method='GET', http_url='http://api.gowalla.com/')
        self.failUnlessEqual(unicode(s), u'GET http://api.gowalla.com/')
    
    
    def test_absolute_url(self):
    
        s = HttpSession(id=543)
        self.failUnlessEqual(s.get_absolute_url(), '/sessions/543')
        
        
    def test_raw_request_with_path(self):
        
        s = HttpSession(http_method='GET', http_url='http://api.gowalla.com/spots')
        expected_request = 'GET /spots HTTP/1.1\r\nHost: api.gowalla.com\r\nAccept: */*\r\n\r\n'
        self.failUnlessEqual(s.get_raw_request(), expected_request)
   
   
    def test_raw_request_for_index(self):
        
        s = HttpSession(http_method='GET', http_url='http://www.carfax.com')
        expected_request = 'GET / HTTP/1.1\r\nHost: www.carfax.com\r\nAccept: */*\r\n\r\n'
        self.failUnlessEqual(s.get_raw_request(), expected_request)
    
    
    def test_needs_to_send_request(self):
    
        s = HttpSession(http_method='GET', http_url='http://api.gowalla.com/')
        
        self.failUnless(s.needs_to_send_request())
        
        s.time_completed = datetime.datetime.now()
        
        self.failIf(s.needs_to_send_request())
        
    def test_raw_request_with_querystring(self):
    
        s = HttpSession(http_method='GET', http_url='http://api.flickr.com/services/rest/?method=flickr.photos.getExif')
        expected_request = 'GET /services/rest/?method=flickr.photos.getExif HTTP/1.1\r\n' + \
            'Host: api.flickr.com\r\nAccept: */*\r\n\r\n'
        self.failUnlessEqual(s.get_raw_request(), expected_request)

    def test_raw_request_with_alternate_url(self):
    
        s = HttpSession(http_method='GET', http_url='http://google.com/')
        raw_request = s.get_raw_request('http://www.google.com/')
        expected_request = 'GET / HTTP/1.1\r\n' + \
            'Host: www.google.com\r\nAccept: */*\r\n\r\n'
        
        self.failUnlessEqual(raw_request, expected_request)

    def test_raw_request_with_body(self):
    
        body = '''
            <fake-xml>
                <key>com.bleedingwolf.PrincipalClass</key>
                <value>SomeClassName</value>
            </fake-xml>
        '''
        content_length = len(body)
        
        s = HttpSession(http_method='POST', http_url='http://localhost:9000/endpoint', http_body=body)
        
        expected_request = '''POST /endpoint HTTP/1.1\r\nHost: localhost\r\n''' + \
            '''Accept: */*\r\nContent-Length: %d\r\n\r\n%s''' % (content_length, body)
                
        self.failUnlessEqual(s.get_raw_request(), expected_request)

    def test_raw_request_with_extra_headers(self):
        headers = '\r\n'.join([
            'User-Agent: Spyglass/0.1',
            'Referer: http://localhost:9000/login.jsp'
        ])
        s = HttpSession(http_method='GET', http_url='http://localhost:9000/endpoint', http_headers=headers)
        
        expected_request = '\r\n'.join([
            'GET /endpoint HTTP/1.1',
            'Host: localhost',
            'Accept: */*',
            'User-Agent: Spyglass/0.1',
            'Referer: http://localhost:9000/login.jsp',
            '',
            '',
        ])
                
        self.failUnlessEqual(s.get_raw_request(), expected_request)
