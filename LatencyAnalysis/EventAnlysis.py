import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

FileName = "abc.txt"
Messages = { "DE":[], "S":[], "C":[] }

# Input : 
#
#	Source (String) : Consist the source of device of which message is started transferring
#	Destination (String) : Consist the Destination of device of which message is transferred
#
# Processing :
# 	This function is calculating the latency of messages transferring from source and destination
#
# Output : 
#
#	Return the latency in Seconds.
#

def Get_Latency(Source,Destination):
	DeliveredI = {}
	DeliveredT = {}
	DeliveredV = {}

	TimeI = 0.00
	TimeT = 0.00
	TimeV = 0.00

	NoOfMEssagesI = 0
	NoOfMEssagesT = 0
	NoOfMEssagesV = 0

	for Event in Messages["DE"]:

		if ( 0 <= Event[2].find(Source) and 0 <= Event[3].find(Destination) ):
			if ( "I" == Event[4][1] ):
				DeliveredI[ Event[4] ] = float(Event[0])
			else:
				if ( "T" == Event[4][1] ):
					DeliveredT[ Event[4] ] = float(Event[0])
				else:
					if ( "V" == Event[4][1] ):
						DeliveredV[ Event[4] ] = float(Event[0])


	for Event in Messages["S"]:
		if ( 0 <= Event[2].find(Source) and 0 <= Event[3].find(Destination) ):
			if ( Event[4][1] == "I" and  Event[4] in DeliveredI ):
				NoOfMEssagesI += 1
				TimeI += DeliveredI[Event[4]] - float(Event[0])
			else:
				if ( Event[4][1] == "T" and  Event[4] in DeliveredT ):
					NoOfMEssagesT += 1
					TimeT += DeliveredT[Event[4]] - float(Event[0])
				else:
					if ( Event[4][1] == "V" and  Event[4] in DeliveredV ):
						NoOfMEssagesV += 1
						TimeV += DeliveredV[Event[4]] - float(Event[0])
	return {
		"Text"    : TimeT/NoOfMEssagesT,
		"Images"  : TimeI/NoOfMEssagesI,
		"Video"   : TimeV/NoOfMEssagesV
	}

def GetDeliveryDTN():

	MessagesTemp = {}
	CreatedI = 0
	CreatedT = 0
	CreatedV = 0

	DeliveredI = 0
	DeliveredT = 0
	DeliveredV = 0

	for Event in Messages["C"]:
		if ( "T" == Event[3][1] ):
			CreatedT += 1
		else:
			if ( "I" == Event[3][1] ):
				CreatedI += 1
			else:
				if ( "V" == Event[3][1] ):
					CreatedV += 1

	for Event in Messages["DE"]:

		if ( 0 <= Event[2].find("dtn") and 0 <= Event[3].find("ADB") ):
			if ( Event[4] in MessagesTemp):
				continue
			else:
				MessagesTemp[Event[4]]=""
			if ( "I" == Event[4][1] ):
				DeliveredI += 1
			
			else:
				if ( "T" == Event[4][1] ):
					DeliveredT += 1
			
				else:
					if ( "V" == Event[4][1] ):
						DeliveredV += 1
	return {
		"Text"  : DeliveredT/CreatedT,
		"Image" : DeliveredI/CreatedI,
		"Video" : DeliveredV/CreatedV
	}


def GetDelivery(PreviousSource, Source, Destination):

	MessagesTemp = {}
	if("dtn" == Source):
		return GetDeliveryDTN()

	SourceRecievedI = 0
	SourceRecievedT = 0
	SourceRecievedV = 0

	DestinationDeliveredI = 0
	DestinationDeliveredT = 0
	DestinationDeliveredV = 0

	for Event in Messages["DE"]:
		
		if ( 0 <= Event[2].find(Source) and 0 <= Event[3].find(Destination) ):
			if ( Event[4] in MessagesTemp):
				continue
			else:
				MessagesTemp[Event[4]]=""
			if ( "I" == Event[4][1] ):
				DestinationDeliveredI += 1
			
			else:
				if ( "T" == Event[4][1] ):
					DestinationDeliveredT += 1
			
				else:
					if ( "V" == Event[4][1] ):
						DestinationDeliveredV += 1

		MessagesTemp = {}
		if ( 0 <= Event[3].find(Source) ):
			if ( Event[4] in MessagesTemp):
				continue
			else:
				MessagesTemp[Event[4]]=""
			if ( "CD" == Destination ):
				if( not 0 <= Event[2].find(PreviousSource) ):
					continue

			if ( "I" == Event[4][1] ):
				SourceRecievedI += 1

			else:
				if ( "T" == Event[4][1] ):
					SourceRecievedT += 1
			
				else:
					if ( "V" == Event[4][1] ):
						SourceRecievedV += 1

	return {
		"Text"  : DestinationDeliveredT/SourceRecievedT,
		"Image" : DestinationDeliveredI/SourceRecievedI,
		"Video" :DestinationDeliveredV/SourceRecievedV
	}
