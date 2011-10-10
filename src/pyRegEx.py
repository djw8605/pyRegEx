'''
Created on Oct 7, 2011

@author: derek weitzel
'''
import sys

main_counter = 0

class NFANode:
    def __init__(self):
        global main_counter
        self.transition = {}
        self.transition["e"] = []
        
        self.id = main_counter
        main_counter += 1
        pass
    def __str__(self):
        return str(self.id)
    #def __str__(self):
        #print self.transition
        #for key in self.transition.keys():
        #    print key + "->" + str(self.transition[key])
    

class NFAGroup(NFANode):
    def __init__(self):
        pass
    

NFAGraph = []

class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left  = left
        self.right = right

    def __str__(self):
        string = ""
        if self.left is not None:
            string += str(self.left)
        string += str(self.cargo)
        if self.right is not None:
            string += str(self.right)
            
        return string


def get_token(token_list, expected):
    if token_list[0] == expected:
        del token_list[0]
        return True
    else:
        return False
    
    
def get_letter(token_list):
    
    if get_token(token_list, '('):
        x = get_star(token_list)
        get_token(token_list, ')')
        return x
    else:
        x = token_list[0]
        if x != 'a' and x != 'b':
            print x
            print "returning none"
            return None
        token_list[0:1] = []
        return Tree (x, None, None)    


def get_or(token_list):
    print token_list
    a = get_letter(token_list)
    print a
    if get_token(token_list, "|"):
        b = get_or(token_list)
        print "Orring %s | %s" % (str(a), str(b))
        return Tree('|', a, b)
    else:
        return a

def get_star(token_list):
    a = get_or(token_list)
    if get_token(token_list, '*'):
        print "Starring %s" % a
        return Tree ('*', a, None)
    else:
        return a

operators = ["|", "&"]

def scan(regex_string, start_index, stop_index, parenthese_level):
    if start_index > stop_index:
        return (None, None)
    found = False
    counter = start_index
    print regex_string[start_index:stop_index+1]
    pcounter = 0
    while(found == False and counter <= stop_index):
        if regex_string[stop_index] == "*":
            (start_node1, final_nodes1) = scan(regex_string, start_index, counter, parenthese_level+1)
            print "Starring %s" % regex_string[start_index:counter+1]
            new_end = NFANode()
            new_start = NFANode()
            new_start.transition["e"].append(start_node1)
            for node in final_nodes1:
                node.transition['e'].append(new_start)
            new_start.transition["e"].append(new_end)
            return (new_start, [new_end])
        elif regex_string[counter] == '(':
            pcounter += 1
        elif regex_string[counter] == ')':
            pcounter -= 1
        elif regex_string[counter] in operators and pcounter <= parenthese_level:
            operator = regex_string[counter]
            print "Splitting on %s,  %s : %s" % (operator, regex_string[start_index:counter], regex_string[counter+1:stop_index+1])
            # Left side
            (start_node1, final_nodes1) = scan(regex_string, start_index, counter-1, parenthese_level+1)
            # Right side
            (start_node2, final_nodes2) = scan(regex_string, counter+1, stop_index, parenthese_level+1)
            operator = regex_string[counter]
            if operator == '&':
                for node in final_nodes1:
                    node.transition['e'].append(start_node2)
                return (start_node1, final_nodes2)
            elif operator == '*':
                new_end = NFANode()
                new_start = NFANode()
                new_start.transition["e"].append(start_node1)
                for node in final_nodes1:
                    node.transition['e'].append(new_start)
                new_start.transition["e"].append(new_end)
                return (new_start, [new_end])
                
            elif operator == '|':
                new_start = NFANode()
                new_start.transition["e"].append(start_node1)
                new_start.transition["e"].append(start_node2)
                print str(new_start) + " " + str(new_start.transition)
                return (new_start, final_nodes1 + final_nodes2)
        counter += 1
        
    start_node = NFANode()
    final_node = NFANode()
    character = regex_string[start_index:stop_index+1].replace('(', '').replace(')', '')
    print character
    start_node.transition[character] = final_node
    return (start_node, [final_node])
        
    pass


def create_graph(regex_string, current_index, first_node, final_nodes):
    print "Reading %s" % regex_string[current_index]
    if regex_string[current_index] == '(':
        return create_graph(regex_string, current_index+1, first_node, final_nodes)
    elif regex_string[current_index] == '|':
        (front_node1, final_nodes1) = create_graph(regex_string, current_index+1, first_node, final_nodes)
        new_front = NFANode()
        new_front.transition["e"] = front_node1
        new_front.transition["e"] = first_node
        return (new_front, [final_nodes])
        
    elif regex_string[current_index] == 'a' or regex_string[current_index] == 'b':
        first_node = NFANode()
        last_node = NFANode()
        first_node.transition[regex_string[current_index]] = last_node
        return (first_node, [last_node])
    

seen_nodes = []
def printtree(node):
   
    tree_dict = node.transition
    for key in tree_dict:
        print str(node) + " ",
        if key == 'e':
            print key + " ",
            for node in tree_dict[key]:
                print str(node),
            print ""
        else:
            print key + " " + str(tree_dict[key])
        
        
        if key == 'e':
            for node in tree_dict[key]:
                if not node in seen_nodes:
                    seen_nodes.append(node)
                    printtree(node)
        else:
            if not tree_dict[key] in seen_nodes:
                seen_nodes.append(tree_dict[key])
                printtree(tree_dict[key])
            


def convert_regex(regex_string):
    new_string = regex_string.replace('aa', 'a&a').replace('ab', 'a&b').replace('ba', 'b&a').replace('bb', 'b&b').replace(')(', ')&(').replace('*a', '*&a').replace('*b', '*&b')
    new_string = new_string.replace('aa', 'a&a').replace('ab', 'a&b').replace('ba', 'b&a').replace('bb', 'b&b').replace(')(', ')&(').replace('*a', '*&a').replace('*b', '*&b')
    new_string = new_string.strip()
    (start_nodes, final_nodes) = scan(new_string, 0, len(new_string)-1, 0)
    print "Start: " + str(start_nodes)
    print "Final: ",
    for node in final_nodes:
        print str(node) + " ",
    print final_nodes
    printtree(start_nodes)
    
    #print new_string
    #graph_start = NFANode()
    #print list(regex_string)
    #token_list = list(regex_string.strip())
    #master_tree = []
    #while len(token_list) > 0:
    #    print "Running tree"
    #    tree = get_star(token_list)
    #    master_tree.append(tree)
    #graph = create_graph(regex_string, 0, None, None)
    #print graph[0].transition
    #print "tree:"
    #print master_tree
        
            
            
            
    pass


def main():
    # Read in input
    regex_string = sys.stdin.readline()
    
    #Convert 
    convert_regex(regex_string)
    
    pass



if __name__ == "__main__":
    main()


