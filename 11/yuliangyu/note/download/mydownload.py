#!/usr/bin/python
#coding:utf-8

class downloader(object):
    def __init__(self):
	self.url = url
	self.num = num
	self.name = url.split('/')[-1]
	r = request.head(self.url)
	self.total = int(r.headers['Content-Length'])
	print 'total is %s' % (self.total)

    def get_range(self):
	ranges = []
	offset = int(self.total/self.num)
	for i in range(self.num):
	    if i == self.num -1:
		ranges.append((i*offset,''))
	    else:
		ranges.append((i*offset,(i+1)*offset))
	return ranges #[(0,12),(12,24),(24,36),(36,'')]

    def download(self):
	f = open()
