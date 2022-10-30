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

import sys
import os.path

import xml.etree.ElementTree as ET

from classRepresentation.packageGiws import packageGiws
from classRepresentation.objectGiws import objectGiws
from classRepresentation.methodGiws import methodGiws
from classRepresentation.parameterGiws import parameterGiws
from datatypes.dataFactoryGiws import dataFactoryGiws


class parseXMLEngine:
    __root = None
    Jpackage = None

    def __init__(self, descFile):
        if not os.path.isfile(descFile):
            print(('Could not find declaration file "%s"' % descFile))
            sys.exit(-2)
        try:
            doc = ET.parse(descFile)
        except ET.ParseError:
            print(('Error while parsing XML file "%s"' % descFile))
            sys.exit(-3)
        self.__root = doc.getroot()
        self.__loadPackage()

    def getJpackage(self):
        return self.Jpackage

    def __loadPackage(self):
        if self.__root.tag != "package":
            print('"Package" is expected as root tag')
            sys.exit(-2)

        packageName = self.__root.attrib["name"]
        self.Jpackage = packageGiws(packageName)
        self.__loadObject()

    def __loadObject(self):
        objectsNode = self.__root.findall("object")
        for objectNode in objectsNode:
            # look for the name of the object
            objectName = objectNode.attrib["name"]

            # look for the hierarchy of the object
            extendsObject = None
            if "extends" in objectNode.attrib:
                extends = objectNode.attrib["extends"]

                # Retrieve the father (inheritance)
                extendsObject = self.Jpackage.getObject(extends)
                if extendsObject is None:
                    print(
                        (
                            'Class "%s" must be defined before being use as father class.\nPlease check that "%s" is defined before "%s".'
                            % (extends, extends, objectName)
                        )
                    )
                    sys.exit(-4)

            # creates the object
            newObject = objectGiws(objectName, extendsObject)

            # Load the methods
            for child in objectNode.iter("method"):
                newObject.addMethod(self.__loadMethods(child))

            # Add to the package the object found
            self.Jpackage.addObject(newObject)

    def __loadMethods(self, method):
        methodName = method.attrib["name"]
        returns = method.attrib["returnType"]

        myFactory = dataFactoryGiws()
        myReturnData = myFactory.create(returns)

        detachThread = False
        if "detachThread" in method.attrib:
            str = method.attrib["detachThread"].lower()
            if str == "true":
                detachThread = True

        if "modifier" in method.attrib:
            modifier = method.attrib["modifier"]
            Jmethod = methodGiws(methodName, myReturnData, detachThread, modifier)
        else:
            Jmethod = methodGiws(methodName, myReturnData, detachThread)

        parametersName = []  # To check if the parameter is not already defined
        for param in method:  # We browse the parameters of the method
            param = self.__loadParameter(param.attrib)
            try:
                if parametersName.index(param.getName()) >= 0:
                    print(("%s is already defined as parameters" % param.getName()))
                    sys.exit(-3)
            except ValueError:  # Cannot find the parameter => not defined. Good!
                parametersName.append(param.getName())

            Jmethod.addParameter(param)
        return Jmethod

    def __loadParameter(self, param):
        type = param["type"]
        name = param["name"]
        return parameterGiws(name, type)


if __name__ == "__main__":
    print("Parsing ...")
    templateObj = parseXMLEngine("template.xml")
    print((templateObj.getJpackage().generateCXXHeader()))
    print((templateObj.getJpackage()))
