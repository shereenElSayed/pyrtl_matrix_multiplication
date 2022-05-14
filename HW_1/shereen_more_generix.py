import pyrtl

def multiply_sum(a, b, matrix_size, bits):
    z = pyrtl.WireVector(bitwidth=matrix_size*bits*2)
    if matrix_size == 3:
        z<<=(a[:bits] * b[:bits]) + (a[bits:bits*2] * b[bits:bits*2]) +\
            (a[bits*2:] * b[bits*2:])

    elif matrix_size == 4:
        z<<=(a[:bits] * b[:bits]) + (a[bits:bits*2] * b[bits:bits*2]) +\
             (a[bits*2:bits*3] * b[bits*2:bits*3]) + (a[bits*3:] * b[bits*3:])
    
    elif matrix_size == 5:
        z<<=(a[:bits] * b[:bits]) + (a[bits:bits*2] * b[bits:bits*2]) +\
             (a[bits*2:bits*3] * b[bits*2:bits*3]) + (a[bits*3:bits*4] * b[bits*3:bits*4]) \
                 + (a[bits*4:] * b[bits*4:]) 
                 

    return z

def rows_cols_names(type, size):
    string = ""
    for i in range(size-1):
        string += f"{type}_{i}, "

    string += f"{type}_{size-1}"
    return string

