# Copyright (C) 2008-2010 Alexander Barth <barth.alexander@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#                                                                           
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Python module to read and write GHER binary files. The origine of this 
fileformat are the Fortran function ureadc and uwritec.
'''

import numpy
import unittest


class GHERFile(object):
    '''Class representing a GHER file'''

    def __init__(self, fileobj, mode='r', endianess='big'):
        if isinstance(fileobj, str):
            self.file = open(fileobj, mode)
        else:
            self.file = fileobj

        self.mode = mode
        self.endianess = endianess

    def read(self):
        '''Read data contained in GHER file (low-level API)'''

        # ignore 10 lines
        self.header = self.file.read(20 * 4)

        reclen = self.file.read(1 * 4)

        if numpy.fromstring(reclen, dtype=numpy.dtype('>i')) == 24:
            int32 = numpy.dtype('>i')
            float32 = numpy.dtype('>f')
            float64 = numpy.dtype('>d')
        elif numpy.fromstring(reclen, dtype=numpy.dtype('<i')) == 24:
            int32 = numpy.dtype('<i')
            float32 = numpy.dtype('<f')
            float64 = numpy.dtype('<d')
        else:
            raise Exception('not a GHER file')

        shape = numpy.fromfile(self.file, dtype=int32, count=3)
        iprec = numpy.fromfile(self.file, dtype=int32, count=1)[0]
        nbmots = numpy.fromfile(self.file, dtype=int32, count=1)[0]
        valex = numpy.fromfile(self.file, dtype=float32, count=1)[0]

        reclen = numpy.fromfile(self.file, dtype=int32, count=2)

        if iprec == 4:
            vtype = float32
        else:
            vtype = float64

        # number of complete records
        nrec = numpy.fix(numpy.prod(shape) / nbmots)

        # number of values on last incomplote record
        irec = numpy.prod(shape) - nbmots * nrec

        if any(shape < 0):
            nrec = 0
            irec = 4

        # load all full records including leading and tailing 4 byte integer
        # for efficiency these integers are read as two floats or one double

        if iprec == 4:
            data = numpy.fromfile(self.file, dtype=vtype, count=nrec * (nbmots + 2))
            data = data.reshape(nbmots + 2, nrec)
        else:
            data = numpy.fromfile(self.file, dtype=vtype, count=nrec * (nbmots + 1))
            data = data.reshape(nbmots + 1, nrec)

        data2 = numpy.fromfile(self.file, dtype=vtype, count=irec)

        # remove leading and tailing 4 byte integer

        data = numpy.concatenate(
            (data[0:nbmots, :].flatten('C'),
             data2))

        return (shape, valex, data)

    def load(self):
        '''Loads a GHER file. The data is returned as a masked numpy array.'''
        (shape, valex, data) = self.read()
        # print (shape, valex, data)
        data = data.reshape(shape[::-1])
        data = numpy.ma.masked_values(data, value=valex)
        return data

    def write(self, data, shape, valex=9999, iprec=4):
        '''Write data to a file in the GHER format (low-level API)'''

        if len(shape) == 1:
            shape = [shape[0], 1, 1]
        elif len(shape) == 2:
            shape = [shape[0], shape[1], 1]

        nbmots = 1024
        shape = numpy.array(shape)
        numel = numpy.prod(shape)

        nrec = numpy.fix(numel / nbmots)
        irec = numel - nbmots * nrec
        ide = 0

        if any(shape < 0):
            nrec = 0
            irec = 4
        else:
            if len(data) != numel:
                raise Exception('number of elements in array is ' +
                                'inconsitent with its shape')

        if self.endianess == 'big':
            int32 = numpy.dtype('>i')
            float32 = numpy.dtype('>f')
            float64 = numpy.dtype('>d')
        else:
            int32 = numpy.dtype('<i')
            float32 = numpy.dtype('<f')
            float64 = numpy.dtype('<d')

        def _write(value, dtype):
            '''writes a value of type dtype to file object'''
            self.file.write(numpy.array(value, dtype).tostring())

        # header

        for i in range(10):
            _write([0, 0], int32)

        _write(24, int32)
        _write(shape, int32)
        _write(iprec, int32)
        _write(nbmots, int32)
        _write(valex, float32)
        _write(24, int32)

        if iprec == 4:
            vtype = float32
        else:
            vtype = float64

        for i in range(nrec):
            _write(4 * nbmots, int32)
            _write(data[ide:ide + nbmots], vtype)
            _write(4 * nbmots, int32)
            ide = ide + nbmots

        _write(4 * irec, int32)
        _write(data[ide:ide + irec], vtype)
        _write(4 * irec, int32)

        self.file.close()

    def save(self, data, valex=9999., iprec=4):
        '''Save a GHER file. The data is provided as a masked numpy array.'''

        shape = numpy.array(data).shape
        if hasattr(data, 'fill_value'):
            data.fill_value = valex
            data = data.filled()

        self.write(data.flatten(), shape, valex, iprec)


class TestGHERFile(unittest.TestCase):
    '''Unittest class for GHERFile class'''

    #    def setUp(self):
    #        pass

    #     def test_loading(self):
    #         mask = '/var/www/web-vis/test.dat'
    #         data = GHERFile(mask).load()
    #         print data[2,1,1]


    def test_save(self):
        '''Test case for saving and loading a vector of data in a GHER file'''
        data = numpy.array(range(2 * 3 * 4))

        GHERFile('testpy.dat', 'w').save(data)

        data2 = GHERFile('testpy.dat').load()

        print data
        print data2

    def test_write(self):
        '''Test case for saving and loading a vector of data in a GHER file 
        using low-level API.'''

        data = [100.0, 33.]
        shape = numpy.array([2, 1, 1])

        GHERFile('testpy.dat', 'w').write(data, shape)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGHERFile)
    suite.debug()
