> To run this injection, you need to input
>> Filename <br>
>> The length of the time series <br>
>> The number of errorVectors <br>
>> The insert position

### main.py
`Class`: Main <br>
`Run`: **run**(benchmark)

### supervisor.py
`Class`: Supervisor <br>
This is the piloting class. It is the top moduel and manages all the other modules, including:
* Board
* Generator
* Resolver

`Run`: **launch**(benchmark) -> **launchNumberedErrors**(benchmark) -> <br> **launchNumberedErrorsCombinations**(1, benchmark) -> **launchEntriesCombinations**(1, benchmark, insertPos, 0.3) -> <br> **Generator.randomError**() & **randomNext**() -> **resolveAll**(errorVector, entryVector) -> **Resolver.resolve()** & **regsolve()**

### board.py
`Class`: Board <br>
Parse the file into a board which is usable in the program <br>
`Attributes`: inputs, outputs, wires (not INPUT), registers (DFF but out OUTPUT), ops (class Op)

#### boardError.py
`Class`: BoardError (Exception)

### op.py
`Class`: Op <br>
`Operands`: AND, NAND, OR, NOR, XOR, XNOR, NOT, DFF

### flawedOp.py
`Class`:FlawedOp <br>
`Function`: calc(modifier)

### generator.py
`Class`: Generator <br>
This generates all possible combinations of N bits <br>
`Run`: **randomNext()**, **randomError()**

### resolver.py
`Class`: Resolver <br>
`Run`: **resolve**, **regsolve**, **solve**
