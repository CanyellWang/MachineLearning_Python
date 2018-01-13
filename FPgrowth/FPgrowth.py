#!/usr/local/bin/python3
# Desc:   FP-growth algorithm for extracting the association rules
# Auther: Gunther
# Date:   2012/07/18
# Log: 
#         created by wjg, 2012/07/18

import os
import sys
import FPTree

class FPGrowth:
    def __init__(self, minsup=2):
        self.fp = []
        self.minsup = minsup
    
    def growth(self, tree, postNodes):
        if tree.isUniquePath():
            nodeCombinations = []
            tree.getCombinationFromPath(nodeCombinations)
            for combination in nodeCombinations:
                support = self._getMinSupport(combination)
                if support is None or support < self.minsup:
                    continue
                #gen pattern
                pattern = ([],support)
                for node in combination:
                    pattern[0].append(node["name"])
                for node in postNodes:
                    pattern[0].append(node)
                if len(pattern[0]) > 1:
                    self.fp.append(pattern)
                    #self._printPattern(pattern)
        else:
            for item in tree.itemTable:
                #gen pattern
                pattern = ([],tree.itemTable[item][0])
                pattern[0].append(item)
                for node in postNodes:
                    pattern[0].append(node)
                if len(pattern[0]) > 1 and pattern[1] > self.minsup: 
                    self.fp.append(pattern)  
                    #self._printPattern(pattern)
                #construct conditional pattern base
                baseSet = []
                tree.getConditionalPatternBase(item,baseSet)  
                tmpTree = FPTree.FPTree(baseSet, minsup=self.minsup) 
                tmpTree.build()
                if not tmpTree.isEmpty():
                    self.growth(tmpTree, pattern[0])       
            
    def _getMinSupport(self, nodes):
        if len(nodes) == 0:
            return None
        support = nodes[0]["support"]
        for node in nodes:
            if node["support"] < support:
                support = node["support"]
        return support
    
    def _printPattern(self, pattern):
        if len(pattern[0]) < 2:
            return
        print("*******************")
        print(pattern[0])
        print(pattern[1])
        print("*******************")   
    
def test():
    #testcase = [[["i2","i1","i5"],1],[["i2","i4"],1],[["i2","i3"],1],[["i2","i1","i4"],1],[["i1","i3"],1],[["i2","i3"],1],[["i1","i3"],1],[["i2","i1","i3","i5"],1],[["i2","i1","i3"],1]]
    testcase = [[["a","b"],1],[["b","c","d"],1],[["a","c","d","e"],1],[["a","d","e"],1],[["a","b","c"],1],[["a","b","c","d"],1],[["a"],1],[["a","b","c"],1],[["a","b","d"],1],[["b","c","e"],1]]
    #testcase = [(["i1","i2"],1),(["i3"],1)]
    tree = FPTree.FPTree(testcase,minsup=2)      
    tree.build()
    algorithm = FPGrowth(minsup=2)
    algorithm.growth(tree,[])
    res = sorted(algorithm.fp, key=lambda d:d[1], reverse = True )
    for rule in res:
        print(rule)
    
if __name__ == "__main__":
    test()    
            
        