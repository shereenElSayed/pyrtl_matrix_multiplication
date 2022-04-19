
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

def multiply(a, b):
    a_counter = rtl.Register(bitwidth=3, name='a_counter')
    b_counter = rtl.Register(bitwidth=3, name='b_counter')

    c = rtl.WireVector(bitwidth=2*2*8, name='c')

    #Assumed dimensions => 2X2
    with rtl.conditional_assignment:
        with a_counter == 0 & b_counter == 0: #initial
                temp = elemwise_product(a[:(2*8)], b[:(2*8)])
                sum = sum_elements(temp)
                c[a_counter][b_counter] = temp
                a_counter.next |= a_counter+1
        
        with a_counter == 2 & b_counter == 2: # Last step
            temp = sum(a[a_counter] * b[b_counter])
            c[a_counter][b_counter] = temp

        with a_counter == 2:
            temp = sum(a[a_counter] * b[b_counter])
            c[a_counter][b_counter] = temp
            a_counter.next |= 0
            b_counter.next |= b_counter+1
        
        with rtl.otherwise:
            temp = sum(a[a_counter] * b[b_counter])
            c[a_counter][b_counter] = temp
            a_counter.next |= a_counter+1

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


for cycle in range(20):
    sim.step({})
   
sim_trace.render_trace()