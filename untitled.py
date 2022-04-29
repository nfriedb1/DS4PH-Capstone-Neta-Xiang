
# geocodio test

from geocodio import GeocodioClient

client = GeocodioClient(3663c5c11ddc5f5b115452242dc6c6630c4c56c)

addresses = client.reverse((38.9002898, -76.9990361))