def DTN_TO_ADB():

	Value = Get_Latency("dtn","ADB")
	print ("\nDTN To ADB (In Seconds) :-",Value ,"\n")
	Value = GetDelivery("dtn","dtn","ADB")
	print ("\nDelivery Probability DTN To ADB  :-", Value,"\n")
	return Value

def ADB_To_CD():
	
	Value = Get_Latency("ADB","CD")
	print ("\nLatency ADB To CD (In Seconds) :-", Value,"\n")
	Value = GetDelivery("dtn","ADB","CD")
	print ("\nDelivery Probability ADB To CD  :-", Value,"\n")
	return Value


def CD_to_GC():

	Value = Get_Latency("CD","ADB")
	print ("\nCD To GC (In Seconds) :-", Value,"\n")
	Value = GetDelivery("ADB","CD","ADB")
	print ("\nDelivery Probability CD To GC :-", Value,"\n")
	return Value 

def GC_to_GC_WiFi():

	Value = Get_Latency("ADB","WIFI")
	print ("\nGC To GC WIFI (In Seconds) :-", Value,"\n")
	Value = GetDelivery("CD","ADB","WIFI")
	print ("\nDelivery Probability GC To GC WiFi  :-", Value,"\n")
	return Value

def GC_WIFI_to_MCS_WiFi():
	
	Value = Get_Latency("WIFI","WIFI")
	print ("\nGC WIFI To MCS WIFI (In Seconds) :-", Value,"\n")
	Value = GetDelivery("ADB","WIFI","WIFI")
	print ("\nDelivery Probability GC WIFI To MCS WIFI  :-", Value,"\n")
	return Value

def MCS_WIFI_to_MCS_ADB():

	Value = Get_Latency("WIFI","ADB")
	print ("\nMCS WiFi To MCS ADB (In Seconds) :-", Value,"\n")
	Value = GetDelivery("WIFI","WIFI","ADB")
	print ("\nDelivery Probability MCS WIFI To MCS ADB  :-", Value,"\n")
	return Value

# Parsing the messages accoring to status in an dictionary
def Parse_Status(Messages, Status):
	
	FileData = open(FileName,"r").read().split("\n")
	
	for StatusRow in FileData:

		StatusRow = StatusRow.split(" ")
		if ( 2 < len(StatusRow) and Status == StatusRow[1] ):
			Messages[Status].append(StatusRow)
def Plot():
 
	objects = (
		'DTN_TO_ADB', 
		'ADB_To_CD', 
		'CD_to_GC', 
		'GC_to_GC_WiFi', 
		'GC_WIFI_to_MCS_WiFi', 
		'MCS_WIFI_to_MCS_ADB'
		)
	y_pos = np.arange(len(objects))
	performance = [DTN_TO_ADB(),
		ADB_To_CD(), 
		CD_to_GC(), 
		GC_to_GC_WiFi(), 
		GC_WIFI_to_MCS_WiFi(), 
		MCS_WIFI_to_MCS_ADB()
	]
	 
	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Time In Seconds')
	plt.title('latency') 
	plt.show()

def GetConfig():
	FileDescriptor = open("Config.txt","w")
	if ( FileDescriptor ):

		print (" Config File not found Error")
		quit()

	else:

		Data = FileDescriptor.read()
		if( 0<= Data.find("FileName") ):
			Data = Data.split("\n")
			for Row in Data:
				if ( 2 < len(Row) ):
					Data = Row.split("=")
					break
			FileName = Data[1]
		else:
			print("FileName Property Not Found in Config File")
			quit()

def main():

	Parse_Status(Messages,"DE")
	Parse_Status(Messages,"S")
	Parse_Status(Messages,"C")
	
	DTN_TO_ADB()
	ADB_To_CD()
	CD_to_GC()
	GC_to_GC_WiFi()
	GC_WIFI_to_MCS_WiFi()
	MCS_WIFI_to_MCS_ADB()


main()