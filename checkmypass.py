import requests
from urllib import response
import hashlib
import sys


def request_api_data(query_char):
  url = 'https://api.pwnedpasswords.com/range/' + query_char
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
  return res


# were going to check the has_to_check and then loop through all the hashes
def get_password_leaks_count(hashes, hash_to_check):
  hashes = (line.split(':') for line in hashes.text.splitlines())
  for h, count in hashes:
    if h == hash_to_check:
      return count
  return 0




def pwned_api_check(password):
  #Check password if it exists in API response
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  first5_char, tail = sha1password[:5], sha1password[5:]
  response = request_api_data(first5_char)
  return get_password_leaks_count(response, tail)
  '''
  #in here we have our SHA1 Password:
  # encode the input into utf-8 
  # Hexidigest return as a hexadecimal string object of double length
  # The last thing is to convert all the hexadecimal to Uppercase to agree with the API
  #get the first 5 characters, then get the characters from 5 til the end
  '''


def main(args):
  for password in args:
    count = pwned_api_check(password)
    if count:   # if you have matches you should change your password
      print(f'{password} was found {count} times... you should probably change your password!')
    else:  # else if there are no matches, your good
      print(f'{password} was Not found. Carry on!')
  return 'Done'



if __name__ == '__main__':
  sys.exit(main(sys.argv[1:])) # sys.exit to exit the program in case it doesn't exit on it's own
