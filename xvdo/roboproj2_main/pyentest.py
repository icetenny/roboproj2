import enchant
d = enchant.Dict("en_US")
print(d.check("Hello my name is ice"))
print(d.check("Helo"))
print(d.suggest("Helo"))

sen = "Hello ny name is Ice. Ronnapee"

for word in sen.split(" "):
    print(word, d.check(word))