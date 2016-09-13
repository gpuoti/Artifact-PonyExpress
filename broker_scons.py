import broker
import SCons.Builder

def __store(target, source, env):

    broker.store_json_file(str(source[0]))
    return None

def __bring(target, source, env):
    fname=str(source[0])
    with open(fname, 'r') as f:
        broker.bring_json(f.read())
    return None

store_artifact = SCons.Builder.Builder( action = __store,
                                        src_suffix = '.json')

bring_dependencies = SCons.Builder.Builder(  action = __bring,
                                             src_suffix = '.json')                                        

def establish_contact (scons_environment):
    scons_environment['BUILDERS']['store'] = store_artifact
    scons_environment['BUILDERS']['bring'] = bring_dependencies
    return scons_environment