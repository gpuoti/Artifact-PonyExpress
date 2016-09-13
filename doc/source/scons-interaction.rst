======================
Interacting with Scons
======================

Many people says Scons is slow. Perhaps it is but I've never experienced it. Probably it is if your project is very big and complex but, as for my (little) experience, it is not for projects with some tent of subprojects and some hunded of KLoc. 

I've not a great experience with build engines but with SCons I was able to do quite advanced stuffs very soon and very sooner then other build engines I've tasted (CMake and Gradle) which have a much stepper learning curve.

Anyway I find it perfect for my intent to extend and integrate with custom build steps. Moreover extend Scons using python functions is extremelly simple and this is exactly what **broker** is.

From your SConstruct file, you have at your service all of the python environment on your building machine. This means that, if you've installed it, you have **broker**. All you need is a SCons accessible interface to let the **broker** be commanded during build.

.. note::
    At the time this was written, the current Scons version 2.5.0 is still not Python 3 compatible so, make sure you have installed **broker** into your python 2.7 environment. You can install with:

    .. code-block:: bash

        > pip2.7 install broker-x.y.z.tar.gz

**Broker** comes with this interface included. All you need to do is prepare your scons environment. Or, in other terms **establish a first contact with the broker**. The following is all you need:

.. code-block:: python

    # Sconstruct file that interact with broker
    
    import broker_scons
    env = broker_scons.establish_contact(Environment())

Then you can use the environment using the **store** and **bring** builders.

.. code-block:: python  

    # a Sconstruct file that interact with broker
    
    import broker_scons
    env = broker_scons.establish_contact(Environment())

    env.bring('meta')
    # ...
    # some more build steps here
    # ...
    env.store('meta')

