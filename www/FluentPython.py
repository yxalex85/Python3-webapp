# # page157
# metro_data = [
#     ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
#     ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
#     ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
#     ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
#     ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
# ]
#
# from operator import itemgetter
# for city in sorted(metro_data, key=itemgetter(1)):
#     print(city)
#
# cc_name = itemgetter(1, 0)
# for city in metro_data:
#     print(cc_name(city))
#
# from collections import namedtuple
# LatLong = namedtuple('LatLong', 'lat long')
# Metropolis = namedtuple('Metropolis', 'name cc pop coord')
# metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long))
#                for name, cc, pop, (lat, long) in metro_data]
# print(metro_areas[1])
#
# from operator import attrgetter
# name_lat = attrgetter('name', 'coord.lat')
# cc_name = itemgetter(0, 3)
# for city in sorted(metro_areas, key=attrgetter('coord.lat')):
#     print(name_lat(city))
#     print(cc_name(city))

# # page 159
# from operator import methodcaller
# s = 'The time has come'
# upcase = methodcaller('upper')
# print(upcase(s))
# print(str.upper(s)) # this is the same as above
# hiphenate = methodcaller('replace', ' ', '_')
# print(hiphenate(s))

# from operator import mul
# from functools import partial
# triple = partial(mul, 3)
# print(triple(7))
# print(list(map(triple, range(1, 10))))

# page 169
# from abc import ABC, abstractmethod
# from collections import namedtuple
#
# Customer = namedtuple('Customer', 'name fidelity')
#
#
# class LineItem:
#     def __init__(self, product, quantity, price):
#         self.product = product
#         self.quantity = quantity
#         self.price = price
#
#     def total(self):
#         return self.price * self.quantity
#
#
# class Order:
#     def __init__(self, customer, cart, promotion=None):
#         self.customer = customer
#         self.cart = list(cart)
#         self.promotion = promotion
#
#     def total(self):
#         if not hasattr(self, '__total'):
#             self.__total = sum(item.total() for item in self.cart)
#         return self.__total
#
#     def due(self):
#         if self.promotion is None:
#             discount = 0
#         else:
#             discount = self.promotion(self)
#         return self.total() - discount
#
#     def __repr__(self):
#         fmt = '<Order total: {:.2f} due: {:.2f}>'
#         return fmt.format(self.total(), self.due())


# def fidelity_promo(order):
#     return order.total()*.05 if order.customer.fidelity >= 1000 else 0
#
#
# def bulk_item_promo(order):
#     discount = 0
#     for item in order.cart:
#         if item.quantity >= 20:
#             discount += item.total()*.1
#     return discount
#
#
# def large_order_promo(order):
#     distinct_items = {item.product for item in order.cart}
#     if len(distinct_items) >= 10:
#         return order.total()*.07
#     return 0
#
#
# # promos = [fidelity_promo, bulk_item_promo, large_order_promo]
#
#
# def best_promo(order):
#     return max(promo(order) for promo in promos)
#
#
# promos = [globals()[name] for name in globals()
#           if name.endswith('_promo')
#           and name != 'best_promo']
#
# page 188
# promos = []
#
#
# def promotion(promo_func):
#     promos.append(promo_func)
#     return promo_func
#
#
# @promotion
# def fidelity(order):
#     return order.total()*.05 if order.customer.fidelity >= 1000 else 0
#
#
# @promotion
# def bulk_item_promo(order):
#     discount = 0
#     for item in order.cart:
#         if item.quantity >= 20:
#             discount += item.total()*.1
#     return discount
#
#
# @promotion
# def large_order_promo(order):
#     distinct_items = {item.product for item in order.cart}
#     if len(distinct_items) >= 10:
#         return order.total()*.07
#     return 0
#
#
# def best_promo(order):
#     return max(promo(order) for promo in promos)
#
#
# print(promos)

# page 192
# class Averager:
#
#     def __init__(self):
#         self.series = []
#
#     def __call__(self, new_value):
#         self.series.append(new_value)
#         total = sum(self.series)
#         return total/len(self.series)
#
#
# def make_averager():
#     series = []
#
#     def averager(new_value):
#         series.append(new_value)
#         total = sum(series)
#         return total/len(series)
#     return averager

# page 196
# def make_averager():
#     count = 0
#     total = 0
#
#     def averager(new_value):
#         nonlocal count, total
#         total += new_value
#         count += 1
#         return total/count
#     return averager
#
#
# avg = make_averager()
# print(avg(0))
# print(avg(11))
# print(avg(12))

