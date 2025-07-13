from pydantic import BaseModel, Field
import asyncio
from bleak import BleakClient
from typing import Optional, List
from config import WRITE_UUID


def from_hex_string(hex_str: str) -> bytes:
    # Converts a hex string like '222001' to bytes
    return bytes.fromhex(hex_str)

def percent_to_hex(percentage):
    """
    Converts a percentage (0-100) to a two-digit hexadecimal string.

    Args:
        percentage (float or int): The percentage value, from 0 to 100.

    Returns:
        str: A two-digit hexadecimal string (e.g., "00", "FF").
             Returns None if the input is outside the valid range.
    """
    if not (0 <= percentage <= 100):
        return None  # Or raise an error for invalid input

    # Scale the percentage to an 8-bit integer (0-255)
    # 100% corresponds to 255, 0% to 0
    scaled_value = int(round((percentage / 100) * 255))

    # Convert the integer to a two-digit hexadecimal string
    # The '02X' format specifier ensures two digits and uppercase hex
    hex_string = "{:02X}".format(scaled_value)
    return hex_string
    
class BLECommand(BaseModel):
    """Base BLE command class."""
    client: BleakClient 
    delay_ms: Optional[float] = .5 # delay after sending command
    class Config:
            arbitrary_types_allowed = True

# connection sequence 
class InitConnectionCommand(BLECommand):
    hex_command: str # = Field(regex=r"^[0-9A-Fa-f]{6}$")

    async def run(self):
        if self.client.is_connected:
            print("running sub commands")

            await self.client.write_gatt_char(WRITE_UUID, 
                                               from_hex_string(self.hex_command), response=False)
            await asyncio.sleep(self.delay_ms)
        else:
            print("Client is not connected")
        
class InitConnectionSequence(BLECommand):
        client: BleakClient
        sequence: List[dict] = Field(default_factory=lambda: [
                                                {'hex_command': '222001', 'delay_ms': .5},
                                                {'hex_command': '27420f4444001f00', 'delay_ms': .01},
                                                {'hex_command': '27420f4444001802', 'delay_ms': .5},
                                                {'hex_command': '27420f4444001f00', 'delay_ms': .01},
                                                {'hex_command': '27420f4444001802', 'delay_ms': 1.0},
                                            ])
        class Config:
            arbitrary_types_allowed = True

        async def run(self):
            print("running init connection sequence")
            if self.client.is_connected:
                for command in self.sequence:
                    print(f"Running command: {command['hex_command']} with delay {command['delay_ms']}")

                    connectionCommand = InitConnectionCommand(
                                            hex_command = command['hex_command'],
                                            delay_ms = command['delay_ms'],
                                            client = self.client
                                        )
                    await connectionCommand.run()
                    
            else:
                print("Client is not connected")

# move_motion 
class MotorControl(BLECommand):
    motor_forward: bool # 0, forward and 8 is backward
    motor_power: int

    class Config:
                arbitrary_types_allowed = True
    
    async def run(self):
        # stop_motor = f"0{str(self.motor_number)}00"
        if self.motor_forward == True:
            motor_direction = "0"
        else:
            motor_direction = '8'

        if self.client.is_connected:
            motor_command_0 = motor_direction+str(0)+str(percent_to_hex(self.motor_power))
            motor_command_1 = motor_direction+str(1)+str(percent_to_hex(self.motor_power))

            stop_motor_0 = "0000"
            stop_motor_1 = "0100"

            await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'29420546{motor_command_0}012C0000'), 
                                    response=False)
            await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'29420546{motor_command_1}012C0000'), 
                                    response=False)
            await asyncio.sleep(self.delay_ms)
            await self.client.write_gatt_char(WRITE_UUID, 
                                            from_hex_string(f'29420546{str(stop_motor_0)}012C0000'), 
                                            response=False)
            await self.client.write_gatt_char(WRITE_UUID, 
                                            from_hex_string(f'29420546{str(stop_motor_1)}012C0000'), 
                                            response=False)

# turning right
class HeadTurnRight(BLECommand):

    class Config:
                arbitrary_types_allowed = True

    async def run(self):
        if self.client.is_connected:
            turn_right_command = "82A0"

            await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'29420546{turn_right_command}012C0000'), 
                                    response=False)
            await asyncio.sleep(self.delay_ms)
            await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'294205460200012C0000'), 
                                    response=False)

# turning left
class HeadTurnLeft(BLECommand):
    # head_percent: Optional[float] = 50
    class Config:
                arbitrary_types_allowed = True

    async def run(self):
        if self.client.is_connected:
            turn_left_command = "02A0"
            await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'29420546{turn_left_command}012C0000'), 
                                    response=False)
            await asyncio.sleep(self.delay_ms)
            await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'294205460200012C0000'), 
                                    response=False)

class HeadNodNo(BLECommand):
     async def run(self):
        head_right = HeadTurnRight(client=self.client, 
                               delay_ms = .5)
        await head_right.run()
        # Head turn Left
        head_left = HeadTurnLeft(client=self.client, 
                                delay_ms = .5)
        await head_left.run()

class SpinLeft(BLECommand):
     motor_power: Optional[int] = 80 

     async def run(self):
        motor_command_0 = "0"+str(0)+str(percent_to_hex(self.motor_power))
        await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'29420546{motor_command_0}012C0000'), 
                                    response=False)
        await asyncio.sleep(self.delay_ms)
        await self.client.write_gatt_char(WRITE_UUID, 
                                            from_hex_string(f'29420546{str("0000")}012C0000'), 
                                            response=False)

class SpinRight(BLECommand):
     motor_power: Optional[int] = 80 
     async def run(self):
        motor_command_1 = "0"+str(1)+str(percent_to_hex(self.motor_power))
        await self.client.write_gatt_char(WRITE_UUID, 
                                    from_hex_string(f'29420546{motor_command_1}012C0000'), 
                                    response=False)
        await asyncio.sleep(self.delay_ms)
        await self.client.write_gatt_char(WRITE_UUID, 
                                            from_hex_string(f'29420546{str("0100")}012C0000'), 
                                            response=False)