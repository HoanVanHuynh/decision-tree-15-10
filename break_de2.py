# Toy dataset.
# Format: 
# Each row is an example .
# The first two columns are features 
# The last column is the label.
# Feel free to play with it by adding more feature and examples.
# Interesting note:
# I've written this so the 2nd and 5th examples
# have the same features, but different labels

# so we can see how the tree handles this case.
training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]

def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])


def vals(rows, col):
    """Find the unique values for a column in a dataset"""
    return [row[col] for row in rows]

def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {} # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column 
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] +=1 
    return counts 

def counts_number(rows, col):
    counts =  {} 
    for row in rows:
        column = row[col] 
        if column not in counts:
            counts[column] = 0 
        counts[column] += 1
    return counts 


class_counts(training_data)




def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

class Question:
    """ A Question is used to partition a dataset.
    
    """
    def __init__(self, column, value):
        self.column = column 
        self.value = value 

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value 
        else:
            return val == self.value 

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (header[self.column], condition, str(self.value))








if __name__ == "__main__":
    vals(training_data, 1)
    unique_vals(training_data,0)

# Demo:
# s = unique_vals(training_data, 0)
# print(s)
# unique_vals(training_data, 1)

