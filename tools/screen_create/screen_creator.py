#!/usr/bin/env python

"""
Zabbix Screen creation tool
Brian Gallew
This is very similar to another script (zabbix_tool) I wrote, except that
it's much more limited in scope: screen creation.  I don't know how many
screens I've created by hand, but really, all the clicking, pointing,
searching, dragging, etc., get more than a little annoying after a while.
https://github.com/gescheit/scripts/blob/master/zabbix/zabbix_api.py
"""

try:
    import zabbix_api
except:
    print "Please install https://github.com/gescheit/scripts/blob/master/zabbix/zabbix_api.py\nbefore trying to run this script."
    exit()
    
import sys
import os
import logging
import ConfigParser
import argparse
import operator
import re
from pprint import pprint

CONFIG = 'config'
LOGLEVEL = 'loglevel'
NAME = 'name'
PASSWORD = 'password'
URL = 'url'
VERBOSE = 'verbose'
FILTER = 'filter'
SECTION = 'section'

CONFIG_HELP = '''
All Screen, Item, Host, and Group identifiers may be either a name or an ID.
The Config file used by %s should look like this:
-------------- CUT HERE -----------------
[zabbix]
username='zabbix-api-user'
password='not-your-password'
url='http://zabbix-api.example.com/'
[dev]
username='zabbix-dev-api-user'
password='not-mine-either'
url='https://zabbix-dev.example.com/'
-------------- CUT HERE -----------------
By default, %s will use the [zabbix] paragraph, but if you use the
-s/--section option, you can tell %s to use a different section.
''' % (sys.argv[0], sys.argv[0], sys.argv[0])


