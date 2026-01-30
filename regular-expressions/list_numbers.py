# If you pass an int here, Python will still TRY to run it...
# ...but it will likely crash the moment it hits a string-only operation.
def isPhoneNumber(text: str):  # Passing exactly 12 characters into the function Ex; 'Call me 415-5', 415-555-1234 
     if len(text) != 12:
          return False
     for i in range(0,3):
        if not text[i].isdecimal():  # It checks whether a string represents a decimal number using decimal digits.
            return False
     if text[3] != '-':
         return False
     for i in range(4, 7):
         if not text[i].isdecimal():
             return False
     if text[7] != '-':
         return False
     for i in range(8, 12):
         if not text[i].isdecimal():
             return False
     return True

message = "Call me 415-555-1238 tomorrow, or at 415-374-3837 for my office extension"

foundNumber = False

for i in range(len(message)):
    chunk = message[i:i+12]  # create small strings of length 12 from original 
    if isPhoneNumber(chunk):  # passing those chunks into function
        print("Phone number found: %s" % (chunk))
        foundNumber = True

if not foundNumber:
    print("Could not find any phone numbers")