#!/usr/bin/python -u 
# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
# 
# This software is a computer program whose purpose is to generate C++ wrapper 
# for Java objects/methods.
# 
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# 
# For more information, see the file COPYING

""" Configuration of the Env """

class configGiws:
	__version="2.0.0"
	__descriptionFile=""
	__splitPerObject=True
	__throwsException=False
	__generateExceptionClass=False
	__disableReturnSize=False
	__output="." # Should be changed elsewhere
	__headerCPPExtension=".hxx"
	__bodyCPPExtension=".cpp"
	__exceptionFileName="GiwsException"
	
	def setDescriptionFile(self, desc):
		self.__descriptionFile=desc
		
	def getDescriptionFile(self):
		return self.__descriptionFile

	def setSplitPerObject(self, split):
		self.__splitPerObject=split

	def setThrowsException(self, excep):
		configGiws.__throwsException=excep

	def setDisableReturnSize(self):
		configGiws.__disableReturnSize=True

	def getDisableReturnSize(self):
		return configGiws.__disableReturnSize

	def enableGenerateExceptionClass(self):
		configGiws.__generateExceptionClass=True

	def generateExceptionClass(self):
		return configGiws.__generateExceptionClass

	def setOutput(self, output):
		self.__output=output
		
	def getOutput(self):
		return self.__output

	def setCPPHeaderExtension(self, ext):
		self.__headerCPPExtension=ext
		
	def getCPPHeaderExtension(self):
		return self.__headerCPPExtension

	def setCPPBodyExtension(self, ext):
		self.__bodyCPPExtension=ext
		
	def getCPPBodyExtension(self):
		return self.__bodyCPPExtension

	def getExceptionFileName(self):
		return self.__exceptionFileName

	def getSplitPerObject(self):
		return self.__splitPerObject

	def getThrowsException(self):
		return configGiws.__throwsException
	
	def getVersion(self):
		return self.__version

	def getFullCommandLine(self):
		return self.__fullCommandLine

	def setFullCommandLine(self, cmd):
		self.__fullCommandLine = cmd