def matrix_multiply(a, b, size, select_size, bits ):
    maximum_element_size = bits*2
    # output_size = maximum_element_size*size*size*bits

    print(f"maximum ele size {maximum_element_size}")
    # print(f"output_size {output_size}")
    print(f"size {size}")
    print(f"select_size {select_size}")
    print(f"bits {bits}")



    out = pyrtl.Register(bitwidth=maximum_element_size, name="out")

    print(rows_cols_names("row", size))
    a_wires = pyrtl.helperfuncs.wirevector_list(rows_cols_names("row", size), bitwidth=maximum_element_size*size) 
    b_wires = pyrtl.helperfuncs.wirevector_list(rows_cols_names("col", size), bitwidth=maximum_element_size*size)

    mux_1_out = pyrtl.Register(bitwidth=maximum_element_size*size, name="mux_1_output")
    mux_2_out = pyrtl.Register(bitwidth=maximum_element_size*size, name="mux_2_output")

    #Prepare wires for mux
    print(len(a_wires))
    for row in range(size):
        print(f"rows: {row*size*bits} : {row*size*bits+(size*bits)}")
        a_wires[row] <<= a[row*size*bits : row*size*bits+(size*bits)]
    
    for col in range(size-1,-1, -1):
        b_wires[col] <<= b[col*size*bits : col*size*bits+(size*bits)]

    if size == 3:
        select_a1 = pyrtl.Register(bitwidth=select_size, name="select_a1")
        select_a2 = pyrtl.Register(bitwidth=select_size, name="select_a2")

        select_b1 = pyrtl.Register(bitwidth=select_size, name="select_b1")
        select_b2 = pyrtl.Register(bitwidth=select_size, name="select_b2")

        with pyrtl.conditional_assignment: 
            with (select_a1 == 0) & (select_b1 == 0) &\
                 (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                (select_a2 == 0) & (select_b2 == 1):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 0) & (select_b1 == 1) & \
                (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[0]
                select_b1.next |= 0
                select_a2.next |= 1

            with (select_a1 == 0) & (select_b1 == 0) &\
                 (select_a2 == 1) & (select_b2 == 0):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 1

            with (select_a1 == 0) & (select_b1 == 0) & \
                (select_a2 == 1) & (select_b2 == 1):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 0) & (select_b1 == 1) & \
                (select_a2 == 1) & (select_b2 == 0):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[0]
                select_b1.next  |= 0
                select_a2.next |= 0
                select_a1.next |= 1


            with (select_a1 == 1) & (select_b1 == 0) &\
                 (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & \
                (select_a2 == 0) & (select_b2 == 1):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 1) & (select_b1 == 1) & \
                (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[0]
                # select_b2.next  |= 0
                # select_a2.next |= 1

            out.next <<= multiply_sum(mux_1_out, mux_2_out, size, bits)
    '''elif size == 4:
        select_a1 = pyrtl.Register(bitwidth=select_size, name="select_a1")
        select_a2 = pyrtl.Register(bitwidth=select_size, name="select_a2")

        select_b1 = pyrtl.Register(bitwidth=select_size, name="select_b1")
        select_b2 = pyrtl.Register(bitwidth=select_size, name="select_b2")

        with pyrtl.conditional_assignment: 
            
            ############# Mux 1 - matrix A ##########
            with (select_a1 == 0) & (select_b1 == 0) & (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & (select_a2 == 0) & (select_b2 == 1):
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 0) & (select_b1 == 1) & (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 1
            with (select_a1 == 0) & (select_b1 == 1) & (select_a2 == 0) & (select_b2 == 1):
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[0]
                select_b2.next  |= 0
                select_b1.next  |= 0
                select_a2.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & (select_a2 == 1) & (select_b2 == 0):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & (select_a2 == 1) & (select_b2 == 1):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 0) & (select_b1 == 1) & (select_a2 == 1) & (select_b2 == 0):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 1
            with (select_a1 == 0) & (select_b1 == 1) & (select_a2 == 1) & (select_b2 == 1):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[0]
                select_b2.next  |= 0
                select_b1.next  |= 0
                select_a2.next  |= 0
                select_a1.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & (select_a2 == 0) & (select_b2 == 1):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 1) & (select_b1 == 1) & (select_a2 == 0) & (select_b2 == 0):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 1
            with (select_a1 == 1) & (select_b1 == 1) & (select_a2 == 0) & (select_b2 == 1):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[0]
                select_b2.next  |= 0
                select_b1.next  |= 0
                select_a2.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & (select_a2 == 1) & (select_b2 == 0):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & (select_a2 == 1) & (select_b2 == 1):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[2]
                select_b2.next  |= 0
                select_b1.next  |= 1
            with (select_a1 == 1) & (select_b1 == 1) & (select_a2 == 1) & (select_b2 == 0):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[1]
                select_b2.next  |= 1
            with (select_a1 == 1) & (select_b1 == 1) & (select_a2 == 1) & (select_b2 == 1):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[0]
            out.next <<= multiply_sum(mux_1_out, mux_2_out, size, bits)
    
    elif size == 5:
        select_a1 = pyrtl.Register(bitwidth=select_size, name="select_a1")
        select_a2 = pyrtl.Register(bitwidth=select_size, name="select_a2")
        select_a3 = pyrtl.Register(bitwidth=select_size, name="select_a3")

        select_b1 = pyrtl.Register(bitwidth=select_size, name="select_b1")
        select_b2 = pyrtl.Register(bitwidth=select_size, name="select_b2")
        select_b3 = pyrtl.Register(bitwidth=select_size, name="select_b3")
        with pyrtl.conditional_assignment: 
            
            ############# Mux 1 - matrix A ##########
            with (select_a1 == 0) & (select_b1 == 0) &\
                 (select_a2 == 0) & (select_b2 == 0) &\
                 (select_a3 == 0) & (select_b3 == 0):
                mux_1_out.next |= a_wires[4]
                mux_2_out.next |= b_wires[4]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 0) & \
                 (select_a3 == 0) & (select_b3 == 1)   :
                mux_1_out.next |= a_wires[4]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 1) & \
                 (select_a3 == 0) & (select_b3 == 0)   :
                mux_1_out.next |= a_wires[4]
                mux_2_out.next |= b_wires[2]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 1) & \
                 (select_a3 == 0) & (select_b3 == 1) :
                mux_1_out.next |= a_wires[4]
                mux_2_out.next |= b_wires[1]
                select_b1.next  |= 1
                select_b2.next  |= 0
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 1) & \
                 (select_a2 == 0) & (select_b2 == 0) & \
                 (select_a3 == 0) & (select_b3 == 0) :
                mux_1_out.next |= a_wires[4]
                mux_2_out.next |= b_wires[0]
                select_b1.next  |= 0
                select_a3.next |= 1
            
            with (select_a1 == 0) & (select_b1 == 0) &\
                 (select_a2 == 0) & (select_b2 == 0) &\
                 (select_a3 == 1) & (select_b3 == 0):
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[4]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 0) & \
                 (select_a3 == 1) & (select_b3 == 1)   :
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 1) & \
                 (select_a3 == 1) & (select_b3 == 0)   :
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[2]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 1) & \
                 (select_a3 == 1) & (select_b3 == 1) :
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[1]
                select_b1.next  |= 1
                select_b2.next  |= 0
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 1) & \
                 (select_a2 == 0) & (select_b2 == 0) & \
                 (select_a3 == 1) & (select_b3 == 0) :
                mux_1_out.next |= a_wires[3]
                mux_2_out.next |= b_wires[0]
                select_b1.next  |= 0
                select_a2.next |= 1
                select_a3.next |= 0

            with (select_a1 == 0) & (select_b1 == 0) &\
                 (select_a2 == 1) & (select_b2 == 0) &\
                 (select_a3 == 0) & (select_b3 == 0):
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[4]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 1) & (select_b2 == 0) & \
                 (select_a3 == 0) & (select_b3 == 1)   :
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 1) & (select_b2 == 1) & \
                 (select_a3 == 0) & (select_b3 == 0)   :
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[2]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 1) & (select_b2 == 1) & \
                 (select_a3 == 0) & (select_b3 == 1) :
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[1]
                select_b1.next  |= 1
                select_b2.next  |= 0
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 1) & \
                 (select_a2 == 1) & (select_b2 == 0) & \
                 (select_a3 == 0) & (select_b3 == 0) :
                mux_1_out.next |= a_wires[2]
                mux_2_out.next |= b_wires[0]
                select_b1.next  |= 0
                select_a3.next |= 1
            
            with (select_a1 == 0) & (select_b1 == 0) &\
                 (select_a2 == 1) & (select_b2 == 0) &\
                 (select_a3 == 1) & (select_b3 == 0):
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[4]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 1) & (select_b2 == 0) & \
                 (select_a3 == 1) & (select_b3 == 1)   :
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 1) & (select_b2 == 1) & \
                 (select_a3 == 1) & (select_b3 == 0)   :
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[2]
                select_b3.next  |= 1
            with (select_a1 == 0) & (select_b1 == 0) & \
                 (select_a2 == 1) & (select_b2 == 1) & \
                 (select_a3 == 1) & (select_b3 == 1) :
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[1]
                select_b1.next  |= 1
                select_b2.next  |= 0
                select_b3.next  |= 0
            with (select_a1 == 0) & (select_b1 == 1) & \
                 (select_a2 == 1) & (select_b2 == 0) & \
                 (select_a3 == 1) & (select_b3 == 0) :
                mux_1_out.next |= a_wires[1]
                mux_2_out.next |= b_wires[0]
                select_b1.next |= 0
                select_a1.next |= 1
                select_a2.next |= 0
                select_a3.next |= 0
            
            
            with (select_a1 == 1) & (select_b1 == 0) &\
                 (select_a2 == 0) & (select_b2 == 0) &\
                 (select_a3 == 0) & (select_b3 == 0):
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[4]
                select_b3.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 0) & \
                 (select_a3 == 0) & (select_b3 == 1)   :
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[3]
                select_b2.next  |= 1
                select_b3.next  |= 0
            with (select_a1 == 1) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 1) & \
                 (select_a3 == 0) & (select_b3 == 0)   :
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[2]
                select_b3.next  |= 1
            with (select_a1 == 1) & (select_b1 == 0) & \
                 (select_a2 == 0) & (select_b2 == 1) & \
                 (select_a3 == 0) & (select_b3 == 1) :
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[1]
                select_b1.next  |= 1
                select_b2.next  |= 0
                select_b3.next  |= 0
            with (select_a1 == 1) & (select_b1 == 1) & \
                 (select_a2 == 0) & (select_b2 == 0) & \
                 (select_a3 == 0) & (select_b3 == 0) :
                mux_1_out.next |= a_wires[0]
                mux_2_out.next |= b_wires[0]
                
            
            out.next <<= multiply_sum(mux_1_out, mux_2_out, size, bits)
        '''

matrix_dimension = 3
bits_per_element = 3
select_bits_size = 2
#Assume matrix B is already inverted
A = [0, 1, 2, 3, 4, 5, 6, 7, 0]
B = [1, 0, 0, 0, 1, 0, 0, 0, 1]

# 4x4
# A = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]
# B = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

# 5x5
# A = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
# B = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]

# flat_a = A
# flat_b = B


a = pyrtl.Input(bitwidth=matrix_dimension*matrix_dimension*bits_per_element, name="a")
b = pyrtl.Input(bitwidth=matrix_dimension*matrix_dimension*bits_per_element, name="b")
# c = pyrtl.Output(bitwidth=3, name="c")
x = matrix_multiply(a, b, matrix_dimension, select_bits_size, bits_per_element)


sim_inputs = {
    'a': int(''.join([f'{i:03b}' for i in A]), 2),
    'b': int(''.join([f'{i:03b}' for i in B]), 2)
}

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
# sim.step_multiple(sim_inputs)

for cycle in range(60):
    sim.step(sim_inputs)
   
sim_trace.render_trace(symbol_len=20)

# Analysis

ta = pyrtl.TimingAnalysis()
print(f'Max timing delay: {ta.max_length()} ps')

print(f'Area: {sum(pyrtl.area_estimation())} mm^2')
            
        
