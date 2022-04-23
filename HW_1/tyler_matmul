import pyrtl as rtl
import numpy as np


def flatten(l): return [val for sublist in l for val in sublist]
def get_col(x, c): return [x[r][c] for r in range(len(x))]
def elemwise_product(a, b): return [a[i] * b[i] for i in range(len(a))]


def matmul(A, B, rows_a: int, cols_a: int, rows_b: int, cols_b: int, bitwidth: int):
    assert cols_a == rows_b, 'Invalid dimensions'

    row_a = cols_a * bitwidth
    row_b = cols_b * bitwidth

    a = [[rtl.WireVector(bitwidth, f'a({r}, {c})')
          for c in range(cols_a)] for r in range(rows_a)]

    b = [[rtl.WireVector(bitwidth, f'b({r}, {c})')
          for c in range(cols_b)] for r in range(rows_b)]

    result = []

    for r in range(rows_a):
        for c in range(cols_a):
            # print(f'({r}, {c})')
            # print(row_a * r + col * c, row_a * r + col * (c + 1))
            # print(A[row_a * r + col * c: row_a * r + col * (c + 1)])
            # print(a[r][c])
            a[r][c] <<= A[row_a * r + bitwidth * c:
                          row_a * r + bitwidth * (c + 1)]

    for r in range(rows_b):
        for c in range(cols_b):
            b[r][c] <<= B[row_b * r + bitwidth * c:
                          row_b * r + bitwidth * (c + 1)]

    for r in range(rows_a):
        for c in range(cols_b):
            ew_product = elemwise_product(a[r], get_col(b, c))

            # elemwise_0 = rtl.WireVector(bitwidth, f'elemwise_({r},{c})[0]')
            # elemwise_0 <<= elemwise_product(a[r], get_col(b, c))[0]
            # elemwise_1 = rtl.WireVector(bitwidth, f'elemwise_({r},{c})[1]')
            # elemwise_1 <<= elemwise_product(a[r], get_col(b, c))[1]

            s = rtl.WireVector(bitwidth, f'res({r}, {c})')
            s <<= sum(ew_product)

            result.append(s)

    return rtl.concat_list(result)


# r = [[rtl.WireVector(bitwidth, f'r({r}, {c})')
#       for c in range(col_r)] for r in range(row_r)]

# for rw in range(row_r):
#     for cl in range(col_r):
#         # print(f'r({r}, {c})')
#         r[rw][cl] <<= result[row_r * rw + col_r * cl:
#                              row_r * rw + bitwidth * (cl + 1)]


## 2x2 ##

# A = [
#     [1, 2],
#     [3, 4]
# ]

# B = [
#     [1, 0],
#     [0, 1]
# ]

## 3x3 ##

# A = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]

# B = [
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1]
# ]

## 4x4 ##

A = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [8, 7, 6, 5],
    [4, 3, 2, 1]
]

B = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

## 2x3 * 3x2 ##

# A = [
#     [0, 2, 3],
#     [7, 2, 1]
# ]

# B = [
#     [1, 2],
#     [1, 2],
#     [1, 2]
# ]

flat_a = flatten(A)
flat_b = flatten(B)

row_r, col_r, bitwidth = len(A), len(B[0]), 8

a = rtl.Input(len(A) * len(A[0]) * bitwidth, 'A')
b = rtl.Input(len(B) * len(B[0]) * bitwidth, 'B')

result = rtl.WireVector(row_r * col_r * bitwidth, 'result')
result <<= matmul(a, b, len(A), len(A[0]), len(B), len(B[0]), bitwidth)


sim_trace = rtl.SimulationTrace()
sim = rtl.Simulation(tracer=sim_trace)

# sim_inputs = {
#     'A': [int(''.join([f'{i:08b}' for i in flat_a]), 2)] * 10,
#     'B': [int(''.join([f'{i:08b}' for i in flat_b]), 2)] * 10
# }

# sim.step_multiple(sim_inputs)

sim_inputs = {
    'A': int(''.join([f'{i:08b}' for i in flat_a]), 2),
    'B': int(''.join([f'{i:08b}' for i in flat_b]), 2)
}

for cycle in range(5):
    sim.step(sim_inputs)
    # assert sim.value[result] == sim_inputs['A']  # Only for multiplying by identity matrix

sim_trace.render_trace()

# with open('vis.txt', 'w') as f:
#     rtl.output_to_graphviz(f)


# Analysis

ta = rtl.TimingAnalysis()
print(f'Max timing delay: {ta.max_length()} ps')

print(f'Area: {sum(rtl.area_estimation())} mm^2')
