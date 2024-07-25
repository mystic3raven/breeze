from breeze_lexer import lexer
from breeze_parser import parser
from breeze_codegen import CodeGenerator

data = '''
let x = 10;
fn add(a: Int, b: Int) -> Int {
    return a + b;
}
'''

# Lexing
lexer.input(data)
for tok in lexer:
    print(tok)

# Parsing
result = parser.parse(data)
print(result)

# Code Generation
codegen = CodeGenerator()
module = codegen.generate(result)
print(module)

# Compile to LLVM bytecode
with open('output.ll', 'w') as f:
    f.write(str(module))

print("LLVM IR written to output.ll")
