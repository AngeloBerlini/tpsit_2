from zeep import Client
from zeep.exceptions import Fault
from flask import Flask, request, render_template

app = Flask(__name__)

# soap service
url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"


def getAllISOCodes(client):
    response = client.service.ListOfCountryNamesByCode()
    return response


@app.route("/", methods=["GET", "POST"])
def load():
    result = None
    response = None
    try:
        client = Client(wsdl=url)
        if request.method == "POST":
            isocode = request.form.get("isocode", "").strip()
            service_name = request.form.get("service", "CapitalCity")
            if not isocode:
                result = "Fill in the ISO code"
            else:
                # dispatch to one of the service calls
                try:
                    if service_name == "CapitalCity":
                        response = client.service.CapitalCity(sCountryISOCode=isocode)
                    elif service_name == "CountryIntPhoneCode":
                        response = client.service.CountryIntPhoneCode(sCountryISOCode=isocode)
                    elif service_name == "FullCountryInfo":
                        # FullCountryInfo returns a complex object; convert to a dict-like representation
                        info = client.service.FullCountryInfo(sCountryISOCode=isocode)
                        # zeep objects can be converted to python dict via _asdict() or by accessing attributes
                        # build a simple dict for template rendering
                        response = {}
                        # safe attribute access
                        for attr in [
                            "sISOCode",
                            "sName",
                            "sCapitalCity",
                            "sPhoneCode",
                            "sContinentCode",
                            "sCurrencyISOCode",
                            "sCountryFlag",
                        ]:
                            try:
                                response[attr] = getattr(info, attr)
                            except Exception:
                                response[attr] = None
                    else:
                        result = f"Unknown service: {service_name}"
                except Fault as e:
                    result = f"SOAP Fault: {e}"
            return render_template("home.html.jinja", response=response, result=result)
        else:
            response = getAllISOCodes(client)
            # discover available methods
            oplist = []
            for service in client.wsdl.services.values():
                for port in service.ports.values():
                    for op in port.binding._operations.values():
                        if op.name not in oplist:
                            oplist.append(op.name)
            return render_template("home.html.jinja", countries=response, oplist=oplist)
    except Fault as exception:
        return f"Errore SOAP: {exception}"


# pip install zeep
# rif. https://docs.python-zeep.org/en/master/
if __name__ == "__main__":
    app.run()