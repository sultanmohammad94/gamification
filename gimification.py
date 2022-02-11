#%%
import pprint
from itertools import combinations, product
from functools import reduce
from operator import add


class Question:
    """This class is responsible for the questions of Gamefication system

    Methods
    ------
    setTitle(title):
        Set the title of the question
    
    getTitle():
        Return the title of the question
    
    setAnswer(answer):
        Set the text that represents the answer of the question
    
    getAnswer():
        Return the Answer of the question

    setOptions(options):
        Set the options dictionary of the question
    
    getOptions():
        Return the options dictionary of the question.    
    """
    def __init__(self, question_text, question_options):
        self.question_text = question_text
        self.question_options = question_options
        self.answer = ''
    
    def setTitle(self,question_text):
        self.question_text = question_text

    def getTitle(self):
        return self.question_text

    def setAnswer(self,answer):
        self.answer = answer

    def getAnswer(self):
        return self.answer
    
    def setOptions(self, options):
        self.question_options = options
    
    def getOptions(self):
        return self.question_options

    def __str__(self) -> str:
        return self.getTitle()

class Package:
    """This class is responsible for the Package of Gamefication system
    
    Methods
    -------
    setTitle(title):
        Set the title of the package
    
    getTitle():
        Returns the title of the package

    setToRange(value):
        Set the value of the To variable
    
    getToRange():
        Return the value of the To variable

    setFromRange(value):
        Set the value of the From variable
    
    getFromRange():
        Return the value of the From variable
    is_Valid(value):
        Return True if the value falls in the range of the package.
    """
    def __init__(self, from_range, to_range, package_title) -> None:
        self.from_range = from_range
        self.to_range = to_range
        self.package_title = package_title
        
    def setTitle(self, title):
        self.package_title = title

    def getTitle(self):
        return self.package_title

    def setToRange(self, value):
        try:
            if value > self.getFromRange():
                self.to_range = value
        except ValueError:
            print(f'>>To Value must be greater than from value')
        
    def getToRange(self):
        return self.to_range

    def setFromRange(self, value):
        try:
            if value < self.getToRange():
                self.from_range = value
        except ValueError:
            print(f'>>From Value must be less than To value')

    def getFromRange(self):
        return self.from_range

    def __str__(self) -> str:
        return self.getTitle()
    
    def is_Valid(self, value):
        '''Returns True if the value belongs to this package.'''
        if self.getFromRange() < value < self.getToRange():
            return True
        else:
            return False

class Gamefication:
    def __init__(self, gamefication_dict) -> None:
        self.gamefication_dict = gamefication_dict
    
    def setGameficationObj(self, dictionary):
        self.gamefication_dict = dictionary
    
    def getGameficationObj(self):
        return self.gamefication_dict

    def getQuestionsTitles(self):
        '''Returns a list of all Questions for the given gamification dict.
        '''
        titles = list(self.getGameficationObj().keys())
        return titles
    def getQuestionOptions(self, question_key):
        '''Returns a list of options for the specified question.
        '''
        question_options = list(self.getGameficationObj()[question_key].keys())
        return question_options

    def getQuestionComplement(self, question):
        '''Returns the complement of the question.
        '''
        questions = self.getQuestionsTitles()
        complement = [item for item in questions if item != question]
        return complement

    def getQuestionCombinations(self):
        '''Returns a list of Combinations for question`s pairs.
        '''
        questions = self.getQuestionsTitles()
        items = []
        for i, question in enumerate(questions, start = 1):
            comb = list(combinations(questions, i+1 ))
            if comb not in items and comb != []:
                items.append(comb)    
        return reduce(add, items)  

    def getCombinValue(self, comb):
        sum = 0
        for c in comb:
            for k, v in self.getGameficationObj().items():
                for sk, sv in v.items():
                    if c == sk:
                        sum += sv
        return sum

if __name__ == "__main__":
    gamification = {
        'COUNTRY':{'LEBANON': 20, 'SYRIA': 40, 'UAE': 80},
        'YEARS_OF_EXP':{'ENTRY_LEVEL': 20, 'INTERMEDIATE': 40, 'EXPERT': 80},
        'INTERNET_MEGABYTE':{'4MB': 20, '8MB': 40, '16MB': 80},
        'HOUSE_SIZE':{'SMALL': 20, 'MEDIUM': 40, 'LARGE': 80, 'VILLA': 100},
    }
    pp = pprint.PrettyPrinter(width=100, compact=True)
    gameification_obj = Gamefication(gamification)
    package_A = Package(0, 90,'A')
    package_B = Package(91, 110,'B')
    package_C = Package(111, 600,'C')
    packages = [package_A, package_B, package_C]

    questions_combins = gameification_obj.getQuestionCombinations()
    combins = []
    for pairs in questions_combins:
        option = [gameification_obj.getQuestionOptions(item) for item in pairs]
        first, *others = option
        combins.append(set(product(first, *others)))
    result = {}
    for i, combin_items in enumerate(combins):
        for j, comb in enumerate(combin_items):
            value = gameification_obj.getCombinValue(comb)
            package_title = ''
            for package in packages:
                if package.is_Valid(value):
                    package_title = package.getTitle()
                    break
            item = ('Option: {}'.format(comb), 'Cost = {} $'.format(value))
            if package_title not in list(result.keys()):
                result.update({package_title: list(item)})
            else:
                result_val = result.get(package_title)
                result_val.append(item)
                result.update({package_title: result_val})
    for k, v in result.items():
        pp.pprint(str.center(f'>>Item Package: {k},  Count = {len(v)}, Item Val = {v}', 30, '*'))
        print('\n')
