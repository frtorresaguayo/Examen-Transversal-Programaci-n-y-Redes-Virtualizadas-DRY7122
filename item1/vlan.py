vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("Corresponde al rango NORMAL.")
elif 1006 <= vlan <= 4094:
    print("Corresponde al rango EXTENDIDO.")
else:
    print("Número de VLAN no válido (El rango permitido es de 1 a 4094).")
