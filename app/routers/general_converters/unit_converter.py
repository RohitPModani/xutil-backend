from fastapi import APIRouter, HTTPException
from app.schemas.general_converters.area_converter_schema import AreaConvertRequest, AreaConvertResponse, UNIT_TO_SQUARE_METERS
from ...schemas.general_converters.angle_converter_schema import AngleConvertRequest, AngleConvertResponse, UNIT_TO_RADIANS
from ...schemas.general_converters.bit_byte_converter_schema import BitByteConvertRequest, BitByteConvertResponse, UNIT_TO_BITS
from ...schemas.general_converters.energy_converter_schema import EnergyConvertRequest, EnergyConvertResponse, UNIT_TO_JOULES
from ...schemas.general_converters.frequency_converter_schema import FrequencyConvertRequest, FrequencyConvertResponse, UNIT_TO_HERTZ
from ...schemas.general_converters.fuel_economy_converter_schema import FuelEconomyConvertRequest, FuelEconomyConvertResponse, UNIT_TO_KM_PER_LITER
from ...schemas.general_converters.length_converter_schema import LengthConvertRequest, LengthConvertResponse, UNIT_TO_METERS
from ...schemas.general_converters.power_converter_schema import PowerConvertRequest, PowerConvertResponse, UNIT_TO_WATTS
from ...schemas.general_converters.pressure_converter_schema import PressureConvertRequest, PressureConvertResponse, UNIT_TO_PASCALS
from ...schemas.general_converters.speed_converter_schema import SpeedConvertRequest, SpeedConvertResponse, UNIT_TO_METERS_PER_SECOND
from ...schemas.general_converters.temperature_converter_schema import TemperatureConvertRequest, TemperatureConvertResponse, TEMPERATURE_UNITS
from ...schemas.general_converters.time_converter_scehma import TimeConvertRequest, TimeConvertResponse, UNIT_TO_SECONDS
from ...schemas.general_converters.volume_converter_schema import VolumeConvertRequest, VolumeConvertResponse, UNIT_TO_LITERS
from ...schemas.general_converters.weight_converter_schema import WeightConvertRequest, WeightConvertResponse, UNIT_TO_GRAMS
from ...crud.general_converters.unit_converter_crud import convert_unit_logic

router = APIRouter(prefix="/unit-converter", tags=["General Converters"])

@router.post("/angle", response_model=AngleConvertResponse)
async def convert_angle(data: AngleConvertRequest) -> AngleConvertResponse:
    """
    Convert angle between different units (deg, rad, grad, arcmin, arcsec, turn).
    
    Args:
        data: AngleConvertRequest containing value and unit
        
    Returns:
        AngleConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or angle value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_RADIANS, response_class=AngleConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/area", response_model=AreaConvertResponse)
async def convert_area(data: AreaConvertRequest) -> AreaConvertResponse:
    """
    Convert area between different units (m², km², ft², yd², acre, hectare).
    
    Args:
        data: AreaConvertRequest containing value and unit
        
    Returns:
        AreaConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or area value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_SQUARE_METERS, response_class=AreaConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/bit-byte", response_model=BitByteConvertResponse)
async def convert_bit_byte(data: BitByteConvertRequest) -> BitByteConvertResponse:
    """
    Convert between bit/byte units (Bit, Byte, Kb, KB, Mb, MB, Gb, GB, Tb, TB, Pb, PB).
    
    Args:
        data: BitByteConvertRequest containing value and unit
        
    Returns:
        BitByteConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If the input unit is invalid
    """
    return convert_unit_logic(data=data, conversion_dict=UNIT_TO_BITS, response_class=BitByteConvertResponse)

@router.post("/energy", response_model=EnergyConvertResponse)
async def convert_energy(data: EnergyConvertRequest) -> EnergyConvertResponse:
    """
    Convert energy between different units (j, kj, cal, kcal, wh, kwh, ev, btu).
    
    Args:
        data: EnergyConvertRequest containing value and unit
        
    Returns:
        EnergyConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or energy value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_JOULES, response_class=EnergyConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error 관심: {str(e)}")
    
@router.post("/frequency", response_model=FrequencyConvertResponse)
async def convert_frequency(data: FrequencyConvertRequest) -> FrequencyConvertResponse:
    """
    Convert frequency between different units (hz, khz, mhz, ghz, rpm).
    
    Args:
        data: FrequencyConvertRequest containing value and unit
        
    Returns:
        FrequencyConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or frequency value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_HERTZ, response_class=FrequencyConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/fuel-economy", response_model=FuelEconomyConvertResponse)
