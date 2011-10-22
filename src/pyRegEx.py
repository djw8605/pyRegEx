'''
Created on Oct 7, 2011

@author: derek weitzel
'''
import sys

main_counter = 0

class NFANode:
    """
    Class for the 'graph' for a NFA
    """
    def __init__(self):
        global main_counter
        self.transition = {}
        self.transition["e"] = []
        
        self.id = main_counter
        main_counter += 1
        pass
    def __str__(self):
        return str(self.id)


# Constants
operators = ["|", "&"]
letters = ["a", "b", "e"]

def parse_regex(regex_string, start_index, stop_index):
    """
    Recursive function to create a NFA
    @param regex_string: String of the regex
    @param start_index: Index of the first character to parse
    @param stop_index: Index of the last character to parse
    @return: (NFANode, [ NFANode ]): Returns the start and final states.
    """
    regex_counter = start_index
    leftside = []
    rightside = []
    while regex_counter <= stop_index:
        # parenthese matching
        if regex_string[regex_counter] == "(":
            pcounter = 0
            find_end_counter = regex_counter+1
            # Search for ending parenthese
            while find_end_counter <= stop_index:
                if regex_string[find_end_counter] == "(":
                    pcounter += 1
                elif regex_string[find_end_counter] == ")" and pcounter == 0:
                    # Found ending parenthese:
                    leftside = parse_regex(regex_string, regex_counter + 1, find_end_counter-1)
                    regex_counter = find_end_counter
                    # break out of while loop 
                    break
                elif regex_string[find_end_counter] == ")":
                    pcounter -= 1
                find_end_counter += 1
                    
        
        
        # if the character is a letter
        elif regex_string[regex_counter] in letters:
            character = regex_string[regex_counter]
            #print "Found character: " + character
            start_node = NFANode()
            final_node = NFANode()
            start_node.transition[character] = []
            start_node.transition[character].append(final_node)
            if len(leftside) == 0:
                leftside = (start_node, [final_node])

        # Starring operation
        elif regex_string[regex_counter] is "*":
            #print "Starring: " + regex_string[start_index:regex_counter+1]
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
            #print "Splitting on %s - %s : %s" % (operator, regex_string[start_index:regex_counter], regex_string[regex_counter+1:stop_index+1])
            (right_start, right_finals) = parse_regex(regex_string, regex_counter+1, stop_index)
            
            if operator == '&':
                for node in leftside[1]:
                    node.transition['e'].append(right_start)
                #print "returning from & ..."
                return (leftside[0], right_finals)
            elif operator == '|':
                new_start = NFANode()
                new_start.transition["e"].append(leftside[0])
                new_start.transition["e"].append(right_start)
                #print str(new_start) + " " + str(new_start.transition)
                #print "returning from | ..."
                return (new_start, leftside[1] + right_finals)
        
        
        #print "At end: " + regex_string[regex_counter]
        regex_counter += 1
    
    #print "returning..."
    return leftside



def GetEStates(state):
    """
    Recursive function to get all states connected to 'state' 
    with an empty string
    """
    current_nodes = []
    #print "Finding e states for " + str(state)
    for node in state.transition["e"]:
        # Break loops
        if node not in current_nodes:
            current_nodes.extend(GetEStates(node))
        
    current_nodes.append(state)
    return current_nodes


def SimulateNFA(NFAStart, input):
    """
    Simulate the NFA
    @param NFAStart: Starting NFANode for the NFA
    @param input: The input string
    """
    current_visited = [NFAStart]
    # loop through the regular expression
    for char in input:
        # First, add to current_visited all nodes linked to current visited
        # by a empty string
        tmp_visited = current_visited[:]
        for node in tmp_visited:
            #print node
            current_visited.extend(GetEStates(node))
        current_visited = list(set(current_visited))
        
        # Next find what states we can transition to
        if char is not 'e':
            tmp_visited = current_visited[:]
            current_visited = []
            for node in tmp_visited:
                if node.transition.has_key(char):
                    current_visited.extend(node.transition[char])
    
    # One last time, transition to all the 'e' states
    tmp_visited = current_visited[:]
    for node in tmp_visited:
        current_visited.extend(GetEStates(node))
    current_visited = list(set(current_visited))
    return current_visited
    

seen_nodes = []
def printtree(node):
    """
    Convenience function to print the output
    @param node: Starting node
    """
   
    tree_dict = node.transition
    for key in tree_dict:
        print str(node) + " ",
        print str(key) + " ",
        for node in tree_dict[key]:
            print str(node),
        print ""
        
        for node in tree_dict[key]:
            if not node in seen_nodes:
                seen_nodes.append(node)
                printtree(node)

            


def convert_regex(regex_string):
    # Add the & symbol for and's to make the expression easier to parse
    new_string = regex_string.replace('aa', 'a&a').replace('ab', 'a&b').replace('ba', 'b&a').replace('bb', 'b&b').replace(')(', ')&(').replace('*a', '*&a').replace('*b', '*&b').replace('*(', '*&(')
    new_string = new_string.replace('aa', 'a&a').replace('ab', 'a&b').replace('ba', 'b&a').replace('bb', 'b&b').replace(')(', ')&(').replace('*a', '*&a').replace('*b', '*&b').replace('*(', '*&(')
    new_string = new_string.strip()

    # parse the regex
    (start_nodes, final_nodes) = parse_regex(new_string, 0, len(new_string)-1)

    return (start_nodes, final_nodes)



def main():
    # Read in input
    regex_string = sys.stdin.readline()
    
    # Convert regex to NFA
    (start_node, final_nodes) = convert_regex(regex_string)
    
    # Read in each line, simulating the NFA each time
    for line in sys.stdin.readlines():
        current_nodes = SimulateNFA(start_node, line.strip())
        
        # See if the current nodes are in the final nodes set
        found_final = False
        for node in current_nodes:
            if node in final_nodes:
                found_final = True
        if found_final:
            print "yes"
        else:
            print "no"




if __name__ == "__main__":
    main()


