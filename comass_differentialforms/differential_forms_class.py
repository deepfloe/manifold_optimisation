from bubble_sort_signed import bubble_sort_signed
import copy

class Form:
    '''Class for differential forms on R^n, supports wedge product and contraction.
    :attribute dict_components: a dictionary representing the components of the differential forms with multiplicity. For example {(0,1,2):4,(1,3,4):-2} represents the differential form
    4 dx_0 ^ dx_1 ^ dx_2 - 2 dx_1 ^ dx_3 ^ dx_4.

    '''
    def __init__(self,dict_components):
        if len(dict_components) == 0:
            self.degree = -1
        else:
            #set degree attribute:
            degrees = list(map(len, dict_components.keys()))
            if not all(x == degrees[0] for x in degrees):
                raise AssertionError('All forms must be of equal degree')
            self.degree = degrees[0]
            #set summands attribute:
        self.summands = {}
        for summand in dict_components.items():
            self.add_summand(summand)

    def set_degree(self,d):
        '''Sets the degree of a Form instance to d if non-empty, otherwise to -1.'''
        if self.summands == {}:
            self.degree = -1
        else:
            self.degree = d

    def add_summand(self, summand, is_sorted = False):
        '''Adds a new summand to a Form object, manipulates self.
        :param summand is a tuple of a multi-index and multiplicity. For example ((1,2,3),6)
        :param is_sorted Boolean if the multi-index of summand is already sorted in increasing order.
        For example, this is case if summand is an entry of a Form and specifying is_sorted = True saves computation time.

        Example: a = Form({(1,2,3):4,(1,2,4):-1}), summand = ((1,2,3),-4). Then a.add_summand(summand) turns a into Form({(1,2,4):-1})
        '''
        multi_ind, multiplicity = summand
        if is_sorted:
            sign = +1
        else:
            multi_ind, sign = bubble_sort_signed(multi_ind)
        if sign != 0:
            if multi_ind in self.summands.keys():
                sum = self.summands[multi_ind] + sign * multiplicity
                if sum == 0:
                    del self.summands[multi_ind]
                else:
                    self.summands[multi_ind] = sum
            else:
                self.summands[multi_ind] = sign * multiplicity


    def __add__(self, other):
        '''Adding two forms, deleting entries with zero multiplicity.'''
        assert self.degree == other.degree or self.degree == -1 or other.degree == -1
        result = Form(copy.deepcopy(self.summands))
        for summand in other.summands.items():
            result.add_summand(summand,is_sorted=True)
        return result

    def __mul__(self, other):
        '''Abusing notation, this is operand used for wedge products of forms.'''
        wedged_summands = Form({})
        for index1, mult1 in self.summands.items():
            for index2, mult2 in other.summands.items():
                index = index1+index2
                multiplicity = mult1 * mult2
                summand = index, multiplicity
                wedged_summands.add_summand(summand)
        if wedged_summands.summands != {}:
            wedged_summands.degree = self.degree * other.degree

        return wedged_summands

    def contract(self,subspace):
        '''Contract a subspace with a Form, returning a form of lower degree. Also known as interior         product in differential geometry.
        :param subspace a two-dimensional numpy array
        :return Form object, the interior product of self with the subspace
        '''
        def contract_single_vec(form, v):
            result = Form({})
            if form.degree < 1:
                return result

            for multi_ind, mult in form.summands.items():
                for i,j in enumerate(multi_ind):
                    if v[j] != 0:
                        index_without_i = multi_ind[:i] + multi_ind[i + 1:]
                        result.add_summand((index_without_i, (-1)**i*mult*v[j]), is_sorted=True)

            result.set_degree(form.degree-1)
            return result

        result = Form(copy.deepcopy(self.summands))
        for v in subspace:
            result = contract_single_vec(result,v)
        return result

    def numpy_float(self):
        '''Converts a Form of degree -1 or 0 into float or numpy_float, which is useful for the manopt package.'''
        if self.degree > 0:
            raise ValueError('Cannot convert a form of positive degree into a float')
        elif self.degree == 0:
            return self.summands[()]
        else:
            return 0.0

    def __float__(self):
        return float(self.numpy_float())


    def __str__(self):
        return str(self.summands)

if __name__ == '__main__':
    a = Form({(0,1):1})
    subspace = [[0.3,1],[5.1,8]]
    b = float(a.contract(subspace))
    print(b)
