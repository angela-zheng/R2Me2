from pydantic import BaseModel, Field
import asyncio
from bleak import BleakClient
from config import WRITE_UUID

class SoundCommand(BaseModel):
    client: BleakClient
    sound_bank_id: int =  Field(ge=0, le=8)
    sound_id: int =  Field(ge=0, le=4)
    ms_delay: float = .05

    class Config:
        arbitrary_types_allowed = True

    async def run(self):
        if self.sound_bank_id == 8:
            str_sound_bank_id = str(8)
        else:
            str_sound_bank_id = str(self.sound_bank_id)
        hex_base = "27420F4444001F0"
        hex_sound_base = "27420F444400180"
        hex_code = hex_base + str_sound_bank_id
        hex_sound_code = hex_sound_base+str(self.sound_id)

        await self.client.write_gatt_char(WRITE_UUID, bytes.fromhex(hex_code))
        await asyncio.sleep(self.ms_delay)
        await self.client.write_gatt_char(WRITE_UUID, bytes.fromhex(hex_sound_code))


