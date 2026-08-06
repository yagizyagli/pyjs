bridge_b.expose("add", add)

result = await bridge_a.call("add", 5, 10)

print(result)
