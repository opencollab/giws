#!/usr/bin/python -u
# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
#
# This software is a computer program whose purpose is to generate C++ wrapper
# for Java objects/methods.
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software. You can  use,
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

from distutils.core import setup
from configGiws import configGiws
import os

root_dir = os.path.dirname(__file__)
if root_dir:
	os.chdir(root_dir)

setup (name = "giws",
    description="Generate C++ class wrappers to call Java methods/objects",
    version=configGiws().getVersion(),
    author="Sylvestre Ledru",
    author_email="sylvestre.ledru@inria.fr",
    url="http://www.scilab.org/giws/",
    packages=['.','classRepresentation','datatypes'],
    scripts=['giws'],
    license="CeCILL",
    long_description="""Giws is basically doing the same stuff as SWIG but the opposite.
 Calling Java from C/C++ can be tricky: JNI calls are complicated 
 especially when dealing with non primivite types or arrays, 
 performance issues must be kept in mind all the time, 
 the code can be redundant (checking exceptions, checking returns
 of operations...).
 Giws hides this complexity through a C++ class which wraps the
 Java class."""
)
