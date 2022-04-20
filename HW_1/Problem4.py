
import pyrtl as rtl

matrix_a = rtl.Input(bitwidth=8*2*2, name='matrix_a')
matrix_b = rtl.Input(bitwidth=8*2*2, name='matrix_b')
matrix_c = rtl.Output(bitwidth=8*2*2, name= 'matrix_c')



def flatten(l): return [val for sublist in l for val in sublist]
def elemwise_product(a, b): return [a[i] * b[i] for i in range(len(a))]
def sum_elements(a):
    sum= 0
    for i in range(0, len(a), 8):
        sum += a[i:i+8]
    return sum

def getcol (matrix, col):
    column = rtl.WireVector(bitwidth=2*8)
    n = 8
    for i in range(col*n, len(matrix), 2*n):
        column += matrix[i:i+n]
    return column

def getrow(matrix, row):
    print(type(matrix))
    return matrix[row*2*8 : row*2*8+(2*8)] 

def multiply(a, b):
    a_counter = rtl.Register(bitwidth=3, name='a_counter')
    b_counter = rtl.Register(bitwidth=3, name='b_counter')

    c = rtl.WireVector(bitwidth=2*2*8, name='c')

    #Assumed dimensions => 2X2
    with rtl.conditional_assignment:
        with a_counter == 0 :
            with b_counter == 0: #initial
                temp = elemwise_product(getrow(a, a_counter),getcol(b, b_counter))
                sum = sum_elements(temp)
                c[-1: -(2*8)] = sum # because elem 0 is at the right hand side
                b_counter.next |= b_counter+1 #Increment b so we will be able to add rows first to the result
        
        with a_counter == 2 & b_counter == 2: # Last step
            temp = elemwise_product(getrow(a, a_counter),getcol(b, b_counter))
            sum = sum_elements(temp)
            c[0:2*8] = sum

        with b_counter == 2:
            temp = elemwise_product(getrow(a, a_counter),getcol(b, b_counter))
            sum = sum_elements(temp)
            c[((a_counter*2) + b_counter)*8: (((a_counter*2) + b_counter)*8) + (2*8)] = sum
            a_counter.next |= a_counter + 1
            b_counter.next |= 0
        
        with rtl.otherwise:
            temp = elemwise_product(getrow(a, a_counter),getcol(b, b_counter))
            sum = sum_elements(temp)
            c[((a_counter*2) + b_counter)*8: (((a_counter*2) + b_counter)*8) + (2*8)] = sum
            
            b_counter.next |= b_counter+1


matrix_c <<= multiply(matrix_a, matrix_b)

a = [[1, 2], [3, 4]]
b = [[1, 0], [1, 0]]

flat_a = flatten(a)
flat_b = flatten(b)


sim_inputs = {
    'A': int(''.join([f'{i:08b}' for i in flat_a]), 2),
    'B': int(''.join([f'{i:08b}' for i in flat_b]), 2)
}
sim_trace = rtl.SimulationTrace()
sim = rtl.Simulation(tracer=sim_trace)
sim.step_multiple(sim_inputs)

for cycle in range(20):
    sim.step({})
   
sim_trace.render_trace()