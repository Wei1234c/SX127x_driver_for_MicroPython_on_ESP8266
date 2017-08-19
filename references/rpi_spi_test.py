import spidev

# to test error rate under each baudrate
# connect MISO to MOSI
     

class Mock:
    pass
    
        
def prepare_spi(spi, speed): 
    if spi:
        spi.open(0, 0) 
        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
        # https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=19489
        spi.max_speed_hz = speed
        spi.mode = 0b00
        spi.lsbfirst = False
        new_spi = Mock()  

        def transfer(value = 0x00): 
            return spi.xfer2(value)
            
        new_spi.transfer = transfer
        new_spi.close = spi.close
        return new_spi 
        
     
def main(speed = 500000):
    spi = None
    try: 
        spi = spidev.SpiDev()
    except Exception as e:
        print(e)
        
    spi = prepare_spi(spi, speed)
    orig = [i for i in range(128)] * 30
    result = spi.transfer(orig)
    # print(orig)
    # print(result)
    count_all, count_err, error_ratio = cal_error_rate(orig, result)
    print('count_all: {}, count_err: {}, error_ratio: {}'.format(count_all, count_err, error_ratio))
    
    if spi: spi.close()  
 
def cal_error_rate(orig, result):
    count_all = len(orig)
    count_err = 0
    
    for i in range(count_all):
        if result[i] != orig[i]:
            count_err += 1
        
    return count_all, count_err, (count_err/count_all)*100
        
main(10000000)
    