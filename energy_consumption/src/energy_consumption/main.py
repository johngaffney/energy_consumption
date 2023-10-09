from datetime import datetime, timedelta
from .open_volt_api.intervals import get_interval_data
from .carbon_intensity_api.regional_intensity import (
    get_regional_intensity_by_postcode,
)
from .open_volt_api.meters import retrieve_meter
from .utils import get_customer_post_code_from_address


# Function returns energy consumption details for a meter in a given date range
# The monthly energy consumed by the building (kWh)
# The amount of CO2 (kgs) emitted by the electricity generated for the building.
# The % of fuel mix (wind/solar/nuclear/coal/etc) used to generate the electricity.
def get_energy_consumption_details(meter_id: str, start_date: str, end_date: str) -> dict:
    total_consumption_kwh = 0
    total_emissions_kg_co2_kwh = 0
    fuel_mix_breakdown = {}
    emissions_g_co2_kwh = 0

    # get customer postcode from meter
    meter_details = retrieve_meter(meter_id=meter_id)
    customer = meter_details.get("customer", {})
    post_code = get_customer_post_code_from_address(customer_address=customer.get("address"))

    # get usage data for meter in hh periods
    adjusted_end_datetime = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    adjusted_end_date = adjusted_end_datetime.strftime("%Y-%m-%d")
    usage_interval_data = get_interval_data(
        meter_id=meter_id, start_date=start_date, end_date=adjusted_end_date, granularity="hh"
    )
    usage_data_by_hh_dict = create_hh_usage_interval_dict(usage_interval_data=usage_interval_data)

    interval_start_date_utc = datetime.strptime(start_date, "%Y-%m-%d")
    num_of_days_in_request_period = (adjusted_end_datetime - interval_start_date_utc).days

    # Get regional intensity for each day in request period
    for day_in_request_period in (
        interval_start_date_utc + timedelta(days=(1 * day_count))
        for day_count in range(num_of_days_in_request_period)
    ):
        next_day = day_in_request_period + timedelta(days=1)
        day_response = get_regional_intensity_by_postcode(
            postcode=post_code,
            start_time=day_in_request_period.isoformat(),
            end_time=next_day.isoformat(),
        ).get("data", [])

        # For each hh period in day, add emissions to total emissions and add to hh period dict
        for hh_period in day_response.get("data", []):
            hh_period_start = datetime.strptime(
                hh_period.get("from"), "%Y-%m-%dT%H:%M%z"
            ).isoformat()
            if usage_data_by_hh_dict.get(hh_period_start):
                # TODO: actual is not being returned by api currently
                intensity_g_c02_kwh = float(
                    hh_period.get("intensity", {}).get("actual")
                    or hh_period.get("intensity", {}).get("forecast")
                )
                hh_period_consumption_kwh = usage_data_by_hh_dict.get(hh_period_start).get(
                    "consumption", 0
                )
                hh_period_emissions_g_co2_kwh = intensity_g_c02_kwh * hh_period_consumption_kwh
                usage_data_by_hh_dict[hh_period_start][
                    "hh_period_emissions_g_co2_kwh"
                ] = hh_period_emissions_g_co2_kwh
                usage_data_by_hh_dict[hh_period_start]["intensity_g_c02_kwh"] = intensity_g_c02_kwh
                emissions_g_co2_kwh = emissions_g_co2_kwh + hh_period_emissions_g_co2_kwh
                total_consumption_kwh = total_consumption_kwh + hh_period_consumption_kwh

                for fuel_type in hh_period.get("generationmix", []):
                    fuel = fuel_type.get("fuel")
                    fuel_kwh_used = hh_period_consumption_kwh * fuel_type.get("perc") / 100
                    fuel_mix_breakdown[fuel] = fuel_mix_breakdown.get(fuel, 0) + fuel_kwh_used

    # Calculate percentage breakdown of fuel mix
    fuel_mix_percentage_breakdown = {
        fuel: (100 / total_consumption_kwh * fuel_mix_breakdown.get(fuel, 0))
        for fuel in fuel_mix_breakdown
    }

    total_emissions_kg_co2_kwh = emissions_g_co2_kwh / 1000
    energy_consumption_details = {
        "meter_id": meter_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_energy_consumed": total_consumption_kwh,
        "energy_consumption_unit": "kWh",
        "total_emissions": total_emissions_kg_co2_kwh,
        "emissions_unit": "kg CO2",
        "fuel_mix_percentage_breakdown": fuel_mix_percentage_breakdown,
    }

    return energy_consumption_details


def create_hh_usage_interval_dict(usage_interval_data: dict):
    usage_data_by_hh_dict = {}
    for interval_data in usage_interval_data.get("data", []):
        start_interval = interval_data.get("start_interval")
        interval_start_date = datetime.strptime(start_interval, "%Y-%m-%dT%H:%M:%S.%f%z")
        consumption = interval_data.get("consumption")
        consumption_units = interval_data.get("consumption_units")
        usage_data_by_hh_dict[interval_start_date.isoformat()] = {
            "consumption": float(consumption),
            "start_interval": start_interval,
            "consumption_units": consumption_units,
        }
    return usage_data_by_hh_dict
