#!/usr/bin/env python3

from pyModbusTCP.client import ModbusClient
import time
import paho.mqtt.publish as publish


c = ModbusClient(host='ALPHAESS_Inverter_IP', port=502, unit_id=85, auto_open=True, auto_close=False)

interval = 300

#list of variables to geting of data
PV1 = 0
PV2 = 0
Battery = 0
BatteryPower = 0
ConsumA = 0
ConsumB = 0
ConsumC = 0
ConsumSum = 0
Temp = 0



# measuring of data
intervalCount = 0 
while intervalCount < interval:
	
	#PV1
	PV1regs = c.read_holding_registers(1056,1)
	if PV1regs:
		PV1regs = int(''.join(str(i) for i in PV1regs))
		PV1 = PV1 + PV1regs
	else:
 		print("read error for PV1 in interval", intervalCount )

	
	#PV2
	PV2regs = c.read_holding_registers(1060,1)
	if PV2regs:
		PV2regs = int(''.join(str(i) for i in PV2regs))
		PV2 = PV2 + PV2regs
	else:
 		print("read error for PV2 in interval", intervalCount )

	
	#Battery
	Batteryregs = c.read_holding_registers(258,1)
	if Batteryregs:
		Batteryregs = int(''.join(str(i) for i in Batteryregs))
		Battery = Battery + Batteryregs
	else:
 		print("read error for Battery in interval", intervalCount )

	
	#BatteryPower
	BatteryPowerregs = c.read_holding_registers(294,1)
	if BatteryPowerregs:
		BatteryPowerregs = int(''.join(str(i) for i in BatteryPowerregs))
		if BatteryPowerregs > 35000:
			BatteryPowerregs = BatteryPowerregs - 65536
		BatteryPower = BatteryPower + BatteryPowerregs
	else:
 		print("read error for BatteryPower in interval", intervalCount )
	

	#ConsumA
	ConsumAregs = c.read_holding_registers(28,1)
	if ConsumAregs:
		ConsumAregs = int(''.join(str(i) for i in ConsumAregs))
		if (ConsumAregs > 30000):
			ConsumAregs = 0
		ConsumA = ConsumA + ConsumAregs
	else:
 		print("read error for ConsumA in interval", intervalCount)
	

	#ConsumB
	ConsumBregs = c.read_holding_registers(30,1)
	if ConsumBregs:
		ConsumBregs = int(''.join(str(i) for i in ConsumBregs))
		if (ConsumBregs > 30000):
			ConsumBregs = 0
		ConsumB = ConsumB + ConsumBregs
	else:
 		print("read error for ConsumB in interval", intervalCount )
	

	#ConsumC
	ConsumCregs = c.read_holding_registers(32,1)
	if ConsumCregs:
		ConsumCregs = int(''.join(str(i) for i in ConsumCregs))
		if (ConsumCregs > 30000):
			ConsumCregs = 0
		ConsumC = ConsumC + ConsumCregs
	else:
 		print("read error for ConsumC in interval", intervalCount )
	

	#ConsumSum
	ConsumSumregs = c.read_holding_registers(34,1)
	if ConsumSumregs:
		ConsumSumregs = int(''.join(str(i) for i in ConsumSumregs))
		if (ConsumSumregs > 30000):
			ConsumSumregs = 0
		ConsumSum = ConsumSum + ConsumSumregs
	else:
 		print("read error for ConsumSumin interval", intervalCount )
	

	#Temp
	Tempregs = c.read_holding_registers(1077,1)
	if Tempregs:
		Tempregs = int(''.join(str(i) for i in Tempregs))
		Temp = Temp + Tempregs
	else:
 		print("read error for Temp in interval", intervalCount )


	time.sleep(1)
	intervalCount = intervalCount + 1



#sending of data via MQTT
publish.single("storion/modbus/PV",round((PV1/interval)+(PV2/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/PV1",round((PV1/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/PV2",round((PV2/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/Battery",round(Battery/interval/10), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/BatteryPower",round((BatteryPower/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/ConsumA",round((ConsumA/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/ConsumB",round((ConsumB/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/ConsumC",round((ConsumC/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/ConsumSum",round((ConsumSum/interval)), hostname="MQTT_bridge_IP")
publish.single("storion/modbus/Temp",round((Temp/interval/10)), hostname="MQTT_bridge_IP")

