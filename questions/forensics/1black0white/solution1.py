import qrcode

def generate_flag_qr_code(numbers_file):
    """Generates a QR code from a file containing numbers representing flag text."""

    try:
        with open(numbers_file, "r") as file:
            numbers = [int(line.strip()) for line in file]

            # Validate and convert numbers to characters
            flag_text = "".join(chr(num) for num in numbers if 0 <= num <= 1114111)
            print(flag_text)

            if not flag_text.startswith("csawctf{"):
                # Option 1: Allow partial flag text
                print("Warning: Flag text doesn't start with 'csawctf{'. Generating QR code with available text.")
            else:
                qr = qrcode.QRCode(
                version=1,  # Adjust version if needed
                error_correction=qrcode.constants.ERROR_CORRECT_H
                )
                qr.add_data(flag_text)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                img.save("flag_qrcode.png")
                print("Flag QR code generated successfully!")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_flag_qr_code("qr_code.txt")
