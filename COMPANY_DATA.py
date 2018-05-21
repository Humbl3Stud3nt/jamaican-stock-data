###############################
# DO NOT EDIT THIS FILE!!!!!!!#
###############################
import datetime
from stocks import Instrument
ALL_DATA = [   Instrument("138 Student Living Jamaica Limited", "138SL", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("138 Student Living Jamaica Limited Variable Preference", "138SLVR", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("1834 Investments Limited", "1834", "JMD", "ORDINARY", "COMMUNICATIONS", None, last_updated=0.0),
    Instrument("Barita Investments Limited", "BIL", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Berger Paints Jamaica Ltd.", "BRG", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("CABLE BAHAMAS LTD FR REDEEMABLE CUMULATIVE JMD PREFERENCE SHAR", "CAB11B", "JMD", "PREFERENCE", "COMMUNICATIONS", None, last_updated=0.0),
    Instrument("Caribbean Cement Company Ltd.", "CCC", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Carreras Limited", "CAR", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("Ciboney Group Limited", "CBNY", "JMD", "ORDINARY", "TOURISM", None, last_updated=0.0),
    Instrument("GraceKennedy Limited", "GK", "JMD", "ORDINARY", "CONGLOMERATES", None, last_updated=0.0),
    Instrument("Jamaica Broilers Group", "JBG", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Jamaica Money Market Brokers Ltd 7.25%", "JMMB7.25", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("Jamaica Money Market Brokers Ltd 7.50%", "JMMB7.5", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("Jamaica Producers Group Ltd.", "JP", "JMD", "ORDINARY", "CONGLOMERATES", None, last_updated=0.0),
    Instrument("Jamaica Public Service 5% C", "JPS5C", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("Jamaica Public Service 5% D", "JPS5D", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("Jamaica Public Service Co. 5%", "JPS5", "JMD", "PREFERENCE", "", None, last_updated=0.0),
    Instrument("Jamaica Public Service Co. 6%", "JPS6", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("Jamaica Public Service Co. 9.5%", "JPS9.5", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("Jamaica Public Service Co. Ltd. 7%", "JPS7", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("Jamaica Stock Exchange", "JSE", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB GROUP 7.00% VR JMD CR PREFERENCE SHARES", "JMMBGL7.00NC", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB GROUP 7.00% VR JMD CR PREFERENCE SHARES", "JMMB7.50NC", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB GROUP 7.25% VR JMD CR PREFERENCE SHARES", "JMMBGL7.25C", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB GROUP 7.25% VR JMD CR PREFERENCE SHARES", "JMMB7.25C", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB Group Limited", "JMMBGL", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB Group Limited 7.25%", "JMMBGL7.25", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("JMMB Group Limited 7.50%", "JMMBGL7.50", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("Kingston Properties Limited", "KPREIT", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Kingston Wharves Limited", "KW", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Mayberry Investments Limited", "MIL", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("NCB FINANCIAL GROUP LIMITED", "NCBFG", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Palace Amusement Co. Ltd.", "PAL", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("PanJam Investment Limited", "PJAM", "JMD", "ORDINARY", "CONGLOMERATES", None, last_updated=0.0),
    Instrument("Portland JSX Limited", "PJX", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("PRODUCTIVE BUSINESS SOLUTIONS LTD 9.75% CUMULATIVE REDEEMABLE", "PBS9.75", "JMD", "PREFERENCE", "OTHER", None, last_updated=0.0),
    Instrument("PROVEN 8.25 CUMULATIVE REDEEMABLE PREFERENCE SHARES", "PROVEN8.25", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("Proven Investments Limited JMD", "ProvenJA", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Pulse Investments Limited", "PULS", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Radio Jamaica Limited", "RJR", "JMD", "ORDINARY", "COMMUNICATIONS", None, last_updated=0.0),
    Instrument("SAGICOR BANK JA CLASS A 7.75% CUMULATIVE REDEEMABLE PREFERENCE", "SBJPSA", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("SAGICOR BANK JA CLASS B 8.25% CUMULATIVE REDEEMABLE PREFERENCE", "SBJPSB", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("Sagicor Group Jamaica Limited", "SJ", "JMD", "ORDINARY", "CONGLOMERATES", None, last_updated=0.0),
    Instrument("Sagicor Real Estate X Fund Ltd.", "XFUND", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Salada Foods Jamaica Ltd.", "SALF", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Scotia Group Jamaica Limited", "SGJ", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Seprod Limited", "SEP", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Sterling Investments Limited", "SIL", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Supreme Ventures Limited", "SVL", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("VICTORIA MUTUAL INVESTMENTS LTD ORDINARY SHARES", "VMIL", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("WISYNCO GROUP LTD ORDINARY SHARES", "WISYNCO", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Access Financial Services Limited", "AFS", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("AMG Packaging  & Paper Company Limited", "AMG", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Blue Power Group Limited", "BPOW", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("C2W Music Limited", "MUSIC", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("CAC 2000 9.5% CUMULATIVE REDEEMABLE PREF SHARES", "CAC9.50", "JMD", "PREFERENCE", "RETAIL", None, last_updated=0.0),
    Instrument("CAC 2000 Limited", "CAC", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("Cargo Handlers Limited", "CHL", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Caribbean Cream Limited", "KREMI", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Caribbean Flavours & Fragrances Limited", "CFF", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Caribbean Producers Jamaica Limited", "CPJ", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("Consolidated Bakeries (Jamaica) Limited", "PURITY", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Derrimon Trading Company Limited", "DTL", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("DERRIMON TRADING COMPANY LTD 2021 PREF SHARES", "DTL9", "JMD", "PREFERENCE", "RETAIL", None, last_updated=0.0),
    Instrument("Dolphin Cove Limited", "DCOVE", "JMD", "ORDINARY", "TOURISM", None, last_updated=0.0),
    Instrument("ELITE DIAGNOSTIC LIMITED", "ELITE", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Eppley Limited", "EPLY", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Eppley Limited 8.25%", "EPLY8.25", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("Eppley Limited 9.5%", "EPLY9.5", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("EPPLEY LTD 8.75% PREF SHARES DUE 2023", "EPLY8.75", "JMD", "PREFERENCE", "FINANCE", None, last_updated=0.0),
    Instrument("EXPRESS CATERING LIMITED", "ECL", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("FOSRICH COMPANY LIMITED", "FOSRICH", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("General Accident Insurance Company (JA) Limited", "GENAC", "JMD", "ORDINARY", "INSURANCE", None, last_updated=0.0),
    Instrument("GWEST CORPORATION LIMITED ORDINARY SHARES", "GWEST", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Honey Bun (1982) Limited", "HONBUN", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("IronRock Insurance Company Limited", "ROC", "JMD", "ORDINARY", "INSURANCE", None, last_updated=0.0),
    Instrument("ISP Finance Services Limited", "ISP", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Jamaican Teas Limited", "JAMT", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("Jetcon Corporation Limited", "JETCON", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("K.L.E. Group Limited", "KLE", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Key Insurance Company Limited", "KEY", "JMD", "ORDINARY", "INSURANCE", None, last_updated=0.0),
    Instrument("Knutsford Express Services Limited", "KEX", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Lasco Distributors Limited", "LASD", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("Lasco Financial Services Limited", "LASF", "JMD", "ORDINARY", "FINANCE", None, last_updated=0.0),
    Instrument("Lasco Manufacturing Limited", "LASM", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("MAIN EVENT ENTERTAINMENT GROUP", "MEEG", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Medical Disposables & Supplies Limited", "MDS", "JMD", "ORDINARY", "RETAIL", None, last_updated=0.0),
    Instrument("Paramount Trading (Jamaica) Limited", "PTL", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("STATIONERY AND OFFICE SUPPLIES LIMITED", "SOS", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0),
    Instrument("Sweet River Abattoir & Supplies Company Ltd", "SRA", "JMD", "ORDINARY", "MANUFACTURING", None, last_updated=0.0),
    Instrument("tTech Limited", "TTECH", "JMD", "ORDINARY", "OTHER", None, last_updated=0.0)]