import perlin_noise

noise = perlin_noise.PerlinNoise(octaves=3.5, seed=777)

print(noise([1,1]))
# # accepts as argument float and/or list[float]
# noise(0.5) == noise([0.5])

# # noise not limited in space dimension and seamless in any space size
# noise([0.5, 0.5]) == noise([0.5, 0.5, 0, 0, 0])
