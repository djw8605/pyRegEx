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


operators = ["|", "&"]

def scan(regex_string, start_index, stop_index, parenthese_level):
    if start_index > stop_index:
        return (None, None)
    found = False
    counter = start_index
    print regex_string[start_index:stop_index+1]
    pcounter = 0
    while(found == False and counter <= stop_index):
        if regex_string[stop_index] == "*" or (regex_string[stop_index] == ")" and regex_string[stop_index-1] == "*"):
            if regex_string[stop_index] == ")" and regex_string[stop_index-1] == "*":
                (start_node1, final_nodes1) = scan(regex_string, start_index, stop_index-2, parenthese_level+1)
            else:
                (start_node1, final_nodes1) = scan(regex_string, start_index, stop_index-1, parenthese_level+1)
            print "Starring %s" % regex_string[start_index:stop_index]
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
                #print str(new_start) + " " + str(new_start.transition)
                return (new_start, final_nodes1 + final_nodes2)
        counter += 1
        
    start_node = NFANode()
    final_node = NFANode()
    character = regex_string[start_index:stop_index+1].replace('(', '').replace(')', '')
    start_node.transition[character] = final_node
    return (start_node, [final_node])
        

letters = ["a", "b", "e"]

def scan2(regex_string, start_index, stop_index):
    regex_counter = start_index
    leftside = []
    rightside = []
    while regex_counter <= stop_index:
        print "Parsing: " + regex_string[regex_counter]
        print "Counter = " + str(regex_counter)
        # parenthese matching
        if regex_string[regex_counter] == "(":
            print "Found start parenth"
            pcounter = 0
            find_end_counter = regex_counter+1
            while find_end_counter <= stop_index:
                print "Searching for end parenthese: " + regex_string[find_end_counter]
                if regex_string[find_end_counter] == "(":
                    pcounter += 1
                elif regex_string[find_end_counter] == ")" and pcounter == 0:
                    # Found ending parenthese:
                    print "Parsing inner: " + regex_string[regex_counter+1:find_end_counter]
                    print "find_end_counter = " + str(find_end_counter)
                    leftside = scan2(regex_string, regex_counter + 1, find_end_counter-1)
                    regex_counter = find_end_counter
                    # break out of while loop 
                    break
                elif regex_string[find_end_counter] == ")":
                    pcounter -= 1
                find_end_counter += 1
                    
        
        
        # if the character is a letter
        elif regex_string[regex_counter] in letters:
            character = regex_string[regex_counter]
            print "Found character: " + character
            start_node = NFANode()
            final_node = NFANode()
            start_node.transition[character] = final_node
            if len(leftside) == 0:
                leftside = (start_node, [final_node])

        # Starring operation
        elif regex_string[regex_counter] is "*":
            print "Starring: " + regex_string[start_index:regex_counter+1]
            new_end = NFANode()
            new_start = NFANode()
            new_start.transition["e"].append(leftside[0])
            for node in leftside[1]:
                node.transition['e'].append(new_start)
            new_start.transition["e"].append(new_end)
            leftside = (new_start, [new_end])

        # operators (or and and)
        elif regex_string[regex_counter] in operators:
            operator = regex_string[regex_counter]
            # Need to get right side
            print "Splitting on %s - %s : %s" % (operator, regex_string[start_index:regex_counter], regex_string[regex_counter+1:stop_index+1])
            (right_start, right_finals) = scan2(regex_string, regex_counter+1, stop_index)
            
            if operator == '&':
                for node in leftside[1]:
                    node.transition['e'].append(right_start)
                print "returning from & ..."
                return (leftside[0], right_finals)
            elif operator == '|':
                new_start = NFANode()
                new_start.transition["e"].append(leftside[0])
                new_start.transition["e"].append(right_start)
                #print str(new_start) + " " + str(new_start.transition)
                print "returning from | ..."
                return (new_start, leftside[1] + right_finals)
        
        
        print "At end: " + regex_string[regex_counter]
        regex_counter += 1
    
    print "returning..."
    return leftside


seen_nodes = []
def printtree(node):
   
    tree_dict = node.transition
    for key in tree_dict:
        print str(node) + " ",
        if key == 'e':
            print str(key) + " ",
            for node in tree_dict[key]:
                print str(node),
            print ""
        else:
            print str(key) + " " + str(tree_dict[key])
        
        
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
    print new_string
    #(start_nodes, final_nodes) = scan(new_string, 0, len(new_string)-1, 0)
    (start_nodes, final_nodes) = scan2(new_string, 0, len(new_string)-1)
    print "Start: " + str(start_nodes)
    print "Final: ",
    for node in final_nodes:
        print str(node) + " ",
    print final_nodes
    printtree(start_nodes)



def main():
    # Read in input
    regex_string = sys.stdin.readline()
    
    #Convert 
    convert_regex(regex_string)
    
    pass



if __name__ == "__main__":
    main()


