import re

file_content='''This XML file does not appear to have any style information associated with it. The document tree is shown below.
<NewDataSet>
<xs:schema xmlns="" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:msdata="urn:schemas-microsoft-com:xml-msdata" id="NewDataSet">
<xs:element name="NewDataSet" msdata:IsDataSet="true" msdata:UseCurrentLocale="true">
<xs:complexType>
<xs:choice minOccurs="0" maxOccurs="unbounded">
<xs:element name="Quantita">
<xs:complexType>
<xs:sequence>
<xs:element name="Data" type="xs:string" minOccurs="0"/>
<xs:element name="Mercato" type="xs:string" minOccurs="0"/>
<xs:element name="Ora" type="xs:string" minOccurs="0"/>
<xs:element name="TOTALE_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="NAT_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="CNOR_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="CSUD_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="NORD_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="SARD_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="SICI_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="SUD_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="AUST_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="BRNN_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="COAC_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="CORS_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="FOGN_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="FRAN_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="GREC_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="MFTV_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="PRGP_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="ROSN_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="SLOV_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="SVIZ_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="BSP_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="MALT_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="XAUS_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="XFRA_ACQUISTI" type="xs:string" minOccurs="0"/>
<xs:element name="TOTALE_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="NAT_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="CNOR_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="CSUD_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="NORD_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="SARD_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="SICI_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="SUD_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="AUST_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="BRNN_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="COAC_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="CORS_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="FOGN_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="FRAN_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="GREC_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="MFTV_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="PRGP_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="ROSN_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="SLOV_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="SVIZ_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="BSP_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="MALT_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="XAUS_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="XFRA_VENDITE" type="xs:string" minOccurs="0"/>
<xs:element name="TOTITABSP_VENDITE" msdata:ReadOnly="true" msdata:Expression="Convert(TOTALE_VENDITE, System.Double) + Convert(BSP_VENDITE,System.Double)" type="xs:string" minOccurs="0"/>
<xs:element name="TOTITABSP_ACQUISTI" msdata:ReadOnly="true" msdata:Expression="Convert(TOTALE_ACQUISTI, System.Double) + Convert(BSP_ACQUISTI, System.Double)" type="xs:string" minOccurs="0"/>
</xs:sequence>
</xs:complexType>
</xs:element>
</xs:choice>
</xs:complexType>
</xs:element>
</xs:schema>
<Quantita>
<Data>20161229</Data>
<Mercato>MGP</Mercato>
<Ora>1</Ora>
<TOTALE_ACQUISTI>24527,457</TOTALE_ACQUISTI>
<NAT_ACQUISTI>24472,890000</NAT_ACQUISTI>
<CNOR_ACQUISTI>2481,365000</CNOR_ACQUISTI>
<CSUD_ACQUISTI>4046,346000</CSUD_ACQUISTI>
<NORD_ACQUISTI>12269,221000</NORD_ACQUISTI>
<SARD_ACQUISTI>855,333000</SARD_ACQUISTI>
<SICI_ACQUISTI>1609,888000</SICI_ACQUISTI>
<SUD_ACQUISTI>1914,304000</SUD_ACQUISTI>
<AUST_ACQUISTI>0,000000</AUST_ACQUISTI>
<BRNN_ACQUISTI>0,000000</BRNN_ACQUISTI>
<COAC_ACQUISTI>80,000000</COAC_ACQUISTI>
<CORS_ACQUISTI>49,000000</CORS_ACQUISTI>
<FOGN_ACQUISTI>0,000000</FOGN_ACQUISTI>
<FRAN_ACQUISTI>120,000000</FRAN_ACQUISTI>
<GREC_ACQUISTI>0,000000</GREC_ACQUISTI>
<MFTV_ACQUISTI>0,000000</MFTV_ACQUISTI>
<PRGP_ACQUISTI>0,000000</PRGP_ACQUISTI>
<ROSN_ACQUISTI>0,000000</ROSN_ACQUISTI>
<SLOV_ACQUISTI>0,000000</SLOV_ACQUISTI>
<SVIZ_ACQUISTI>977,000000</SVIZ_ACQUISTI>
<BSP_ACQUISTI>0,000000</BSP_ACQUISTI>
<MALT_ACQUISTI>125,000000</MALT_ACQUISTI>
<XAUS_ACQUISTI>0,000000</XAUS_ACQUISTI>
<XFRA_ACQUISTI>0,000000</XFRA_ACQUISTI>
<TOTALE_VENDITE>23705,464</TOTALE_VENDITE>
<NAT_VENDITE>24472,890000</NAT_VENDITE>
<CNOR_VENDITE>1798,480000</CNOR_VENDITE>
<CSUD_VENDITE>3336,172000</CSUD_VENDITE>
<NORD_VENDITE>9203,113000</NORD_VENDITE>
<SARD_VENDITE>1445,507000</SARD_VENDITE>
<SICI_VENDITE>1251,171000</SICI_VENDITE>
<SUD_VENDITE>3275,983000</SUD_VENDITE>
<AUST_VENDITE>32,000000</AUST_VENDITE>
<BRNN_VENDITE>680,094000</BRNN_VENDITE>'''
li=[]
data=re.findall("<(.*?)>(.*?)<\/.*?>",str(file_content),re.I)
#
# for datum in data:
#     print datum[0]
# print data[0]
li.append(data)

for data in li:
    print data
    for val in data:
        print val[1]
