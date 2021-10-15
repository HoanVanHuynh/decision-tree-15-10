training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]
header = ["color", "diameter", "label"]

def unique_vals(rows, col):
    """Find the unique values for a column 
    in a dataset."""
    return set([row[col] for row in rows])

def vals(rows, col):
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

def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

class Question:
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


def partition(rows, question):
    true_rows, false_rows = [], [] 
    for row in rows:
        if question.match(row):
            true_rows.append(row) 
        else:
            false_rows.append(row) 
    return true_rows, false_rows 

# Let's partition the training data based on whether rows are Red. 

true_rows, false_rows = partition(training_data, Question(0, 'Red'))
# This will contain all the 'Red' rows.
true_rows
# This will contain everything else. 
false_rows 

def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity 

#######
# Demo: 
# Let's look at some example to understand how Gini Impurity works. 


def gini2(rows=10):
    
    counts = [4,3,2,1]
    impurity = 1
    for lbl in counts:
        prob_of_lbl = lbl / 10
        # impurity -= prob_of_lbl**2
        impurity = impurity - prob_of_lbl**2
    return impurity 


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1-p) * gini(right) 

# """ 
# """Builds the tree.
# Rules of recursion: 
# 1> Believe that it works.
# 2> Start by checking for the base case (no further information gain).
# 3> Prepare for giant stack traces. """ 
#  """
def find_best_split(rows):
    best_gain = 0 
    best_question = None 
    current_uncertainty = gini(rows) 
    n_features = len(rows[0]) - 1 
    # terate over every value for the features. 
    for col in range(n_features):
        values = set([row[col] for row in rows]) 
        for val in values:

            # generate a question for that feature
            question = Question(col, val) 
            print('question is ', question)

            # partition the data on it
            true_rows, false_rows = partition(rows, question)

            # discard any questions that fail to produce a split 
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue 

            # calculate our information gain
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            print('gain is: ', gain)
            # we keep track of the best value 
            if gain >= best_gain:
                best_gain, best_question = gain, question 
        
    return best_gain, best_question 

best_gain, best_question = find_best_split(training_data) 

class Leaf:
    """A leaf node classifies data.
    This holds a dictionary of class (e.g., "Apple") -> 
    number of times it appears in the rows from the training data that reach this leaf."""
    def __init__(self, rows):
        self.predictions = class_counts(rows) 

class Decision_Node:
    """A Decision Node asks a question.
    This holds a reference to the question, and to the two child nodes.""" 
    def __init__(self, question, true_branch, false_branch):
        self.question = question 
        self.true_branch = true_branch 
        self.false_branch = false_branch 


def build_tree(rows):
    gain, question = find_best_split(rows)
    print(gain, question)
    if gain == 0:
        return Leaf(rows) 
    true_rows, false_rows = partition(rows, question) 

    true_branch = build_tree(true_rows) 
    false_branch = build_tree(false_rows) 

    return  Decision_Node(question, true_branch, false_branch) 

my_tree = build_tree(training_data)


def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return 
    print(spacing + str(node.question)) 

    print(spacing + '--> True:') 
    print_tree(node.true_branch, spacing + "  ") 

    print(spacing + '--> False:') 
    print_tree(node.false_branch, spacing + " ")



def classify(row, node):

    if isinstance(node, Leaf):
        return node.predictions 

    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch) 