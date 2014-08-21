#coding=utf8
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('../data/IMine.Qrel.SMJ.xml').read())
root = soup.find('root')
print root