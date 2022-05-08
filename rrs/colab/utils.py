import ast


def prettyPrint(message):
    print("\n" + " " + "#"*15 + " " + message + " " + "#"*15)


# Function that extract keys from the nested dictionary
def extract_keys(attr, key):
    if attr == None:
        return "{}"
    if key in attr:
        return attr.pop(key)


# convert string to dictionary
def str_to_dict(attr):
    if attr != None:
        return ast.literal_eval(attr)
    else:
        return ast.literal_eval("{}")
