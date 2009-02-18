from solidfuel.Logic.Condition import Condition
import unittest

class SimpleStatusTestCase(unittest.TestCase):
    def runTest(self):
        b = True
        c = Condition(lambda: b)
        assert c.status

        b = False
        assert c.status
        c.poll()
        assert not c.status

class SubConditionTestCase(unittest.TestCase):
    def runTest(self):
        mylist = [3, 5]
        c1 = Condition(lambda: mylist[0] == mylist[1])
        c2 = Condition(lambda: mylist[1] == 5)
        c3 = c1 | c2
        c4 = c1 & c2
        c5 = ~((c1 | c2) | (c1 & c2))

        def assertStatus(statuses):
            conds = (c1, c2, c3, c4, c5)

            for i in range(len(conds)):
                if statuses[i]:
                    assert conds[i].status
                else:
                    assert not conds[i].status

        assertStatus((False, True, True, False, False))

        mylist[0] = 5
        c1.poll()
        c2.poll()
        assertStatus((True, True, True, True, False))

        mylist[1] = 3
        c1.poll()
        c2.poll()
        assertStatus((False, False, False, False, True))
        
if __name__ == "__main__":
    unittest.main()
