from unittest.mock import ANY, patch
from .data import (
    SAMPLE_INTENSITY_DATA,
    SAMPLE_INTERVAL_DATA,
    SAMPLE_METER_RESPONSE,
)
from src.energy_consumption.main import get_energy_consumption_details


@patch(
    "src.energy_consumption.open_volt_api.meters.retrieve_meter",
    lambda *args: SAMPLE_METER_RESPONSE,
)
@patch(
    "src.energy_consumption.open_volt_api.intervals.get_interval_data",
    lambda *args: SAMPLE_INTERVAL_DATA,
)
@patch(
    "src.energy_consumption.carbon_intensity_api.regional_intensity.get_regional_intensity_by_postcode",
    lambda *args: SAMPLE_INTENSITY_DATA,
)
def test_get_energy_consumption_details():
    # Given
    meter_id = "6514167223e3d1424bf82742"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    expected_total_energy_consumed = 102046.0
    expected_total_emissions = 16845.035
    expected_fuel_mix_percentage_breakdown = {
        "biomass": 1.253528800736922,
        "coal": 0.9184544225153366,
        "gas": 28.747268878740936,
        "hydro": 1.0532191364678671,
        "imports": 21.484101287654592,
        "nuclear": 11.409642710150333,
        "other": 0.0,
        "solar": 1.4443554867412725,
        "wind": 33.68628755659213,
    }
    # When
    result = get_energy_consumption_details(
        meter_id=meter_id, start_date=start_date, end_date=end_date
    )

    # Then
    assert result.get("meter_id") == meter_id
    assert result.get("start_date") == start_date
    assert result.get("end_date") == end_date
    assert result.get("total_energy_consumed") == expected_total_energy_consumed
    assert result.get("energy_consumption_unit") == "kWh"
    assert result.get("total_emissions") == expected_total_emissions
    assert result.get("emissions_unit") == "kg CO2"
    assert result.get("fuel_mix_percentage_breakdown") == expected_fuel_mix_percentage_breakdown
