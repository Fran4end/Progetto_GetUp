import math

def decimalToSexagesimal(lat, lon):
    out = str(math.floor(lat)) + "°"
    lat = (lat - (math.floor(lat))) * 60
    out += str(math.floor(lat)) + "'"
    lat = (lat - (math.floor(lat))) * 60
    out += str(math.floor(lat)) + "'' "
    out += str(math.floor(lon)) + "°"
    lon = (lon - (math.floor(lon))) * 60
    out += str(math.floor(lon)) + "'"
    lon = (lon - (math.floor(lon))) * 60
    out += str(math.floor(lon)) + "''"
    return out


print(decimalToSexagesimal(4533.068971, 1218.784441))
