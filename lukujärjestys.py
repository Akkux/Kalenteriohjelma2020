#Lukujärjestys


def viiva():
    print("-----------------------------------------------------------------")

def ylä():
    print("   Klo   |    Ma    |    Ti    |    Ke    |    To    |    Pe    |")

def rivi(kello,a,b,c,d,e):
    print("  {}  |{}|{}|{}|{}|{}|".format(kello,a,b,c,d,e))

def tulostus():
    #print()
    print("Lukujärjestys:")
    print()
    ylä()
    viiva()
    rivi("08-10","          ","          ","          ","          ","          ")
    viiva()
    rivi("10-12","          ","          ","          ","          ","          ")
    viiva()
    rivi("12-14","          ","          ","          ","          ","          ")
    viiva()
    rivi("14-16","          ","          ","          ","          ","          ")
    viiva()
    #rivi("16-18","          ","          ","          ","          ","          ")
    #viiva()
    #print()
    print()
