import os as _os

H = 0

V = 1

def main(_solution):
    # checkpoint
    print(0)
    # read m, n
    print(end="", flush=True)
    [m, n] = map(int, input().split())
    # call res = is_tilable(m, n)
    res = int(_solution.is_tilable(m, n))
    # write res
    print(res)
    # if res {...}
    if res:
        # read choice
        print(end="", flush=True)
        [choice] = map(int, input().split())
        # if choice {...}
        if choice:
            # read m1, n1
            print(end="", flush=True)
            [m1, n1] = map(int, input().split())
            # call compose_tiling(m1, n1) callbacks {...}
            def _callback_place_tile(row, col, dir):
                # callback place_tile
                print(1, 0)
                # write row, col, dir
                print(row, col, dir)
            _solution.compose_tiling(m1, n1, _callback_place_tile)
            # no more callbacks
            print(0, 0)
    # exit
    print(end="", flush=True)
    _os._exit(0)


if __name__ == '__main__':
    import sys
    import runpy
    
    if len(sys.argv) != 2:
        print("Usage: {} <solution>".format(sys.argv[0]))
    
    class Wrapper: pass 
    solution = Wrapper()
    solution.__dict__ = runpy.run_path(sys.argv[1])
    main(solution)

