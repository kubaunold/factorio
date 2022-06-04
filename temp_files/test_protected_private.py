class Parent(object):
    def _protected(self):
        pass

    def __private(self):
        print("Is it really private?")

class Child(Parent):
    def foo(self):
        self._protected()

    def bar(self):
        self.__private()

c = Child()
c._Parent__private()