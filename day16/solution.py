HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

with open("input.txt") as f:
    input_hex = f.readline().strip()


def hex_to_binary_str(hex_str):
    bin_str = ""
    for c in hex_str:
        bin_str += HEX_TO_BIN[c]
    return bin_str


# assert hex_to_binary_str("38006F45291200") == "00111000000000000110111101000101001010010001001000000000"
# assert hex_to_binary_str("EE00D40C823060") == "11101110000000001101010000001100100000100011000001100000"


def decode_literal(packet):
    # Literal value, read groups of 5 bits until reaching 0 head
    literal_value_str = ""
    index = 0
    while packet[index] != "0":
        literal_value_str += packet[index + 1:index + 5]
        index += 5
    literal_value_str += packet[index + 1:index + 5]
    return int(literal_value_str, 2), index + 5


def decode_subpackets_0(packets, n_bits, op):
    index = 0
    version_sum = 0
    result = None
    while index < n_bits:
        version, value, bits_read = decode_packet(packets[index:])
        version_sum += version
        result = value if result is None else op(result, value)
        index += bits_read

    return version_sum, result, n_bits


def decode_subpackets_1(packets, n_packets, op):
    index = 0
    n_packets_read = 0
    version_sum = 0
    result = None
    while n_packets_read < n_packets:
        version, value, bits_read = decode_packet(packets[index:])
        version_sum += version
        result = value if result is None else op(result, value)
        index += bits_read
        n_packets_read += 1

    return version_sum, result, index


def get_op(type_id):
    if type_id == 0:
        return lambda x, y: x + y
    elif type_id == 1:
        return lambda x, y: x * y
    elif type_id == 2:
        return min
    elif type_id == 3:
        return max
    elif type_id == 5:
        return lambda x, y: x > y
    elif type_id == 6:
        return lambda x, y: x < y
    elif type_id == 7:
        return lambda x, y: x == y


def decode_packet(packet):
    version = int(packet[:3], 2)
    type_id = int(packet[3:6], 2)
    if type_id == 4:
        value, bits_read = decode_literal(packet[6:])
        bits_read += 6
    else:
        op = get_op(type_id)
        if packet[6] == "0":
            total_subpacket_bits = int(packet[7:22], 2)
            version_sum, value, bits_read = decode_subpackets_0(packet[22:], total_subpacket_bits, op)
            version += version_sum
            bits_read += 22
        else:
            num_subpackets = int(packet[7:18], 2)
            version_sum, value, bits_read = decode_subpackets_1(packet[18:], num_subpackets, op)
            version += version_sum
            bits_read += 18
    return version, value, bits_read


# print(decode_packet(hex_to_binary_str("D2FE28")))
# print(decode_packet(hex_to_binary_str("38006F45291200")))
# print(decode_packet(hex_to_binary_str("EE00D40C823060")))

test_transmissions = [
    "8A004A801A8002F478",  # 16
    "620080001611562C8802118E34",  # 12
    "C0015000016115A2E0802F182340",   # 23
    "A0016C880162017C3686B18A3D4780",  # 31
]
for t in test_transmissions:
    print(decode_packet(hex_to_binary_str(t)))
print(decode_packet(hex_to_binary_str(input_hex)))


'''
first three bits: version
next three bits: type ID
type id 4: literal value, encoded in groups of 4 with prefix indicating whether to keep reading
other type id: operator, contains 1+ subpackets
- bit after header is length type id
  - 0: next 15 bits represent total length in bits of subpackets
  - 1: next 11 bits represent number of subpackets
'''

