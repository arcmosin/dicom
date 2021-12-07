# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_CTPosition(z):
    IPP=[]
    for i in range(85):
        IPP.append(i*5-193)
    return IPP.index(z)

print(get_CTPosition(-63))