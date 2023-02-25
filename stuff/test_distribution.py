import random
import statistics
from PIL import Image

canvas_size = (1280//2, 720//2)
img = Image.new('RGB', canvas_size)
pixels = img.load()


num_pixels = 2

range_x = canvas_size[0]-1
#range_x = min(canvas_size[0]-1, range_x // 3) # add bias

points = []
color = (255,0,0)
for i in range(num_pixels):
    x = random.randint(0,canvas_size[0]-1)
    x = int(x * random.random()) # add bias towards the left side
    y = random.randint(0,canvas_size[1]-1)
    pixels[x,y] = color
    points.append([x,y])


# # draw centeroid
# x = [p[0] for p in points]
# y = [p[1] for p in points]
# centroid = (sum(x) / len(points), sum(y) / len(points))
# pixels[centroid[0],centroid[1]] = (60,255,60)


# mean_x = statistics.median(list(zip(*points))[0])
# mean_y = statistics.median(list(zip(*points))[1])
# pixels[mean_x,mean_y] = (255,255,0)


mode_x = statistics.mode(list(zip(*points))[0])
mode_y = statistics.mode(list(zip(*points))[1])
pixels[mode_x,mode_y] = (255,255,255)

#print("median: {} {}, avg: {} {}".format(mean_x,mean_y, centroid[0],centroid[1]))



img.show()