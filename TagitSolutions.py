class SGTIN96EPC():
    def __init__(self, sgtin96epc_hex):
        sgtin96epc_bin = self.SGTIN96EPC_Hex2Bin(sgtin96epc_hex = sgtin96epc_hex)
        if (len(sgtin96epc_bin) == 96):
            partition_bin = self.Partition_bin(sgtin96epc_bin = sgtin96epc_bin)
            partition_dec = self.Bin2Dec(bin_number = partition_bin)
            company_prefix_Nbits = self.CompanyPrefixNBits4Partition(partition = partition_dec)
            item_ref_Nbits = self.ItemRefNBits(company_prefix_Nbits = company_prefix_Nbits)
            company_prefix_bin = self.CompanyPrefix_bin(sgtin96epc_bin = sgtin96epc_bin, company_prefix_Nbits = company_prefix_Nbits)
            self.company_prefix_dec = self.Bin2Dec(bin_number = company_prefix_bin)
            item_ref_bin = self.ItemRef_bin(sgtin96epc_bin = sgtin96epc_bin, company_prefix_Nbits = company_prefix_Nbits, item_ref_Nbits = item_ref_Nbits)
            self.item_ref_dec = self.Bin2Dec(bin_number = item_ref_bin)
            serial_bin = self.Serial_bin(sgtin96epc_bin = sgtin96epc_bin)
            self.serial_dec = self.Bin2Dec(bin_number = serial_bin)
            self.NotEncodedProperlyIndicator = 0
        else:
            self.NotEncodedProperlyIndicator = 1

    def Table_Hex2Bin(self):
        Dict = {}

        Dict["0"] = "0000"
        Dict["1"] = "0001"
        Dict["2"] = "0010"
        Dict["3"] = "0011"
        Dict["4"] = "0100"
        Dict["5"] = "0101"
        Dict["6"] = "0110"
        Dict["7"] = "0111"
        Dict["8"] = "1000"
        Dict["9"] = "1001"
        Dict["A"] = "1010"
        Dict["B"] = "1011"
        Dict["C"] = "1100"
        Dict["D"] = "1101"
        Dict["E"] = "1110"
        Dict["F"] = "1111"

        return Dict

    def SGTIN96EPC_Hex2Bin(self, sgtin96epc_hex):
        Hex2Bin = self.Table_Hex2Bin()
        sgtin96epc_bin = ""
        for i in range (0, len(sgtin96epc_hex)):
            try:
                temp = Hex2Bin[sgtin96epc_hex[i]]
            except KeyError:
                temp = ""
            sgtin96epc_bin = sgtin96epc_bin + temp
        return sgtin96epc_bin

    def Partition_bin(self, sgtin96epc_bin):
        partition = sgtin96epc_bin[11:14]
        return partition

    def Bin2Dec(self, bin_number):
        dec_number = 0
        for i in range (0, len(bin_number)):
            dec_number = dec_number + int(bin_number[-(i + 1)])*2**i
        return dec_number

    def CompanyPrefixNBits4Partition(self, partition):
        if (partition == 0):
            company_prefix_Nbits = 40
        elif (partition == 1):
            company_prefix_Nbits = 37
        elif (partition == 2):
            company_prefix_Nbits = 34
        elif (partition == 3):
            company_prefix_Nbits = 30
        elif (partition == 4):
            company_prefix_Nbits = 27
        elif (partition == 5):
            company_prefix_Nbits = 24
        elif (partition == 6):
            company_prefix_Nbits = 20

        return company_prefix_Nbits

    def ItemRefNBits(self, company_prefix_Nbits):
        item_ref_Nbits = 44 - company_prefix_Nbits
        return item_ref_Nbits

    def CompanyPrefix_bin(self, sgtin96epc_bin, company_prefix_Nbits):
        company_prefix_bin = sgtin96epc_bin[14:14 + company_prefix_Nbits]
        return company_prefix_bin

    def ItemRef_bin(self, sgtin96epc_bin, company_prefix_Nbits, item_ref_Nbits):
        item_ref_bin = sgtin96epc_bin[14 + company_prefix_Nbits:14 + company_prefix_Nbits + item_ref_Nbits]
        return item_ref_bin

    def Serial_bin(self, sgtin96epc_bin):
        serial_bin = sgtin96epc_bin[58:]
        return serial_bin

class MainProgram():
    Milka_company_prefix_dec = 69124
    Milka_item_ref_dec = 1253252
    NMilka = 0
    MilkaSerials = []
    NotEncodedProperlyTags = []

    File = open("tags.txt", "r")
    
    for line in File:
        tag = line.split("\n")[0]
        sgtin96epc = SGTIN96EPC(sgtin96epc_hex = tag)
        if (sgtin96epc.NotEncodedProperlyIndicator == 0):
            if ((sgtin96epc.company_prefix_dec == Milka_company_prefix_dec) and (sgtin96epc.item_ref_dec == Milka_item_ref_dec)):
                NMilka = NMilka + 1
                MilkaSerials.append(sgtin96epc.serial_dec)
        else:
            NotEncodedProperlyTags.append(tag)

    File.close()    

    print("Number of Milka Oreo chocolates: ", NMilka)
    print("Milka Oreo chocolate serials: ")
    for i in range (0, NMilka):
        print(MilkaSerials[i])
    print("Tags which are not encoded properly in SGTIN-96 format:")
    for i in range (0, len(NotEncodedProperlyTags)):
        print(NotEncodedProperlyTags[i])

MainProgram()

k = input("Press close to exit.") 