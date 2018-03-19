
def getchar(words, pos):
    """ Returns character group at `pos` of `words`, or None if out of bounds """

    if pos < 0 or pos >= len(words):
        return None

    # return corresponding character group
    c = words[pos]

    if c in '01':
        return 'D_UPTO1'

    if c == '2':
        return 'D_2'

    if c == '3':
        return 'D_3'

    if c in '45':
        return 'D_UPTO5'

    if c in '6789':
        return 'D_ANY'

    if c in ':.':
        return 'DELIMITER'

    return 'OTHER'


def scan(text, transition_table, accept_states):
    """ Scans `text` while transitions exist in 'transition_table'.
    After that, if in a state belonging to `accept_states`,
    returns the corresponding token, else ERROR_TOKEN.
    """

    # initial state
    pos = 0
    state = 'q0'

    while True:

        c = getchar(text, pos)  # get next char

        if state in transition_table and c in transition_table[state]:

            state = transition_table[state][c]  # set new state
            pos += 1  # advance to next char

        else:  # no transition found

            # check if current state is accepting
            if state in accept_states:
                return accept_states[state], pos

            # current state is not accepting
            return 'ERROR_TOKEN', pos


# the transition table, as a dictionary
td = {
    'q0': {'D_UPTO1': 'q1', 'D_2': 'q3', 'D_3': 'q2', 'D_UPTO5': 'q2', 'D_ANY': 'q2'},
    'q1': {'D_UPTO1': 'q2', 'D_2': 'q2', 'D_3': 'q2', 'D_UPTO5': 'q2', 'D_ANY': 'q2', 'DELIMITER': 'q4'},
    'q2': {'DELIMITER': 'q4'},
    'q3': {'D_UPTO1': 'q2', 'D_2': 'q2', 'D_3': 'q2', 'DELIMITER': 'q4'},
    'q4': {'D_UPTO1': 'q5', 'D_2': 'q5', 'D_3': 'q5', 'D_UPTO5': 'q5'},
    'q5': {'D_UPTO1': 'q6', 'D_2': 'q6', 'D_3': 'q6', 'D_UPTO5': 'q6', 'D_ANY': 'q6'}
}

# the dictionary of accepting states and their
# corresponding token
ad = {'q6': 'TIME_TOKEN'}

# get a string from input
text = input('give some input> ')

# scan text until no more input
while text:  # that is, while len(text)>0

    # get next token and position after last char recognized
    token, position = scan(text, td, ad)

    if token == 'ERROR_TOKEN':
        print('unrecognized input at pos', position + 1, 'of', text)
        break

    print("token:", token, "string:", text[:position])

    # remaining text for next scan
    text = text[position:]
