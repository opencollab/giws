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

from datatypes.intDataGiws import intDataGiws
from datatypes.charDataGiws import charDataGiws
from datatypes.longDataGiws import longDataGiws
from datatypes.doubleDataGiws import doubleDataGiws
from datatypes.booleanDataGiws import booleanDataGiws
from datatypes.byteDataGiws import byteDataGiws
from datatypes.floatDataGiws import floatDataGiws
from datatypes.shortDataGiws import shortDataGiws
from datatypes.stringDataGiws import stringDataGiws
from datatypes.voidDataGiws import voidDataGiws
from datatypes.DoubleBufferDataGiws import DoubleBufferDataGiws
from datatypes.LongBufferDataGiws import LongBufferDataGiws
from datatypes.ByteBufferDataGiws import ByteBufferDataGiws
from datatypes.CharBufferDataGiws import CharBufferDataGiws
from datatypes.DoubleBufferDataGiws import DoubleBufferDataGiws
from datatypes.FloatBufferDataGiws import FloatBufferDataGiws
from datatypes.IntBufferDataGiws import IntBufferDataGiws
from datatypes.ShortBufferDataGiws import ShortBufferDataGiws
import datatypes
import new

""" Factory which create the different data types """
class dataFactoryGiws:
	  def __init__(self):

		  self.dict = {
			  "int":     intDataGiws,
			  "char":    charDataGiws,
			  "long":    longDataGiws,
			  "double":  doubleDataGiws,
			  "boolean": booleanDataGiws,
			  "byte":    byteDataGiws,
			  "float":   floatDataGiws,
			  "short":   shortDataGiws,
			  "String":  stringDataGiws,
			  "void":    voidDataGiws,
			  "DoubleBuffer": DoubleBufferDataGiws,
			  "ByteBuffer": ByteBufferDataGiws,
			  "CharBuffer": CharBufferDataGiws,
			  "DoubleBuffer": DoubleBufferDataGiws,
			  "FloatBuffer": FloatBufferDataGiws,
			  "IntBuffer": IntBufferDataGiws,
			  "LongBuffer": LongBufferDataGiws,
			  "ShortBuffer": ShortBufferDataGiws
			  }

	  def create(self, dataTypeToCreate):
			""" Create an GIWS datatype
			it can be int, char, long, double, boolean, byte, float, short,
			String and void
			if there is a trailing [], this object will consider it as an
			array of this data

			"""
			isArray=False
			arrayDimension=0 # Scalar
			if dataTypeToCreate.endswith("[]"): # It is an array
				  isArray=True
				  arrayDimension=dataTypeToCreate.count("[]")
				  # Trim to load the right object
				  dataTypeToCreate=dataTypeToCreate[0:len(dataTypeToCreate)-(arrayDimension*2)]

			
			if dataTypeToCreate not in self.dict:
				  raise Exception("Don't know how to manage the data type %s",dataTypeToCreate)

			myType=self.dict[dataTypeToCreate]()

			if myType.isByteBufferBased():
				  arrayDimension=1
				  # It is a byte buffer type
				  isArray=True
			
			myType.setIsArray(isArray)
			myType.setDimensionArray(arrayDimension)
			return myType

if __name__ == '__main__':
	myFactory=dataFactoryGiws()
	myData=myFactory.create("int")
	myData=myFactory.create("IntBuffer")
        print myFactory.isByteBufferBased()
	myData2=myFactory.create("doesnt-exist")
	print myData.getDescription()
