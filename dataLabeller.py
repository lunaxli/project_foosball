#!/usr/bin/python

import os
import sys

import xml.etree.ElementTree as ET
from time import sleep
from mobile_insight.monitor import OfflineReplayer
from mobile_insight.analyzer import MsgLogger, LteRrcAnalyzer, WcdmaRrcAnalyzer, LteNasAnalyzer, UmtsNasAnalyzer, LtePhyAnalyzer, LteMacAnalyzer


messages = ["lte-rrc.rrcConnectionReconfiguration_element",
			"lte-rrc.rrcConnectionReconfigurationComplete_element",
			"lte-rrc.rrcConnectionRelease_element"]

def dump_logs(path):
	logger = MsgLogger()
	logger.set_decode_format(MsgLogger.XML)
	logger.set_dump_type(MsgLogger.FILE_ONLY)
	logger.save_decoded_msg_as(path)
	logger.set_source(src)

	lte_rrc_analyzer = LteRrcAnalyzer()
	lte_rrc_analyzer.set_source(src)

	wcdma_rrc_analyzer = WcdmaRrcAnalyzer()
	wcdma_rrc_analyzer.set_source(src)

	lte_nas_analyzer = LteNasAnalyzer()
	lte_nas_analyzer.set_source(src)

	umts_nas_analyzer = UmtsNasAnalyzer()
	umts_nas_analyzer.set_source(src)

	lte_phy_analyzer = LtePhyAnalyzer()
	lte_phy_analyzer.set_source(src)

	src.run()

def locate_handoff(root):
	for pkt in root:
		#print pkt.tag, pkt.attrib

		for pair in pkt.iter('pair'):
			#print "    ", pair.attrib, pair.text
			if pair.attrib['key'] == "Msg":
				for elem in pair[0][0]:
					#print "        ", elem.attrib
					if elem.attrib["name"] == "fake-field-wrapper":
						for a in elem[0].iter('field'):
							if a.get("name") == "lte-rrc.message":
								for b in a:
									if b.get("name") == "lte-rrc.c1":
										for c in b.iter("field"):
											#print c.attrib
											if c.attrib["name"] == messages[0]:
												print "Reconfig Start"
											if c.attrib["name"] == messages[1]:
												print "Reconfig Complete"
											if c.attrib["name"] == messages[2]:
												print "Reconfig Release"

if __name__ == "__main__":
	src = OfflineReplayer()
	src.set_input_path("./example.mi2log")

	if not os.path.isfile('./logdump.xml'):
		dump_logs('./logdump.xml')

	#with open('./logdump.xml', 'r+') as f:
	#	content = f.read()
	#	f.seek(0, 0)
	#	f.write('<root>\n' + content)

	#with open('./logdump.xml', 'a+') as f:
	#	f.write('</root>')
	#	f.close()

	#sleep(60)

	#with open('./logdump.xml', 'rb') as f, open('./logdumpwithroot.xml', 'wb') as g:
	#	g.write('<ROOT>{}</ROOT>'.format(f.read()))

	tree = ET.parse('./logdump.xml')
	root = tree.getroot()

	locate_handoff(root)