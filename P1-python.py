class MovCtaBancaria:
    def __init__(self, f, doc, ab, car):
        self.fecha = f
        self.documento = doc
        self.abono = ab
        self.cargo = car
        
    def getFecha(self):
        return self.fecha
    
    def getDocumento(self):
        return self.documento
    
    def getAbono(self):
        return self.abono
    
    def getCargo(self):
        return self.cargo


class CtaBancaria:
    def __init__(self, nro, nom, dir):
        self.nroCtaBancaria = nro
        self.nombres = nom
        self.direccion = dir
        self.movimientos = []
        
    def ingresarDatosGenerales(self):
        self.nroCtaBancaria = input("Ingrese el número de cuenta bancaria: ")
        self.nombres = input("Ingrese el nombre del titular de la cuenta: ")
        self.direccion = input("Ingrese la dirección del titular de la cuenta: ")
        
    def depositar(self, fecha, monto):
        self.movimientos.append(MovCtaBancaria(fecha, "depósito", monto, 0))
        
    def retirar(self, monto):
        self.movimientos.append(MovCtaBancaria("", "retiro", 0, monto))
        
    def obtenerSaldo(self):
        saldo = 0
        for movimiento in self.movimientos:
            saldo += movimiento.getAbono() - movimiento.getCargo()
        return saldo
    
    def mostrarMovimientos(self):
        print("Movimientos de la cuenta bancaria " + self.nroCtaBancaria + ":")
        for movimiento in self.movimientos:
            print("Fecha: " + movimiento.getFecha())
            print("Documento: " + movimiento.getDocumento())
            print("Abono: " + str(movimiento.getAbono()))
            print("Cargo: " + str(movimiento.getCargo()))
            

opcion = 0
monto = 0
fecha = ""
cuenta = CtaBancaria("0", "", "")

while opcion != 6:
    print("::::::::::::::::::::MENU::::::::::::::::::::")
    print("<1> Ingresar Datos Generales")
    print("<2> Depósitos")
    print("<3> Retiros")
    print("<4> Mostrar Saldos")
    print("<5> Mostrar Movimientos")
    print("<6> Salir")
    opcion = int(input("Ingrese una opción: "))
    
    if opcion == 1:
        cuenta.ingresarDatosGenerales()
        
    elif opcion == 2:
        fecha = input("Ingrese la fecha del depósito (en formato dd/mm/aaaa): ")
        monto = float(input("Ingrese el monto a depositar: "))
        cuenta.depositar(fecha, monto)
        
    elif opcion == 3:
        monto = float(input("Ingrese el monto a retirar: "))
        cuenta.retirar(monto)
        
    elif opcion == 4:
        print("El saldo de la cuenta es: " + str(cuenta.obtenerSaldo()))
        
    elif opcion == 5:
        cuenta.mostrarMovimientos()
        
    elif opcion == 6:
        print("Saliendo del programa...")
        
    else:
        print("Opción inválida. Por favor ingrese una opción del 1 al 6.")
