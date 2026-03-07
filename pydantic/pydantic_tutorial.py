from pydantic import BaseModel
class PersonPydantic(BaseModel):
    name : str
    age : int
    city : str

from dataclasses import dataclass
@dataclass
class PersonDataClass:
    name : str
    age : int
    city : str

person = PersonDataClass(name = "Biman", age = 32, city = "Patna")
print("from the data class", person)
person = PersonPydantic(name = "Biman", age = 32, city = "Patna")
print("from Pydantic", person)


""" as we  see that both dataclass and pydantic have the same advantage defining the output"""


person = PersonDataClass(name = "Biman", age = "32", city = "Patna")
print("from dataclass ", person)
person = PersonPydantic(name = "Biman", age ="32", city = "patna")
print("from pydantic validation for city ", person)
person = PersonPydantic(name = "Biman", age = 32, city = 10)
print("from pydantic validation for city ", person)

from typing import Optional

class PersonPydanticOptional(BaseModel):
    name : str
    age : int
    city : str
    department: str
    salary : Optional[float] = None
    is_active: Optional[bool] = False

person = PersonPydanticOptional(name = "Biman", age ="32", city = "patna", department = "AI")
print("from pydantic validation for city ", person)
from pydantic import BaseModel
from typing import List

class ClassRoom(BaseModel):
    room_number : int
    students : List[str]
    capacity : int

classroom = ClassRoom(room_number = 101, students = ["Biman", "Giri"], capacity = 10)
print("classroom pydantic class with list ", classroom)
try:

    classroom = ClassRoom(room_number = 101, students = ["Biman", "Giri", 123], capacity = 10)
    print("classroom pydantic class with list ", classroom)
except ValueError as e:
    print(e)


### Nested Model


class Address(BaseModel):
    state : str
    pin : int
    country: str


class Person(BaseModel):
    name : str
    address : Address 

person_details = Person(name = "biman giri", address = {"state" : "west bengal", "pin" : 721457, "country" : "india"})
print("object of person", person_details)



### Pydantic Fields : Customization and Constrainsts
""" The Field function in pydantic enhances modle fields beyond basic type hints by allowing you to specify validatoin rules, defaults values, aliases, and mmore. Here's a comprehensive tutorial with examples."""

from pydantic import BaseModel, Field

class Item(BaseModel):
    name : str  = Field(min_length = 2, max_length = 50)
    price : float = Field(gt =0 , le = 100) # greater than 0 and less than 100
    quantity : int = Field(ge = 0, le = 10)

item = Item ( name = "TV", price = 10, quantity = 5)
print("Item 1 ", item)

# make the price 1000 so that it violates the validation 
item = Item ( name = "TV", price = 1000, quantity = 5)
print("Item 1 ", item)

from  pydantic import BaseModel, Field

class User(BaseModel):

    username : str = Field(..., description = "unique username for the user")
    age : int = Field(default = 18 , description = "user age, defaults to 18")
    email : str = Field(default_factory=lambda: "user@example", description = "default email address")

user1 = User(username = "alice")
print("user 1 : ", user1)

user2 = User(username = "bob", age = 25, email = "bob@domain.com")
print("user2 : ", user2)
print("printing user schema: ", user2.model_json_schema())
