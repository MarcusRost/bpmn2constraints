"""
A minimal working example for parsing JSON and constructing SiGNAL constraints.
"""
from bpmnsignal.matching_templates import init, end, succession


def parse_bpmn(j_bpmn):
    """Takes a BPMN model in Signavio's proprietary JSON format and
    extracts a (linear) ordered list of activities from it.

    Args:
        j_bpmn (json): BPMN model in Signavio's proprietary JSON format

    Returns:
        list: List of activities ordered by occurence
    """
    elements = j_bpmn['childShapes']
    sequence = []
    for element in elements:
        if element['stencil']['id'] == 'StartNoneEvent':
            successors = element['outgoing']
            has_successor = len(successors) > 0
            while has_successor:
                successor = successors[0]['resourceId']
                element = [
                    element for element in elements if element['resourceId'] == successor][0]
                if not element['stencil']['id'] in ['SequenceFlow', 'EndNoneEvent']:
                    sequence.append(element['properties']['name'])
                successors = element['outgoing']
                has_successor = len(successors) > 0
    return sequence


def construct_linear_constraints(sequence):
    """Generates SIGNAL constraints from a linear sequence of activities

    Args:
        sequence (List): Activity sequence

    Returns: 
        List: List of SIGNAL constraints
    """
    constraints = []
    for index, element in enumerate(sequence):
        if index == 0:
            constraints.append(init(element))
        if index == len(sequence) - 1:
            constraints.append(end(element))
            break
        constraints.append(succession(element, sequence[index + 1]))
    return constraints
