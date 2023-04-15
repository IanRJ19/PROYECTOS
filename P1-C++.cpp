#include <iostream>
#include <string>
#include <vector>

using namespace std;

class MovCtaBancaria {
private:
    string fecha;
    string documento;
    double abono;
    double cargo;
public:
    MovCtaBancaria(string f, string doc, double ab, double car) {
        fecha = f;
        documento = doc;
        abono = ab;
        cargo = car;
    }
    string getFecha() { return fecha; }
    string getDocumento() { return documento; }
    double getAbono() { return abono; }
    double getCargo() { return cargo; }
};

class CtaBancaria {
private:
    string nroCtaBancaria;
    string nombres;
    string direccion;
    vector<MovCtaBancaria> movimientos;
public:
    CtaBancaria(string nro, string nom, string dir) {
        nroCtaBancaria = nro;
        nombres = nom;
        direccion = dir;
    }
    void ingresarDatosGenerales() {
        cout << "Ingrese el número de cuenta bancaria: ";
        getline(cin, nroCtaBancaria);
        cout << "Ingrese el nombre del titular de la cuenta: ";
        getline(cin, nombres);
        cout << "Ingrese la dirección del titular de la cuenta: ";
        getline(cin, direccion);
    }
    void depositar(string fecha, double monto) {
        movimientos.push_back(MovCtaBancaria(fecha, "depósito", monto, 0));
    }
    void retirar(double monto) {
        movimientos.push_back(MovCtaBancaria("", "retiro", 0, monto));
    }

    double obtenerSaldo() {
        double saldo = 0;
        for (int i = 0; i < movimientos.size(); i++) {
            saldo += movimientos[i].getAbono() - movimientos[i].getCargo();
        }
        return saldo;
    }
    void mostrarMovimientos() {
        cout << "Movimientos de la cuenta bancaria " << nroCtaBancaria << ":" << endl;
        for (int i = 0; i < movimientos.size(); i++) {
            cout << "Fecha: " << movimientos[i].getFecha() << endl;
            cout << "Documento: " << movimientos[i].getDocumento() << endl;
            cout << "Abono: " << movimientos[i].getAbono() << endl;
            cout << "Cargo: " << movimientos[i].getCargo() << endl;
        }
    }
};

int main() {
    int opcion = 0;
    double monto = 0;
    string fecha;
    CtaBancaria cuenta("0", "", "");
    while (opcion != 6) {
        cout << "::::::::::::::::::::MENU::::::::::::::::::::" << endl;
        cout << "<1> Ingresar Datos Generales" << endl;
        cout << "<2> Depósitos" << endl;
        cout << "<3> Retiros" << endl;
        cout << "<4> Mostrar Saldos" << endl;
        cout << "<5> Mostrar Movimientos" << endl;
        cout << "<6> Salir" << endl;
        cout << "Ingrese una opción: ";
        cin >> opcion;
        cin.ignore();
        switch (opcion) {
            case 1:
                cuenta.ingresarDatosGenerales();
                break;
            case 2:
                cout << "Ingrese la fecha del depósito (en formato dd/mm/aaaa): ";
                getline(cin, fecha);
                cout << "Ingrese el monto a depositar: ";
                cin >> monto;
                cuenta.depositar(fecha, monto);
                break;
            case 3:
            cout << "Ingrese el monto a retirar: ";
            cin >> monto;
            cuenta.retirar(monto);
            break;
            case 4:
                cout << "El saldo de la cuenta es: " << cuenta.obtenerSaldo() << endl;
                break;
            case 5:
                cuenta.mostrarMovimientos();
                break;
            case 6:
                cout << "Saliendo del programa..." << endl;
                break;
            default:
                cout << "Opción inválida. Por favor ingrese una opción del 1 al 6." << endl;
                break;
        }
    }
    return 0;
    }
