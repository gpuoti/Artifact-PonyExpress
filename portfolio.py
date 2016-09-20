import collections
import json
from alternative_set import combine
from  pymongo import MongoClient
import dependencies as dep
import networkx as nx

import sys
from bson.binary import Binary

def remove_any(l, ilist):
    for i in [x for x in ilist if x in l]:
        l.remove(i)

    return l

class MongoConnectionInfo:
    def __init__(self, pony_arguments = None):
        if pony_arguments and pony_arguments.user:
            self.host = pony_arguments.mongo
            self.port = pony_arguments.port
            self.user = pony_arguments.user
            self.pwd = pony_arguments.pwd
            self.controlled_access  = True
        else:
            self.host = 'localhost'
            self.port = 27017
            self.controlled_access  = False
            
            
    def connect(self):
        cli= MongoClient(host = self.host, port=self.port)
        print('connecting to: ' + self.host + ' : ' + str(self.port) + ' [controlled:' + str(self.controlled_access) + ']' )
        if self.controlled_access:
            cli.pony_charge.authenticate(self.user, self.pwd)
        return cli
        

def join(g, u):
    gnames = set([n.NAME for n in g.nodes()])
    unames = set([n.NAME for n in u.nodes()])
    req_names = gnames.union( unames)
    
    not_acceptable_nodes_u = [n for n in u.nodes() if n.NAME in gnames and n not in g.nodes()]
    not_acceptable_nodes_g = [n for n in g.nodes() if n.NAME in unames and n not in u.nodes()]
    
    u.remove_nodes_from(not_acceptable_nodes_u)
    g.remove_nodes_from(not_acceptable_nodes_g)
    gr = nx.compose(g, u)
    
    names = set([n.NAME for n in gr.nodes()])
    if not gnames.issubset(names):
        raise Exception("Detected conflict: " + str(gnames.difference(names)) + """
        gnames: """ +str(gnames) + """
        names : """ + str(names) )
    
    return gr
    
    
class YetInPortfolio (Exception):
    
    def __init__ (self, meta_informations):
        self.explain = meta_informations
        
    def __str__ (self):
        return """
        Error trying to insert package into the portfolio. 
                It contains yet a package with same metadata. Perhaps you want to increase your version.
        
        Received metadata:
          """ + self.explain 
        
    def __str__ (self):
        return """
        Error trying to insert package into the portfolio. 
                It contains yet a package with same metadata. Perhaps you want to increase your version.
        
        Received metadata:
          """ + str(self.explain) 

class NotInPortfolio (Exception):
    
    def __init__ (self, meta_informations):
        self.explain = meta_informations
        
    def __str__ (self):
        return """
        Error trying to take package from the portfolio. 
                It do not contains yet a package with compatible metadata.
        
        Received metadata:
          """ + str(self.explain) 
 
class ImpossibleConfigurationException(Exception):
    """Exception raised in case pony can't find an acceptable dependency configuration."""
    def __init__(self, gr):
        self.gr = gr

    def __str__ (self):
        return """Can't fulfill all dependencies in a compatible way.
The dependency graph is
""" + to_dot_string(self.gr)


class ProjectCluster:
    """A project cluster is a group of project in the application dependency graph with the same name."""

    def __init__(self, G, name):
        self.graph = G
        self.incoming_edges = []
        self.name = name

        components = [n for n in self.graph.nodes() if n.NAME == name]
        for n in components:
            self.incoming_edges += self.graph.in_edges(n)

    def dependants(self):
        """get the dependant projects that is projects that depends from any of the projects in the cluster."""
        return [in_edge[0] for in_edge in self.incoming_edges]

    def components(self):
        "get the component projects into the cluster"
        #return [in_edge[1] for in_edge in self.incoming_edges]
        return  [n for n in self.graph.nodes() if n.NAME == self.name]

    def unaccepted_nodes(self):        
        """
        Any project in the cluster that do not satify the requirement
        from any dependant, is considered unaccepted and returned by this method.
        Notice that it is possible that, once you have considered unacceptable a project, 
        other dependant project may become unacceptable because of unmeet requirements. """
        
        dependant_projects = set([dependant.NAME for dependant in self.dependants()])
        unacceptable = []
        for n in self.components():
            dependants = set([dependency[0].NAME for dependency in self.incoming_edges if dependency[1] == n])
            if len(dependants) < len(dependant_projects):
                unacceptable.append(n)
        
        return unacceptable

    def __iter__(self):
        return self.components().__iter__()

    def __getitem__(self, i):
        return self.components().__getitem__(i)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def make_project_clusters(G):
    """
    Clusterize projects in the graph based on their names.
    """

    clusters = []
    pnames = set()
    for n in G.nodes():
        pnames.add(n.NAME)

    for pname in pnames:
        clusters.append( ProjectCluster( G, pname) )

    return clusters

