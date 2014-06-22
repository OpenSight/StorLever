"""
storlever.web.menu
~~~~~~~~~~~~~~~~

This module implements web menu system

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

from pyramid.i18n import TranslationString
from pyramid.i18n import TranslationStringFactory
from storlever.rest.common import get_view
from storlever.lib.exception import StorLeverError
from storlever.lib.lock import lock

def includeme(config):
    config.add_route('menu_list', '/menu_list')

@get_view(route_name='menu_list')
def get_menu_list(request):
    mgr = WebMenuManager
    root_node_list = mgr.get_root_node_list()
    menu = []
    for node in root_node_list:
        menu.append(node.to_dict(request.localizer))
    return menu


class MenuNode(object):
    def __init__(self, node_id, parent_id, node_type, text, uri):
        if not isinstance(text, TranslationString):
            raise StorLeverError("text must be a instance of TranslationString", 400)
        self.node_id = str(node_id)
        self.parent_id = str(parent_id)
        self.node_type = str(node_type)
        self.text = text
        self.uri = str(uri)
        self._sub_nodes = []
        self._lock = lock()   # protect the _sub_nodes property update

    def to_dict(self, text_localizer=None):

        if text_localizer is None:
            text = str(self.text)
        else:
            text = text_localizer.translate(self.text)

        sub_nodes = self.get_sub_nodes()
        sub_nodes_list = []
        for node in sub_nodes:
            sub_node_dict = node.to_dict(text_localizer)
            sub_nodes_list.append(sub_node_dict)

        return {
            "node_id": self.node_id,
            "parent_id": self.parent_id,
            "node_type": self.node_type,
            "text": text,
            "uri": self.uri,
            "sub_nodes": sub_nodes_list
        }

    def add_sub_node(self, sub_node):
        if not isinstance(sub_node, MenuNode):
            raise StorLeverError("sub_node must be a instance of MenuNode", 400)
        with self._lock:
            self._sub_nodes.append(sub_node)

    def get_sub_nodes(self):
        with self._lock:
            return self._sub_nodes[:]

    def del_sub_node(self, sub_node):
        if not isinstance(sub_node, MenuNode):
            raise StorLeverError("sub_node must be a instance of MenuNode", 400)
        with self._lock:
            self._sub_nodes.remove(sub_node)


class WebMenuManager(object):
    """contains all methods to manage NTP server in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.nodes = {}
        self.root_list = []

    def add_root_node(self, node_id, text, uri):
        root_node = MenuNode(node_id, "", "root", text, uri)
        with self.lock:
            #check id duplicate
            if node_id in self.nodes:
                raise StorLeverError("node_id already exist", 400)

            # add the exist sub node to the new intermediate node
            for entry_id, entry_node in self.nodes.items():
                if entry_node.parent_id == node_id:
                    # check some rules
                    if entry_node.node_type == "leaf":
                        raise StorLeverError("leaf node (%s) cannot be sub node of "
                                             "a root node (%s)" %
                                             (entry_node.node_id, root_node.node_id), 400)

                    root_node.add_sub_node(entry_node)

            self.nodes[root_node.node_id] = root_node
            self.root_list.append(root_node)

    def add_intermediate_node(self, node_id, parent_id, text, uri):

        inter_node = MenuNode(node_id, parent_id, "intermediate", text, uri)

        with self.lock:
            #check id duplicate
            if node_id in self.nodes:
                raise StorLeverError("node_id already exist", 400)

            # add the sub node to the new intermediate node
            for entry_id, entry_node in self.nodes.items():
                if entry_node.parent_id == node_id:
                    if entry_node.node_type != "leaf":
                        raise StorLeverError("intermediate node (%s) cannot be sub node of "
                                             "another intermediate node (%s)" %
                                             (entry_node.node_id, inter_node.node_id), 400)

                    inter_node.add_sub_node(entry_node)

            # add the new intermediate node to the exist root node
            parent_node = self.nodes.get(inter_node.parent_id)
            if parent_node is not None:
                #check some rules
                if parent_node.node_type != "root":
                    raise StorLeverError("intermediate node (%s) cannot be sub node of "
                                         "an non-root node (%s)" %
                                         (inter_node.node_id, parent_node.node_id), 400)
                parent_node.add_sub_node(inter_node)

            self.nodes[inter_node.node_id] = inter_node

    def add_leaf_node(self, node_id, parent_id, text, uri):

        leaf_node = MenuNode(node_id, parent_id, "leaf", text, uri)

        with self.lock:
            #check id duplicate
            if node_id in self.nodes:
                raise StorLeverError("node_id already exist", 400)

            # add the new intermediate node to the exist root node
            parent_node = self.nodes.get(leaf_node.parent_id)
            if parent_node is not None:
                #check some rules
                if parent_node.node_type != "intermediate":
                    raise StorLeverError("leaf node (%s) cannot be sub node of "
                                         "an non-intermediate node (%s)" %
                                         (leaf_node.node_id, parent_node.node_id), 400)
                parent_node.add_sub_node(leaf_node)

            self.nodes[leaf_node.node_id] = leaf_node

    def get_root_node_list(self):
        """return a new temp list contains all the root nodes"""
        with self.lock:
            root_nodes = self.root_list[:]
        return root_nodes

    def get_node_by_id(self, node_id):
        with self.lock:
            if node_id not in self.nodes:
                raise StorLeverError("Node (%s) Not Found" % node_id, 404)
            return self.nodes[node_id]

    def del_node_by_id(self, node_id):
        with self.lock:
            if node_id not in self.nodes:
                raise StorLeverError("Node (%s) Not Found" % node_id, 404)

            node = self.nodes[node_id]
            del self.nodes[node_id]

            if node.node_type == "root":
                self.root_list.remove(node)

            elif node.parent_id != "" and node.parent_id in self.nodes:
                parent_node = self.nodes[node.parent_id]
                if node in parent_node.get_sub_nodes():
                    parent_node.del_sub_node(node)






WebMenuManager = WebMenuManager()

def web_menu_mgr():
    """return the global user manager instance"""
    return WebMenuManager
