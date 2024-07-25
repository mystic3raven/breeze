from llvmlite import ir

class CodeGenerator:
    def __init__(self):
        self.module = ir.Module(name="breeze_module")
        self.builder = None
        self.funcs = {}
        self.locals = {}

    def generate(self, node):
        self.visit(node)
        return self.module

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Let(self, node):
        var_name = node.identifier
        var_type = ir.IntType(32)
        var_value = self.visit(node.expression)
        var_alloca = self.builder.alloca(var_type, name=var_name)
        self.builder.store(var_value, var_alloca)
        self.locals[var_name] = var_alloca

    def visit_Var(self, node):
        var_name = node.identifier
        var_type = ir.IntType(32)
        var_value = self.visit(node.expression)
        var_alloca = self.builder.alloca(var_type, name=var_name)
        self.builder.store(var_value, var_alloca)
        self.locals[var_name] = var_alloca

    def visit_Function(self, node):
        func_name = node.name
        func_type = ir.FunctionType(self.get_llvm_type(node.return_type), [self.get_llvm_type(param.type) for param in node.params])
        func = ir.Function(self.module, func_type, name=func_name)
        self.funcs[func_name] = func
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        for param, llvm_param in zip(node.params, func.args):
            llvm_param.name = param.name
            alloca = self.builder.alloca(llvm_param.type, name=param.name)
            self.builder.store(llvm_param, alloca)
            self.locals[param.name] = alloca
        for statement in node.body:
            self.visit(statement)
        self.builder.ret(self.builder.load(self.locals[node.body[-1].identifier]))

    def visit_GpuFunction(self, node):
        func_name = node.name
        func_type = ir.FunctionType(self.get_llvm_type(node.return_type), [self.get_llvm_type(param.type) for param in node.params])
        func = ir.Function(self.module, func_type, name=func_name)
        self.funcs[func_name] = func
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        for param, llvm_param in zip(node.params, func.args):
            llvm_param.name = param.name
            alloca = self.builder.alloca(llvm_param.type, name=param.name)
            self.builder.store(llvm_param, alloca)
            self.locals[param.name] = alloca
        for statement in node.body:
            self.visit(statement)
        self.builder.ret(self.builder.load(self.locals[node.body[-1].identifier]))

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == '+':
            return self.builder.add(left, right, name="addtmp")
        elif node.op == '-':
            return self.builder.sub(left, right, name="subtmp")
        elif node.op == '*':
            return self.builder.mul(left, right, name="multmp")
        elif node.op == '/':
            return self.builder.sdiv(left, right, name="divtmp")

    def visit_Number(self, node):
        return ir.Constant(ir.IntType(32), node.value)

    def visit_String(self, node):
        return ir.Constant(ir.IntType(8).as_pointer(), node.value)

    def visit_Bool(self, node):
        return ir.Constant(ir.IntType(1), node.value)

    def visit_Identifier(self, node):
        return self.builder.load(self.locals[node.name], name=node.name)

    def get_llvm_type(self, type_name):
        if type_name == "Int":
            return ir.IntType(32)
        elif type_name == "Float":
            return ir.FloatType()
        elif type_name == "String":
            return ir.IntType(8).as_pointer()
        elif type_name == "Bool":
            return ir.IntType(1)
        elif type_name == "Void":
            return ir.VoidType()
        # Add more type mappings as needed
        raise Exception(f"Unknown type: {type_name}")

# Test the code generator
from breeze_parser import parser

data = '''
let x = 10;
fn add(a: Int, b: Int) -> Int {
    return a + b;
}
'''

result = parser.parse(data)
codegen = CodeGenerator()
module = codegen.generate(result)
print(module)
