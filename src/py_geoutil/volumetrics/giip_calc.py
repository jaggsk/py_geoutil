from ..utils.validation import validate_string,validate_number,validate_fraction
from ..conversions import convert_ft3_m3,convert_m3_ft3,convert_sm3_boe,convert_cf_boe

def calculate_giip(grv:float = None,
                   grv_units: str = "ft3",
                   por: float = None,
                   ng:float = None,
                   water_sat:float = None,
                   bg:float = None,
                   bg_units: str= "1/bg",
                   wet_gas_shrinkage: float = None,
                   condensate_yield:float = None,
                   rec_factor:float = None,
                   rec_factor_condensate:float =None):
    
    """
    Docstring for calculate_giip
    
    :param grv: Description
    :type grv: float
    :param grv_units: Description
    :type grv_units: str
    :param por: Description
    :type por: float
    :param por_units: Description
    :type por_units: float
    :param ng: Description
    :type ng: float
    :param ng_units: Description
    :type ng_units: float
    :param gas_sat: Description
    :type gas_sat: float
    :param gas_sat_units: Description
    :type gas_sat_units: float
    :param bg: Description
    :type bg: float
    :param bg_units: Description
    :type bg_units: str
    """

    giip_dict = {}

    validate_string(grv_units, ["ft3", "m3"],name="GRV UNits")
    validate_number(por,name="Porosity")
    validate_number(ng,name="Net:Gross")
    validate_number(water_sat,name="Water Saturation")
    validate_number(condensate_yield,name="Condensate Yield")
    validate_number(rec_factor,name="Recovery Factor")
    validate_number(rec_factor_condensate,name="Recovery Factor Condensate")

    validate_fraction(por, name="Porosity")
    validate_fraction(ng, name="Net:Gross")
    validate_fraction(water_sat, name="Water Saturation")
    validate_fraction(rec_factor, name="Recovery Factor")
    validate_fraction(rec_factor_condensate, name="Recovery Factor Condensate")

    if grv_units == "ft3":
        grv = convert_ft3_m3(grv)
        grv = grv / 1000000
    elif grv_units == "m3":
        #Comvert m3 to 1E6m3
        grv = grv / 1000000

    nrv = grv * ng 
    hcpv = nrv * por * (1-water_sat)
    giip = hcpv * bg * wet_gas_shrinkage

    giip_dict["GRV 1E6 m3"] = grv
    giip_dict["NRV 1E6 m3"] = nrv
    giip_dict["HCPV 1E6 m3"] = hcpv
    #giip_dict["GIIP 1e6 Sm3"] = giip
    giip_dict["GIIP 1e9 Sm3"] = (giip * wet_gas_shrinkage) / 1000
    giip_dict["GIIP BCF"] = convert_m3_ft3(giip_dict["GIIP 1e9 Sm3"])
    giip_dict["Accumulation Size HC Liquid 1E6 Sm3"] = (condensate_yield * (giip_dict["GIIP 1e9 Sm3"]*1000))/1000000
    giip_dict["Accumulation Size HC Liquid 1E6 STB"] = convert_sm3_boe(giip_dict["Accumulation Size HC Liquid 1E6 Sm3"])
    giip_dict["Accumulation Size Total Resources 1E6 STB OE"] = convert_cf_boe(giip_dict["GIIP BCF"]*1000000)/1000000

    giip_dict["Recoverable Gas BCF"] = giip_dict["GIIP BCF"] * rec_factor
    giip_dict["Recoverable Condensate 1E6 Sm3"] = giip_dict["Accumulation Size HC Liquid 1E6 Sm3"] * rec_factor_condensate
    giip_dict["Recoverable Condensate 1E6 STB"] = convert_sm3_boe(giip_dict["Recoverable Condensate 1E6 Sm3"])
    giip_dict["Recoverable Accumulation Size Total Resources 1E6 STB OE"] = (convert_cf_boe(giip_dict["Recoverable Gas BCF"]*1000000)/1000000) + giip_dict["Recoverable Condensate 1E6 STB"]

    return giip_dict