"""
BioXen Time Simulator - Pure Earth Time Cycles for Biological VMs

This module simulates Earth's natural temporal cycles (rotation, orbit, lunar phases)
to provide environmental cues for circadian rhythm modeling in biological VMs.
"""

import time
import math
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class CyclePhase(Enum):
    """Phases based on Earth's astronomical cycles"""
    SOLAR_DAY = "solar_day"          # ~24 hours (Earth's rotation)
    SOLAR_NIGHT = "solar_night"
    LUNAR_NEW = "lunar_new"          # Lunar cycle phases
    LUNAR_WAXING = "lunar_waxing"
    LUNAR_FULL = "lunar_full"
    LUNAR_WANING = "lunar_waning"
    SEASONAL_SPRING = "seasonal_spring"  # Orbital seasons
    SEASONAL_SUMMER = "seasonal_summer"
    SEASONAL_AUTUMN = "seasonal_autumn"
    SEASONAL_WINTER = "seasonal_winter"


@dataclass
class TemporalState:
    """Complete temporal state of the simulated Earth environment"""
    solar_phase: CyclePhase
    lunar_phase: CyclePhase
    seasonal_phase: CyclePhase
    light_intensity: float      # 0.0-1.0 (solar irradiance)
    lunar_illumination: float   # 0.0-1.0 (moonlight intensity)
    seasonal_resource_factor: float  # 0.5-1.5 (resource availability)
    temperature_modifier: float     # -10.0 to +10.0 °C
    gravitational_tide_factor: float  # 0.95-1.05 (lunar gravitational effects)
    simulation_time_elapsed: float   # Total simulated seconds


