#!/usr/bin/python -u

""" The engine which will write files """

class outputWriter:

	def stripTab(self, text):
		return text.replace("\t","")
	
	def writeIntoFile(self, directory, fileName, content):
		f=open(directory+"/"+fileName, 'w')
		f.write(self.stripTab(content))
		f.close()

