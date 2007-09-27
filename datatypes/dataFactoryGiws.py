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

	  def create(self, dataTypeToCreate):
            """ Create an GIWS datatype
            it can be int, long, double, boolean, byte, float, short,
            String and void
            if there is a trailing [], this object will consider it as an
            array of this data

            """
            isArray=False
            if dataTypeToCreate.endswith("[]"): # It is an array
                  isArray=True
                  # Trim to load the right object
                  dataTypeToCreate=dataTypeToCreate[0:len(dataTypeToCreate)-2]

                  
            if dataTypeToCreate not in self.dict:
                  raise Exception("Don't know how to manage the data type %s"%dataTypeToCreate)
            
            myType=self.dict[dataTypeToCreate]()
            myType.setIsArray(isArray)
            return myType

if __name__ == '__main__':
	myFactory=dataFactoryGiws()
	myData=myFactory.create("int")
	myData2=myFactory.create("doesnt-exist")
	print myData.getDescription()
