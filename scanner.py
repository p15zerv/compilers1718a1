
def getchar(words, pos):
    """ Returns character group at `pos` of `words`, or None if out of bounds """

    if pos < 0 or pos >= len(words):
        return None

    # return corresponding character group
    c = words[pos]

    if c in '01':
        return 'DIGIT_UPTO1'

    if c == '2':
        return 'DIGIT_2'

    if c == '3':
        return 'DIGIT_3'

    if c in '45':
        return 'DIGIT_UPTO5'

    if c in '6789':
        return 'ANY_DIGIT'

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


def groups_up_to(group):
    """ Returns a list of the groups up to and including `group`
    """
    digit_group_priority = ['DIGIT_UPTO1', 'DIGIT_2', 'DIGIT_3',
                            'DIGIT_UPTO5', 'ANY_DIGIT']
    return [g for g in digit_group_priority[:digit_group_priority.index(group) + 1]]


# the transition table, as a dictionary
td = {'q0': {'DIGIT_UPTO1': 'q1', 'DIGIT_2': 'q6', 'DIGIT_UPTO5': 'q2', 'ANY_DIGIT': 'q2'},
      # using comprehensions to make the transition table shorter and hopefully more readable
      'q1': {g: 'q2' for g in groups_up_to('ANY_DIGIT')},
      'q2': {'DELIMITER': 'q3'},
      'q3': {g: 'q4' for g in groups_up_to('DIGIT_UPTO5')},
      'q4': {g: 'q5' for g in groups_up_to('ANY_DIGIT')},
      'q6': {g: 'q2' for g in groups_up_to('DIGIT_3')}
      }

# the dictionary of accepting states and their
# corresponding token
ad = {'q5': 'TIMESTAMP_TOKEN'}

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
