from board import *
from generator import *
from analyst import *
import flawedOp
import random

class Supervisor:
    """
    This is the piloting class, it manages all the other module and is the top one.
    """

    def __init__(self, file, modifier="00", q=0.5, klim=[-1, -1]):
        """
        If modifier is '01', stuck-at-one is activated.
        If mofifier is '10', stuck-at-zero is activated.
        If modifier is '00', no stuck is activated.

        klim aim to delimitate the number of injected error
        klim must be formatted like [kmin, kmax]
        """
        # boards
        self.rBoard = Board(file)
        print ("ops",len(self.rBoard.ops))
        self.fBoard = Board(file, True)
        # constants
        self.N = len(self.rBoard.inputs)  # input size
        self.P = len(self.rBoard.outputs)  # output size
        self.M = FlawedOp.count  # flawed nodes number
        print ("M",self.M)
        # tools, ref and flaw
        self.rResolver = Resolver(self.rBoard)
        self.fResolver = Resolver(self.fBoard)
        self.rGenerator = Generator(self.N)
        self.fGenerator = Generator(self.M)
        # counts
        self.entryCount = 0
        self.errorCount = 0
        self.error_count = 0 #num of difference during a period
        # the modifier
        self.modifier = modifier
        # the limits for errors
        self.limits = []
        self.insertion_map = {'f':0, 'm':0.4, 'e':0.6}
        self.valid_sample = 0
       
        if klim == [-1, -1]:
            self.limits = []
            self.limits.append(0)
            self.limits.append(self.M + 1)
            # self.limits.append(1)
        else:
            self.limits = klim
            # the analyst
            # self.analyst = Analyst(self.N, self.P, self.M, self.limits, q)

    def reset_resolver(self):
        self.rResolver.reset()
        self.fResolver.reset()

    def launch(self):
        self.rGenerator.reset()
        randomnum = 1#input("\nPlease input number of combinations.\n")
        length = input("\Please input how long do you want to run?\n")
        self.randomnum = int(randomnum)
        self.length = int(length)

        self.launchNumberedErrors()



        # print(self.errorCount, " different errors considered")
        # print(self.entryCount, " combinations tested")
        # print("The board reliability is ", self.analyst.compute())

    def launchNumberedErrors(self):
        ##        print ("selfi.limits0",self.limits[0])
        ##        print ("self.limits1",self.limits[1])
        ##        for k in range(self.limits[0], self.limits[1]):
        ##            self.launchNumberedErrorsCombinations(k)
        errorCount = input("\nPlease type the number of errorVectors you want to simulate \n\n>")
        self.errorCount = int(errorCount)
        singleError = 'y'#raw_input("\nSingle fault or not? ")
        if singleError == "y":
            self.launchNumberedErrorsCombinations(1)
        else:
            self.launchNumberedErrorsCombinations(self.limits[1] - 1)

    def launchNumberedErrorsCombinations(self, k):
        recur = 0
        benchmark = 'b10'
        insertionPos = 'f'
        error_ratio = 0.3
        fin = open('inputdata_%s_%s_%.1f'%(benchmark, insertionPos,error_ratio), 'a+')
        lines = len(fin.readlines())
        self.valid_sample = lines / self.length
        fin.close()
        while self.valid_sample < self.errorCount:
            recur += 1
            self.fGenerator.reset()
            #errorVector = self.fGenerator.randomError(k,i)
            self.launchEntriesCombinations(k, benchmark, insertionPos, error_ratio)
            print "recur:", recur, "# of valid sample:", self.valid_sample

    def launchEntriesCombinations(self, k, benchmark, insertionPos='f',error_ratio=0.3):
        begin_cycle = self.length * self.insertion_map[insertionPos] 
        #print ("begin cycle",begin_cycle)
        for self.entryCount in range(self.randomnum):
            self.reset_resolver()
            self.fin_write = []
            self.ferror_write = []
            self.flipped_write = []
            self.affected_write = []
            self.error_count = 0
            fin = open('inputdata_%s_%s_%.1f'%(benchmark, insertionPos, error_ratio), 'a+')
            ferror = open('inputerror_%s_%s_%.1f'%(benchmark, insertionPos, error_ratio), 'a+')
            flipped = open('flipped_%s_%s'%(benchmark, insertionPos), 'a+')
            affected = open('affected_%s_%s'%(benchmark, insertionPos), 'a+')
            for i in xrange(self.length):
                if i>=begin_cycle and i<begin_cycle+error_ratio*self.length and random.randint(0,1)==1:
                    errorVector = self.fGenerator.randomError(k,random.randint(0,self.M))
                else:
                    self.fGenerator.reset()
                    errorVector = self.fGenerator.randomError(0)
                self.flipped_write.append(' '.join(errorVector) + '\n')
                #print errorVector
                entryVector = self.rGenerator.randomnext()
                if i==0:
                    self.resolveAll(errorVector, entryVector, 0)
                else:
                    self.resolveAll(errorVector, entryVector, 1)
            print "error_count: ", self.error_count
            #print 'LLL: ', self.length
            if self.error_count >= 0.1*self.length:
                self.valid_sample += 1
                fin.writelines(self.fin_write)
                ferror.writelines(self.ferror_write)
                flipped.writelines(self.flipped_write)
                affected.writelines(self.affected_write)
            else:
                fin.close()
                ferror.close()
                flipped.close()
                affected.close()
                break
            fin.close()
            ferror.close()
            flipped.close()
            affected.close()

    def resolveAll(self, errorVector, entryVector, length=1):
        # get input

        inputs = {}
        i = 0
        
        """
        print for test start
        """

        """
        print for test end
        """

        for input in self.rBoard.inputs:
            inputs[input] = int(entryVector[i])
            i += 1
            #self.fin_write.append(str(inputs[input])+' ')
            #self.ferror_write.append(str(inputs[input])+' ')

            # fin.write(str(inputs[input]))
            # fin.write(' ')
            # ferror.write(str(inputs[input]))
            # ferror.write(' ')

        # get reference output
        rvector = ""
        i = 0
        outputint = 0
        rOutputs = self.rResolver.resolve(inputs)
        regValue = {}
        # print("length of regValue = ", len(regValue),"\n")
        for reg in self.rBoard.wires:
            regValue[reg] = self.rResolver.regsolve(reg, inputs)
        for regv in self.rBoard.registers:
            self.fin_write.append(str(regValue[regv])+' ')

        # fright = open('right.txt','a')
        # for rOutput in rOutputs:
            # rvector += str(rOutputs[rOutput])
            # outputint += (int(rOutputs[rOutput])) * (2 ** i)
            # i += 1
            # self.fin_write.append(str(rOutputs[rOutput])+' ')
            # fin.write(str(rOutputs[rOutput]))
            # fin.write(' ')
        # fin.write(str(outputint+1))
        self.fin_write.append('\n')

        # get flawed output
        fvector = ""
        fOutputs = self.fResolver.resolve(inputs, errorVector, self.modifier)
        regError = {}
        for reg in self.fBoard.wires:
            regError[reg] = self.fResolver.regsolve(reg, inputs, errorVector, self.modifier)
        # register error count
        for regv in self.fBoard.registers:
            if regError[regv]!=regValue[regv]:
                self.error_count += 1
                self.affected_write.append(str(1)+' ')
            else:
                self.affected_write.append(str(0)+' ')
            self.ferror_write.append(str(regError[regv])+' ')

        #output error count
        # for fOutput in fOutputs:
            # if fOutputs[fOutput] != rOutputs[fOutput]:
                # self.error_count += 1
            # self.ferror_write.append(str(fOutputs[fOutput])+' ')
        ##			fvector += str(fOutputs[fOutput])
        ##		ferror.write(fvector)
        self.affected_write.append('\n')
        self.ferror_write.append('\n')

        # register it to the analyser
        # self.analyst.push(errorVector, entryVector, rvector, fvector)

