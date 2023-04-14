import sys

m = ENV['m']
n = ENV['n']

h = ENV['h']
k = ENV['k']

my = ENV['my_conjecture']

def main():
    return (m * n) % (h * k) == 0

if __name__ == "__main__":
    main()