class Client(object):

    '''Zabbix API CLI tool.  All public functions should return a list
    which will be printed and summarized.'''

    _APPLICATIONID = 'applicationid'
    _APPLICATIONIDS = 'applicationids'
    _DESCRIPTION = 'description'
    _ERROR = 'error'
    _EXTEND = 'extend'
    _FILTER = 'filter'
    _GRAPHID = 'graphid'
    _GRAPHIDS = 'graphids'
    _GROUPID = 'groupid'
    _GROUPIDS = 'groupids'
    _HEIGHT = 'height'
    _HOST = 'host'
    _HOSTID = 'hostid'
    _HOSTIDS = 'hostids'
    _HOSTS = 'hosts'
    _HSIZE = 'hsize'
    _ITEMID = 'itemid'
    _ITEMIDS = 'itemids'
    _KEY = 'key_'
    _LIMIT = 'limit'
    _NAME = 'name'
    _OUTPUT = 'output'
    _PROXYID = 'proxyid'
    _PROXYIDS = 'proxyids'
    _RESOURCEID = 'resourceid'
    _RESULT = 'result'
    _SCREENID = 'screenid'
    _SCREENIDS = 'screenids'
    _SEARCH = 'search'
    _SEARCHWILDCARDSENABLED = 'searchwildcardsenabled'
    _SELECTHOSTS = 'selectHosts'
    _SELECTTRIGGERS = 'selectTriggers'
    _SORTFIELD = 'sortfield'
    _SORTORDER = 'sortorder'
    _STATUS = 'status'
    _TEMPLATEID = 'templateid'
    _TEMPLATEIDS = 'templateids'
    _TEMPLATES = 'templates'
    _TRIGGERIDS = 'triggerids'
    _VSIZE = 'vsize'
    _WIDTH = 'width'

    def __init__(self, options, timeout=60):
        '''Connect to Zabbix server
        :param options: Result of parsing command line
        :param timeout: Maximum length of time for a single RPC
        :returns: None
        '''
        logging.debug("ENTERED: Client.__init__")
        self.options = options
        self.template = None    # Placeholder for a template we may never use
        self.z = zabbix_api.ZabbixAPI(server=options.url, timeout=timeout)
        if not getattr(self.z, 'screenitem'):
            print dir(self.z)
            screenitem_error()

        self.z.set_log_level(logging.root.level)
        self.z.login(user=options.username, password=options.password)
        return

    def get_screen(self, identifier):
        '''Look up a screen.
        :param identifier: the name or ID of a screen
        :returns: Zabbix screen object or empty dict'''
        logging.debug("ENTERED: Client.get_screen")
        self.get_template()
        try:
            int(identifier)
            if self.template:
                result = self.z.templatescreen.get({self._SCREENIDS: identifier,
                                                    self._TEMPLATEIDS: self.template[self._TEMPLATEID],
                                                    self._OUTPUT: self._EXTEND})
            else:
                result = self.z.screen.get({self._SCREENIDS: identifier,
                                            self._OUTPUT: self._EXTEND})
        except:
            if self.template:
                result = self.z.templatescreen.get({self._FILTER: {self._NAME: identifier},
                                                    self._TEMPLATEIDS: self.template[self._TEMPLATEID],
                                                    self._OUTPUT: self._EXTEND})
            else:
                result = self.z.screen.get({self._FILTER: {self._NAME: identifier},
                                            self._OUTPUT: self._EXTEND})
        logging.debug("Client.get_screen result: %s", str(result))
        self.screen = result and result[0] or {}
        return self.screen

    def get_template(self):
        '''Look up a template by name or ID number.  Returns a list with a single element'''
        if self.template: return
        if not self.options.template: return
        try:
            result = self.z.template.get({self._TEMPLATEIDS: int(self.options.template), self._OUTPUT: self._EXTEND})
        except:
            result = self.z.template.get({self._FILTER: {self._HOST: self.options.template}, self._OUTPUT: self._EXTEND})
        if not result:
            logging.fatal("Unable to find template %s", self.options.template)
        self.template = result[0]

    def get_graph(self, identifier):
        '''Look up a graph.
        :param identifier: name or ID of a graph
        :returns: List of Zabbix graph objects or []'''
        logging.debug("ENTERED: Client.get_graph")
        params = {self._OUTPUT: self._EXTEND}
        if self.template:
            params[self._TEMPLATEIDS] = self.template[self._TEMPLATEID]
        try:
            params[self._GRAPHIDS] = int(identifier)
        except:
            params[self._FILTER] = {self._NAME: identifier}
        result = self.z.graph.get(params)
        logging.debug("Client.get_graph result: %s", str(result))
        return result or []

    def get_hostgroup(self, hostgroup):
        '''Look up a hostgroup by name or ID number.
        :param hostgroup: name or ID of a hostgroup
        :returns: Zabbix hostgroup object or {}
        '''
        logging.debug("ENTERED: Client.get_hostgroup")
        try:
            int(hostgroup)
            result = self.z.hostgroup.get({self._GROUPIDS: hostgroup,
                                           self._OUTPUT: self._EXTEND})
        except:
            result = self.z.hostgroup.get({self._FILTER:
                                           {self._NAME: hostgroup}})
        logging.debug("Client.get_hostgroup result: %s", str(result))
        return result and result[0] or {}

    def get_host(self, host):
        '''Look up a host by name or ID number.
        :param host: name or ID of a host
        :returns: Zabbix host object or {}'''
        logging.debug("ENTERED: Client.get_host")
        try:
            int(host)
            result = self.z.host.get({self._HOSTIDS: host,
                                      self._OUTPUT: self._EXTEND})
        except:
            result = self.z.host.get({self._FILTER: {self._HOST: host}})
        return result and result[0] or {}

    def get_hostgroup_hosts(self, hostgroup):
        '''Look up all of the hosts which belong to a given hostgroup.  This
        uses it's own call to self.z.hostgroup because it wants to use the
        _SELECTHOSTS extension.
        :param hostgroup: name or ID of a hostgroup
        :returns: list of Zabbix hosts or []
        '''
        logging.debug("ENTERED: Client.get_hostgroup_hosts")
        hostgroup = self.get_hostgroup(hostgroup)
        if not hostgroup:
            return hostgroup
        hosts = []
        for x in self.z.hostgroup.get({self._GROUPIDS: hostgroup[self._GROUPID],
                                       self._SELECTHOSTS: self._EXTEND
                                       }):
            hosts.extend(x[self._HOSTS])
        return sorted(hosts, key=operator.itemgetter(self._HOST))

    def create(self):
        """Creates a screen.
        :param name: The name of the new screen
        :param hsize: How many graphs wide the screen will be
        :param vsize: How many graphs high the screen will be
        :returns: screen (zabbix screen object)
        """
        logging.debug("ENTERED: Client.create")
        if self.template:
            result = self.z.templatescreen.create({
                self._TEMPLATEID: self.template[self._TEMPLATEID],
                self._NAME: self.options.screen,
                self._HSIZE: self.options.hsize or 1,
                self._VSIZE: self.options.vsize or 1
            })
        else:
            result = self.z.screen.create({
                self._NAME: self.options.screen,
                self._HSIZE: self.options.hsize or 1,
                self._VSIZE: self.options.vsize or 1
            })
        logging.debug("Client.create result: %s", str(result))
        if result: self.get_screen(result[self._SCREENIDS][0])
        return self.screen

    def update_screen_settings(self):
        '''Check the options to see if the screen needs to be updated,
        then do so.
        :returns: the (possibly updated) screen
        '''
        logging.debug("ENTERED: Client.update_screen_settings")
        params = {}
        if self.options.rename and self.screen[self._NAME] != self.options.rename:
            params[self._NAME] = self.options.rename
        if self.options.hsize and self.screen[self._HSIZE] != self.options.hsize:
            params[self._HSIZE] = self.options.hsize
        if self.options.vsize and self.screen[self._VSIZE] != self.options.vsize:
            params[self._VSIZE] = self.options.vsize
        if params:
            params[self._SCREENID] = self.screen[self._SCREENID]
            if self.template:
                params[self._TEMPLATEID] = self.template[self._TEMPLATEID]
                # This should probably check the return value
                self.z.templatescreen.update(params)
            else:
                # This should probably check the return value
                self.z.screen.update(params)
            self.get_screen(self.screen[self._SCREENID])
        return self.screen

    def delete_screen(self):
        '''Deletes a screen.  Exit when done.
        '''
        screen = self.get_screen(self.options.screen)
        if screen:
            if self.template:
                self.z.templatescreen.delete([self.screen[self._SCREENID], ])
            else:
                self.z.screen.delete([self.screen[self._SCREENID], ])
        self.screen = None
        self.template = None
        return

    def add_screenitem(self, screenid, graphid, x, y):
        '''Adds one graph to a screen, possibly explicitly setting the height or
        width of the graph.
        :param screenid: ID of the screen to be updated
        :param graphid: ID of the graph to be added
        :param x: horizontal position of the graph
        :param y: vertical position (from the top) of the graph
        '''
        params = {self._SCREENID: screenid,
                  self._RESOURCEID: graphid,
                  'resourcetype': 0,
                  'rowspan': 0,
                  'colspan': 0,
                  'x': x,
                  'y': y}
        for param in [self._HEIGHT, self._WIDTH]:
            value = getattr(self.options, param, None)
            if value: params[param] = value
        self.z.screenitem.create(params)
        return

    def add_graphs_to_screen(self, graphs):
        '''Add graphs directly to a screen object.
        :param graphs: list of Zabbix graph objects
        :returns: None or an error message
        '''
        # Get the current screen configuration
        existing_items = self.z.screenitem.get({self._SCREENIDS: self.screen[self._SCREENID],
                                                self._OUTPUT: self._EXTEND})

        # Build a matrix to use for graph positioning
        graph_matrix = [[None for x in xrange(int(self.screen[self._HSIZE]))]
                        for x in xrange(int(self.screen[self._VSIZE]))]

        # This lookup table is created so that we don't have to repeatedly
        # iterate over the list of graphs.
        lookup_table = {}
        for graph in graphs: lookup_table[graph[self._GRAPHID]] = graph
            
        # Add each item from the existing item set into the matrix.  While
        # we're at it, ensure we remove them all from the set of graphs to
        # be added (no duplicates!).
        for item in existing_items:
            graph_matrix[int(item['y'])][int(item['x'])] = item
            if item[self._RESOURCEID] in lookup_table:
                logging.info('add_graphs_to_screen: Removing existing item from add list: %s', item[self._RESOURCEID])
                graphs.remove(lookup_table[item[self._RESOURCEID]])

        # Iterate through the matrix looking for empty graph locations.
        for y, row in enumerate(graph_matrix):
            for x, item in enumerate(row):
                if not graphs: break
                if item: continue
                value = graphs.pop(0)
                self.add_screenitem(self.screen[self._SCREENID],
                                    value[self._GRAPHID],
                                    x,
                                    y)
                graph_matrix[y][x] = value
        if not graphs: return   # We're all done!
        return '%d graphs were not added because the screen is too small (%s x %s)' % (len(graphs),
                                                                                       self.screen[self._HSIZE],
                                                                                       self.screen[self._VSIZE])
        

    def add_all_template(self):
        '''Add all of the graphs associated with the template to the screen.
        '''
        if not self.template:   # Check to see if we're using a template
            return              # Bail if not

        # Get the graph set for the host in question.
        filter = re.compile(self.options.filter)
        graphs = self.z.graph.get({self._TEMPLATEIDS: self.template[self._TEMPLATEID], self._OUTPUT: self._EXTEND})
        graphs.sort(key=operator.itemgetter(self._NAME))
        logging.info('add_all_host: Got %d graphs', len(graphs))
        graphs = [x for x in graphs if filter.search(x[self._NAME])]
        if not graphs: return 'All graphs filtered out'
        
        return self.add_graphs_to_screen(graphs)

    def add_all_host(self):
        '''Add all of the graphs associated with the host to the screen.
        '''
        if not self.options.add_all_host: # Check to see if we're adding host graphs
            return                   # Bail if not
        if self.template:
            loggin.warn("--add-all-host isn't valid with --template, ignoring it")
            return

        # Get our host information
        host = self.get_host(self.options.add_all_host)
        if not host:
            return 'Unable to find host %s' % self.options.add_all_host
        logging.debug('add_all_host: hostid is %s', host[self._HOSTID])

        # Get the graph set for the host in question.
        filter = re.compile(self.options.filter)
        graphs = self.z.graph.get({self._HOSTIDS: host[self._HOSTID], self._OUTPUT: self._EXTEND})
        graphs.sort(key=operator.itemgetter(self._NAME))
        logging.info('add_all_host: Got %d graphs', len(graphs))
        graphs = [x for x in graphs if filter.search(x[self._NAME])]
        if not graphs: return 'All graphs filtered out'
        
        return self.add_graphs_to_screen(graphs)

    def add_all_group(self):
        '''Add all of the graphs associated with the given hostgroup to the given
        screen.
        :returns: None or an error message
        '''
        if not self.options.add_all_group: # Check to see if we're really doing this
            return                   # Bail if not
        if self.template:
            loggin.warn("--add-all-group isn't valid with --template, ignoring it")
            return
        # Get our host information
        hostlist = self.get_hostgroup_hosts(self.options.add_all_group[0])
        if not hostlist:
            return 'Unable to find hostgroup %s' % self.options.add_all_group[0]

        filter = re.compile(self.options.filter)

        hostlist = [x[self._HOSTID] for x in hostlist if filter.search(x[self._NAME]) or filter.search(x[self._HOST])]
        if not hostlist: return 'All hosts filtered out'
        logging.debug('add_all_group: hosts are %s', str(hostlist))
        
        # Get the graph set for the hosts in question.
        graphs = self.z.graph.get({self._HOSTIDS: hostlist, self._OUTPUT: self._EXTEND,
                                   self._FILTER: {self._NAME: self.options.add_all_group[1]}})
        logging.info('add_all_group: Got %d graphs', len(graphs))

        # This oddity is to sort the graphs, because we'd *like* the graphs
        # to be ordered by hostname.  Of course, if there are "holes" in
        # the screen, they will play hob with this ordering, but that's a
        # different problem.
        sorted_graphs = []
        for hostid in hostlist:
            sorted_graphs.extend([x for x in graphs if x[self._HOSTS][0][self._HOSTID] == hostid])
        logging.debug('add_all_group: Sorted into %d graphs', len(sorted_graphs))
        
        return self.add_graphs_to_screen(sorted_graphs)

