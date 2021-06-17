class A:
    def __init__(self, sim=1):
        self.sim = sim

class B(A):
    def __init__(self, sim=2):
        A.__init__(self, sim)

        print self.sim

if __name__ == '__main__':
    abc = B(3)