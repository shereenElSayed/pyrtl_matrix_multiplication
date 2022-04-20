import pyrtl
#multiply 16 bit numbers in matrixes uptil 16*16 values

#global memory
shared_mem = pyrtl.MemBlock(32, 8, "shared_mem", 1, 10)
#global counter
counter = pyrtl.Register(8, "counter")
#input buffers
row_buffer = pyrtl.MemBlock(16, 4, "row_mem", 10, 0)
col_buffer = pyrtl.MemBlock(16, 4, "col_mem", 10, 0)

def kachonk(a, b, prev_sum):
    mul = pyrtl.WireVector(32,"mul")
    agg = pyrtl.WireVector(32,"agg")
    mul <<= a*b
    #to aggregate or to sum
    with pyrtl.conditional_assignment:
        with prev_sum != 0: #agg value exists
            agg |= prev_sum + a + b #aggregate new values
        with prev_sum == 0: #agg value doesn't exist
            agg |= a+b #aggregate current values
    return agg

def kachonker(row_a, col_b, w_mem):
    #both row_a and col_b would be 10 (16 bit) registers. 
    prev_sum = pyrtl.WireVector(16,"prev_sum")
    for i in range(10):
        #warp design, following 10 kachonks
        counter.next <<= counter + 1
        with pyrtl.conditional_assignment:
            with w_mem == 1:
                shared_mem[counter] |= kachonk(row_a[i], col_b[i], prev_sum)
                prev_sum |= pyrtl.Const(0, 32)
            with pyrtl.otherwise:
                prev_sum |= kachonk(row_a[i], col_b[i], prev_sum)
    




