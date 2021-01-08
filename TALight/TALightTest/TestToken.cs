using NUnit.Framework;
using TALightObjects;

namespace TALightTest
{
    public class TestToken
    {
        [SetUp]
        public void Setup()
        {

        }

        [Test]
        public void Test1()
        {
            Token t = new Token();

            Assert.AreEqual(t.Secret, "");
            Assert.AreEqual(t.Secret, t.Secret);

            t.Generate();
            Assert.AreNotEqual(t.Secret, "");
        }
    }
}