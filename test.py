from typing import List

from pydantic import BaseModel


class Test(BaseModel):
    id: int
    name: str


o1 = Test(
    id=1,
    name="one",
)

o2 = Test(
    id=2,
    name="two",
)

l = [o1, o2]

print(type(l))

# i = 0
# while i < len(l):
#     l[i].id += 2
#     l[i].name += "three"
#     i += 1

for i in range(0, len(l), 1):
    l[i].id += 2
    l[i].name += "three"

print(l)
