
import networkx as nx
import dependencies as dep

def combine(alternative_sets):

    if len(alternative_sets) > 0:
        frist_set = alternative_sets[0]
        if type(alternative_sets[0]) is not list:
            frist_set = list(alternative_sets[0])
            frist_set.sort()

        if len(alternative_sets) <2:
            for alternative in frist_set:
                yield alternative, 
        else:
            for alternative in [(alt,) for alt in frist_set]:
                for sub_configuration in combine(alternative_sets[1:]):
                    yield alternative + sub_configuration


class ConfigurationImpossible(Exception):
    """Exception raised in case pony can't find an acceptable dependency configuration."""

    def __str__ (self):
        return """Can't fulfill all dependencies in a compatible way.
"""

class config_generator:
    def __init__(self, gr):
        self.gr = gr
        self.clusters = dict()

        for n in self.gr.nodes():
            try:
                self.clusters[n.NAME] += [n]
            except KeyError:
                self.clusters[n.NAME] = [n]

            self.gr.node[n]['ndep'] = self._ndep(self.gr.neighbors(n))
        
        print("clusters")
        print(self.clusters)
    
    def _ndep(self,requirements):
        """
        Given a requirement list, calculate the number of projects involved as dependecy.
        """

        dependant_projects = set()
        for r in requirements:
            try:
                dependant_projects.add( r.NAME )
            except KeyError:
                # ignore empty graph node for now
                pass

        return len(dependant_projects)
    def _reduce_graph(gr, removed_alternatives):
        reduced_gr = gr.copy()
        reduced_gr.remove_nodes_from( removed_alternatives)
        return resuced_gr

    def _local_constraint(self, n, configuration):
        if(type(configuration) != dict):
            print("_local_constraint configuration is not a dict")
            print(configuration)
        
        print ("constrining local")
        print (configuration)
        local_constrained_configuration = dict()
        for valid_neighbor in  self.gr.neighbors(n):
            if valid_neighbor not in configuration[valid_neighbor.NAME]: 
                print (valid_neighbor)
                print("not in")
                print(configuration[valid_neighbor.NAME])
                continue
            try:
                local_constrained_configuration[valid_neighbor.NAME] += [valid_neighbor]
            except KeyError:
                local_constrained_configuration[valid_neighbor.NAME] = [valid_neighbor]

        if len(local_constrained_configuration) < self.gr.node[n]['ndep']:
            print ("raising exception")
            print(len(local_constrained_configuration))
            print("while ndep for " + str(n))
            print(self.gr.node[n]['ndep']) 
            raise ConfigurationImpossible

        for variable in local_constrained_configuration:
            configuration[variable] = local_constrained_configuration[variable]
        print('return constrained configuration')
        print(configuration)
        return configuration

    def _constraint_next(self, variables, unconstrained_configuration):
        if(type(unconstrained_configuration) != dict):
            print("_constraint_next unconstrained_configuration is not a dict")
            print(unconstrained_configuration)
        
        if len (variables) > 0:
            cluster = variables[0]

            for alternative in  unconstrained_configuration[cluster]:
                print ("entering alternative")
                print (alternative)
                try:
                    constrained = unconstrained_configuration
                    constrained[cluster] = [alternative]

                    constrained= self._local_constraint(alternative, constrained)
                    print ('constrained')
                    print (constrained)
                    for sub_configuration in self._constraint_next(variables[1:], constrained): 
                        print ("yield config  " + str((alternative,) + sub_configuration))
                        yield (alternative,) + sub_configuration

                except ConfigurationImpossible:
                    print ("impossible configuration catched")
                    pass
        else:
            yield ()
                
    def constraint(self):
        print ('entering contraint method')
        alternative_count = 0
        for config in self._constraint_next(list(self.clusters.keys()), self.clusters):
            print("--- yielding configuration ---")
            print (config)
            alternative_count += 1


            gr_config = self.gr.copy()
            for n in [n for n in gr_config.nodes() if n not in config]:
                gr_config.node[n]['pruned'] = True
            #gr_config.remove_nodes_from([n for n in gr_config.nodes() if n not in config])
                
                
            yield gr_config
            
            
        if alternative_count == 0:
            raise ConfigurationImpossible