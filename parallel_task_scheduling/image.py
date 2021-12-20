import matplotlib.pyplot as plt

circle1 = plt.Circle((0.5, 0.5), 0.1, color='r')
circle2 = plt.Circle((0.8, 0.5), 0.1, color='g')
circle3 = plt.Circle((0.5, 0.8), 0.1, color='g', clip_on=False)
circle4 = plt.Circle((0.2, 0.5), 0.1, color='g', clip_on=False)
circle5 = plt.Circle((0.5, 0.2), 0.1, color='g', clip_on=False)

fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)
ax.add_patch(circle4)
ax.add_patch(circle5)

plt.show()
