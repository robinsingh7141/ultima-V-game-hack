#robin Singh
#CECS 378 Malware LAB
#04-07-2023

import mmap
# in the following we defined character data with their hex offsets
charData = [
  ('MainChar', '0e', '0f', '10', '12', '13', '14', '15', '16', '17'),
  ('Shamino', '2e', '2f', '30', '32', '33', '34', '35', '36', '37'),
  ('Iolo', '4e', '4f', '50', '52', '53', '54', '55', '56', '57'),
  ('Mariah', '6e', '6f', '70', '72', '73', '74', '75', '76', '77'),
  ('Geoffrey', '8e', '8f', '90', '92', '93', '94', '95', '96', '97'),
  ('Jaana', 'Ae', 'Af', 'B0', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'),
  ('Julia', 'Ce', 'Cf', 'D0', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'),
  ('Dupre', 'Ee', 'Ef', 'F0', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7'),
  ('Katrina', '10e', '10f', '110', '112', '113', '114', '115', '116', '117'),
  ('Sentri', '12e', '12f', '130', '132', '133', '134', '135', '136', '137'),
  ('Gwenno', '14e', '14f', '150', '152', '153', '154', '155', '156', '157'),
  ('Johne', '16e', '16f', '170', '172', '173', '174', '175', '176', '177'),
  ('Gorn', '18e', '18f', '190', '192', '193', '194', '195', '196', '197'),
  ('Maxwell', '1Ae', '1Af', '1B0', '1B2', '1B3', '1B4', '1B5', '1B6', '1B7'),
  ('Toshi', '1Ce', '1Cf', '1D0', '1D2', '1D3', '1D4', '1D5', '1D6', '1D7'),
  ('Saduj', '1Ee', '1Ef', '1F0', '1F2', '1F3', '1F4', '1F5', '1F6', '1F7')
]

fileOptions = {
  '1': 'INIT.GAM',  # Option 1 for INIT.GAM
  '2': 'SAVED.GAM'  # Option 2 for SAVED.GAM
}
#it defines the item name
itemNames = [
  "Magic Axes", "Black Badge", "Skull Keys", "Magic Carpets", "Gems", "Keys",
  "Gold"
]
#it defines the stats names
statNames = [
  "Strength", "Dexterity", "Intelligence", "Health", "Max Health", "Experience"
]

def hexInt(hex_str):#converting hex string to integer
  return int(hex_str, 16)

def sthexVals(pos1, pos2, value):#it converts the int value into the 4 digit hex string
  hexd = format(value, '04x')
  m[pos1], m[pos2] = hexInt(hexd[2:]), hexInt(hexd[:2])#it splits the 4 digit hex string into 2
                                                      
def char_statAdj(stat_type, *args):
  # It Checks if the stat_type argument is 'c' (for custom input)
  if stat_type.lower() == 'c':
    # Setting the maximum values allowed
    max_vals = [255, 255, 255, 999, 999, 999]
    stats = [# it Prompts user to input custom values for each stat, 
             #ensuring they are within the allowed range
      int(input(f'{stat_name} Val ({max_val} Max)\n'))
      for stat_name, max_val in zip(statNames, max_vals)
    ]
  else:
    print('Max Values Set\n')
    stats = [99, 99, 99, 999, 999, 9999]

  m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)#creatting a mmap file
  m[args[0]], m[args[1]], m[args[2]] = stats[:3]#assigning positions
  for val1, val2, stat in zip(args[3::2], args[4::2], stats[3:]):#updates the mmap 
    sthexVals(val1, val2, stat)
  m.flush()

#change the item quantities from user input
def itemQ_adj(choice):
  if choice.lower() == 'y':# if user select y to change the item quantity 
    maxVals = [255, 255, 255, 255, 255, 255, 9999]#max values
    quantities = [
      int(input(f'How Many {itemName} ({maxVal} Max)\n'))#checks user input if they are within max set values
      for itemName, maxVal in zip(itemNames, maxVals)
    ]
  else:
    print('\nDefault modified values set.')
    quantities = [10, 1, 100, 2, 100, 100, 9999]

  m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)#creatting a mmap file
  sthexVals(hexInt('204'), hexInt('205'), quantities[-1])#update the mmap file with last iten Qty
  for pos, qty in zip(
    [hexInt(val) for val in ['240', '218', '20b', '20a', '207', '206']],#update mmap file with neew qty
      quantities[:-1]):
    m[pos] = qty
  m.flush()

# main program
print('Ultima game stats editor ')
input('\nPlease Press the Enter')#asks user to press enter

print("Please Choose the file to modify:")#asks user to schoose file wants to edit
print("1. INIT.GAM\n2. SAVED.GAM")
fileChoice = input("Enter the number (1/2) for your choice: ")

f = open(fileOptions[fileChoice], 'a+b')#open selected file

print('\n~~~ Character Stat editor ~~~\n')
m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)#create mmap
charMod = input('Do you want to modify the Character Stats? (Y/N): ')
if charMod.lower() == 'y':
  custom_mod = input(
    'Do you want to MAX the stats or Customize them individually? (m/c): ')
  #iterate over characters and then apply changes
  for char_name, *hexOffsets in charData:
    print(f'{char_name}:')#dispay name
    char_statAdj(custom_mod, *[hexInt(offset) for offset in hexOffsets])#adjusts the stats 

  print('\nChanges have been made to all of the characters')
else:
  print('\nSkipped.')

print('\n~~~ Item quantity editor ~~~')
itemMod = input('Do you want to modify the quantity of items? (y/n): ')
if itemMod.lower() == 'y':
  custChoice = input(
    '\nDo you want to customize the values individually? (y/n): \n')
  itemQ_adj(custChoice)
  print('\nChanges have been made to all of the Item Quantities.')
else:
  print('\nskipped.')
#it is closing the file and memory map
m.flush()
m.close()
f.close()
