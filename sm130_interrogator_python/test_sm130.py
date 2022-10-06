from sm130_read import Interrogator

def main(): 
    # address information
    address = "192.168.1.11"
    port = 1852
    # create interrogator
    interrogator = Interrogator( address, port )

    # rawdata
    rawdata = interrogator.getData()
    print(rawdata)
    print(type(rawdata))
    # get header info
    header = interrogator.getHeader()
    
    # print some value in Interrogaotor
    print(interrogator.available_ch)


if __name__ == "__main__":
    main()
