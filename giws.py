#!/usr/bin/python -u 

import sys
import getopt
import os.path

from parseXMLEngine import parseXMLEngine
from configGiws import configGiws
from CXXFile import CXXFile


class giws:
	config=configGiws()
	def __init__(self, argv=sys.argv):
		try:
			opts, args = getopt.getopt(sys.argv[1:], "f:o:e:b:shv", ["description-file=","output-dir=","header-extension-file=","body-extension-file=","split-per-object","help","version"])
			# if more than one "standalone" argument (more than conf file)
			# show help and exit...
			if len(args) > 1:
				raise getopt.GetoptError
				"""elif len(args) == 1:
				self.__dict__["config_file"] = args[0]
				self.__cmd_opt.append("config_file")"""
			elif len(args) == 1:
				self.__dict__["module"] = args[0]
				
		except getopt.GetoptError:
			raise
			self.show_help(argv,1)    # exit with EXIT_FAILURE return code

		for option, value in opts:
			if option in ("-f", "--description-file"):
				if os.path.isfile(value):
					self.config.setDescriptionFile(value)
				else:
					print "Deadly error : Cannot find file %s"%value
					print ""
					self.show_help(argv,0)
					
			if option in ("-o", "--output-dir"):
				if os.path.isdir(value):
					self.config.setOutput(value)
				else:
					print "Deadly error : Cannot find output dir %s"%value
					print ""
					self.show_help(argv,0)
					
			if option in ("-s", "--split-per-object"):
				self.config.setSplitPerObject(True)

			if option in ('e','--header-extension-file'):
				self.config.setCPPHeaderExtension(value)

			if option in ('b','--body-extension-file'):
				self.config.setCPPBodyExtension(value)

			if option in ("-v", "--version"):
				self.show_version(0)
				
			elif option in ("-h", "--help"):
				self.show_help(argv,0)

		templateObj=parseXMLEngine(self.config.getDescriptionFile())

		CXX=CXXFile(templateObj.getJpackage())
		CXX.generateCXXHeader(self.config)
		CXX.generateCXXBody(self.config)
		# this will be changed ... should not be called on the package itself
#		.generateCXXHeader(self.config)
#		templateObj.getJpackage().generateCXXBody(self.config)
		
	"""
	load configuration from command line parameters
	takes sys.argv as parameter and does all the job...
	"""
	def show_help(self, argv, exit_status=0):
		print "Giws usage: %s [options]"%argv[0]
		print ""
		print "Options can be:"
		print "-f     --description-file=file    Description of the method of the Java Object"
		print "-o     --output-dir=dir           The directory where to export files"
		print "-s     --split-per-object         Each wrapper classe will stored in one file"
		print "--header-extension-file           Specify the extension of the header file generated [Default : .hxx]"
		print "--body-extension-file             Specify the extension of the body file generated [Default : .cpp]"
		print "-v     --version                  Display the version informations"
		print "-h     --help                     Display the help"
		
		sys.exit(exit_status)

	def show_version(self, exit_status=0):
		print "Swig %s"%self.config.getVersion()
		print "Copyright (C) 2007 INRIA / Scilab"
		print """This software is governed by the CeCILL license under French law and
abiding by the rules of distribution of free software. You can use, 
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
http://www.cecill.info/ . """
		print ""
		print "Written by Sylvestre Ledru <sylvestre.ledru@inria.fr>"
		sys.exit(exit_status)

if __name__ == '__main__':
	giws()

