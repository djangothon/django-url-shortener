django-url-shortener
--------------------

This is URL shortening application written using the Django framework. It began
as a fork of https://github.com/tehranian/url-shortener, but now includes
functionality for creating custom shortened URLs including non-English
characters. It also stores geo-location and origin of short link usage.

The project has also been updated to work on a Redis Backend, because Redis
is a perfecrt fit for this application, bringing blazingly fast operation.


Features
--------

* More efficient and simpler method of mapping between short url and long url.

* Ability to create custom short URLs.
  Ex: http://you.rs/KimK -> http://www.kimkardashian.com

* Ability to create non-english custom short URLs.
  Ex. http://you.rs/見.香港 -> http://www.kimkardashian.com

* Keeps count of how many time each URL is followed.

* Keeps geolocation information each time URL is followed.

* Keeps origin information each time URL is followed.


Dependancies
------------

* Redis server

* django 1.4

* redisco

* requests


How to use
----------

* add `shortener` to INSTALLED_APPS.

* add `REDIS_HOST` and `REDIS_PORT` to settings.
