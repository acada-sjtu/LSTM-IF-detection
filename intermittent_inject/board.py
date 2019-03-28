from op import *
from flawedOp import *
from resolver import *


def wire_sort(wire, inputs, registers, gate_struct):
    global wires_sequence
    print wire
    if wires_sequence[wire] != -1:
        return wires_sequence[wire]
    if wire in inputs:
        wires_sequence[wire] = 0
    else:
        sort_list = []
        for item in gate_struct[wire]:
            if item in inputs:
                wires_sequence[wire] = 0
                break
            elif item in registers:
                sort_list.append(dff_sort(item, inputs, registers, gate_struct))
            else:
                sort_list.append(wire_sort(item, inputs, registers, gate_struct))
        wires_sequence[wire] = min(sort_list)
        print min(sort_list)
    return wires_sequence[wire]


def dff_sort(dff, inputs, registers, gate_struct):
    global wires_sequence
    if wires_sequence[dff] != -1:
        return wires_sequence[dff]

    if (gate_struct[dff][0] in inputs):
        wires_sequence[dff] = 1
    elif gate_struct[dff][0] in registers:
        wires_sequence[dff] = dff_sort(gate_struct[dff][0], inputs, registers, gate_struct) + 1
    else:
        wires_sequence[dff] = wire_sort(gate_struct[dff][0], inputs, registers, gate_struct) + 1
    return wires_sequence[dff]


class gate_struct:
    def __init__(self):
        self.gate_dic = {}


class Board:
    """
    This aims to translate the .v file to something usable in the program.
    """

    def __init__(self, path, isFlawed=False):
        gate = gate_struct()
        file = open(path, "rU")
        inputs = ""
        outputs = ""
        self.wires = []
        self.registers = []
        line = ""
        self.ops = {}
        self.isFlawed = isFlawed
        global wires_sequence
        wires_sequence = dict()

        while line.find("input ") < 0:
            line = file.readline()
        while line != "\n" and line.find("output ") < 0:
            inputs += line.strip()
            line = file.readline()
        # getting rid of input keyword and semicolon
        inputs = inputs[6:len(line) - 2]
        self.inputs = inputs.split(",")
        # if not self.isFlawed:
        print "inputs: ", self.inputs
        print "input:" + str(len(self.inputs)) + "\n"
        while 1:
            line = file.readline()
            if not line:
                break
            if line.find('output')>=0:
                outputs += line.strip()
                # getting rid of output keyword and semicolon
                outputs = outputs[7:len(line) - 2]
                self.outputs = outputs.split(",")
                print "outputs: ", self.outputs
                continue

            if line != "\n" and line != "":
                #print line
                info = line.replace(')', '').split(" = ")
                out = info[0]
                if (out not in self.inputs):
                    self.wires.append(out)
                rightpart = info[1].split("(")
                which = rightpart[0]  # NAND AND NOT OR DFF
                # print which
                if which == "DFF":
                    if (out != "") and (out not in self.outputs):
                        self.registers.append(out)
                ins = []
                rightop = rightpart[1].replace(',', '').replace('\n', '').split(" ")

                for op in rightop:
                    ins.append(op)

                if self.isFlawed:
                    newOp = FlawedOp(which, ins)
                else:
                    # print("which is :", which,"ins :", ins)
                    newOp = Op(which, ins)
                self.ops[out] = newOp
            
    
        if not self.isFlawed:
            # print("wires: ", self.wires)
            print len(self.wires)
            # print("registers: ", self.registers)
            print("# of registers:", len(self.registers), self.registers)
            #print("ops: ",self.ops)
        for wire in self.wires:
            wires_sequence[wire] = -1    
