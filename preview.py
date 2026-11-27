# # digital prorotype same interface

def show(pen):
    for r in range(pen.num_rows):
        line = ""
        for c in range(pen.num_cols):
            line += "●" if pen.is_on(r, c) else "·"
        print(line)
    print()