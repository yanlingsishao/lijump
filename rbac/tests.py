from django.test import TestCase

# Create your tests here.

try:
    print(1)
    try:
        z = open("11","r")
        print(z,2)
    except Exception as e:
        print(e,2)
except Exception as e:
    print(e, 1)
