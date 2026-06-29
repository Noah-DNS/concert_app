import qrcode

tickets = ["1", "2", "3"]

for ticket in tickets:
    img = qrcode.make(ticket)
    img.save(f"qr_{ticket}.png")

print("QR créés")