def parse_command_line():
    '''Handle command-line options
    :returns: options, Client
    '''
    parser = argparse.ArgumentParser(epilog=CONFIG_HELP,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--config", dest="config",
                        default=os.environ['HOME'] + '/.zabbix',
                        help="CONFIG file", metavar="CONFIG")
    parser.add_argument("-s", "--section", dest="section", default='zabbix',
                        help="Section of config file to use file", metavar="SECTION")
    parser.add_argument("-d", "--debug", action='store_true', default=False,
                        help="Enable debugging messages")
    parser.add_argument("-v", "--verbose", action='store_true', default=False,
                        help="Enable verbose messages")
    parser.add_argument("--delete", action='store_true', default=False,
                        help="Delete a screen")
    parser.add_argument("--add-all-host",
                        help="Add all of the graphs from the given host")
    parser.add_argument("--add-all-group", nargs=2, metavar=('GROUP', 'GRAPH'),
                        help="For all of the hosts in the given group, add the given graph")
    parser.add_argument("--hsize", type=int,
                        help="Set the width of the screen (in graph objects)")
    parser.add_argument("--vsize", type=int,
                        help="Set the height of the screen (in graph objects)")
    parser.add_argument("--height", default=0, type=int,
                        help="The height of all graphs to be added")
    parser.add_argument("--width", default=0, type=int,
                        help="The width of all graphs to be added")
    parser.add_argument("--filter", default='.*',
                        help="REGEX filter graph names for hosts, host names for hostgroups.")
    parser.add_argument("--rename", help="Change the name of the screen")
    parser.add_argument("-t", "--template", default=None,
                        help="Working with the give template")
    parser.add_argument("screen", help="The screen")

    options = parser.parse_args()
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(options.config))
    except ConfigParser.Error, config_exception:
        msg = 'Unable to parse the configuration file(%s): %s\n\n'
        print msg % (options.config, config_exception)
        raise
    if not options.section in config.sections():
        raise SystemExit('No [zabbix] section in the configuration file')

    for (key, value) in config.items(options.section, 1):
        setattr(options, key, eval(value))

    return options, Client(options)      # Cheating!


def main():
    '''Program entry point'''
    options, tool = parse_command_line()
    
    # If we're deleting the screen, don't do anything else!
    if options.delete:
        tool.delete_screen()
        exit()

    screen = tool.get_screen(options.screen)

    if not screen:
        screen = tool.create()
    else:
        screen = tool.update_screen_settings()
    for fn in [tool.add_all_host, tool.add_all_group, tool.add_all_template]:
        result = fn()
        if result:
            logging.fatal(result)
            exit(1)
    print screen
    return

if __name__ == '__main__':
    main()