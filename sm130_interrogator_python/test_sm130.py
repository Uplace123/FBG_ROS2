from sm130_read import Interrogator

def main(): 
    # address information
    address = "192.168.1.11"
    port = 1852
    # create interrogator
    interrogator = Interrogator( address, port )

    # getting peak message data
    peak_msg = interrogator.getData()
    # return none if cant connect with interrogator
    # return data contain "header" and "peak_container" which contain all the signals from CH1 to CH4
    
    # check if peak_msg is empty
    if peak_msg is not None:
        """
        print( "Status Header: ", peak_msg.header )
        print( '\n')
        print( "Peak Container:", peak_msg.peak_container )
        print( '\n')
        """
        # get the signals
        print(peak_msg.peak_container.CH1)
        print(peak_msg.peak_container.CH2)
        print(peak_msg.peak_container.CH3)
        print(peak_msg.peak_container.CH4)


if __name__ == "__main__":
    main()
