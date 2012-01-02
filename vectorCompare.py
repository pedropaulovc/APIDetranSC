'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

import math

class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for _, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))