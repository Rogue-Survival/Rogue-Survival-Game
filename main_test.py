import unittest
from main import Player, Enemy, Bullet, Bat, SkeletonKing, BasicAttack, XP, XPBar, Map
#"pyest.ini"
class TestPlayer(unittest.TestCase):

    def test_speed_typerror(self):
        # Checks for type error
        with self.assertRaises(TypeError):
            p = Player()
            p.speed("e")

    def test_instance(self):
        #checks if two instances are the same
        b = Player()
        p = Player()
        self.assertNotEqual(b,p)
    def test_init(self):
        #Checks if the player initializes
        p = Player()
        p.health = 10
        self.assertEquals(p.health,10)
    def test_attribute_fail(self):
        #checks for a error when calling a non existing attribute
        with self.assertRaises(AttributeError):
            p = Player()
            p.weight()


class TestEnemy(unittest.TestCase):

    def test_speed(self):
        e = Enemy(0,0)
        e2 = Enemy(0,0)
        e.speed = 5
        e2.speed = 5.0
        self.assertEqual(e.speed, e2.speed)
    def test_if_variables_are_empty(self):
        e = Enemy(0,0)
        e.health = 1
        e.speed = 1
        self.assertTrue(e.health, e.speed)

    def test_typeerror(self):
        e = Enemy(0,0)
        with self.assertRaises(TypeError):
            e.health("e")
    def test_diff_instances(self):
        b = Enemy(0,0)
        p = Player()
        self.assertNotEqual(b,p)
    def test_seperate_instances(self):
        b = Enemy(0, 0)
        p = Enemy(0,0)
        self.assertNotEqual(b, p)
    def test_instance(self):
        e = Enemy(0,0)
        self.assertEquals(e,Enemy(0,0))
    def test_attribute_fail(self):
        with self.assertRaises(AttributeError):
            p = Enemy(0,0)
            p.weight()


class TestBat(unittest.TestCase):

    def test_speed_typerror(self):
        # Checks for type error
        with self.assertRaises(TypeError):
            p = Bat()
            p.speed("e")
    def test_instance(self):
        bat = Bat(0,0)
        self.assertTrue(bat)
    def test3(self):
        bat = Bat(0,0)
        bat.health = 1
        bat.speed = 1
        self.assertTrue(bat.health, bat.speed)
    def test_diff_instances(self):
        b = Bat(0,0)
        p = Player
        self.assertNotEqual(b,p)
    def test_seperate_instances(self):
        b = Bat(0,0)
        p = Bat(0,0)
        self.assertNotEqual(b,p)
    def test_attribute_fail(self):
        with self.assertRaises(AttributeError):
            p = Bat(0,0)
            p.weight()
class TestBasicAtt(unittest.TestCase):
    def test_value(self):
        b = BasicAttack()
        b.damage = 1
        self.assertEquals(b.damage,1)
    def test_value2(self):
        b =  BasicAttack()
        b.timerTarget = 1
        self.assertEquals(b.timerTarget,1)
    def test_diff_instances(self):
        b = BasicAttack()
        p = Player()
        self.assertNotEqual(b,p)
    def test_value3(self):
        b = BasicAttack()
        b.rangeIncrease = 1
        self.assertEquals(b.rangeIncrease,1)
    def test_seperate_instances(self):
        b = BasicAttack()
        c = BasicAttack()
        self.assertNotEqual(b,c)
    def test_attribute_fail(self):
        with self.assertRaises(AttributeError):
            p = BasicAttack()
            p.wieght()

class TestEXP(unittest.TestCase):
    def test_instance(self):
        x = XP(0,0)
        self.assertTrue(XP(0,0))
    def test_two_intances(self):
        x = XP(0,0)
        y = XP(0,0)
        self.assertNotEqual(x,y)
    def test_value(self):
        x = XP(0,0)
        x.x = 1
        self.assertEqual(x.x,1)
    def test_value2(self):
        x = XP(0,0)
        x.y = 1
        self.assertEqual(x.y,1)
    def test_attribute_fail(self):
        with self.assertRaises(AttributeError):
            x = XP(0,0)
            x.weight()
    def test_diff_instances(self):
        x = Player()
        y = XP(0,0)
        self.assertNotEqual(x,y)
class TestMap(unittest.TestCase):
    def test_two_instances(self):
        x = Map()
        y = Map()
        self.assertNotEqual(x,y)
    def test_diff_instances(self):
        x = Player()
        y = Map()
        self.assertNotEqual(x,y)
    def test_value(self):
        x = Map()
        x.mapX = 1
        self.assertEqual(x.mapX,1)
    def test_instance(self):
        x = Map()
        self.assertTrue(Map())
    def test_attribute_fail(self):
        with self.assertRaises(AttributeError):
            x = Map()
            x.weight()
class TestSK(unittest.TestCase):

    def test1(self):
        sk = SkeletonKing(0,0)
        self.assertEquals(sk = SkeletonKing(0,0))
    def test2(self):
        sk = SkeletonKing(0,0)
        sk.health = 1
        self.assertFalse(sk.felled, 'sk is not dead')
    def test3(self):
        sk = SkeletonKing(0,0)
        sk.health = "e"
        with self.assertRaises(AttributeError):
            sk.follow_mc()
    def test4(self):
        b = SkeletonKing(0,0)
        p = Player()
        self.assertNotEqual(b,p)
    def test5(self):
        b = SkeletonKing(0,0)
        p = SkeletonKing(0,0)
        self.assertNotEqual(b,p)
    def test6(self):
        sk = SkeletonKing(0,0)
        self.assertEqual(sk.x, 0)
    def test7(self):
        with self.assertRaises(AttributeError):
            p = SkeletonKing(0,0)
            p.wieght()
class TestXP(unittest.TestCase):
    def test1(self):
        x = XPBar()
        self.assertTrue(XPBar())
    def test2(self):
        x = XPBar()
        y = XPBar()
        self.assertNotEqual(x,y)
    def test3(self):
        x = XPBar()
        x.level = 1
        self.assertTrue(x.level)
    def test4(self):
        x = XPBar()
        x.y = 1
        self.assertTrue(x.y)
    def test5(self):
        with self.assertRaises(AttributeError):
            x = XP(0,0)
            x.weight()
    def test6(self):
        x = Player()
        y = XPBar()
        self.assertNotEqual(x,y)

if __name__ == '__main__':
    unittest.main()