===============================================
Django Bootstrapped with Twitter Bootstrap v2.0
===============================================

Bootstrapped is a reusable Django application to quickly integrate the Bootstrap toolkit from Twitter.  It's a
collection of the bootstrap toolkit files and template tags to display them.

This application depends on django.contrib.staticfiles.

No files from Twitter's Bootstrap toolkit have been modified and retain their Apache 2.0 license.

* Note: This app only works on Django 1.3 and newer.

Installation
============

pip install git+git://github.com/MechanisM/django-bootstrap2.git


Configuration
=============

#. Add the `bootstrapped` directory to your Python path.

#. Ensure `django.contrib.staticfiles` is added to your `INSTALLED_APPS` setting.

#. Ensure `django.contrib.staticfiles` is configured properly.

#. Add `bootstrap2` to your `INSTALLED_APPS` setting.

#. Run `manage.py collectstatic` to copy the Twitter Bootstrap toolkit files to your static directory.

#. Ensure you added {% load bootstrap2 %} before use tags in templates.


Template Usage
=================
This application exposes a few template tags for including the Bootstrap toolkit files.

Load the template tags before usage::

    {% load bootstrap2 %}

```bootstrap_css```

This tag renders the link tag for the bootstrap.min.css file.  It will render the un-minified version if
settings.TEMPLATE_DEBUG is set to True::

    {% bootstrap_css %}

Output::

    <link rel="stylesheet" href="/static/bootstrap.css">

```bootstrap_js```

The Bootstrap toolkit provides some javascript love (http://bootstrap.io/Demo/Javascript) that is
compatible with jQuery and Ender.  This tag renders the appropriate script include tag for each plugin defined.  The tag
does not include jQuery or Ender, that's up to you::

    {% bootstrap_js modal alerts dropdown %}

Output::

    <script src="YOUR_STATIC_URLjs/bootstrap-alerts.js"></script>
    <script src="YOUR_STATIC_URLjs/bootstrap-dropdown.js"></script>
    <script src="YOUR_STATIC_URLjs/bootstrap-modal.js"></script>

* Note: The popover javascript file has a dependency on the twipsy file.  If you add popover to the list and forget to add twipsy, the tag will do it for you.

Alternatively, you may just want to include all of the scripts.  If so, just use `all` for the tag arguments::

    {% bootstrap_js all %}



Forms
=====

To style forms do something like::

        <form method="POST" action="">{% csrf_token %}
        {{ form|as_bootstrap }}
        <div class="actions"><button type="submit" class="btn primary">Submit</button></div>
        </form>
