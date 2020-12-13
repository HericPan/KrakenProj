class Poly:
    def __init__(self,*terms):
        # __str__ uses the name self.terms for the dictionary of terms
        # So __init__ should build this dictionary from terms
        self.terms = dict()
        for c,p in terms:
            assert type(c) in (int, float)
            assert type(p) == int and p >=0
            assert p not in self.terms
            if c != 0:
                self.terms[p] = c
        

            
    # I have written str(...) because it is used in the bsc.txt file and
    #   it is a bit subtle to get correct. Notice that it assumes that
    #   every Poly object stores a dict whose keys are powers and whose
    #   associated values are non-zero coefficients. This function does not
    #   depend on any other method in this class being written correctly.   
    def __str__(self):
        def term(c,p,var):
            return (str(c) if p == 0 or c != 1 else '') +\
                   ('' if p == 0 else var+('^'+str(p) if p != 1 else ''))
        if len(self.terms) == 0:
            return '0'
        else:
            return ' + '.join([term(c,p,'x') for p,c in sorted(self.terms.items(),reverse=True)]).replace('+ -','- ')
  
    
    def __repr__(self):
        return "Poly(" + ",".join(str((c,p)) for p,c in self.terms.items()) + ")"
    

    def __len__(self):
        if self.terms == dict():
            return 0
        else:
            return max(self.terms.keys())
    

    def __call__(self,arg):
        answer = 0
        for p,c in self.terms.items():
            answer += c*(arg**p)
        return answer

    
    def __iter__(self):
        class Poly_iter:
            def __init__(self, d):
                self.d = d
                self.p = max(d.keys()) if self.d != dict() else -1
            def __iter__(self):
                return self
            def __next__(self):
                if self.p < 0:
                    raise StopIteration
                p = self.p
                self.p -= 1
                if p in self.d:
                    return (self.d[p], p)


        return Poly_iter(self.terms)

            
    def __getitem__(self,index):
        if type(index) != int or index < 0:
            raise TypeError("The index is illegal since it's not int or smaller than 0")
        else:
            return self.terms.get(index, 0)

            
    def __setitem__(self,index,value):
        if type(index) != int or index < 0:
            raise TypeError("The index is illegal since it's not int or smaller than 0")
        else:
            
            if value != 0:
                self.terms[index] = value
            else:
                if index in self.terms: del self.terms[index]

            
    def __delitem__(self,index):
        if type(index) != int or index < 0:
            raise TypeError("The index is illegal since it's not int or smaller than 0")
        else:
            if index in self.terms: del self.terms[index]
            
    def __eq__(self,right):
        if type(right) not in (Poly, int, float):
            raise TypeError("The two objects are not comparable.")
        else:
            if type(right) in (float, int):
                if len(self) == 0 and 0 in self.terms:
                    return self.terms[0] == right
                else:
                    return False
            else:
                return self.terms == right.terms
    
    
    def _add_term(self,c,p):
        if type(c) not in (int,float) or type(p) != int or p < 0:
            raise TypeError("The coefficient and power are illegal.")
        else:
            self[p] += c

       
    def __add__(self,right):
        if type(right) not in (Poly, int, float):
            raise TypeError("The two objects are not comparable.")
        else:
            if type(right) in (float, int):
                newP = eval(repr(self))
                newP._add_term(right,0)
                return newP
            else:
                newP = eval(repr(self))
                for p,c in right.terms.items():
                    newP._add_term(c,p)
                return newP

    
    def __radd__(self,left):
        return self.__add__(left)

    
    def __mul__(self,right):
        if type(right) not in (Poly, int, float):
            raise TypeError("The two objects are not comparable.")
        else:
            if type(right) in (float, int):
                newP = eval(repr(self))
                for p in newP.terms:
                    newP.terms[p] *= right
                return newP
            else:
                newP = Poly()
                for pl, cl in self.terms.items():
                    for pr, cr in right.terms.items():
                        newP[pl+pr] += cl*cr
                return newP

    
    def __rmul__(self,left):
        return self.__mul__(left)


    def derivative(self):
        newP = Poly()
        for p,c in self.terms.items():
            if p > 0:
                newP[p-1] = c*p
        return newP

    
    def integral(self):
        newP = Poly()
        for p,c in self.terms.items():
            if p > 0:
                newP[p+1] = c/(p+1)
            elif p == 0:
                newP[1] = c
        return newP
   



    
if __name__ == '__main__':
#     # Some simple tests; you can comment them out and/or add your own before
#     # the driver is called.
    print('Start simple tests')
    p = Poly()
    print('  Polynomial: 0 prints as')
    print('   ', str(p))
    p = Poly((3,2),(-2,1), (4,0))
    print('  Polynomial: 3x^2 - 2x + 4 prints as')
    print('   ', str(p))
    print('  Using p =', str(p))
    print('  repr(p):',repr(p))
    print('  len(p):',len(p))
    print('  p(2):',p(2))
    print('  list collecting iterator results:',[t for t in p])
    # __getitem__, __setitem__, and __delitem__ not tested here
    print('  p==p:',p==p)
    print('  p+p:',p+p)
    print('  p+2:',p+2)
    print('  p*p:',p*p)
    print('  p*2:',p*2)
    print('End simple tests\n')
#     
    import driver
    driver.default_file_name = 'bscile2S20.txt'
    #Uncomment the following lines to see MORE details on exceptions
    driver.default_show_exception=True
    driver.default_show_exception_message=True
    driver.default_show_traceback=True
    driver.driver()