def quote(s, qm = '"'):
    return qm+ str(s) + qm

def to_dot_string(G):
    """
    Construct a string that represent the graph using dot languale.
    It assumes G is a directed graph.
    """

    dot_string = "digraph {\n"
    # first print out any node to be sure to not forget any isolated node
    sorted_nodes = G.nodes()
    sorted_nodes.sort()
    for n in sorted_nodes:
        dot_string += "    " + quote(n) + " [penwidth=3 "
        if('invalid' in G.node[n]):
            dot_string += "color=red "
        elif G.node[n]['pruned']:
            dot_string += "color=blue "
        dot_string += "];\n"

    dot_string += "\n"

    # then write down any edge
    sorted_edges = G.edges(data=True)
    sorted_edges.sort()
    for edge in sorted_edges:
        dot_string += "    " +  quote(edge[0]) + " -> " + quote(edge[1]) 
        if 'valid' in edge[2]:
            if edge[2]['valid']:
                dot_string += '[color=black penwidth=3]'
            else:
                dot_string += '[color=red penwidth=3]'

        dot_string += ";\n"
    dot_string += "}\n"

    return dot_string


class Portfolio:
    def __init__(self, db_connection_info=MongoConnectionInfo()):
        # setup the mongo connection
        self.connection = db_connection_info.connect()
        self.collection = self.connection.pony_store.packages
        self.silent = False

    def encode_requirements(self, meta):
        if "DEPENDENCIES" in meta.keys():
            meta["DEPENDENCIES"] = json.dumps(meta["DEPENDENCIES"])
        return meta

    def decode_requirements(self, meta):
        query_requirements = []
        requirements = []
        if "DEPENDENCIES" in meta.keys():
            query_requirements = json.loads(meta["DEPENDENCIES"])
            for query in query_requirements:
                mongo_cursor = self.collection.find(query)
                for r in mongo_cursor:
                    requirements.append(r)

            meta['DEPENDENCIES'] = requirements
        return requirements

    def check(self, meta):
        same_meta_cursor = self.collection.find(meta)
        fail = same_meta_cursor.count() > 0
        if fail:
            pass#print(same_meta_cursor[0])
        return fail

    def charge (self,  package, meta):
        meta = self.encode_requirements(meta)
        if(self.check(meta)):
            raise YetInPortfolio(meta)
        # add content to metadata. it will become a rich package!
        if sys.version_info < (3, 0):
            meta['package'] = Binary(package)
        else:
            meta['package'] = package
        id = self.collection.insert_one(meta)
        
        del meta['package']
        if not self.silent:
            print ('package archived')
            print (str(meta))
    
    def _select_all(self, meta_request):
        """Select all alternative package matching the request"""
        print('filter is: ' + str(type(meta_request) )+ '  ' + str(meta_request))

        if type(meta_request) is dep.Requirement:
            meta_request = meta_request.meta_request()

        matching_packages = self.collection.find(meta_request)
        if matching_packages.count() == 0:
            raise NotInPortfolio(meta_request)
        
        # return the first matching package
        return matching_packages
            
    def _select(self,meta_request):
        """Select an arbitrary alternative requested package from the set of matching one"""
        selection = []
        matching_packages = self._select_all(meta_request)
        
        
        for p in matching_packages:
            selection.append(p)
        
        for p in selection:
            p = self.decode_requirements(p)
                
        # return the first matching package
        return selection[0] 
        
    
    def take(self, meta_request):
        # take the package from charged document
        package = self._select(meta_request)['package']
        return package
        
    def translate_requirements(self, requests, select_any = True):
        """Translates the requirements into an explicit requirement given the matching boxed into actually in the portfolio. """
        
        if not isinstance(requests, list):
            requests = [requests]    

        meta_requests = [r.meta_request() for r in requests]

        requirements =[]
        for meta_request in meta_requests:
            for p in self._select_all(meta_request):
                requirements.append(dep.Requirement(p))
            
        return requirements

    def requirements_for (self, request, select_any = True):
        """
        Retrieve additional dependencies for a requirements_for
        """
        meta_request = request.meta_request()
        package = self._select(meta_request) if select_any else self._select_all(meta_request)
        requirements = []
        try:
            requirements = dep.make_direct(package['DEPENDENCIES'], parent=request)  
        except KeyError:
            # no dependencies for this package!
            pass
            
        return requirements
      

    def requirements_graph (self, direct_requirements, known_nodes = []):
        gr = nx.DiGraph()

        if not isinstance(direct_requirements, collections.Iterable):
            direct_requirements = [direct_requirements]

        while len(direct_requirements) > 0:
            req = direct_requirements.pop()
            more_requirements = self.requirements_for(req)
            #more_requirements.remove(req)

            local_gr = nx.DiGraph()
            for child_req in more_requirements:
                gr.add_edge(req, child_req, valid=True)
                gr.node[child_req]['pruned'] = False

            gr.add_node(req)
            gr.node[req]['pruned'] = False
            _gr = to_dot_string(gr)
            
            # get the graph describing the direct requirements requirements
            # then join it with the one describing direct requirements (local)
            sub_gr = self.requirements_graph(more_requirements)
            
            gr = nx.compose(gr, sub_gr)
            
        return gr

    def alternative_graph_maker(self, raw_graph):
        print ("making alternatives")
        clusters = make_project_clusters(raw_graph)
        print ("based on " + str(clusters))
        for alternative in combine(clusters):
            gr = raw_graph.copy()
            print("making alternative graph")
            for n in gr.nodes():
                gr.node[n]['pruned'] = n not in alternative
                if n in alternative:
                    print(str(n)) 
            
            yield gr

    def check_node(self, gr, node):
        """Checks that the number of dependant project classified by name is the same as the number of not pruned dependant project node."""

        dependant_nodes = [edge[1] for edge in gr.edges(node)]
        dependant_valid_nodes = [edge[1] for edge in gr.edges(node) if not gr.node[edge[1]]['pruned'] ]
        dependant_projects = set()
        
        for n in dependant_nodes:
            try:
                dependant_projects.add( n.NAME )
            except KeyError:
                # ignore empty graph node for now
                pass
        print("valid nodes: " + str(dependant_valid_nodes))
        print("dependant projects: " + str(dependant_projects))
        print(str(len(dependant_valid_nodes) == len(dependant_projects)))
        return len(dependant_valid_nodes) == len(dependant_projects) 
        
    
    def check_graph(self, gr):
        acceptable = True;
        clusters = make_project_clusters(gr)
        
        for cluster in clusters:
            acceptable_cluster = False
            for n in cluster.components():
                acceptable_cluster = acceptable_cluster or self.check_node(gr, n)
            acceptable = acceptable and acceptable_cluster
        
        
        return acceptable
        
    
    def acceptable_configurations(self, gr):
        if len(gr.nodes()) == 0:
            return [gr]
        configurations = [config for config in self.alternative_graph_maker(gr) if self.check_graph(config)]
        print("" + str(len(configurations)) + " valid configurations")
        if len(configurations) == 0:
            raise ImpossibleConfigurationException(gr)
        return configurations

    def requirements_discover(self, direct_requirements):
        direct_requirements = self.translate_requirements(direct_requirements, select_any=False)
        raw_graph = self.requirements_graph(direct_requirements)

        graph = self.acceptable_configurations(raw_graph)[-1]
      
        return [n for n in graph.nodes() if not graph.node[n]['pruned']], graph