# page 196
# import time
#
#
# def clock(func):
#     def clocked(*args):
#         t0 = time.perf_counter()
#         result = func(*args)
#         elapsed = time.perf_counter()
#         name = func.__name__
#         arg_str = ', '.join(repr(arg) for arg in args)
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#     return clocked
#
#
# @clock
# def snooze(seconds):
#     time.sleep(seconds)
#
#
# @clock
# def factorial(n):
#     return 1 if n < 2 else n*factorial(n-1)
#
#
# if __name__ == '__main__':
#     print('*'*40, 'Calling snooze(.123')
#     snooze(.123)
#     print('*'*40, 'Calling factorial(6)')
#     print('6! =', factorial(6))

# page 200
# import functools
#
# @functools.lru_cache()
# @clock
# def fibonacci(n):
#     if n < 2:
#         return n
#     return fibonacci(n-2) + fibonacci(n-1)
#
#
# if __name__ == '__main__':
#     print(fibonacci(6))

# page 207
# registry = set()


# def register(active=True):
#     def decorate(func):
#         print('running register(active=%s)->decorate(%s)'
#               % (active, func))
#         if active:
#             registry.add(func)
#         else:
#             registry.discard(func)
#         return func
#     return decorate
#
#
# @register(active=False)
# def f1():
#     print('running f1()')
#
#
# @register()
# def f2():
#     print('running f2()')
#
#
# def f3():
#     print('running f3()')

# page 228
# class bus:
#
#     def __init__(self, passengers=None):
#         if passengers is None:
#             self.passengers = []
#         else:
#             self.passengers = list(passengers)
#
#     def pick(self, name):
#         self.passengers.append(name)
#
#     def drop(self, name):
#         self.passengers.remove(name)
#
#
# basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
# bus1 = bus(basketball_team)
# bus1.drop('Tina')
# bus1.drop('Pat')


# page 231
# import copy
#
#
# class Hauntedbus:
#
#     def __init__(self, passengers=[]):
#         self.passengers = passengers
#
#     def pick(self, name):
#         self.passengers.append(name)
#
#     def drop(self, name):
#         self.passengers.remove(name)
#
#
# bus1 = Hauntedbus(['Alice', 'Bill'])
# bus1.pick('Charlie')
# bus1.drop('Alice')
# bus2 = Hauntedbus()
# bus2.pick('Carrie')
# bus3 = Hauntedbus()
# bus3.pick('Dave')

# page 238
# class Cheese:
#
#     def __init__(self, kind):
#         self.kind = kind
#
#     def __repr__(self):
#         return 'Cheese(%r)' % self.kind
#
#
# import weakref
#
#
# stock = weakref.WeakValueDictionary()
# catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
#            Cheese('Brie'), Cheese('Parmesan')]
#
#
# for cheese in catalog:
#     stock[cheese.kind] = cheese
#
# print(sorted(stock.items()))

# page 256
# def angle(self):
#     return math.atan2(self.x, self.y)
#
#
# def __format__(self, fmt_spec=''):
#     if fmt_spec.endswith('p'):
#         fmt_spec = fmt_spec[:-1]
#         coords = (abs(self), self.angle())
#         outer_fmt = '<{}, {}>'
#     else:
#         coords = self
#         outer_fmt = '({}, {})'
#     components = (format(c, fmt_spec) for c in coords)
#     return outer_fmt.format(*components)

# page 277
# from array import array
# import reprlib
# import math
# #
# #
# class Vector:
#     typecode = 'd'
#
#     def __init__(self, components):
#         self._components = array(self.typecode, components)
#
#     def __iter__(self):
#         return iter(self._components)
#
#     def __repr__(self):
#         components = reprlib.repr(self._components)
#         print(components)
#         components = components[components.find('['):-1]
#         print(components)
#         return 'Vector({})'.format(components)
#
#     def __str__(self):
#         return str(tuple(self))
#
#     def __bytes__(self):
#         return (bytes([ord(self.typecode)]) +
#                 bytes(self._components))
#
#     def __eq__(self, other):
#         return tuple(self) == tuple(other)
#
#     def __abs__(self):
#         return math.sqrt(sum(x*x for x in self))
#
#     def __bool__(self):
#         return bool(abs(self))
#
#     @classmethod
#     def frombytes(cls, octets):
#         typecode = chr(octets[0])
#         memv = memoryview(octets[1:]).cast(typecode)
#         return cls(memv)
# page 283
# def __len__(self):
#     return len(self._c)
#
# def __getitem_(self, index):
#     cls = type(self)
#     if isinstance(index, slice):
#         retunr cls(_self.components[index])
#     elif isinstance(index, numbers.Integral):
#         return _self.components[index]
#     else:
#         msg = '{cls.__name} indices must be integer'
#         return TypeError(msg.format(cls=cls))

clsname = 'abcd'
print(len(clsname))