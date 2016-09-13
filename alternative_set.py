
def combine(alternative_sets):

    if len(alternative_sets) > 0:
        frist_set = alternative_sets[0]
        if type(alternative_sets[0]) is not list:
            frist_set = list(alternative_sets[0])
            frist_set.sort()

        if len(alternative_sets) <2:
            for alternative in frist_set:
                yield alternative, 
        else:
            for alternative in [(alt,) for alt in frist_set]:
                for sub_configuration in combine(alternative_sets[1:]):
                    yield alternative + sub_configuration
