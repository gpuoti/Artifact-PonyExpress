======================
Interacting with Scons
======================

Many people says Scons is slow. Perhaps it is but I've never experienced it. Probably it is if your project is very big and complex but, as for my (little) experience, it is not for projects with some tent of subprojects and some hunded of KLoc. 

I've not a great experience with build engines but with SCons, I was able to do quite advanced stuffs very soon and very sooner then any other build engines I've tasted (CMake and Gradle) which have a much stepper learning curve.

Anyway I find it perfect for my intent to extend and integrate with custom build steps. Moreover extend Scons using python functions is extremelly simple and this is exactly what **pony** aims to do.

From your SConstruct file, you have at your service all of the python environment on your building machine. This means that, if you've installed it, you have **pony**. All you need is a SCons accessible interface to let the **pony** be commanded during build.

.. note::
    At the time this was written, the current Scons version 2.5.0 is still not Python 3 compatible. So, make sure you have installed **pony** into your python 2.7 environment. You can install with:

    .. code-block:: bash

        > pip2 install pony-x.y.z.tar.gz

**Pony** comes with this interface included. All you need to do is prepare your scons environment or, in other terms **establish a first contact with the pony**. The following is all you need:

.. code-block:: python

    # Sconstruct file that interact with pony
    
    import pony_scons
    env = pony_scons.establish_contact(Environment())

Then you can use the environment using the **charge** and **deliver** builders.

.. code-block:: python  

    # a Sconstruct file that interact with pony
    
    import pony_scons
    env = pony_scons.establish_contact(Environment())

    dep_resolver = env.deliver('meta')
    # ...
    # some more build steps here
    # ...
    publish = env.charge('meta')

In the simple example above, I've not specified a particular mongodb server host so pony assumes I'm requiring it to connect to the service running on localhost waiting at mongodb default port 27017. This will probably not be the case in your working environment.
To request pony to connect to a specific host at a non default port, you can specify additional properties for the required environment:

    mongo_db
        the host you want to connect to

    mongo_port
        the port to use for the comunication with the host

    mongo_user
        to connect as a specific user

    mongo_pwd
        to be able to use mongo service as an authenticated user

Consider that, to not write your password in the code, you'll probably feed the password as a command line parameter at the scons lanch. So a real sconstruct file will probably look like:

.. code-block:: python

  import pony_scons


  AddOption('--pwd',
            dest='mongo_password',
            type='string',
            nargs=1,
            action='store',
            help='mongodb server password')


  env = Environment(MSVC_VERSION='14.0', TARGET_ARCH='x86', mongo_db='mongo-service.com', mongo_user='user-name', mongo_pwd=GetOption('mongo_password'), mongo_port=12345)
  env = pony_scons.establish_contact(env)



    