class TimeSimulator:
    """
    Simulates Earth's natural temporal cycles for biological rhythm modeling.

    Uses astronomical constants to provide pure temporal cues that biological
    VMs can respond to, enabling accurate circadian and circannual rhythm studies.
    """

    # Astronomical constants (in seconds)
    SOLAR_DAY_LENGTH = 86164.0905    # Mean solar day (23h 56m 4.0905s)
    SIDEREAL_DAY_LENGTH = 86164.0905  # Same as solar for simplicity
    LUNAR_SYNODIC_MONTH = 2551442.8   # Synodic month (~29.53 days)
    TROPICAL_YEAR = 31556925.445     # Tropical year (~365.242 days)

    def __init__(self,
                 latitude: float = 37.7749,  # San Francisco (radians would be better)
                 longitude: float = -122.4194,
                 start_time: Optional[float] = None,
                 time_acceleration: float = 1.0):
        """
        Initialize the time simulator.

        Args:
            latitude: Geographic latitude in degrees (-90 to 90)
            longitude: Geographic longitude in degrees (-180 to 180)
            start_time: Simulation start time (Unix timestamp, defaults to now)
            time_acceleration: Speed multiplier (1.0 = real Earth time)
        """
        self.latitude = math.radians(latitude)  # Convert to radians
        self.longitude = math.radians(longitude)
        self.start_time = start_time or time.time()
        self.time_acceleration = time_acceleration

        # Pre-compute some constants
        self._solar_day_radians = 2 * math.pi / self.SOLAR_DAY_LENGTH
        self._lunar_month_radians = 2 * math.pi / self.LUNAR_SYNODIC_MONTH
        self._year_radians = 2 * math.pi / self.TROPICAL_YEAR

    def get_current_state(self) -> TemporalState:
        """
        Get the complete temporal state of the simulated environment.

        Returns:
            TemporalState with all current environmental conditions
        """
        elapsed = (time.time() - self.start_time) * self.time_acceleration

        solar_phase = self._get_solar_phase(elapsed)
        lunar_phase = self._get_lunar_phase(elapsed)
        seasonal_phase = self._get_seasonal_phase(elapsed)

        light_intensity = self._calculate_light_intensity(elapsed)
        lunar_illumination = self._calculate_lunar_illumination(elapsed)
        seasonal_resource_factor = self._calculate_seasonal_resources(elapsed)
        temperature_modifier = self._calculate_temperature_modifier(elapsed)
        gravitational_tide_factor = self._calculate_tidal_factor(elapsed)

        return TemporalState(
            solar_phase=solar_phase,
            lunar_phase=lunar_phase,
            seasonal_phase=seasonal_phase,
            light_intensity=light_intensity,
            lunar_illumination=lunar_illumination,
            seasonal_resource_factor=seasonal_resource_factor,
            temperature_modifier=temperature_modifier,
            gravitational_tide_factor=gravitational_tide_factor,
            simulation_time_elapsed=elapsed
        )

    def _get_solar_phase(self, elapsed: float) -> CyclePhase:
        """Determine solar day/night phase based on Earth's rotation."""
        solar_fraction = (elapsed % self.SOLAR_DAY_LENGTH) / self.SOLAR_DAY_LENGTH
        return CyclePhase.SOLAR_DAY if solar_fraction < 0.5 else CyclePhase.SOLAR_NIGHT

    def _get_lunar_phase(self, elapsed: float) -> CyclePhase:
        """Determine lunar phase based on Earth-Moon synodic cycle."""
        lunar_fraction = (elapsed % self.LUNAR_SYNODIC_MONTH) / self.LUNAR_SYNODIC_MONTH

        if lunar_fraction < 0.125:
            return CyclePhase.LUNAR_NEW
        elif lunar_fraction < 0.375:
            return CyclePhase.LUNAR_WAXING
        elif lunar_fraction < 0.625:
            return CyclePhase.LUNAR_FULL
        elif lunar_fraction < 0.875:
            return CyclePhase.LUNAR_WANING
        else:
            return CyclePhase.LUNAR_NEW

    def _get_seasonal_phase(self, elapsed: float) -> CyclePhase:
        """Determine seasonal phase based on Earth's orbit around Sun."""
        year_fraction = (elapsed % self.TROPICAL_YEAR) / self.TROPICAL_YEAR

        if year_fraction < 0.25:
            return CyclePhase.SEASONAL_WINTER
        elif year_fraction < 0.5:
            return CyclePhase.SEASONAL_SPRING
        elif year_fraction < 0.75:
            return CyclePhase.SEASONAL_SUMMER
        else:
            return CyclePhase.SEASONAL_AUTUMN

    def _calculate_light_intensity(self, elapsed: float) -> float:
        """
        Calculate solar irradiance based on time of day and latitude.

        Uses simplified sinusoidal model with latitude correction.
        """
        solar_fraction = (elapsed % self.SOLAR_DAY_LENGTH) / self.SOLAR_DAY_LENGTH

        # Base sinusoidal light curve - shift to start at sunrise (6am = 0.25)
        # sin(π * (fraction - 0.25)) shifted to positive values
        phase_shifted = (solar_fraction + 0.75) % 1.0  # Shift so peak is at noon
        base_intensity = max(0.0, math.sin(2 * math.pi * phase_shifted - math.pi/2))

        # Latitude correction (simplified - polar regions have extremes)
        latitude_factor = math.cos(self.latitude)

        # Ensure non-negative and scale to 0-1
        result = max(0.0, min(1.0, base_intensity * latitude_factor))
        return result

    def _calculate_lunar_illumination(self, elapsed: float) -> float:
        """Calculate moonlight intensity based on lunar phase."""
        lunar_fraction = (elapsed % self.LUNAR_SYNODIC_MONTH) / self.LUNAR_SYNODIC_MONTH

        # Lunar illumination follows triangular wave (simplified)
        if lunar_fraction < 0.5:
            return 2 * lunar_fraction  # Waxing
        else:
            return 2 * (1 - lunar_fraction)  # Waning

    def _calculate_seasonal_resources(self, elapsed: float) -> float:
        """Calculate resource availability based on seasonal cycle."""
        year_fraction = (elapsed % self.TROPICAL_YEAR) / self.TROPICAL_YEAR

        # Resource availability peaks in summer, troughs in winter
        seasonal_variation = math.sin(2 * math.pi * year_fraction)

        # Scale to 0.5-1.5 range
        return 1.0 + 0.5 * seasonal_variation

    def _calculate_temperature_modifier(self, elapsed: float) -> float:
        """Calculate temperature variation based on seasonal cycle."""
        year_fraction = (elapsed % self.TROPICAL_YEAR) / self.TROPICAL_YEAR

        # Temperature follows seasonal sine wave
        seasonal_temp = 20 * math.sin(2 * math.pi * (year_fraction - 0.25))  # Peak in summer

        # Add latitude-based baseline modification
        latitude_temp_modifier = -10 * math.cos(self.latitude)  # Colder at poles

        return seasonal_temp + latitude_temp_modifier

    def _calculate_tidal_factor(self, elapsed: float) -> float:
        """
        Calculate gravitational tidal effects from lunar cycle.

        Affects membrane potential, ion transport, etc. in biological systems.
        """
        lunar_fraction = (elapsed % self.LUNAR_SYNODIC_MONTH) / self.LUNAR_SYNODIC_MONTH

        # Tidal force varies with lunar phase (simplified)
        tidal_amplitude = 0.05  # ±5% variation
        tidal_variation = tidal_amplitude * math.sin(2 * math.pi * lunar_fraction)

        return 1.0 + tidal_variation

    def advance_time(self, delta_seconds: float):
        """
        Manually advance simulation time.

        Args:
            delta_seconds: Seconds to advance (in simulated time)
        """
        self.start_time -= delta_seconds / self.time_acceleration

    def set_acceleration(self, acceleration: float):
        """
        Set time acceleration factor.

        Args:
            acceleration: New acceleration factor (1.0 = real time)
        """
        self.time_acceleration = acceleration

    def get_circadian_phase(self) -> float:
        """Get current circadian phase (0-1, where 0 = dawn, 0.5 = dusk)."""
        elapsed = (time.time() - self.start_time) * self.time_acceleration
        solar_fraction = (elapsed % self.SOLAR_DAY_LENGTH) / self.SOLAR_DAY_LENGTH
        return solar_fraction

    def get_circannual_phase(self) -> float:
        """Get current circannual phase (0-1, where 0 = winter solstice)."""
        elapsed = (time.time() - self.start_time) * self.time_acceleration
        year_fraction = (elapsed % self.TROPICAL_YEAR) / self.TROPICAL_YEAR
        return year_fraction

    def __repr__(self) -> str:
        state = self.get_current_state()
        return (f"TimeSimulator(lat={math.degrees(self.latitude):.2f}°, "
                f"lon={math.degrees(self.longitude):.2f}°, "
                f"elapsed={state.simulation_time_elapsed:.0f}s, "
                f"phase={state.solar_phase.value})")