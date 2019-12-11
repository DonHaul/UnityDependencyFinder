class Flags():
    def __init__(self):
        self.reset()

    def reset(self):
        self.inlinecomment=False
        self.multilinecomment=False
        self.constructor=False
        self.inheritance=False
        self.classdefinition=False
        self.string = False

    def detector(self,c1,c2):
        
        #flag handler
        if c1 != "\\" and c2 =='"':
            self.string = not self.string
        elif c1=="class":
            self.classdefinition=True
        elif c1=='/' and c2=='/':
            self.inlinecomment=True
        elif c1=='\n':
            self.inlinecomment=False

        elif c1== 'new':
            self.constructor = True

        elif c1== '(':
            self.constructor = False

        elif c1 == '/' and c2 == '*':
            self.multilinecomment = True       
        elif c1 == '*' and c2 == '/':
            self.multilinecomment = False

        elif c1 == ':':
            self.inheritance = True
            self.classdefinition = True
        elif c1 == '{':
            self.inheritance = False
            self.classdefinition = False