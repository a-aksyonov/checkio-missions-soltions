from dataclasses import dataclass
from textwrap import wrap


@dataclass(init=True, eq=True)
class Person:
    first_name: str
    last_name: str
    birth_date: str
    job: str
    working_years: float
    salary: int
    country: str
    city: str
    gender: str = 'unknown'

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        return 2018 - int(self.birth_date.rsplit('.', maxsplit=1)[1]) - 1

    def work(self):
        if self.gender == 'male':
            pronoun = "he "
        elif self.gender == 'female':
            pronoun = "she "
        else:
            pronoun = ""
        return f"{pronoun}is a {self.job}".capitalize()

    def money(self):
        money_rev = str(self.salary * self.working_years * 12)[::-1]
        money_three_list = wrap(money_rev, 3)
        return " ".join(money_three_list)[::-1]

    def home(self):
        return f"Lives in {self.city}, {self.country}"


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing

    p1 = Person("John", "Smith", "19.09.1979", "welder", 15, 3600, "Canada",
                "Vancouver", "male")
    p2 = Person("Hanna Rose", "May", "05.12.1995", "designer", 2.2, 2150,
                "Austria", "Vienna")
    assert p1.name() == "John Smith", "Name"
    assert p1.age() == 38, "Age"
    assert p2.work() == "Is a designer", "Job"
    print(p1.money())
    assert p1.money() == "648 000", "Money"
    assert p2.home() == "Lives in Vienna, Austria", "Home"
    print("Coding complete? Let's try tests!")
