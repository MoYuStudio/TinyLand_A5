
import numpy
map = numpy.zeros((3,3,3))

print(map.shape)
print(numpy.shape(map))

# xyz
print(map[0][0][0])

map[0][0][0] = 1

print(type(map))