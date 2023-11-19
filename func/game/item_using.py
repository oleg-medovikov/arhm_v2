from mdls import Person, Item
from func.game.demand import demand


async def item_using(person: "Person", item: "Item"):
    """ """

    # нужно проверить требования к персонажу, перед использованием
    check = await demand(person, item.demand)

    if not 
