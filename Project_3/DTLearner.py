"""Decision Tree Learner
Python 3.6
CS7646 Project 3
Mike Tong (mtong31)
"""
import pandas as pd
import numpy as np

class DTLearner(object):
    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.dataframe = None
        self.tree = None
    
    def author(self):
        return('mtong31')
        
    def get_dataframe(self):
        return(self.dataframe)
        
    def get_tree(self):
        return(self.tree)
        
    def addEvidence(self, Xtrain, Ytrain):
        """Accepts inputs (Xtrain) and outputs (Ytrain) and calls the build_tree function on the data, updates the tree attribute"""
        dataframe = pd.DataFrame(Xtrain)
        dataframe['Y'] = Ytrain.reshape(len(Ytrain),1)
        
        self.data = dataframe
        self.tree = self.build_tree(dataframe)
        self.query_tree = self.tree.copy()
            
    def highest_correlation(self, df):
        """Returns the highest correlated feature by its index value"""
        correlations = np.tril(np.array(df.corr()), k=-1) # takes the lower half of the correlation table without the diagonal.
        return(abs(np.nan_to_num(correlations[-1])).argmax())
    
    def split_val(self, df):
        """Acceptes a df and returns (best_feature, value to split on)"""
        best_feature = self.highest_correlation(df)
        column = df.iloc[:, best_feature]
        return best_feature, column.median()
    
    def build_tree(self, data):         
        """Recursively build's a tree by returning arrays in the form [feature, split value, less than index, greater than index]
        leaf values are denoted as feature == -1"""   
        
        if data.shape[0] <= self.leaf_size or len(pd.unique(data.iloc[:,-1])) == 1:
            return(np.array([-1, data.iloc[np.random.choice(range(data.shape[0])), -1], np.nan, np.nan]).reshape(1,4))
        
        else:
            best_feature, split_val = self.split_val(data)
            
            # when split_val does not separate a feature, it will iterate forever, bandaid fix with min
            if data[best_feature].shape[0] == data[data[best_feature] <= split_val].shape[0]:
                split_val = data[best_feature].min()
                
            left_tree  = self.build_tree(data[data.iloc[:, best_feature] <= split_val])
            right_tree = self.build_tree(data[data.iloc[:, best_feature] > split_val])
            root = [best_feature, split_val, 1, left_tree.shape[0] + 1]   
            temp_tree = np.vstack([root, left_tree, right_tree])
            return(temp_tree)
#    
    def query_value(self, values):
        """Queries a single list of values, returns the output of the tree"""
        current_pos = 0
        while True:
            tree_pos = self.tree[current_pos]
            if current_pos > self.tree.shape[0]: 
                return('Error querying value')
            elif int(tree_pos[0]) == -1: 
                return(tree_pos[1])            
            elif values[int(tree_pos[0])] <= tree_pos[1]: 
                current_pos += 1
            else: 
                current_pos += int(tree_pos[3]) 
            
    def query(self,Xtest):
        """Given an input (Xtest), returns the associated query output(s), can accept arrays"""
        try: # assumes multiple test values
            return([self.query_value(i) for i in Xtest])
                
        except:
            return([self.query_value(Xtest)])
        
        

## recursive method below is much slower (~3x), but objectively prettier
#    def query_value(self, xval):
#        if self.query_tree[0][0] == -1:
#            ans = self.query_tree[0][1]
#            self.query_tree = self.tree.copy()
#            return ans
#        
#        elif self.query_tree[0][1] >= xval[int(self.query_tree[0][0])]:
#            self.query_tree = self.query_tree[int(self.query_tree[0][2]):]
#            return(self.query_value(xval))
#            
#        elif self.query_tree[0][1] < xval[int(self.query_tree[0][0])]:
#            self.query_tree = self.query_tree[int(self.query_tree[0][3]):]
#            return(self.query_value(xval))
#            
#    def query(self, queries):
#        try:
#            return([self.query_value(q) for q in queries])
#        except:
#            return([self.query_value(queries)])
            
#import os
#os.chdir("/home/mike/OMCS/CS7646-ML For Trading/CS7646_Assignments/data/decision_tree_data")
#test = pd.read_csv('Istanbul.csv', index_col='date')
#test = test.rename(columns={x:y for x,y in zip(test.columns, range(len(test.columns)))})
#test = np.array(test)
#x = test[:,:-1]
#y = test[:,-1]
#learner = DTLearner(1)
#t = learner.addEvidence(x,y)
#a = learner.query(x)
#print(a)

test = np.array([
        [0.61, 0.63, 8.4, 3],
        [0.885, 0.33, 9.1, 4],
        [0.56, 0.5, 9.4, 6],
        [0.735, 0.57, 9.8, 5],
        [0.32, 0.78, 10, 6],
        [0.26, 0.63, 11.8, 8],
        [0.5, 0.68, 10.5, 7],
        [0.725, 0.39, 10.9, 5],
    ])

learner = DTLearner(1)
x = test[:,0:-1]
y = test[:, -1]
test = learner.addEvidence(x, y)
print(learner.tree)
a=learner.query(x)
print(a)