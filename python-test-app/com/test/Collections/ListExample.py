#List Example 1st

numbers = []
strings = []
names = ["John", "Eric", "Jessica"]

# write your code here
second_name = names[1]

numbers.append(1)
numbers.append(2)
numbers.append(3)

strings.append("hello")
strings.append("world")

# this code should write out the filled arrays and the second name in the names list (Eric).
print(numbers)
print(strings)
print("The second name on the names list is %s" % second_name)

print("======================================================================")

#List Example 2nd
#Lists can be joined with the addition operators:
even_numbers = [2,4,6,8]
odd_numbers = [1,3,5,7]
all_numbers = odd_numbers + even_numbers
print("\nFinal joined List:  ")
print(all_numbers)

print("======================================================================")

#List Example 2nd
mylist = []
mylist.append(1)
mylist.append(2)
mylist.append(3)

#print(mylist[0])
#print(mylist[1])
#print(mylist[2])

# Loop
# prints out 1,2,3
for x in mylist:
    print(x)
print("======================================================================")

#Accessing an index which does not exist generates an exception
#print(mylist[3])

#Just as in strings, Python supports forming new lists with a repeating sequence using the multiplication operator:
print([1,2,3] * 3)

print("======================================================================")

# Complex object example
x = object()
y = object()

# TODO: change this code
x_list = [x]*10
y_list = [y]*10
big_list = x_list+y_list


print("x_list contains %d objects" % len(x_list))
print("y_list contains %d objects" % len(y_list))
print("big_list contains %d objects" % len(big_list))

# testing code
if x_list.count(x) == 10 and y_list.count(y) == 10:
    print("Almost there...")
if big_list.count(x) == 10 and big_list.count(y) == 10:
    print("Great!")