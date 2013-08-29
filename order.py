#!/usr/bin/python
#-*- coding:utf-8 -*-
"""
    自动定饭脚本
"""
import sys,getopt,os
import cookielib,urllib2,urllib
import re

#login url 地址
LOGIN_URL='http://workflow.d.xiaonei.com/login/authenticate';
#order url
ORDER_URL='http://workflow.d.xiaonei.com/dinner/workTonight'
#获取带有cookie信息的opener
def getOpener(name,pwd):
	cookiejar = cookielib.CookieJar();
	urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar));
	#Send login/password to get session cookie
	para = {
	    'userName' : name,
	    'password' : pwd,
	    'mail_type' : 'renren-inc'	
	 };
	postData = urllib.urlencode(para);
	request = urllib2.Request(LOGIN_URL,postData);
	url = urlOpener.open(request);
	#cookies
	res = url.read(500000);
	if '对不起,你的用户名或者密码不对' in res:
		return None;
	else:
		return urlOpener;

#Order dinner
def orderDinner(msg,opener):
	data = {
		'workContent':msg
	};
	postData = urllib.urlencode(data);
	url = opener.open(ORDER_URL,postData);
	res = url.read(200000);
	if (url.code == 200):
		if '请用5个以上的字符描述你的加班内容' in res:
			print '请用5个以上的字符描述你的加班内容';
		else:
			print 'success';
	else:
		print 'Error Code:%s' % (url.code);
	opener.close();

#入口方法
def main(argv):
	opts,args = getopt.getopt(argv[1:],'n:p:m:',['username=','password=','message=']);
	name='';
	pwd='';
	msg='';
	for op,value in opts:
		if op in ('-n','--username'):
			name = value;
		elif op in ('-p','--password'):
			pwd = value;
		elif op in ('-m','--message'):
			msg = value;		
	if  (name) and (pwd) and (msg):
		opener = getOpener(name,pwd);
		orderDinner(msg,opener);
	else:
		print 'invalid input';
#main	
if __name__ == '__main__':
	main(sys.argv);
