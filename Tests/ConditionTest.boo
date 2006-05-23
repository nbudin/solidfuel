import Condition from SolidFuel.Logic
import NUnit.Framework from "nunit.framework"

[TestFixture]
class ConditionFixture:
    
    [Test]
    def SimpleStatusTest():
        b = true
        c = Condition({return b})
        Assert.IsTrue(c.Status)
        
        b = false
        Assert.IsTrue(c.Status)
        c.Poll()
        Assert.IsFalse(c.Status)

    [Test]
    def SubConditionTest():
        mylist = (3, 5)
        c1 = Condition({return mylist[0] == mylist[1]})
        c2 = Condition({return mylist[1] == 5})
        c3 = c1 | c2
        c4 = c1 & c2
        c5 = -((c1 | c2) | (c1 & c2))

        assertStatus = def(statuses as (bool)):
            conds = (c1, c2, c3, c4, c5)

            for i in range(len(conds)):
                if statuses[i]:
                    Assert.IsTrue(conds[i].Status)
                else:
                    Assert.IsFalse(conds[i].Status)

        assertStatus((false, true, true, false, false))

        mylist[0] = 5
        c1.Poll()
        c2.Poll()
        assertStatus((true, true, true, true, false))

        mylist[1] = 3
        c1.Poll()
        c2.Poll()
        assertStatus((false, false, false, false, true))
