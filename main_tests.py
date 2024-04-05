import unittest
# import pygame
# pygame.init()
from main import Player, Enemy, Bullet, Bat, SkeletonKing, BasicAttack, XP, XPBar, Map
#"pyest.ini"
class Player_Test(unittest.TestCase):

    def test_invalid_speed(self):
        with self.assertRaises(TypeError):
            p = Player()
            p.speed("e")

    def test4(self):
        p = Player()
        self.assertTrue(p.image.endswith(".png"), "p.image does not end with .png")

    def test5(self):
        b = Player()
        p = Player()
        self.assertNotEqual(b,p)
    def test6(self):
        p = Player()
        self.assertTrue(Player())
    def test7(self):
        with self.assertRaises(AttributeError):
            p = Player()
            p.wieght()


class Enemy_Test(unittest.TestCase):

    def test1(self):
        e = Enemy(0,0)
        e2 = Enemy(0,0)
        e.speed = 5
        e2.speed = 5.0
        self.assertTrue(e.speed, e2.speed)
    def test2(self):
        e = Enemy(0,0)
        e.health = 1
        e.speed = 1
        self.assertTrue(e.health, e.speed)

    def test3(self):
        e = Enemy(0,0)
        with self.assertRaises(TypeError):
            e.health("e")
    def test4(self):
        b = Enemy(0,0)
        p = Player()
        self.assertNotEqual(b,p)
    def test5(self):
        b = Enemy(0, 0)
        p = Enemy(0,0)
        self.assertNotEqual(b, p)
    def test6(self):
        e = Enemy(0,0)
        self.assertTrue(Enemy(0,0))
    def test7(self):
        with self.assertRaises(AttributeError):
            p = Enemy(0,0)
            p.wieght()

class Bullet_Test(unittest.TestCase):

    def test1(self):
        b = Bullet()
        b.bulletSpeed = 50
        self.assertTrue(b.bulletSpeed)
    def test2(self):
        b = Bullet()
        b.bulletIncrement = 50.0
        self.assertTrue(b.bulletIncrement)
    def test3(self):
        b = Bullet()
        b.damage = 100
        self.assertTrue(b.damage)
    def test4(self):
        b = Bullet()
        p = Player()
        self.assertNotEqual(b,p)
    def test5(self):
        b = Bullet()
        self.assertTrue(Bullet())
    def test7(self):
        with self.assertRaises(AttributeError):
            p = Bullet()
            p.wieght()
    def test8(self):
        b = Bullet()
        p = Bullet()
        self.assertNotEqual(b,p)

class skeletonKing_Test(unittest.TestCase):

    def test1(self):
        sk = (
            SkeletonKing(0,0))
        self.assertTrue(sk.skeletonKing)
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
        self.assertTrue(SkeletonKing(0,0))
    def test7(self):
        with self.assertRaises(AttributeError):
            p = SkeletonKing(0,0)
            p.wieght()

class Bat_Test(unittest.TestCase):
    def test1(self):
        bat = Bat(0,0)
        self.assertTrue(bat)
    def test2(self):
        bat = Bat(0,0)
        with self.assertRaises(TypeError):
            bat.health = "e"
    def test3(self):
        bat = Bat(0,0)
        bat.health = 1
        bat.speed = 1
        self.assertTrue(bat.health, bat.speed)
    def test4(self):
        b = Bat(0,0)
        p = Player
        self.assertNotEqual(b,p)
    def test5(self):
        b = Bat(0,0)
        p = Bat(0,0)
        self.assertNotEqual(b,p)
    def test6(self):
        b = Bat(0,0)
        self.assertTrue(Bat(0,0))
    def test7(self):
        with self.assertRaises(AttributeError):
            p = Bat(0,0)
            p.wieght()
class BasicAttack_Test(unittest.TestCase):
    def test1(self):
        b = BasicAttack()
        b.damage = 1
        self.assertTrue(b.damage)
    def test2(self):
        b =  BasicAttack()
        b.timerTarget = 1
        self.assertTrue(b.timerTarget)
    def test3(self):
        b = BasicAttack()
        p = Player()
        self.assertNotEqual(b,p)
    def test4(self):
        b = BasicAttack()
        self.assertTrue(Bat(0,0))
    def test5(self):
        b = BasicAttack()
        c = BasicAttack()
        self.assertNotEqual(b,c)
    def test6(self):
        with self.assertRaises(AttributeError):
            p = BasicAttack()
            p.wieght()

class XP_Test(unittest.TestCase):
    def test1(self):
        x = XP(0,0)
        self.assertTrue(XP(0,0))
    def test2(self):
        x = XP(0,0)
        y = XP(0,0)
        self.assertNotEqual(x,y)
    def test3(self):
        x = XP(0,0)
        x.x = 1
        self.assertTrue(x.x)
    def test4(self):
        x = XP(0,0)
        x.y = 1
        self.assertTrue(x.y)
    def test5(self):
        with self.assertRaises(AttributeError):
            x = XP(0,0)
            x.weight()
    def test6(self):
        x = Player()
        y = XP(0,0)
        self.assertNotEqual(x,y)
class XP_Bar_Test(unittest.TestCase):
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
class Map_Test(unittest.TestCase):
    def test1(self):
        x = Map()
        y = Map()
        self.assertNotEqual(x,y)
    def test2(self):
        x = Player()
        y = Map()
        self.assertNotEqual(x,y)
    def test3(self):
        x = Map()
        x.mapX = 1
        self.assertTrue(x.mapX)
    def test4(self):
        x = Map()
        self.assertTrue(Map())
    def test5(self):
        with self.assertRaises(AttributeError):
            x = Map()
            x.weight()


if __name__ == '__main__':
    unittest.main()
