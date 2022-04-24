import pyrtl

def flatten(l): return [val for sublist in l for val in sublist]


def multiply_sum(a, b):
    z = pyrtl.WireVector(bitwidth=12)
    z<<=(a[:3] * b[:3]) + (a[3:] * b[3:])
    return z


def matrix_multiply(a, b):
    select = pyrtl.Register(bitwidth=2, name="select")
    out = pyrtl.Register(bitwidth=6*2*2*3, name="out")
    a_wires = pyrtl.helperfuncs.wirevector_list('row_0, row_1', bitwidth=6) 
    b_wires = pyrtl.helperfuncs.wirevector_list('col_0, col_1', bitwidth=6) 
    #Prepare wires for mux
    for row in range(2):
        # row_wire = pyrtl.WireVector(bitwidth=3*2, name=f"row_{row}")
        a_wires[row] <<= a[row*2*3 : row*2*3+(2*3)]
        # a_wires.append(row_wire)
    
    for col in range(1,-1, -1):
        print(col)
        # col_wire = pyrtl.WireVector(bitwidth=3*2, name=f"col_{col}")
        b_wires[col] <<= b[col*2*3 : col*2*3+(2*3)]
        # b_wires.append(col_wire)
    
    # res = pyrtl.WireVector(bitwidth=8, name="res")
    
    with pyrtl.conditional_assignment:
        with select == 0:
            out.next |= pyrtl.shift_left_arithmetic(multiply_sum(a_wires[1], b_wires[1]),9)
            select.next |= 1
        with select == 1:
            
            out.next |= out | pyrtl.shift_left_arithmetic(multiply_sum(a_wires[1], b_wires[0]),6)
            select.next |= 2
        with select == 2:
            out.next |= out | pyrtl.shift_left_arithmetic(multiply_sum(a_wires[0], b_wires[1]), 3)
            select.next |= 3
        with select == 3:
            out.next |= out | multiply_sum(a_wires[0], b_wires[0])
    return out


A = [1, 2, 3, 4]
B = [1, 1, 1, 1] #Assume matrix B is already inverted
flat_a = A
flat_b = B


a = pyrtl.Input(bitwidth=2*2*3, name="a")
b = pyrtl.Input(bitwidth=2*2*3, name="b")
# c = pyrtl.Output(bitwidth=3, name="c")
x = matrix_multiply(a, b)


sim_inputs = {
    'a': int(''.join([f'{i:03b}' for i in flat_a]), 2),
    'b': int(''.join([f'{i:03b}' for i in flat_b]), 2)
}

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
# sim.step_multiple(sim_inputs)

for cycle in range(5):
    sim.step(sim_inputs)
   
sim_trace.render_trace()

# Analysis

ta = pyrtl.TimingAnalysis()
print(f'Max timing delay: {ta.max_length()} ps')

print(f'Area: {sum(pyrtl.area_estimation())} mm^2')