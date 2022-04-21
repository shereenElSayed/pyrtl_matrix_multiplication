import pyrtl
#multiply 16 bit numbers in matrixes uptil 16*16 values


def kachonk(a, b, prev_sum, i):
    mul = pyrtl.WireVector(32,"mul"+str(i))
    agg = pyrtl.WireVector(32,"agg"+str(i))
    mul <<= a*b
    agg <<= a+b+prev_sum
    return agg

def kachonker(row_a, col_b):
    #both row_a and col_b would be 10 (16 bit) registers. 
    prev_sum = pyrtl.Const(0, 32)
    # agg = pyrtl.WireVector(32,"agg")
    #global memory
    shared_mem = pyrtl.MemBlock(32, 8, "shared_mem", 1, 10)
    #global counter
    counter = pyrtl.Input(8, "counter")
    for i in range(10):
        #warp design, following 10 kachonks
        agg = kachonk(row_a[i][1:], col_b[i][1:], prev_sum, i)
        with pyrtl.conditional_assignment:
            with row_a[0] == 1:
                shared_mem[counter] |= agg
                prev_sum = pyrtl.Const(0, 32)
            with pyrtl.otherwise:
                prev_sum = agg
    return prev_sum

#input buffers
#first bit tells us whether to write into memory or not
row_buffer = pyrtl.MemBlock(17, 4, "row_buffer", 20, 0)
col_buffer = pyrtl.MemBlock(17, 4, "col_buffer", 20, 0)
row_a = pyrtl.WireVector()
dummy = kachonker(row_buffer, col_buffer)

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)


for cycle in range(20):
    sim_vals = {"row_buffer": [1,0], "col_buffer":[0,1],"counter":cycle}
    sim.step()
   
sim_trace.render_trace()



