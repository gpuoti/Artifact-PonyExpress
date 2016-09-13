.. _quick_start_guide:

=================
Quick start guide
=================

Let have a taste of what the benefits of using **Broker** are with a very quick tour.
Suppose you are going to start a new project and that, over years, your company has developed a bounce of little software components that easy your life so much once they are in place. If they are small, they possibly also are many.

Suppose you are going to develop a microservice that will comunicate by means of json strings exchanged over a proprietary protocol. Of course your company have his own libraries to deal with theese basic tasks:

+-----------------------+-------------------+--------------------------+
| content/functionality |  component kind   | file groups              |
+=======================+===================+==========================+
| serialize/parse json  |  lib              | our_son.lib              |
|                       |                   +--------------------------+
|                       |                   | our_son/*.hpp            |
+-----------------------+-------------------+--------------------------+ 
| convinient-socket     |  lib              | easy-socket              |
|                       |                   +--------------------------+
|                       |                   | easy_socket/*.hpp        |
+-----------------------+-------------------+--------------------------+
| utilities-mix         |  header only      | utilities/*.hpp          |                      
+-----------------------+-------------------+--------------------------+
| better-strings        |  lib              | better_strings.lib       |
|                       |                   +--------------------------+
|                       |                   | better_strings/string.hpp|
+-----------------------+-------------------+--------------------------+
                                        
Now, if your company use a binary repository to store those artifacts, and use **Broker** in particular, instead of prepare your environment by hand, you can prepare a meta information file like the following one:

.. code-block:: json

  {
    "NAME"          : "FantasticProject",
    "MajorVersion"  : "2.1.7",
    "TARGET"        : "x86"
    
    "DEPENDENCIES"  : [
                        { 
                          "NAME"     : "our_son",
                          "Version"  : "1.2.0",
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "easy-socket",
                          "Version"  : "1.6.1",
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "utilities-mix",
                          "Version"  : "3.1.1",
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "better-strings",
                          "Version"  : "1.2.8",
                          "TARGET"   : "x86"
                        }
                      ]
                      
    "__UNBOX_INSTRUCTIONS__" : [
                                  {
                                    "FROM"    : "lib",
                                    "TO"      : "lib",
                                    "FILTER"  : "*.lib"
                                  },
                                  
                                  {
                                    "FROM"    : "include",
                                    "TO"      : "include-ext",
                                    "FILTER"  : "*.hpp"
                                  }
                               ]
  }
  
In this example, I'm supposing that the box format in use has:
    
    * library files (.lib) in the boxes are placed into a first level folder named lib 
    * header files into are placed into the box fist folder named include.
    * and that files into the boxes are organized to not collide with names of objects from other boxes (I mean boxes containing different components)
    
 If you have followed a well defined box format, you will simply have a standard structured once **Broker** has resolved dependencies for you. To do this just run broker with:

.. code-block:: bash

  broker bring

or, in a more complex environment with a properly hosted mongodb cluster: 

  broker --mongo mongo_host_name --port 1234 --user your_name --pwd your_pwd bring


 
 Prepare to deliver
 ------------------
 
 Now, expecially if your FantasticProject is actually a midleware library, you will probably want to store its releases using the same **Broker**. To let the **Broker** accept your delivery, you must provide boxing instructions into your metadata object witch may become:
 
 .. code-block:: json
 
    {
    "NAME"          : "FantasticProject",
    "MajorVersion"  : "2.1.7",
    "TARGET"        : "x86"
    
    "DEPENDENCIES"  : [
                        { 
                          "NAME"     : "our_son",
                          "Version"  : "1.2.0",
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "easy-socket",
                          "Version"  : "1.6.1",
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "utilities-mix",
                          "Version"  : "3.1.1",
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "better-strings",
                          "Version"  : "1.2.8",
                          "TARGET"   : "x86"
                        }
                      ]
                      
    "__UNBOX_INSTRUCTIONS__" : [
                                  {
                                    "FROM"    : "lib",
                                    "TO"      : "lib",
                                    "FILTER"  : "*.lib"
                                  },
                                  
                                  {
                                    "FROM"    : "include",
                                    "TO"      : "include-ext",
                                    "FILTER"  : "*.hpp"
                                  }
                               ],
    
    "__BOX_INSTRUCTIONS__" : [
                                  {
                                    "FROM"    : "lib",
                                    "TO"      : "lib",
                                    "FILTER"  : "FantasticProject.lib"
                                  },
                                  
                                  {
                                    "FROM"    : "include",
                                    "TO"      : "include",
                                    "FILTER"  : "*.hpp"
                                  }
                               ],
  
  }
  
Once your project is ready for delivery, as a manual step running a command line command or, even (much) better, as a final step of your build process ask **broker** to store your results with:

.. code-block:: bash

  broker --mongo mongo_host_name --port 1234 --user your_name --pwd your_pwd store

or, if your environment is very simple with mongo daemon running on localhost:

.. code-block:: bat

  broker store

.. note:: 

  Remember that if you have access to the python interpreter from the build script, you can even use the full power of the broker's python interface.

That's it, hope you found this simple enough. I think writing this metainformation still is quite boring but this save you from doing it by hand witch seams a simpler operation as you don't need to request operations in formal language but indeed is a quite long and also much more error prone operation. Moreover here you are doing much more then prepare your sandbox, you are also declaring dependencies for the new project witch may become quite useful when time passes and the number of version of involved components increase.