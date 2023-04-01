from src.map import Map

my_map = Map()
my_map.generate()
my_map.add_bloks()
for row in my_map.map:
    print(" ".join(row))