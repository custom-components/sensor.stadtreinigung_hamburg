import pytest
from homeassistant.setup import async_setup_component
from homeassistant.const import STATE_UNKNOWN

@pytest.mark.asyncio
async def test_setup(hass, enable_custom_integrations):
    """Test that the component can be setup and creates sensors."""
    config = {
        'stadtreinigung_hamburg': {
            'name': 'Test Sensor',
            'street': 'Jungfernstieg',
            'number': '1',
        }
    }
    assert await async_setup_component(hass, 'stadtreinigung_hamburg', config)
    await hass.async_block_till_done()

    # Check that the component is loaded
    assert 'stadtreinigung_hamburg' in hass.config.components

    # Verify that sensors are created
    state = hass.states.get('sensor.test_sensor')
    assert state is not None
    assert state.state != STATE_UNKNOWN

