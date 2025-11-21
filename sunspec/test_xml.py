import xml.etree.ElementTree as ET

xml_data = """
<mbmap func="holding" addr="40000">
    <regs offset="0" len="2" type="u16" access="rw">0x1234</regs>
</mbmap>
"""

root = ET.parse("sunspec-sim/modsim/smdx_00113.xml").getroot()
print(root)
# Access attributes of root
version = root.attrib.get('v')

for regs in root[0][0].findall("point"):
    print(regs)

# Iterate over child elements
for regs in root:
    if regs.tag == "model" and regs.attrib.get("id") == "113":
        block = regs[0]
        for point in block:
            id = point.attrib.get("id")
            offset = point.attrib.get("offset")
            type = point.attrib.get("type")
            units = point.attrib.get("units")
            mandatory = point.attrib.get("mandatory")
            # print(f""" Point id: {id} offset: {offset} type:{type} units: {units} mandatory: {mandatory} len: {len(point)}""")
    

    

# country_data_as_string ="""<?xml version="1.0"?>
# <data>
#     <country name="Liechtenstein">
#         <rank>1</rank>
#         <year>2008</year>
#         <gdppc>141100</gdppc>
#         <neighbor name="Austria" direction="E"/>
#         <neighbor name="Switzerland" direction="W"/>
#     </country>
#     <country name="Singapore">
#         <rank>4</rank>
#         <year>2011</year>
#         <gdppc>59900</gdppc>
#         <neighbor name="Malaysia" direction="N"/>
#     </country>
#     <country name="Panama">
#         <rank>68</rank>
#         <year>2011</year>
#         <gdppc>13600</gdppc>
#         <neighbor name="Costa Rica" direction="W"/>
#         <neighbor name="Colombia" direction="E"/>
#     </country>
# </data>"""

# import xml.etree.ElementTree as ET
# root = ET.fromstring(country_data_as_string)