async def convert_fuel_economy(data: FuelEconomyConvertRequest) -> FuelEconomyConvertResponse:
    """
    Convert fuel economy between different units (mpg_us, mpg_uk, km_l, l_100km).
    
    Args:
        data: FuelEconomyConvertRequest containing value and unit
        
    Returns:
        FuelEconomyConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or fuel economy value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_KM_PER_LITER, response_class=FuelEconomyConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/length", response_model=LengthConvertResponse)
async def convert_length(data: LengthConvertRequest) -> LengthConvertResponse:
    """
    Convert length between different units (mm, cm, m, km, in, ft, yd, mi, nm).
    
    Args:
        data: LengthConvertRequest containing value and unit
        
    Returns:
        LengthConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or length value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_METERS, response_class=LengthConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/power", response_model=PowerConvertResponse)
async def convert_power(data: PowerConvertRequest) -> PowerConvertResponse:
    """
    Convert power between different units (W, kW, hp_metric, hp_imperial, MW, ft-lb/s).
    
    Args:
        data: PowerConvertRequest containing value and unit
        
    Returns:
        PowerConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or power value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_WATTS, response_class=PowerConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/pressure", response_model=PressureConvertResponse)
async def convert_pressure(data: PressureConvertRequest) -> PressureConvertResponse:
    """
    Convert pressure between different units (Pa, kPa, atm, bar, mbar, psi, mmHg, torr).
    
    Args:
        data: PressureConvertRequest containing value and unit
        
    Returns:
        PressureConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or pressure value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_PASCALS, response_class=PressureConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/speed", response_model=SpeedConvertResponse)
async def convert_speed(data: SpeedConvertRequest) -> SpeedConvertResponse:
    """
    Convert speed between different units (m_s, km_h, mph, ft_s, kn).
    
    Args:
        data: SpeedConvertRequest containing value and unit
        
    Returns:
        SpeedConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or speed value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_METERS_PER_SECOND, response_class=SpeedConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/temperature", response_model=TemperatureConvertResponse)
async def convert_temperature(data: TemperatureConvertRequest) -> TemperatureConvertResponse:
    """
    Convert temperature between different units (Celsius, Fahrenheit, Kelvin).
    
    Args:
        data: TemperatureConvertRequest containing value and unit
        
    Returns:
        TemperatureConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or temperature value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=TEMPERATURE_UNITS, response_class=TemperatureConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/time", response_model=TimeConvertResponse)
async def convert_time(data: TimeConvertRequest) -> TimeConvertResponse:
    """
    Convert time between different units (ns, μs, ms, s, min, hr, day, week, month, year, decade, century).
    
    Args:
        data: TimeConvertRequest containing value and unit
        
    Returns:
        TimeConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If the input unit is invalid
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_SECONDS, response_class=TimeConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/volume", response_model=VolumeConvertResponse)
async def convert_volume(data: VolumeConvertRequest) -> VolumeConvertResponse:
    """
    Convert volume between different units (m3, cm3, l, ml, ft3, in3, gal, qt, pt, fl_oz).
    
    Args:
        data: VolumeConvertRequest containing value and unit
        
    Returns:
        VolumeConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or volume value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_LITERS, response_class=VolumeConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/weight", response_model=WeightConvertResponse)
async def convert_weight(data: WeightConvertRequest) -> WeightConvertResponse:
    """
    Convert weight between different units (mg, g, kg, t, oz, lb, st).
    
    Args:
        data: WeightConvertRequest containing value and unit
        
    Returns:
        WeightConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or weight value)
    """
    try:
        return convert_unit_logic(data=data, conversion_dict=UNIT_TO_GRAMS, response_class=WeightConvertResponse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")