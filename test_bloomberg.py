import blpapi

SESSION_OPTIONS = blpapi.SessionOptions()
SESSION_OPTIONS.setServerHost("localhost")
SESSION_OPTIONS.setServerPort(8194)

session = blpapi.Session(SESSION_OPTIONS)
if not session.start():
    print("FAILED to start session — is Bloomberg running?")
    exit(1)

if not session.openService("//blp/refdata"):
    print("FAILED to open refdata service")
    exit(1)

service = session.getService("//blp/refdata")

# Test 1: BDP — single snapshot fields
print("=== BDP Test (KO) ===")
request = service.createRequest("ReferenceDataRequest")
request.append("securities", "KO US Equity")
request.append("fields", "NAME")
request.append("fields", "PX_LAST")
request.append("fields", "CUR_MKT_CAP")
request.append("fields", "GICS_SECTOR_NAME")
request.append("fields", "BETA_RAW_OVERRIDABLE")
request.append("fields", "PE_RATIO")
request.append("fields", "BEST_TARGET_PRICE")
request.append("fields", "BEST_ANALYST_RATING")

session.sendRequest(request)

while True:
    event = session.nextEvent(500)
    for msg in event:
        if msg.hasElement("securityData"):
            data = msg.getElement("securityData")
            for i in range(data.numValues()):
                sec = data.getValueAsElement(i)
                fields = sec.getElement("fieldData")
                print(f"  Name: {fields.getElementAsString('NAME')}")
                print(f"  Price: {fields.getElementAsFloat('PX_LAST')}")
                print(f"  Mkt Cap: {fields.getElementAsFloat('CUR_MKT_CAP')}")
                print(f"  Sector: {fields.getElementAsString('GICS_SECTOR_NAME')}")
                print(f"  Beta: {fields.getElementAsFloat('BETA_RAW_OVERRIDABLE')}")
                print(f"  P/E: {fields.getElementAsFloat('PE_RATIO')}")
                print(f"  Target: {fields.getElementAsFloat('BEST_TARGET_PRICE')}")
                print(f"  Rating: {fields.getElementAsFloat('BEST_ANALYST_RATING')}")
    if event.eventType() == blpapi.Event.RESPONSE:
        break

# Test 2: BDS — peer list
print("\n=== BDS Test (KO Peers) ===")
request = service.createRequest("ReferenceDataRequest")
request.append("securities", "KO US Equity")
request.append("fields", "PEER_RANKED_LIST")

session.sendRequest(request)

while True:
    event = session.nextEvent(500)
    for msg in event:
        if msg.hasElement("securityData"):
            data = msg.getElement("securityData")
            for i in range(data.numValues()):
                sec = data.getValueAsElement(i)
                fields = sec.getElement("fieldData")
                if fields.hasElement("PEER_RANKED_LIST"):
                    peers = fields.getElement("PEER_RANKED_LIST")
                    for j in range(peers.numValues()):
                        peer = peers.getValueAsElement(j)
                        print(f"  {peer}")
    if event.eventType() == blpapi.Event.RESPONSE:
        break

# Test 3: BDH — historical financials
print("\n=== BDH Test (KO 3yr Revenue) ===")
request = service.createRequest("HistoricalDataRequest")
request.append("securities", "KO US Equity")
request.append("fields", "SALES_REV_TURN")
request.append("fields", "NET_INCOME")
request.append("fields", "IS_DILUTED_EPS")
request.set("startDate", "20220101")
request.set("endDate", "20251231")
request.set("periodicitySelection", "YEARLY")

overrides = request.getElement("overrides")
override = overrides.appendElement()
override.setElement("fieldId", "FUND_PER")
override.setElement("value", "FY")

session.sendRequest(request)

while True:
    event = session.nextEvent(500)
    for msg in event:
        if msg.hasElement("securityData"):
            sec = msg.getElement("securityData")
            if sec.hasElement("fieldData"):
                data = sec.getElement("fieldData")
                for i in range(data.numValues()):
                    row = data.getValueAsElement(i)
                    date = row.getElementAsString("date")
                    rev = row.getElementAsFloat("SALES_REV_TURN") if row.hasElement("SALES_REV_TURN") else "N/A"
                    ni = row.getElementAsFloat("NET_INCOME") if row.hasElement("NET_INCOME") else "N/A"
                    eps = row.getElementAsFloat("IS_DILUTED_EPS") if row.hasElement("IS_DILUTED_EPS") else "N/A"
                    print(f"  {date}: Revenue={rev}  NI={ni}  EPS={eps}")
    if event.eventType() == blpapi.Event.RESPONSE:
        break

session.stop()
print("\nDone — Bloomberg connection works!")
