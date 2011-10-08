'''
Created on Oct 7, 2011

@author: derek weitzel
'''
import sys

class NFANode:
    transition = {}
    def __init__(self):
        pass
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

operators = ["|", "*", "&"]

def scan(regex_string, start_index, stop_index, parenthese_level):
    if start_index == stop_index:
        return
    found = False
    counter = start_index
    print regex_string[start_index:stop_index+1]
    pcounter = 0
    while(found == False and counter <= stop_index):
        if regex_string[counter] == '(':
            pcounter += 1
        elif regex_string[counter] == ')':
            pcounter -= 1
        elif regex_string[counter] in operators and pcounter <= parenthese_level:
            print "Splitting on %s,  %s : %s" % (regex_string[counter], regex_string[start_index:counter], regex_string[counter+1:stop_index+1])
            scan(regex_string, start_index, counter-1, parenthese_level+1)
            scan(regex_string, counter+1, stop_index, parenthese_level+1)
            return
        counter += 1
        
    print "Found Character: " + regex_string[start_index:stop_index+1].replace('(', '').replace(')', '')
        
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
    


def convert_regex(regex_string):
    new_string = regex_string.replace('aa', 'a&a').replace('ab', 'a&b').replace('ba', 'b&a').replace('bb', 'b&b').replace(')(', ')&(').replace('*a', '*&a').replace('*b', '*&b')
    scan(new_string, 0, len(regex_string)-1, 0)
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


