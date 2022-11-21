## About script
This python script is used only to reading of selected registers, counting of average value and sending to MQTT bridge.
Connection to Alpha ESS inverter via Modbus TCP and all readable registers are described in https://github.com/DrKTM/Alpha-ESS-Modbus-TCP-Monitor-Openhab

The script perform sending of average data in one interval. For rerunning I recomend to create own service.

# Settings of script
1/ Line 8> ALPHAESS_Inverter_IP = IP address of your inverter.
<br />2/ Line 10> interval = count of reading which will be averaged. All Alpha ESS inverters should give modbus data in 1sec interval. So default value 300 = 5 min interval.
<br />3/ Line 126 to 135> MQTT_bridge_IP = IP address of your MQTT bridge.

## After this settings average of those registers are counted and send
PV1 = segment of photovoltaic panels in Watts.
<br />PV2 = segment of photovoltaic panels in Watts.
<br />Battery = battery level in %.
<br />BatteryPower = battery power in Watts. Negative value is charging of battery, positive value is discharging of battery.
<br />ConsumA = Consumption from grid for A phase in Watts.
<br />ConsumB = Consumption from grid for B phase in Watts.
<br />ConsumC = Consumption from grid for C phase in Watts.
<br />ConsumSum = Total consumption from grid in Watts.
<br />Temp = Temperature of inverter in °C.

## Add new register
1/ add variables ADDREGISTER and set 0 as default
<br />2/ add this block:
```
ADDREGISTERregs = c.read_holding_registers(XXX,1)
	if ADDREGISTERregs:
		ADDREGISTERregs = int(''.join(str(i) for i in ADDREGISTERregs))
		ADDREGISTER =  + ADDREGISTERregs
	else:
 		print("read error for ADDREGISTERregs in interval", intervalCount )
```
<br />3/ Add 
```
publish.single("storion/modbus/ADDREGISTE",round((ADDREGISTE/interval)), hostname="MQTT_bridge_IP")
```
<br />4/ Change all "ADDREGISTER" to your new register, "XXX" change to registers address in decimal.

### NOTE
Problems occurse if registers give negative number because this number is deduced from 65 535. In case BatteryPower, number is recounted into negative format, in case ConsumA/B/C negative number is not needed, so all numbers which should be negative are transformed to zero. (Negative number mean grid feed-in)

## Remove register
Remove variable, block and sending or only sending of coresponding register.
