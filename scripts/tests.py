from solvro_city import SolvroCity


###############################################################################


test = SolvroCity(".", "test_map")

route1_result = test.get_shortest_route("one", "two")
route1_expected = {"route": [{"name": "one"}, {"name": "two"}], "distance": 4}
print(route1_result == route1_expected)

route2_result = test.get_shortest_route("one", "six")
route3_result = test.get_shortest_route("six", "one")
print(
    4 + 1 + 10 + 0 + 120
    == route2_result["distance"]
    == route3_result["distance"]
)


###############################################################################


original = SolvroCity(".")


route1_result = original.get_shortest_route(
    "Przystanek Cudowny student PWr", "Przystanek Zdenerwowany programista"
)

# expectations based on graph preview
route1_expected = {
    "route": [
        {"name": "Przystanek Cudowny student PWr"},
        {"name": "Przystanek Beznadziejny programista"},
        {"name": "Przystanek Dziki jamnik"},
        {"name": "Przystanek Zdenerwowany programista"},
    ],
    "distance": 36,
}
print(route1_result == route1_expected)


route2_result = original.get_shortest_route(
    "Przystanek Dziki jamnik", "Przystanek Cudowny programista"
)
route2_expected_distance = 35
print(route2_result["distance"] == route2_expected_distance)

route3_result = original.get_shortest_route(
    "Przystanek Zasmucony muczaczo", "Przystanek Zasmucony student PWr"
)

# expected direct connection
route3_expected = {
    "route": [
        {"name": "Przystanek Zasmucony muczaczo"},
        {"name": "Przystanek Zasmucony student PWr"},
    ],
    "distance": 12,
}
print(route3_result == route3_expected)


route4_result = original.get_shortest_route(
    "Przystanek Cudowny student PWr", "Przystanek Dziki jamnik"
)
print(route4_result)
# False, because many stops with same names have got different ids, and we
# don't know which stop exacly is the choosen one. Stop that is not connected
# with anothers is simply overriding connected one. Better solution would be an
# ID-based search, but task guidelines were were different :(.
