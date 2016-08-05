from xml.etree.ElementTree import ElementTree, Element


def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    tree.write(out_path, encoding="GB2312", xml_declaration=True)


def if_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


# ---------------search -----
def find_nodes(tree, path):
    return tree.findall(path)


def get_node_by_keyvalue(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


# ---------------change -----
def change_node_properties(nodelist, kv_map, is_delete=False):
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def create_node(tag, property_map, content):
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)


def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)


if __name__ == "__main__":

    tree = read_xml("./TestUnit.xml")

    nodes = find_nodes(tree, "DestUserID/item")

    change_node_properties(nodes, {"UserID": "1"})
    nodes=find_nodes(tree,"BizUnit")
    a = create_node("Unit", {"type": "message", "RunSeconds":"0", "time":"20", "interval":"0", "sleepPerThd":"0", "filename":"message.xml", "evrMsgLog":"y","NODE":"0"},'')

    add_child_node(nodes,a)
    write_xml(tree, "./out4.xml")
