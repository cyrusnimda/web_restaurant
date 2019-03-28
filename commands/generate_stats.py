import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import collections
import os

base_path = os.path.dirname(os.path.realpath(__file__)) + "/../web/static/img/"

#
# generate yesterday bookings
#
labels = 'Booked', 'Free'
sizes = [15, 30]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')

plt.title('Yesterday occupation rate')
plt.savefig(base_path + 'stats_booking_rate.png')

#
# generate stats per day
#
data = collections.OrderedDict()
data['Mo'] = 10
data['Tu'] = 15
data['We'] = 12
data['Th'] = 20
data['Fr'] = 39
data['Sa'] = 41
data['Su'] = 35

names = list(data.keys())
values = list(data.values())

fig2, ax2 = plt.subplots()
rects = ax2.bar(names, values)
for rect in rects:
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2., height, '%d' % int(height), ha='center', va='bottom')

plt.title('Number of bookings per day')
plt.savefig(base_path + 'stats_bookings_per_day.png')

#
# generate stats per hour
#
data = collections.OrderedDict()
data['10:00'] = 10
data['11:00'] = 12
data['12:00'] = 20
data['13:00'] = 25
data['14:00'] = 17
data['15:00'] = 4
data['16:00'] = 2
data['17:00'] = 8
data['18:00'] = 14
data['19:00'] = 29
data['20:00'] = 31
data['21:00'] = 24
data['22:00'] = 12

names = list(data.keys())
values = list(data.values())

fig2, ax2 = plt.subplots()
rects = ax2.plot(names, values)
ax2.set_xticklabels(names, rotation=60, fontsize=8)

plt.title('Number of bookings per hours')
plt.savefig(base_path + 'stats_bookings_per_hours.png')