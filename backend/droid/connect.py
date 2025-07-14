from time import sleep
from threading import Thread
from bleak import BleakScanner, BleakClient
from pydantic import BaseModel, Field
from typing import Optional, Dict

class DroidConnection(BaseModel):
    droids: Dict[str,str]
    connected_droid_address: str
    connected_client: Optional[BleakClient] = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    async def _find_droids():
        """
        Scans for nearby BLE devices and prints their information.
        """
        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover()
        if not devices:
            print("No BLE devices found.")
            return
        print("Discovered BLE devices:")
        droids = {device.name:device.address for device in devices if device.name and 'DROID' in device.name}
        # for device in devices:
        #     if device.name and 'DROID' in device.name:
        #         print(f"  Name: {device.name if device.name else 'N/A'}")
        #         print(f"  Address: {device.address}")
        #         print("-" * 20)

        return droids
    
    @staticmethod
    async def connect_to_device(address):
        try:
            client = BleakClient(address)
            await client.connect()
            if client.is_connected:
                print(f"Connected to {address}")
                return client
            else:
                print(f"Failed to connect to {address}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def get_device_services(self):
        print("running get_device_services")
        client = self.connected_client 
        if not client or not client.is_connected:
            print("Client is not connected.")
            return
        try:
            services = await client.get_services()
            print("SERVICES: ", services)
            for service in services:
                print(f"Service UUID: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic UUID: {characteristic.uuid}")
                print(f"  Characteristic Properties: {characteristic.properties}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_client(self):
        return self.connected_client 
    
    @classmethod 
    async def connect(cls):
        droids = await cls._find_droids()
        device_name = list(droids.keys())[0]
        device_address = droids[device_name]
        client = await cls.connect_to_device(device_address)
        return cls(droids = droids, 
                   connected_droid_address=device_address,
                   connected_client = client)
    
    async def change_droid_connection(self, address):
        client = await self.connect_to_device(address)
        self.connected_droid_address = address
        self.connected_client = client 

    # async def send_command(self):
    #     client = self.connected_client
    #     if not client or not client.is_connected:
    #         print("Client not connected.")
    #         return
    #     try:
    #         characteristic_uuid = "09b600b1-3e42-41fc-b474-e9c0c8f0c801"
    #         await client.write_gatt_char(characteristic_uuid, b"\x8F\x03\x01\xFF", response=False)
    #         await client.write_gatt_char(characteristic_uuid, b"\x8F\x03\x02\xFF", response=False)
    #         print("commands ent")
    #         # print(f"Sending command: {command}")
    #         # await client.write_gatt_char(characteristic_uuid, command.encode("utf-8"))
    #         # print("Command sent.")
    #     except Exception as e:
    #         print(f"Error sending command: {e}")

    @staticmethod
    def from_hex_string(hex_str: str) -> bytes:
        # Converts a hex string like '222001' to bytes
        return bytes.fromhex(hex_str)