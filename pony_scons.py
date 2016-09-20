import pony
import SCons.Builder

def __charge(target, source, env):

    pony.charge_json_file(str(source[0]))
    return None

def __deliver(target, source, env):
    fname=str(source[0])
    with open(fname, 'r') as f:
        pony.deliver_json(f.read())
    return None

charge_artifact = SCons.Builder.Builder( action = __charge,
                                        src_suffix = '.json')

deliver_dependencies = SCons.Builder.Builder(  action = __deliver,
                                             src_suffix = '.json')                                        

def establish_contact (scons_environment):
    scons_environment['BUILDERS']['charge'] = charge_artifact
    scons_environment['BUILDERS']['deliver'] = deliver_dependencies
    return scons_environment