#!/usr/bin/python -u
from datatypes.intDataGiws import intDataGiws
from datatypes.longDataGiws import longDataGiws
from datatypes.doubleDataGiws import doubleDataGiws
from datatypes.booleanDataGiws import booleanDataGiws
from datatypes.byteDataGiws import byteDataGiws
from datatypes.floatDataGiws import floatDataGiws
from datatypes.shortDataGiws import shortDataGiws
from datatypes.stringDataGiws import stringDataGiws
from datatypes.voidDataGiws import voidDataGiws
import datatypes
import new

""" Factory which create the different data types """
class dataFactoryGiws:
	  def __init__(self):

		  self.dict = {
			  "int":    intDataGiws,
			  "long":   longDataGiws,
			  "double": doubleDataGiws,
              "boolean": booleanDataGiws,
              "byte": byteDataGiws,
              "float": floatDataGiws,
              "short": shortDataGiws,
			  "String": stringDataGiws,
			  "void": voidDataGiws
			  }

	  def create(self, site):
            if site not in self.dict:
                  raise Exception("Don't know how to manage the data type %s"%site)
            return self.dict[site]()

if __name__ == '__main__':
	myFactory=dataFactoryGiws()
	myData=myFactory.create("int")
	myData2=myFactory.create("doesnt-exist")
	print myData.getDescription()
