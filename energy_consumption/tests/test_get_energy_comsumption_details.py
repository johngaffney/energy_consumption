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
    expected_total_energy_consumed = 98613.0
    expected_total_emissions = 16304.841
    expected_fuel_mix_percentage_breakdown = {
        "biomass": 1.1707067019561315,
        "coal": 0.8912029854076032,
        "gas": 28.87762972427569,
        "hydro": 1.0643667670591093,
        "imports": 21.859328891728264,
        "nuclear": 11.330397614918931,
        "other": 0.0,
        "solar": 1.4082788273351368,
        "wind": 33.3952633019987,
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
    assert result.get("emissions_unit") == "kg CO2/kWh"
    assert result.get("fuel_mix_percentage_breakdown") == expected_fuel_mix_percentage_breakdown
